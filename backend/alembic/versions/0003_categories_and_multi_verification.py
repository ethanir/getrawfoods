"""Categories and multi-verification.

Revision ID: 0003
Revises: 0002
Create Date: 2026-04-29

Schema change for v0.4:
  - farms.verification_level (VARCHAR) → farms.verification_levels (JSONB array)
    so Miller's can carry both Aajonus-verified and dev-verified.
  - dev_recommended is renamed to dev_verified during the backfill.
  - New farms.categories JSONB array (raw_dairy, raw_meat, raw_organs, oysters)
    backing the new category-led navigation in ADR 0005.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── verification_level (string) → verification_levels (JSONB array) ──
    op.drop_index("idx_farms_verification", table_name="farms")

    op.add_column(
        "farms",
        sa.Column(
            "verification_levels",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )

    # Backfill: wrap the single string in an array; rename dev_recommended →
    # dev_verified at the same time. unverified stays unverified.
    op.execute(
        """
        UPDATE farms
        SET verification_levels = jsonb_build_array(
            CASE
                WHEN verification_level = 'dev_recommended' THEN 'dev_verified'
                ELSE verification_level
            END
        )
        WHERE verification_level IS NOT NULL
          AND verification_level <> 'unverified'
        """
    )

    op.drop_column("farms", "verification_level")

    op.create_index(
        "idx_farms_verification_levels",
        "farms",
        ["verification_levels"],
        postgresql_using="gin",
    )

    # ── categories ────────────────────────────────────────────────────────
    op.add_column(
        "farms",
        sa.Column(
            "categories",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )
    op.create_index(
        "idx_farms_categories",
        "farms",
        ["categories"],
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_index("idx_farms_categories", table_name="farms")
    op.drop_column("farms", "categories")

    op.drop_index("idx_farms_verification_levels", table_name="farms")

    op.add_column(
        "farms",
        sa.Column(
            "verification_level",
            sa.String(20),
            nullable=False,
            server_default="unverified",
        ),
    )
    # Best-effort restore: pick the first level if multiple exist; map
    # dev_verified back to dev_recommended.
    op.execute(
        """
        UPDATE farms
        SET verification_level = CASE
            WHEN jsonb_array_length(verification_levels) = 0 THEN 'unverified'
            WHEN verification_levels->>0 = 'dev_verified' THEN 'dev_recommended'
            ELSE verification_levels->>0
        END
        """
    )

    op.drop_column("farms", "verification_levels")

    op.create_index("idx_farms_verification", "farms", ["verification_level"])
