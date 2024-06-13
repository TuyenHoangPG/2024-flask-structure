from enum import Enum


class ERROR_MESSSAGE(str, Enum):
    SERVER_ERROR = "Internal Server Error"
    FORBIDDEN = "Forbidden"
    UNAUTHORIZED = "Unauthorized"
    INVALID_TOKEN_TYPE = "Invalid token type"
    INVALID_TOKEN = "Invalid token"
    INVALID_USER = "Invalid user"
    TOKEN_REQUIRE = "Token require"
    PERMISSION_DENIED = "Permission denied"
    USER_NOT_FOUND = "User not found"
    INVALID_OLD_PASSWORD = "Old password is not correct"
    REFRESH_TOKEN_NOT_EXISTED = "Refresh token does not existed"
    REFRESH_TOKEN_EXPIRED = "Refresh token is expired"
    EMAIL_EXISTED = "Email is already existed"
    INVALID_EMAIL_OR_PASSWORD = "Invalid email or password"
    USER_NOT_ACTIVE = "User is not active"
