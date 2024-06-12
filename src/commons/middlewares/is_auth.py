from functools import wraps
from http.client import UNAUTHORIZED

from flask import request

from ..constants.constant import USER_STATUS
from ..constants.message import ERROR_MESSSAGE
from .exception import ApiException


def is_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from src.apps.auth.auth_service import AuthService
        from src.apps.user.user_service import UserService

        if "Authorization" in request.headers:
            authorization = request.headers.get("Authorization", "")
            type = authorization.split(" ")[0]
            token = authorization.split(" ")[1]

            auth_service = AuthService()
            if not type or not token or type != "Bearer":
                raise ApiException(
                    message=ERROR_MESSSAGE.INVALID_TOKEN_TYPE, status_code=UNAUTHORIZED
                )

            payload, is_invalid = auth_service.decode_access_token(token)
            if is_invalid:
                raise ApiException(
                    message=ERROR_MESSSAGE.INVALID_TOKEN, status_code=UNAUTHORIZED
                )

            user_service = UserService()
            user = user_service.get_by_id(payload.get("user_id"))

            if not user or user.status == USER_STATUS.INACTIVE:
                raise ApiException(
                    message=ERROR_MESSSAGE.INVALID_USER, status_code=UNAUTHORIZED
                )

            if user.role != payload.get("role"):
                raise ApiException(
                    ERROR_MESSSAGE.USER_ROLE_HAS_BEEN_CHANGED, status_code=UNAUTHORIZED
                )

            return func(user=user, *args, **kwargs)
        else:
            raise ApiException(
                message=ERROR_MESSSAGE.TOKEN_REQUIRE, status_code=UNAUTHORIZED
            )

    return wrapper
