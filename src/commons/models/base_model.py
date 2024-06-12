from uuid import uuid4

from ..extensions import db
from ..utils.datetime import utc_now


class BaseModel:
    id = db.Column(db.UUID(), primary_key=True, default=uuid4)
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
