import math

from flask_apispec import doc, marshal_with, use_kwargs

from src.apps.user.user_service import UserService
from src.commons.constants.constant import DOCS_REQUIRE_AUTHORIZED, USER_ROLES
from src.commons.dtos.api_exception_response import ApiExceptionResponse
from src.commons.dtos.base_resource import BaseResource
from src.commons.middlewares.is_auth import is_auth
from src.commons.middlewares.valid_roles import valid_roles
from src.commons.middlewares.validation import valid_schema
from src.commons.utils.pagination import get_filter_params_query

from .dtos.requests import AddUserRequest, UpdateUserRequest, ViewListUserRequest
from .dtos.responses import UserResponse, ViewListUserResponse


@doc(
    tags=["Users"],
    description="User module",
    params={**DOCS_REQUIRE_AUTHORIZED},
)
@marshal_with(ApiExceptionResponse, code=400)
class UserBaseController(BaseResource):
    user_service = UserService()


class UserListResource(UserBaseController):
    @is_auth
    @valid_roles([USER_ROLES.SUPER_ADMIN, USER_ROLES.ADMIN])
    @use_kwargs(ViewListUserRequest, location="query")
    @valid_schema(ViewListUserRequest)
    @marshal_with(ViewListUserResponse)
    def get(self, data, **kwargs):
        """View list user."""
        data = get_filter_params_query(data)

        total, items = self.user_service.get_list(
            page=data.get("page"),
            page_size=data.get("page_size"),
            keyword=data.get("keyword"),
            search_by=data.get("search_by"),
            sort_by=data.get("sort_by"),
            sort_type=data.get("sort_type"),
        )

        return {
            "current_page": data.get("page"),
            "total_page": math.ceil(total / data.get("page_size")),
            "total_record": total,
            "data": items,
        }

    @is_auth
    @valid_roles([USER_ROLES.SUPER_ADMIN, USER_ROLES.ADMIN])
    @use_kwargs(AddUserRequest)
    @valid_schema(AddUserRequest)
    @marshal_with(UserResponse)
    def post(self, data, **kwargs):
        """Add new user detail."""
        return self.user_service.add_new_user(data)


class UserResource(UserBaseController):
    @is_auth
    @valid_roles([USER_ROLES.SUPER_ADMIN])
    @marshal_with(UserResponse)
    def get(self, id, **kwargs):
        """View user detail."""
        return self.user_service.get_by_id(id)

    @is_auth
    @valid_roles([USER_ROLES.SUPER_ADMIN])
    @use_kwargs(UpdateUserRequest)
    @valid_schema(UpdateUserRequest)
    @marshal_with(UserResponse)
    def put(self, id, data, **kwargs):
        """Update user detail."""
        return self.user_service.update_user(id, data)

    @is_auth
    @valid_roles([USER_ROLES.SUPER_ADMIN])
    def delete(self, id, **kwargs):
        """View user detail."""
        return self.user_service.delete_user(id)
