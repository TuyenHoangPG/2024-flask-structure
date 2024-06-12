from functools import wraps
from http.client import FORBIDDEN

from ..constants.message import ERROR_MESSSAGE
from .exception import ApiException


def valid_roles(list_role: list):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user")

            if not user or not user.role in list_role:
                raise ApiException(
                    message=ERROR_MESSSAGE.PERMISSION_DENIED, status_code=FORBIDDEN
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator
