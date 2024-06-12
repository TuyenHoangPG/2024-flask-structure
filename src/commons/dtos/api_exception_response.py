import marshmallow as ma

from .response import Response


class ApiExceptionResponse(Response):
    status_code = ma.fields.Integer()
    message = ma.fields.String()
    error = ma.fields.String()
    payload = ma.fields.String()
