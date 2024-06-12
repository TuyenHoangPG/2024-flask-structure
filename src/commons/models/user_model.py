from uuid import uuid4

from flask import current_app
from sqlalchemy.orm import Mapped

from ..extensions import bcrypt, db
from ..constants.constant import USER_ROLES, USER_STATUS
from .base_model import BaseModel


class User(db.Model, BaseModel):
    __tablename__ = "users"

    email = db.Column(db.String(255), nullable=False, unique=True)
    full_name = db.Column(
        db.String(255),
        nullable=False,
    )
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum(
            USER_ROLES.ADMIN,
            USER_ROLES.SUPER_ADMIN,
            USER_ROLES.USER,
        ),
        nullable=False,
        default=USER_ROLES.USER,
    )
    status = db.Column(
        db.Enum(USER_STATUS.ACTIVE, USER_STATUS.INACTIVE),
        nullable=False,
        default=USER_STATUS.ACTIVE,
    )

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)
        if kwargs["password"]:
            self.password = self.hash_password(kwargs["password"])
        else:
            self.password = None

    def __repr__(self):
        return f"<User email={self.email}, role={self.role}>"

    @classmethod
    def hash_password(cls, password):
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        return hash_bytes.decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
