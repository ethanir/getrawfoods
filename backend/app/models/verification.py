"""Verification: a single (farm, category, tier) badge.

Verification is per (farm, category) tuple, not farm-wide. A farm can
carry an Aajonus-verified badge for meat but no badge for dairy if the
published sourcing materials only spoke to the meat program. See
docs/adr/0003-verification-model.md for the full reasoning.

The composite unique constraint on (farm_id, category_id, tier_id)
prevents the same badge from being attached twice. Cascade deletes from
farms and categories; deletion of a tier is restricted because dropping a
tier with attached verifications should be an explicit operation.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.farm import Farm
    from app.models.tier import Tier


class Verification(Base):
    __tablename__ = "verifications"
    __table_args__ = (
        UniqueConstraint(
            "farm_id",
            "category_id",
            "tier_id",
            name="uq_verification_farm_category_tier",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    farm_id: Mapped[int] = mapped_column(
        ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tier_id: Mapped[int] = mapped_column(
        ForeignKey("tiers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    farm: Mapped["Farm"] = relationship(back_populates="verifications")
    category: Mapped["Category"] = relationship(back_populates="verifications")
    tier: Mapped["Tier"] = relationship(back_populates="verifications")
