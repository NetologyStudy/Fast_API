"""add created_at on booking

Revision ID: 6d363b8bddda
Revises: f81bac01c967
Create Date: 2026-01-18 15:14:28.075798

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6d363b8bddda"
down_revision: Union[str, Sequence[str], None] = "f81bac01c967"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("bookings", sa.Column("created_at", sa.DateTime(), nullable=False))



def downgrade() -> None:
    op.drop_column("bookings", "created_at")
