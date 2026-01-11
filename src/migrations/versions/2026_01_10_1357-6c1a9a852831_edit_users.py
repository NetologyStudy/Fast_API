"""edit users

Revision ID: 6c1a9a852831
Revises: d6b84274c590
Create Date: 2026-01-10 13:57:38.897869

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6c1a9a852831"
down_revision: Union[str, Sequence[str], None] = "d6b84274c590"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["nickname"])
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")
