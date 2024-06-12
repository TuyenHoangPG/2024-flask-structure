import marshmallow as ma

from src.commons.dtos.list_response import ListResponse
from src.commons.dtos.response import Response
from src.commons.utils.enum import retrieve_enum_value


class UserResponse(Response):
    id = ma.fields.String()
    email = ma.fields.String()
    full_name = ma.fields.String()
    role = ma.fields.String()
    status = ma.fields.String()

    @ma.post_dump
    def transform_role(self, data, **kwargs):
        if "role" in data:
            data["role"] = retrieve_enum_value(data["role"])

        if "status" in data:
            data["status"] = retrieve_enum_value(data["status"])

        return data


class ViewListUserResponse(ListResponse):
    data = ma.fields.List(ma.fields.Nested(UserResponse))
