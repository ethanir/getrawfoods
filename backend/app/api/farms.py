"""Farm listing and detail endpoints."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.farm import Farm
from app.schemas.farm import FarmDetail, FarmListItem

router = APIRouter(prefix="/api/farms", tags=["farms"])


@router.get("", response_model=List[FarmListItem])
def list_farms(
    db: Session = Depends(get_db),
    verification_level: Optional[str] = Query(
        None,
        description="Filter farms whose verification_levels array contains this level "
        "(aajonus_verified, dev_verified, community_verified, unverified).",
    ),
    diet_profile: Optional[str] = Query(
        None,
        description="Filter farms that serve this diet profile "
        "(raw_carnivore, aajonus_primal, weston_a_price).",
    ),
    category: Optional[str] = Query(
        None,
        description="Filter farms in this product category "
        "(raw_dairy, raw_meat, raw_organs, oysters).",
    ),
    state: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> List[Farm]:
    stmt = select(Farm).where(Farm.status != "closed")
    if verification_level:
        stmt = stmt.where(Farm.verification_levels.contains([verification_level]))
    if state:
        stmt = stmt.where(Farm.state == state.upper())
    if diet_profile:
        stmt = stmt.where(Farm.diet_profiles.contains([diet_profile]))
    if category:
        stmt = stmt.where(Farm.categories.contains([category]))
    stmt = stmt.order_by(Farm.name.asc()).limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())


@router.get("/{slug}", response_model=FarmDetail)
def get_farm(slug: str, db: Session = Depends(get_db)) -> Farm:
    stmt = (
        select(Farm)
        .where(Farm.slug == slug)
        .options(
            selectinload(Farm.products),
            selectinload(Farm.fulfillment),
            selectinload(Farm.tips),
            selectinload(Farm.citations),
        )
    )
    farm = db.execute(stmt).scalar_one_or_none()
    if farm is None:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm
