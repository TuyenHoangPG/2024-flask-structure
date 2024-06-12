from functools import wraps
from http.client import BAD_REQUEST

from flask import request
from marshmallow import ValidationError

from src.commons.utils.validation_message import retrieve_validate_error

from .exception import ApiException


def valid_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            queries = request.args
            json_data = request.get_json(silent=True)
            files = request.files

            try:
                payload = {}
                if json_data is not None:
                    payload = json_data
                elif queries is not None and bool(queries.to_dict()):
                    payload = queries
                elif files is not None and bool(files.to_dict()):
                    payload = files

                result = schema().load(payload)
            except ValidationError as error:
                message = retrieve_validate_error(error.messages)
                raise ApiException(message=message, status_code=BAD_REQUEST)

            return func(data=result, *args, **kwargs)

        return wrapper

    return decorator
