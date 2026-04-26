"""Pydantic request/response schemas for farms."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FarmProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_type: str
    notes: str | None = None
    must_specify: str | None = None
    price_per_unit: str | None = None
    unit: str | None = None


class FarmFulfillmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    method: str


class FarmTipRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tip_type: str
    title: str
    body: str


class FarmCitationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_type: str
    source_name: str
    source_detail: str | None = None
    source_url: str | None = None
    quote: str | None = None
    verified: bool = False


class FarmListItem(BaseModel):
    """Compact farm representation for the directory list."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    description: str | None = None
    city: str | None = None
    state: str | None = None
    country: str = "USA"
    verification_level: str
    status: str
    diet_profiles: list[str] = []
    best_for: str | None = None


class FarmMapPin(BaseModel):
    """Lightweight payload for the map view — one pin per farm."""

    model_config = ConfigDict(from_attributes=True)

    slug: str
    name: str
    lat: float
    lng: float
    city: str | None = None
    state: str | None = None
    verification_level: str
    best_for: str | None = None
    diet_profiles: list[str] = []


class FarmDetail(BaseModel):
    """Full farm representation for the detail page."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    alt_names: list[str] | None = None
    description: str | None = None
    address_line1: str | None = None
    city: str | None = None
    state: str | None = None
    zip: str | None = None
    country: str = "USA"
    website: str | None = None
    phone: str | None = None
    email: str | None = None
    support_email: str | None = None
    contact_person: str | None = None
    status: str
    verification_level: str
    verification_source: str | None = None
    diet_profiles: list[str] = []
    best_for: str | None = None
    is_approved: bool
    created_at: datetime
    updated_at: datetime
    products: list[FarmProductRead] = []
    fulfillment: list[FarmFulfillmentRead] = []
    tips: list[FarmTipRead] = []
    citations: list[FarmCitationRead] = []
