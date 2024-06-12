from marshmallow import Schema, EXCLUDE


class Response(Schema):
    class Meta:
        unknown = EXCLUDE
