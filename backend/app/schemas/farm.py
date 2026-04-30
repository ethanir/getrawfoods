"""Pydantic request/response schemas for farms."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FarmProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_type: str
    notes: Optional[str] = None
    must_specify: Optional[str] = None
    price_per_unit: Optional[str] = None
    unit: Optional[str] = None


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
    source_detail: Optional[str] = None
    source_url: Optional[str] = None
    quote: Optional[str] = None
    verified: bool = False


class FarmListItem(BaseModel):
    """Compact farm representation for the directory list."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    description: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "USA"
    verification_levels: List[str] = []
    status: str
    diet_profiles: List[str] = []
    categories: List[str] = []
    best_for: Optional[str] = None


class FarmDetail(BaseModel):
    """Full farm representation for the detail page."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    name: str
    alt_names: Optional[List[str]] = None
    description: Optional[str] = None
    address_line1: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: str = "USA"
    website: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    support_email: Optional[str] = None
    contact_person: Optional[str] = None
    status: str
    verification_levels: List[str] = []
    verification_source: Optional[str] = None
    diet_profiles: List[str] = []
    categories: List[str] = []
    best_for: Optional[str] = None
    is_approved: bool
    created_at: datetime
    updated_at: datetime
    products: List[FarmProductRead] = []
    fulfillment: List[FarmFulfillmentRead] = []
    tips: List[FarmTipRead] = []
    citations: List[FarmCitationRead] = []
