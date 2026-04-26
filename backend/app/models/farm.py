"""Farm-related ORM models.

The schema is defined in the migration file; these classes mirror it for
the ORM. Keep them in sync — when changing one, change the other.
"""

import uuid
from datetime import datetime

from geoalchemy2 import Geography
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Farm(Base):
    __tablename__ = "farms"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    alt_names: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Location
    address_line1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)
    zip: Mapped[str | None] = mapped_column(String(20), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=False, server_default="USA")
    location: Mapped[Geography | None] = mapped_column(
        Geography(geometry_type="POINT", srid=4326), nullable=True
    )

    # Contact
    website: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    support_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_person: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Status & verification
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="active")
    verification_level: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="unverified", index=True
    )
    verification_source: Mapped[str | None] = mapped_column(Text, nullable=True)

    diet_profiles: Mapped[list] = mapped_column(JSONB, nullable=False, server_default="[]")
    best_for: Mapped[str | None] = mapped_column(String(80), nullable=True)

    # Submission
    submitted_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    approved_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    is_approved: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Relationships
    products: Mapped[list["FarmProduct"]] = relationship(
        back_populates="farm", cascade="all, delete-orphan"
    )
    fulfillment: Mapped[list["FarmFulfillment"]] = relationship(
        back_populates="farm", cascade="all, delete-orphan"
    )
    tips: Mapped[list["FarmTip"]] = relationship(
        back_populates="farm", cascade="all, delete-orphan"
    )
    citations: Mapped[list["FarmCitation"]] = relationship(
        back_populates="farm", cascade="all, delete-orphan"
    )


class FarmProduct(Base):
    __tablename__ = "farm_products"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True
    )
    product_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    must_specify: Mapped[str | None] = mapped_column(Text, nullable=True)
    price_per_unit: Mapped[str | None] = mapped_column(String(50), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(60), nullable=True)

    farm: Mapped[Farm] = relationship(back_populates="products")


class FarmFulfillment(Base):
    __tablename__ = "farm_fulfillment"
    __table_args__ = (UniqueConstraint("farm_id", "method", name="uq_farm_fulfillment"),)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True
    )
    method: Mapped[str] = mapped_column(String(50), nullable=False)

    farm: Mapped[Farm] = relationship(back_populates="fulfillment")


class FarmTip(Base):
    __tablename__ = "farm_tips"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True
    )
    tip_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    upvotes: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")
    submitted_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    farm: Mapped[Farm] = relationship(back_populates="tips")


class FarmCitation(Base):
    __tablename__ = "farm_citations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    farm_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True
    )
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    source_detail: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    quote: Mapped[str | None] = mapped_column(Text, nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default="false")

    farm: Mapped[Farm] = relationship(back_populates="citations")
