"""Seed the database with v1 reference data.

Idempotent: running on a populated database is a no-op for already-present
slugs and adds anything new in app.seed.data. Run from the backend directory:

    python -m app.seed.seed
"""

import sys

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import Category, Farm, Tier, Verification
from app.seed.data import CATEGORIES, FARMS, TIERS


def seed_categories(db: Session) -> dict[str, Category]:
    by_slug: dict[str, Category] = {c.slug: c for c in db.scalars(select(Category)).all()}
    for spec in CATEGORIES:
        if spec.slug in by_slug:
            continue
        cat = Category(
            slug=spec.slug,
            name=spec.name,
            description=spec.description,
            display_order=spec.display_order,
        )
        db.add(cat)
        by_slug[spec.slug] = cat
    db.flush()
    return by_slug


def seed_tiers(db: Session) -> dict[str, Tier]:
    by_slug: dict[str, Tier] = {t.slug: t for t in db.scalars(select(Tier)).all()}
    for spec in TIERS:
        if spec.slug in by_slug:
            continue
        tier = Tier(
            slug=spec.slug,
            name=spec.name,
            description=spec.description,
            display_order=spec.display_order,
        )
        db.add(tier)
        by_slug[spec.slug] = tier
    db.flush()
    return by_slug


def seed_farms(
    db: Session,
    categories: dict[str, Category],
    tiers: dict[str, Tier],
) -> None:
    existing = {f.slug for f in db.scalars(select(Farm)).all()}
    for spec in FARMS:
        if spec.slug in existing:
            continue
        farm = Farm(
            slug=spec.slug,
            name=spec.name,
            location=spec.location,
            description=spec.description,
            website=spec.website,
            phone=spec.phone,
            email=spec.email,
            sourcing_tips=spec.sourcing_tips,
        )
        db.add(farm)
        db.flush()
        for v in spec.verifications:
            db.add(
                Verification(
                    farm_id=farm.id,
                    category_id=categories[v.category_slug].id,
                    tier_id=tiers[v.tier_slug].id,
                )
            )


def run() -> None:
    with SessionLocal() as db:
        categories = seed_categories(db)
        tiers = seed_tiers(db)
        seed_farms(db, categories, tiers)
        db.commit()
        print(
            f"Seed complete: {len(CATEGORIES)} categories, "
            f"{len(TIERS)} tiers, {len(FARMS)} farms.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    run()
