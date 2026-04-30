"""Verification tiers: Aajonus-verified, Dev-verified, Community-verified,
Unverified. Modeled as a table so display order and tier descriptions live
in the database, and so adding a future tier (e.g. an editorial tier) is a
data change rather than a schema migration.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.verification import Verification


class Tier(Base):
    __tablename__ = "tiers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    verifications: Mapped[list["Verification"]] = relationship(back_populates="tier")
