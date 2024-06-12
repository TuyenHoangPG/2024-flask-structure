from datetime import datetime, timedelta, timezone
from http.client import UNAUTHORIZED
from uuid import uuid4

from flask import current_app, request
from jwt import decode, encode

from src.commons.models.user_model import User
from src.apps.user.user_service import UserService
from src.commons.extensions import Singleton, cache
from src.commons.constants.constant import USER_ROLES, USER_STATUS
from src.commons.constants.message import ERROR_MESSSAGE
from src.commons.middlewares.exception import ApiException
from src.commons.utils.password import get_random_string
from src.libs.send_mail.mail_service import SendMailService


class AuthService(Singleton):
    user_service = UserService()

    def generate_access_token(self, user_id: str):
        user = self.user_service.get_by_id(user_id)
        now = datetime.now(timezone.utc)
        token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
        token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
        expire = now + timedelta(hours=token_age_h, minutes=token_age_m)
        if current_app.config["TESTING"]:
            expire = now + timedelta(seconds=5)
        payload = {
            "exp": expire,
            "iat": now,
            "user_id": user_id,
            "role": user.role,
        }
        key = current_app.config.get("SECRET_KEY")
        return encode(payload, key, algorithm="HS256")

    def decode_access_token(self, token: str):
        try:
            payload = decode(
                token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
            )
            return payload, False
        except Exception as e:
            current_app.logger.error(e)

        return None, True

    def generate_refresh_token(self):
        now = datetime.now(timezone.utc)
        return {
            "token": str(uuid4()),
            "expire": now
            + timedelta(seconds=current_app.config.get("REFRESH_TOKEN_EXPIRED_TIME")),
        }

    def verify_refresh_token(self, refreshToken: dict):
        now = datetime.now(timezone.utc)
        return refreshToken["expire"] > now

    def generate_token(self, user):
        token = self.generate_access_token(user_id=str(user.id))
        refresh_token = self.generate_refresh_token()

        cache.set(
            refresh_token["token"],
            {**refresh_token, "user_id": str(user.id), "role": user.role},
            timeout=current_app.config.get("REFRESH_TOKEN_EXPIRED_TIME"),
        )

        return {
            "token": token,
            "refresh_token": refresh_token["token"],
        }

    def sign_in(self, data: dict):
        user: User = self.user_service.get_by_email(data.get("email"))
        if user is None or not user.check_password(data.get("password")):
            raise ApiException(ERROR_MESSSAGE.INVALID_EMAIL_OR_PASSWORD)

        if user.status == USER_STATUS.INACTIVE:
            raise ApiException(ERROR_MESSSAGE.USER_NOT_ACTIVE)

        return {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            **self.generate_token(user),
        }

    def forgot_password(self, email):
        user = self.user_service.get_by_email(email)
        if (
            user is None
            or user.status == USER_STATUS.INACTIVE
            or user.role != USER_ROLES.USER
        ):
            raise ApiException(ERROR_MESSSAGE.USER_NOT_FOUND)

        new_password = get_random_string()
        user.update(password=User.hash_password(new_password))

        SendMailService.send_email_forgot_password(
            email=email, new_password=new_password
        )

        return {"success": True}

    def change_password(self, user: User, data: dict):
        if not user.check_password(data["old_password"]):
            raise ApiException(ERROR_MESSSAGE.INVALID_OLD_PASSWORD)

        user.update(password=User.hash_password(data["new_password"]))

        return {"success": True}

    def refresh_token(self, token):
        token = str(token)
        refresh = cache.get(token)
        if refresh is None:
            raise ApiException(
                ERROR_MESSSAGE.REFRESH_TOKEN_NOT_EXISTED, status_code=UNAUTHORIZED
            )

        if not self.verify_refresh_token(refresh):
            raise ApiException(
                ERROR_MESSSAGE.REFRESH_TOKEN_EXPIRED, status_code=UNAUTHORIZED
            )

        user = self.user_service.get_by_id(refresh["user_id"])
        if user is None or user.status == USER_STATUS.INACTIVE:
            cache.delete(token)
            raise ApiException(ERROR_MESSSAGE.USER_NOT_FOUND)

        cache.delete(token)
        return self.generate_token(user)

    def sign_up(self, data: dict):
        new_user = self.user_service.add_new_user(data)

        return {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "role": new_user.role,
            **self.generate_token(new_user),
        }
