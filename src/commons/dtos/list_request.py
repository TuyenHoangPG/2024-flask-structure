import marshmallow as ma

from ..constants.constant import SORT_TYPE
from .request import Request


class ListRequest(Request):
    page = ma.fields.Integer(default=1)
    page_size = ma.fields.Integer(default=10)
    keyword = ma.fields.String(default="")
    sort_by = ma.fields.String()
    sort_type = ma.fields.Enum(enum=SORT_TYPE)
    search_by = ma.fields.String()
