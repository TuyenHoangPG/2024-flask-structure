from flask import Blueprint

from .auth_controller import (
    ChangePasswordResource,
    ForgotPasswordResource,
    GetMeResource,
    RefreshTokenResource,
    SignInResource,
    SignUpResource,
    TestAsyncTaskResource,
)

auth_route = Blueprint("auth", __name__, url_prefix="/api/auth")

resources = [
    (SignInResource, "/sign-in", "sign_in", ["POST"]),
    (ForgotPasswordResource, "/forgot-password", "forgot_password", ["POST"]),
    (ChangePasswordResource, "/change-password", "change_password", ["POST"]),
    (GetMeResource, "/me", "get_me", ["GET"]),
    (RefreshTokenResource, "/refresh-token", "refresh_token", ["POST"]),
    (SignUpResource, "/sign-up", "sign_up", ["POST"]),
    (TestAsyncTaskResource, "/test", "test", ["GET"]),
]
