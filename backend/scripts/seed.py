"""Seed the database from docs/seed_data.json.

Idempotent: running multiple times will not duplicate farms (matched by slug).
For v0.2, also clears any farms whose slugs are no longer in seed_data.json
so the trimmed list takes effect.
"""
import json
import sys
from pathlib import Path

# Ensure the app package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select  # noqa: E402

from app.core.database import SessionLocal  # noqa: E402
from app.models.farm import (  # noqa: E402
    Farm,
    FarmCitation,
    FarmFulfillment,
    FarmProduct,
    FarmTip,
)

SEED_PATH_CANDIDATES = [
    Path("/app/docs/seed_data.json"),
    Path(__file__).resolve().parent.parent / "seed_data.json",
    Path(__file__).resolve().parent.parent.parent / "docs" / "seed_data.json",
]


def find_seed_file() -> Path:
    for p in SEED_PATH_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError(
        f"Could not find seed_data.json. Tried: {[str(p) for p in SEED_PATH_CANDIDATES]}"
    )


def seed() -> None:
    seed_file = find_seed_file()
    print(f"Loading seed data from {seed_file}")
    data = json.loads(seed_file.read_text())

    desired_slugs = {f["slug"] for f in data["farms"]}

    db = SessionLocal()
    try:
        # Remove farms not in the current seed (e.g. trimmed in v0.2)
        existing = db.execute(select(Farm)).scalars().all()
        removed = 0
        for farm in existing:
            if farm.slug not in desired_slugs:
                db.delete(farm)
                removed += 1
        if removed:
            db.commit()
            print(f"Removed {removed} farms no longer in seed list.")

        added = 0
        skipped = 0
        for farm_data in data["farms"]:
            existing_farm = db.execute(
                select(Farm).where(Farm.slug == farm_data["slug"])
            ).scalar_one_or_none()
            if existing_farm:
                # Update diet_profiles + best_for in place so v0.2 tags apply
                existing_farm.diet_profiles = farm_data.get("diet_profiles", [])
                existing_farm.best_for = farm_data.get("best_for")
                skipped += 1
                continue

            address = farm_data.get("address", {}) or {}
            contact = farm_data.get("contact", {}) or {}

            farm = Farm(
                slug=farm_data["slug"],
                name=farm_data["name"],
                alt_names=farm_data.get("alt_names"),
                description=farm_data.get("description"),
                address_line1=address.get("street"),
                city=address.get("city"),
                state=address.get("state"),
                zip=address.get("zip"),
                country=address.get("country", "USA"),
                website=contact.get("website"),
                phone=contact.get("phone"),
                email=contact.get("email"),
                support_email=contact.get("support_email"),
                contact_person=contact.get("contact_person"),
                verification_level=farm_data.get("verification_level", "unverified"),
                verification_source=farm_data.get("verification_source"),
                diet_profiles=farm_data.get("diet_profiles", []),
                best_for=farm_data.get("best_for"),
                is_approved=True,
            )
            for product in farm_data.get("products", []):
                farm.products.append(
                    FarmProduct(
                        product_type=product["type"],
                        notes=product.get("notes"),
                        must_specify=product.get("must_specify"),
                        price_per_unit=product.get("price_per_unit"),
                        unit=product.get("unit"),
                    )
                )
            for method in farm_data.get("fulfillment_methods", []):
                farm.fulfillment.append(FarmFulfillment(method=method))
            for tip in farm_data.get("tips", []):
                farm.tips.append(
                    FarmTip(
                        tip_type=tip["type"],
                        title=tip["title"],
                        body=tip["body"],
                    )
                )
            for cite in farm_data.get("citations", []):
                farm.citations.append(
                    FarmCitation(
                        source_type=cite["source_type"],
                        source_name=cite["source_name"],
                        source_detail=cite.get("source_detail"),
                        source_url=cite.get("source_url"),
                        quote=cite.get("quote"),
                        verified=cite.get("verified", False),
                    )
                )

            db.add(farm)
            added += 1

        db.commit()
        print(f"Done. Added {added} farms, updated tags on {skipped} existing.")
    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    try:
        seed()
    except Exception as e:
        print(f"Skipping seed: {e}")
