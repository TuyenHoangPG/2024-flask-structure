import marshmallow as ma

from src.commons.dtos.request import Request


class RefreshTokenRequest(Request):
    token = ma.fields.UUID(
        required=True,
    )
