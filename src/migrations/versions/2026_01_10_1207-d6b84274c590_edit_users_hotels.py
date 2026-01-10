"""edit users, hotels

Revision ID: d6b84274c590
Revises: cdc70eef53e9
Create Date: 2026-01-10 12:07:34.052138

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d6b84274c590"
down_revision: Union[str, Sequence[str], None] = "cdc70eef53e9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=64), nullable=False),
        sa.Column("last_name", sa.String(length=64), nullable=False),
        sa.Column("nickname", sa.String(length=64), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("last_name"),
        sa.UniqueConstraint("nickname"),
    )
    op.add_column("hotels", sa.Column("stars", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.drop_column("hotels", "stars")
    op.drop_table("users")

