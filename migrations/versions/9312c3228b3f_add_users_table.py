"""Add users table

Revision ID: 9312c3228b3f
Revises: 
Create Date: 2024-06-13 00:22:01.492041

"""

from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from src.commons.models.user_model import User
from src.commons.constants.constant import USER_ROLES, USER_STATUS
from src.commons.utils.datetime import utc_now


# revision identifiers, used by Alembic.
revision = "9312c3228b3f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    user_table = op.create_table(
        "users",
        sa.Column("id", sa.UUID(as_uuid=True), nullable=False, default=uuid4),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "SUPER_ADMIN",
                "ADMIN",
                "USER",
                name="user_role_enum",
            ),
            nullable=False,
            default=USER_ROLES.USER,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "ACTIVE",
                "INACTIVE",
                name="user_status_enum",
            ),
            nullable=False,
            default=USER_STATUS.ACTIVE,
        ),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), nullable=True, default=utc_now
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=True, default=utc_now
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.bulk_insert(
        user_table,
        [
            {
                "email": "admin@test.co",
                "full_name": "admin",
                "role": USER_ROLES.ADMIN,
                "password": User.hash_password("Matkhau1@3"),
            },
            {
                "email": "super_admin@test.co",
                "full_name": "super_admin",
                "role": USER_ROLES.SUPER_ADMIN,
                "password": User.hash_password("Matkhau1@3"),
            },
        ],
    )


def downgrade():
    op.drop_table("users")

    user_status = postgresql.ENUM("ACTIVE", "INACTIVE", name="user_status_enum")
    user_status.drop(op.get_bind())

    user_role = postgresql.ENUM(
        "SUPER_ADMIN",
        "ADMIN",
        "USER",
        name="user_role_enum",
    )
    user_role.drop(op.get_bind())
