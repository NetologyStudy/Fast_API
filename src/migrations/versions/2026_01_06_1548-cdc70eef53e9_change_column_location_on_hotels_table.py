"""change column location on hotels table

Revision ID: cdc70eef53e9
Revises: 424bad1c26ba
Create Date: 2026-01-06 15:48:46.970448

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cdc70eef53e9"
down_revision: Union[str, Sequence[str], None] = "424bad1c26ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f("hotels_title_key"), "hotels", type_="unique")


def downgrade() -> None:
    op.create_unique_constraint(
        op.f("hotels_title_key"),
        "hotels",
        ["title"],
        postgresql_nulls_not_distinct=False,
    )
