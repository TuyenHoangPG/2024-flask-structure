from http.client import BAD_REQUEST

from flask import jsonify


def error_template(data: dict, status_code=BAD_REQUEST):
    return {
        "status_code": status_code,
        "message": data.get("message"),
        "error": data.get("error"),
        "payload": data.get("payload"),
    }


class ApiException(Exception):
    status_code = BAD_REQUEST

    def __init__(self, message, status_code=None, payload=None, error=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code
        self.response = error_template(
            {"message": message, "payload": payload, "error": error}, self.status_code
        )

    def to_json(self):
        res = self.response
        return jsonify(res), res["status_code"]
