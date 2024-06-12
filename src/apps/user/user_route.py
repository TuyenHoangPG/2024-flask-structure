from flask import Blueprint

from src.apps.user.user_controller import (
    UserListResource,
    UserResource,
)

user_route = Blueprint("users", __name__, url_prefix="/api/users")

resources = [
    (UserListResource, "/", "user_list", ["GET", "POST"]),
    (UserResource, "/<id>", "user", ["GET", "PUT", "DELETE"]),
]
