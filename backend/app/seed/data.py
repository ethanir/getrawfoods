"""Seed data for v1: five categories, four tiers, four farms.

Editing this file changes what `python -m app.seed.seed` writes to a
fresh database. The seed script is idempotent: re-running on a populated
database is a no-op for already-present slugs and adds anything new.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CategorySeed:
    slug: str
    name: str
    description: str | None
    display_order: int


@dataclass(frozen=True)
class TierSeed:
    slug: str
    name: str
    description: str | None
    display_order: int


@dataclass(frozen=True)
class VerificationSeed:
    category_slug: str
    tier_slug: str


@dataclass(frozen=True)
class FarmSeed:
    slug: str
    name: str
    description: str
    location: str | None = None
    website: str | None = None
    phone: str | None = None
    email: str | None = None
    sourcing_tips: str | None = None
    verifications: tuple[VerificationSeed, ...] = field(default_factory=tuple)


CATEGORIES: tuple[CategorySeed, ...] = (
    CategorySeed(
        slug="raw-dairy",
        name="Raw Dairy",
        description="Unpasteurized milk, cream, butter, and cheese.",
        display_order=1,
    ),
    CategorySeed(
        slug="raw-meat",
        name="Raw Meat",
        description="Pasture-raised meats from farms that support raw consumption.",
        display_order=2,
    ),
    CategorySeed(
        slug="raw-organs",
        name="Raw Organs",
        description="Liver, heart, kidney, and other organs, fresh or frozen.",
        display_order=3,
    ),
    CategorySeed(
        slug="oysters",
        name="Oysters",
        description="Live shellfish for raw eating.",
        display_order=4,
    ),
    CategorySeed(
        slug="wild-seafood",
        name="Wild Seafood",
        description="Wild-caught fish and roe.",
        display_order=5,
    ),
)


TIERS: tuple[TierSeed, ...] = (
    TierSeed(
        slug="aajonus-verified",
        name="Aajonus-verified",
        description="Appears in Aajonus Vonderplanitz's published sourcing materials.",
        display_order=1,
    ),
    TierSeed(
        slug="dev-verified",
        name="Dev-verified",
        description=(
            "The maintainer has personally ordered from this farm and stands "
            "behind it for the categories listed."
        ),
        display_order=2,
    ),
    TierSeed(
        slug="community-verified",
        name="Community-verified",
        description="Submitted by community members and confirmed by multiple users.",
        display_order=3,
    ),
    TierSeed(
        slug="unverified",
        name="Unverified",
        description="Submitted but not yet confirmed.",
        display_order=4,
    ),
)


FARMS: tuple[FarmSeed, ...] = (
    FarmSeed(
        slug="millers-organic-farm",
        name="Miller's Organic Farm",
        location="Bird-in-Hand, PA",
        description=(
            "Direct Aajonus-lineage Amish farm. A2/A2 raw dairy, no-salt cheeses "
            "made with homemade rennet, grass-fed and pastured meats, organs, "
            "and exotic dairy (water buffalo, camel). $30 one-time membership "
            "fee. Premium pricing."
        ),
        website="https://amosmillerorganicfarm.com",
        phone="717-556-0672",
        sourcing_tips=(
            "Sometimes sells fresh organs but usually frozen — ask before "
            "ordering. Butter is usually frozen but can be requested fresh."
        ),
        verifications=(
            VerificationSeed(category_slug="raw-dairy", tier_slug="aajonus-verified"),
            VerificationSeed(category_slug="raw-dairy", tier_slug="dev-verified"),
            VerificationSeed(category_slug="raw-meat", tier_slug="aajonus-verified"),
            VerificationSeed(category_slug="raw-meat", tier_slug="dev-verified"),
            VerificationSeed(category_slug="raw-organs", tier_slug="aajonus-verified"),
            VerificationSeed(category_slug="raw-organs", tier_slug="dev-verified"),
        ),
    ),
    FarmSeed(
        slug="frankies-free-range-meat",
        name="Frankie's Free Range Meat",
        description=(
            "Small-operation pasture-raised meat program. Stocks fresh organs "
            "intermittently. Premium pricing."
        ),
        website="https://frankiesfreerangemeat.com",
        email="info@frankiesfreerangemeat.com",
        sourcing_tips=(
            "Confirm fresh-never-frozen at checkout — substitutions have been reported."
        ),
        verifications=(
            VerificationSeed(category_slug="raw-meat", tier_slug="dev-verified"),
            VerificationSeed(category_slug="raw-organs", tier_slug="dev-verified"),
        ),
    ),
    FarmSeed(
        slug="mark-nolt-farm",
        name="Mark Nolt Farm",
        location="Newville, PA",
        description=(
            "Old-school Amish farm with no website — phone-only ordering. "
            "Aajonus named this farm in his published sourcing materials. A "
            "solid backup when Miller's Organic is sold out."
        ),
        phone="717-776-7575",
        sourcing_tips=(
            "Phone-only ordering. Call to confirm current availability before "
            "driving out."
        ),
        verifications=(
            VerificationSeed(category_slug="raw-dairy", tier_slug="aajonus-verified"),
            VerificationSeed(category_slug="raw-meat", tier_slug="aajonus-verified"),
        ),
    ),
    FarmSeed(
        slug="northstar-bison",
        name="Northstar Bison",
        location="Rice Lake, WI",
        description=(
            "Wisconsin bison ranch with a verified fresh-never-frozen program. "
            "The cleanest US option for raw bison meat and bison organs."
        ),
        website="https://northstarbison.com",
        phone="1-888-295-6332",
        sourcing_tips=(
            "Cuts Mon-Tue, ships Wed for Thu delivery. Call ahead if a specific "
            "cut is needed."
        ),
        verifications=(
            VerificationSeed(category_slug="raw-meat", tier_slug="aajonus-verified"),
            VerificationSeed(category_slug="raw-organs", tier_slug="aajonus-verified"),
        ),
    ),
)
