import marshmallow as ma

from .response import Response


class Item(ma.Schema):
    id = ma.fields.String()


class ListResponse(Response):
    current_page = ma.fields.Integer()
    total_page = ma.fields.Integer()
    total_record = ma.fields.Integer()
    data = ma.fields.List(ma.fields.Nested(Item))
