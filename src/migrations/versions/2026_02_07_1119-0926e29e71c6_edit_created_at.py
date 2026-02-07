"""edit created_at

Revision ID: 0926e29e71c6
Revises: ef7eaa179d8e
Create Date: 2026-02-07 11:19:20.441722

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "0926e29e71c6"
down_revision: Union[str, Sequence[str], None] = "ef7eaa179d8e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.alter_column(
        "bookings",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        nullable=False,
        server_default=sa.text("now()"),
        existing_server_default=None
    )


def downgrade() -> None:
    op.alter_column(
        "bookings",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=False,
        nullable=False,
        server_default=sa.text("now()"),
        existing_server_default=None
    )
