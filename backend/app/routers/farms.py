"""Farm endpoints.

Two routes:
  GET /api/farms          - list, with verifications inlined
  GET /api/farms/{slug}   - detail, with everything

Both eager-load verifications, categories, and tiers via selectinload to
avoid the N+1 pattern that would otherwise emit a query per farm and per
verification when rendering the home page.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.models import Farm, Verification
from app.schemas import FarmDetail, FarmListItem, VerificationRead

router = APIRouter()


def _verifications_for(farm: Farm) -> list[VerificationRead]:
    """Map a farm's ORM verifications to the API shape, ordered by
    category display_order then tier display_order so the badges render
    in the same order across the list and detail views.
    """
    items = sorted(
        farm.verifications,
        key=lambda v: (v.category.display_order, v.tier.display_order),
    )
    return [VerificationRead(category=v.category.slug, tier=v.tier.slug) for v in items]


@router.get("/farms", response_model=list[FarmListItem])
def list_farms(db: Session = Depends(get_db)) -> list[FarmListItem]:
    stmt = (
        select(Farm)
        .options(
            selectinload(Farm.verifications).selectinload(Verification.category),
            selectinload(Farm.verifications).selectinload(Verification.tier),
        )
        .order_by(Farm.name)
    )
    farms = list(db.scalars(stmt))
    return [
        FarmListItem(
            slug=farm.slug,
            name=farm.name,
            location=farm.location,
            verifications=_verifications_for(farm),
        )
        for farm in farms
    ]


@router.get("/farms/{slug}", response_model=FarmDetail)
def get_farm(slug: str, db: Session = Depends(get_db)) -> FarmDetail:
    stmt = (
        select(Farm)
        .where(Farm.slug == slug)
        .options(
            selectinload(Farm.verifications).selectinload(Verification.category),
            selectinload(Farm.verifications).selectinload(Verification.tier),
        )
    )
    farm = db.scalar(stmt)
    if farm is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farm not found")
    return FarmDetail(
        slug=farm.slug,
        name=farm.name,
        location=farm.location,
        description=farm.description,
        website=farm.website,
        phone=farm.phone,
        email=farm.email,
        sourcing_tips=farm.sourcing_tips,
        verifications=_verifications_for(farm),
    )
