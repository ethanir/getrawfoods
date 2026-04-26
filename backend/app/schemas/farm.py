"""Pydantic schemas for farm-related API responses.

These define the public API shape — keep them thin and explicit.
Never return ORM models directly; always serialize through these.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FarmProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_type: str
    notes: str | None = None
    must_specify: str | None = None
    price_per_unit: str | None = None
    unit: str | None = None


class FarmFulfillmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    method: str


class FarmTipRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tip_type: str
    title: str
    body: str
    upvotes: int
    created_at: datetime


class FarmCitationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    source_type: str
    source_name: str
    source_detail: str | None = None
    source_url: str | None = None
    quote: str | None = None
    verified: bool


class FarmListItem(BaseModel):
    """Slim shape used in list views (homepage, search results)."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    description: str | None = None
    city: str | None = None
    state: str | None = None
    country: str
    verification_level: str
    status: str


class FarmDetail(BaseModel):
    """Full shape used on the farm detail page."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    alt_names: list | None = None
    description: str | None = None

    address_line1: str | None = None
    city: str | None = None
    state: str | None = None
    zip: str | None = None
    country: str

    website: str | None = None
    phone: str | None = None
    email: str | None = None
    support_email: str | None = None
    contact_person: str | None = None

    status: str
    verification_level: str
    verification_source: str | None = None

    products: list[FarmProductRead] = []
    fulfillment: list[FarmFulfillmentRead] = []
    tips: list[FarmTipRead] = []
    citations: list[FarmCitationRead] = []

    created_at: datetime
    updated_at: datetime
