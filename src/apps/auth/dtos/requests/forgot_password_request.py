import marshmallow as ma
from marshmallow import validate

from src.commons.dtos.request import Request


class ForgotPasswordRequest(Request):
    email = ma.fields.Email(required=True, validate=validate.Email())
