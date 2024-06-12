import marshmallow as ma

from src.commons.dtos.response import Response


class RefreshTokenResponse(Response):
    token = ma.fields.String()
    refresh_token = ma.fields.String()
