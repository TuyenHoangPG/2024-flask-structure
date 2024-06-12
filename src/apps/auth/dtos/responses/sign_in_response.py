import marshmallow as ma

from src.commons.dtos.response import Response
from src.commons.utils.enum import retrieve_enum_value


class SignInResponse(Response):
    id = ma.fields.String()
    token = ma.fields.String()
    full_name = ma.fields.String()
    email = ma.fields.String()
    role = ma.fields.String()
    refresh_token = ma.fields.String()

    @ma.post_dump
    def transform_role(self, data, **kwargs):
        if "role" in data:
            data["role"] = retrieve_enum_value(data["role"])

        return data
