# Schema reference

Status: v1 (read-only directory).

The schema is defined by the SQLAlchemy models in `backend/app/models/` and migrated by Alembic from `backend/alembic/versions/`. This document is the human-readable mirror of those.

## Tables

### `categories`

Five fixed entries in v1: raw dairy, raw meat, raw organs, oysters, wild seafood. The home page renders one section per category, in `display_order`.

| Column | Type | Notes |
|---|---|---|
| `id` | integer | Primary key. |
| `slug` | varchar(64), unique | URL-safe identifier (`raw-dairy`, `raw-meat`, ...). |
| `name` | varchar(128) | Display name (`Raw Dairy`). |
| `description` | text, nullable | Short blurb shown under the category section header. |
| `display_order` | integer | Controls section ordering on the home page. |
| `created_at` | timestamptz | Server default `now()`. |

Indexes: `slug` (unique).

### `tiers`

Four fixed entries in v1: aajonus-verified, dev-verified, community-verified, unverified. Modeled as a table rather than a Postgres enum so display ordering and descriptions live in the database.

| Column | Type | Notes |
|---|---|---|
| `id` | integer | Primary key. |
| `slug` | varchar(64), unique | `aajonus-verified`, `dev-verified`, `community-verified`, `unverified`. |
| `name` | varchar(128) | Display name. |
| `description` | text, nullable | What the tier means. |
| `display_order` | integer | Badge ordering when multiple tiers apply. |
| `created_at` | timestamptz | Server default `now()`. |

Indexes: `slug` (unique).

### `farms`

The core directory entry. One row per farm.

| Column | Type | Notes |
|---|---|---|
| `id` | integer | Primary key. |
| `slug` | varchar(128), unique | URL-safe identifier (`millers-organic-farm`). |
| `name` | varchar(256) | Display name. |
| `location` | varchar(256), nullable | "Bird-in-Hand, PA" — optional; some farms do not disclose. |
| `description` | text | Paragraph shown on detail page. |
| `website` | varchar(512), nullable | |
| `phone` | varchar(64), nullable | Stored verbatim; no format normalization in v1. |
| `email` | varchar(256), nullable | |
| `sourcing_tips` | text, nullable | Plain text, paragraph-separated. Operational notes (e.g., "verify fresh-never-frozen at checkout"). Markdown is **not** rendered in v1. |
| `created_at` | timestamptz | Server default `now()`. |
| `updated_at` | timestamptz | Server default `now()`, refreshed on update. |

Indexes: `slug` (unique), `name`.

### `verifications`

The join table. One row per (farm, category, tier) badge.

| Column | Type | Notes |
|---|---|---|
| `id` | integer | Primary key. |
| `farm_id` | integer, FK → `farms.id` `ON DELETE CASCADE` | |
| `category_id` | integer, FK → `categories.id` `ON DELETE CASCADE` | |
| `tier_id` | integer, FK → `tiers.id` `ON DELETE RESTRICT` | Tier deletion is restricted because losing a tier with attached verifications should be an explicit operation. |
| `created_at` | timestamptz | Server default `now()`. |

Constraints: composite UNIQUE on `(farm_id, category_id, tier_id)`.
Indexes: each foreign key column.

See [ADR-0003](./adr/0003-verification-model.md) for why verification is per (farm, category) rather than per farm.

## v1 cardinality

5 categories, 4 tiers, 4 farms, 14 verifications.
