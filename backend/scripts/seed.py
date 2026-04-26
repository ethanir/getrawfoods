"""Seed the database from docs/seed_data.json.

Idempotent — safe to run multiple times. Uses slug as the unique key for farms.
"""

import json
import sys
from pathlib import Path

# Ensure app package is importable when run as a script
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
    Path("/app/docs/seed_data.json"),  # docker-mounted location
    Path(__file__).resolve().parent.parent / "seed_data.json",
    Path(__file__).resolve().parent.parent.parent / "docs" / "seed_data.json",
]


def find_seed_file() -> Path:
    for path in SEED_PATH_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError(
        f"Could not find seed_data.json. Tried: {[str(p) for p in SEED_PATH_CANDIDATES]}"
    )


def seed() -> None:
    seed_path = find_seed_file()
    print(f"Loading seed data from {seed_path}")
    data = json.loads(seed_path.read_text())

    db = SessionLocal()
    try:
        farms_added = 0
        farms_skipped = 0

        for farm_data in data.get("farms", []):
            slug = farm_data["slug"]

            existing = db.scalar(select(Farm).where(Farm.slug == slug))
            if existing:
                farms_skipped += 1
                continue

            address = farm_data.get("address", {}) or {}
            contact = farm_data.get("contact", {}) or {}

            farm = Farm(
                slug=slug,
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
                is_approved=True,  # seed entries are pre-approved
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
            farms_added += 1

        db.commit()
        print(f"Done. Added {farms_added} farms, skipped {farms_skipped} (already present).")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
