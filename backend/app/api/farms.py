"""Farm-related API endpoints.

Public read-only endpoints in this phase. Write endpoints (submit, edit,
review, vote) come in Phase 3+ when auth is in place.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.farm import Farm
from app.schemas.farm import FarmDetail, FarmListItem

router = APIRouter(prefix="/api/farms", tags=["farms"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[FarmListItem])
def list_farms(
    db: DbSession,
    state: Annotated[str | None, Query(description="Filter by US state")] = None,
    verification_level: Annotated[
        str | None,
        Query(description="aajonus_verified | dev_recommended | community_verified | unverified"),
    ] = None,
    q: Annotated[str | None, Query(description="Substring search on name + description")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Farm]:
    """List farms with optional filters.

    Returns the slim representation suitable for a directory list.
    """
    stmt = select(Farm).where(Farm.status != "closed")

    if state:
        stmt = stmt.where(Farm.state == state)
    if verification_level:
        stmt = stmt.where(Farm.verification_level == verification_level)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Farm.name.ilike(like), Farm.description.ilike(like)))

    # Order: aajonus_verified first, then dev_recommended, then alphabetical
    verification_order = {
        "aajonus_verified": 0,
        "dev_recommended": 1,
        "community_verified": 2,
        "unverified": 3,
    }
    farms = list(db.scalars(stmt.limit(limit).offset(offset)))
    farms.sort(key=lambda f: (verification_order.get(f.verification_level, 99), f.name.lower()))
    return farms


@router.get("/{slug}", response_model=FarmDetail)
def get_farm(slug: str, db: DbSession) -> Farm:
    """Get a single farm by slug, with all related data eager-loaded."""
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
    farm = db.scalar(stmt)
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    return farm
