"""Add diet_profiles and best_for columns to farms.

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-26

Adds two columns supporting the diet-profile filter feature:
  - diet_profiles: JSONB array of profile slugs the farm serves
  - best_for: short tagline shown on the farm row (e.g. "raw bison + organs")
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "farms",
        sa.Column(
            "diet_profiles",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )
    op.add_column(
        "farms",
        sa.Column("best_for", sa.String(80), nullable=True),
    )
    # GIN index on diet_profiles so profile filter queries are fast
    op.create_index(
        "idx_farms_diet_profiles",
        "farms",
        ["diet_profiles"],
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_index("idx_farms_diet_profiles", table_name="farms")
    op.drop_column("farms", "best_for")
    op.drop_column("farms", "diet_profiles")
