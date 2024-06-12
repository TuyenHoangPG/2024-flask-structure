import marshmallow as ma
from marshmallow import validate

from src.commons.constants.constant import regex_password
from src.commons.dtos.request import Request


class ChangePasswordRequest(Request):
    old_password = ma.fields.String(required=True)
    new_password = ma.fields.String(
        required=True, validate=validate.Regexp(regex=regex_password)
    )
