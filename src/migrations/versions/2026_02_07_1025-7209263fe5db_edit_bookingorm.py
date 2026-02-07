"""edit BookingOrm

Revision ID: 7209263fe5db
Revises: ef7eaa179d8e
Create Date: 2026-02-07 10:25:07.970891

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7209263fe5db"
down_revision: Union[str, Sequence[str], None] = "ef7eaa179d8e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "bookings", "created_at", existing_type=postgresql.TIMESTAMP(), nullable=True
    )


def downgrade() -> None:
    op.alter_column(
        "bookings", "created_at", existing_type=postgresql.TIMESTAMP(), nullable=False
    )