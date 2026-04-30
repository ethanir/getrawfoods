"""Smoke-test the seed: after running against a clean DB, the four farms
exist with the verifications described in the brief, and re-running the
seed is a no-op.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Category, Farm, Verification
from app.seed.data import FARMS
from app.seed.seed import seed_categories, seed_farms, seed_tiers


def test_seed_creates_four_farms_with_correct_verifications(db: Session) -> None:
    categories = seed_categories(db)
    tiers = seed_tiers(db)
    seed_farms(db, categories, tiers)
    db.commit()

    farms = db.scalars(select(Farm).order_by(Farm.slug)).all()
    assert len(farms) == 4

    by_slug = {f.slug: f for f in farms}
    assert set(by_slug) == {
        "millers-organic-farm",
        "frankies-free-range-meat",
        "mark-nolt-farm",
        "northstar-bison",
    }

    millers = by_slug["millers-organic-farm"]
    badges = {(v.category.slug, v.tier.slug) for v in millers.verifications}
    assert badges == {
        ("raw-dairy", "aajonus-verified"),
        ("raw-dairy", "dev-verified"),
        ("raw-meat", "aajonus-verified"),
        ("raw-meat", "dev-verified"),
        ("raw-organs", "aajonus-verified"),
        ("raw-organs", "dev-verified"),
    }

    frankies = by_slug["frankies-free-range-meat"]
    frankies_badges = {(v.category.slug, v.tier.slug) for v in frankies.verifications}
    assert frankies_badges == {
        ("raw-meat", "dev-verified"),
        ("raw-organs", "dev-verified"),
    }
    assert all(v.category.slug != "raw-dairy" for v in frankies.verifications), (
        "Frankie's must not appear under raw-dairy: the maintainer has only "
        "verified meat and organs."
    )


def test_seed_is_idempotent(db: Session) -> None:
    categories = seed_categories(db)
    tiers = seed_tiers(db)
    seed_farms(db, categories, tiers)
    db.commit()

    seed_categories(db)
    seed_tiers(db)
    seed_farms(db, categories, tiers)
    db.commit()

    assert db.scalar(select(Category).where(Category.slug == "raw-dairy")) is not None
    farms = db.scalars(select(Farm)).all()
    assert len(farms) == len(FARMS)
    verifications = db.scalars(select(Verification)).all()
    expected_total = sum(len(f.verifications) for f in FARMS)
    assert len(verifications) == expected_total
