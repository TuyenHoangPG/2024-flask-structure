from marshmallow import Schema, EXCLUDE


class Request(Schema):
    class Meta:
        strict = True
        unknown = EXCLUDE
