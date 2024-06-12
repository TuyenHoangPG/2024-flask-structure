from enum import Enum

from marshmallow import fields

from src.commons.constants.constant import SORT_TYPE
from src.commons.dtos.list_request import ListRequest


class UserSearchByEnum(str, Enum):
    NAME = "NAME"
    EMAIL = "EMAIL"
    STATUS = "STATUS"


class ViewListUserRequest(ListRequest):
    search_by = fields.Enum(enum=UserSearchByEnum)
    sort_by = fields.Enum(enum=UserSearchByEnum)
    sort_type = fields.Enum(enum=SORT_TYPE)
