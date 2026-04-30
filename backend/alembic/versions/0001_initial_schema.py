"""initial schema: categories, tiers, farms, verifications

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-04-29

Creates the four tables that constitute the v1 schema. See
docs/schema.md for the column-by-column reference and
docs/adr/0003-verification-model.md for why verification is a join table
rather than a per-farm flag.
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(64), nullable=False, unique=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_categories_slug", "categories", ["slug"], unique=True)

    op.create_table(
        "tiers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(64), nullable=False, unique=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_tiers_slug", "tiers", ["slug"], unique=True)

    op.create_table(
        "farms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(128), nullable=False, unique=True),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("location", sa.String(256), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("website", sa.String(512), nullable=True),
        sa.Column("phone", sa.String(64), nullable=True),
        sa.Column("email", sa.String(256), nullable=True),
        sa.Column("sourcing_tips", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_farms_slug", "farms", ["slug"], unique=True)
    op.create_index("ix_farms_name", "farms", ["name"])

    op.create_table(
        "verifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "farm_id",
            sa.Integer(),
            sa.ForeignKey("farms.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "category_id",
            sa.Integer(),
            sa.ForeignKey("categories.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "tier_id",
            sa.Integer(),
            sa.ForeignKey("tiers.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "farm_id",
            "category_id",
            "tier_id",
            name="uq_verification_farm_category_tier",
        ),
    )
    op.create_index("ix_verifications_farm_id", "verifications", ["farm_id"])
    op.create_index("ix_verifications_category_id", "verifications", ["category_id"])
    op.create_index("ix_verifications_tier_id", "verifications", ["tier_id"])


def downgrade() -> None:
    op.drop_index("ix_verifications_tier_id", table_name="verifications")
    op.drop_index("ix_verifications_category_id", table_name="verifications")
    op.drop_index("ix_verifications_farm_id", table_name="verifications")
    op.drop_table("verifications")

    op.drop_index("ix_farms_name", table_name="farms")
    op.drop_index("ix_farms_slug", table_name="farms")
    op.drop_table("farms")

    op.drop_index("ix_tiers_slug", table_name="tiers")
    op.drop_table("tiers")

    op.drop_index("ix_categories_slug", table_name="categories")
    op.drop_table("categories")
