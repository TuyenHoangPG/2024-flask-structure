from marshmallow import fields, validate

from src.commons.constants.constant import regex_password
from src.commons.dtos.request import Request


class SignUpRequest(Request):
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.String(
        required=True,
        validate=validate.Regexp(regex=regex_password),
    )
    full_name = fields.String(required=True)
