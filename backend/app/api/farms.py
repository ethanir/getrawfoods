"""Farm listing and detail endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from geoalchemy2 import Geometry
from sqlalchemy import cast, func, select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.farm import Farm
from app.schemas.farm import FarmDetail, FarmListItem, FarmMapPin

router = APIRouter(prefix="/api/farms", tags=["farms"])


@router.get("", response_model=list[FarmListItem])
def list_farms(
    db: Session = Depends(get_db),
    verification_level: str | None = Query(None),
    diet_profile: str | None = Query(
        None,
        description=(
            "Filter farms that serve this diet profile "
            "(raw_carnivore, aajonus_primal, weston_a_price)."
        ),
    ),
    state: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[Farm]:
    stmt = select(Farm).where(Farm.status != "closed")
    if verification_level:
        stmt = stmt.where(Farm.verification_level == verification_level)
    if state:
        stmt = stmt.where(Farm.state == state.upper())
    if diet_profile:
        # JSONB containment: row's diet_profiles array must contain the requested profile
        stmt = stmt.where(Farm.diet_profiles.contains([diet_profile]))
    stmt = (
        stmt.order_by(
            # Aajonus-verified first, then dev-recommended, then everything else
            Farm.verification_level.desc(),
            Farm.name.asc(),
        )
        .limit(limit)
        .offset(offset)
    )
    return list(db.execute(stmt).scalars().all())


@router.get("/map", response_model=list[FarmMapPin])
def list_farm_pins(
    db: Session = Depends(get_db),
    diet_profile: str | None = Query(None),
) -> list[FarmMapPin]:
    """Lightweight farm pins for the map view.

    Defined before /{slug} so FastAPI matches the literal path first;
    otherwise the slug route would consume requests for /map.
    """
    geom = cast(Farm.location, Geometry)
    stmt = select(
        Farm.slug,
        Farm.name,
        func.ST_Y(geom).label("lat"),
        func.ST_X(geom).label("lng"),
        Farm.city,
        Farm.state,
        Farm.verification_level,
        Farm.best_for,
        Farm.diet_profiles,
    ).where(Farm.location.is_not(None), Farm.status != "closed")
    if diet_profile:
        stmt = stmt.where(Farm.diet_profiles.contains([diet_profile]))
    rows = db.execute(stmt).mappings().all()
    return [FarmMapPin(**row) for row in rows]


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
