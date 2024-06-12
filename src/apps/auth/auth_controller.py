from flask import current_app
from flask_apispec import doc, marshal_with, use_kwargs

from src.apps.auth.auth_service import AuthService
from src.apps.user.dtos.responses.view_list_user_response import UserResponse
from src.commons.constants.constant import DOCS_REQUIRE_AUTHORIZED
from src.commons.dtos.api_exception_response import ApiExceptionResponse
from src.commons.dtos.base_resource import BaseResource
from src.commons.middlewares.is_auth import is_auth
from src.commons.middlewares.validation import valid_schema
from src.libs.task.async_task import celery

from .dtos.requests import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    RefreshTokenRequest,
    SignInRequest,
    SignUpRequest,
)
from .dtos.responses import RefreshTokenResponse, SignInResponse, SignUpResponse


@doc(tags=["Auths"], description="Auth module")
@marshal_with(ApiExceptionResponse, code=400)
class AuthBaseController(BaseResource):
    auth_service = AuthService()


class SignInResource(AuthBaseController):

    @use_kwargs(SignInRequest)
    @valid_schema(SignInRequest)
    @marshal_with(SignInResponse)
    def post(self, data, **kwargs):
        """Login"""
        return self.auth_service.sign_in(data)


class ForgotPasswordResource(AuthBaseController):
    @use_kwargs(ForgotPasswordRequest)
    @valid_schema(ForgotPasswordRequest)
    def post(self, data, **kwargs):
        """User forgot password"""
        return self.auth_service.forgot_password(data["email"])


class ChangePasswordResource(AuthBaseController):
    @use_kwargs(ChangePasswordRequest)
    @valid_schema(ChangePasswordRequest)
    @is_auth
    @doc(
        params={**DOCS_REQUIRE_AUTHORIZED},
    )
    def post(self, user, data, **kwargs):
        """User change password"""
        return self.auth_service.change_password(user, data)


class GetMeResource(AuthBaseController):
    @doc(
        params={**DOCS_REQUIRE_AUTHORIZED},
    )
    @is_auth
    @marshal_with(UserResponse)
    def get(self, user):
        return user


class RefreshTokenResource(AuthBaseController):
    @use_kwargs(RefreshTokenRequest)
    @valid_schema(RefreshTokenRequest)
    @marshal_with(RefreshTokenResponse)
    def post(self, data, **kwargs):
        return self.auth_service.refresh_token(data.get("token"))


class SignUpResource(AuthBaseController):
    @use_kwargs(SignUpRequest)
    @valid_schema(SignUpRequest)
    @marshal_with(SignUpResponse)
    def post(self, data, **kwargs):
        """Sign up"""
        return self.auth_service.sign_up(data)


class TestAsyncTaskResource(AuthBaseController):
    def get(self, **kwargs):
        celery.send_task(
            f'{current_app.config.get("ENV")}.do_some_tasks',
            args=["Hello world"],
            queue=current_app.config.get("ENV"),
            routing_key=f'{current_app.config.get("ENV")}.do_some_tasks',
            exchange=f'tasks_{current_app.config.get("ENV")}',
        )
        return {"success": True}
