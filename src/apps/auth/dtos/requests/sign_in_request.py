import marshmallow as ma
from marshmallow import validate

from src.commons.dtos.request import Request


class SignInRequest(Request):
    email = ma.fields.Email(required=True, validate=validate.Email())
    password = ma.fields.String(required=True)
