from marshmallow import fields

from src.commons.dtos.request import Request


class UpdateUserRequest(Request):
    full_name = fields.String(required=True)
