# ADR 0006: Multi-verification and product categories

**Status**: Accepted
**Date**: 2026-04-29

## Context

The v0.2 schema had two limitations that v0.4 needs to lift:

1. `verification_level` is a single string. Miller's Organic Farm is verified
   by both Aajonus (it appears in his published sourcing materials) *and* by
   the maintainer (who orders from there regularly). The single-string field
   forces us to pick one badge or invent a hybrid level. Both options lose
   information.

2. There's no way to express what *kind of food* a farm sells in a way that
   the directory can navigate by. Products exist as rows in `farm_products`
   keyed to specific items (raw_cow_milk, beef_cuts, etc.) — useful for the
   detail page, useless for "show me everyone selling raw dairy."

## Decision

### Multi-verification

`farms.verification_level: VARCHAR(20)` becomes
`farms.verification_levels: JSONB NOT NULL DEFAULT '[]'`. Multiple values
allowed. Render order in UI is fixed:
`aajonus_verified` → `dev_verified` → `community_verified` → `unverified`.
A farm with no levels is implicitly unverified and shouldn't ship.

`dev_recommended` is renamed to `dev_verified` in the new schema — "verified"
is the accurate term for "the maintainer has personally bought from and stands
behind this farm." Existing rows are migrated via the migration's data step.

GIN index on the new column for fast containment queries
(`WHERE verification_levels @> '["aajonus_verified"]'`).

### Product categories

New column `farms.categories: JSONB NOT NULL DEFAULT '[]'`. v0.4 vocab:

- `raw_dairy`
- `raw_meat`
- `raw_organs`
- `oysters`

A farm carries every category it meaningfully sells **and is verified for**.
Miller's = `["raw_dairy", "raw_meat", "raw_organs"]`. Frankie's =
`["raw_meat", "raw_organs"]`. Northstar = `["raw_meat", "raw_organs"]`.
Mark Nolt = `["raw_dairy", "raw_meat"]`.

A farm is listed under a category only when verified (Aajonus-verified or
dev-verified) for *that category's products*. Frankie's offers raw dairy
on their site but is dev-verified only for meat and organs, so it does not
appear in the raw dairy section. This keeps the directory honest — a
listing means someone trusted has actually bought and stood behind that
food type from that farm, not that the farm has it on their price list.

GIN index on the column. API exposes `GET /api/farms?category=raw_meat`.

The existing `farm_products` table stays. Categories are a coarse navigation
layer over the fine-grained product inventory — they're not redundant.
A farm's `categories` is computed-from-intent (set in seed / submission flow),
not derived from `farm_products` rows; this lets us list a category without
having every specific product cataloged yet.

### Diet profiles

No change to `diet_profiles` schema. UI stops rendering the filter in v0.4
per ADR 0005 but the data persists.

## Consequences

### Positive
- Miller's accurately wears both badges (Aajonus + dev) without inventing a
  hybrid level.
- Category navigation maps to how users actually shop.
- Schema change is small (two array columns + one rename) and reversible.

### Negative
- API contract changes: `verification_level` (string) → `verification_levels`
  (array). Frontend needs a coordinated update. v0.4 ships both schema and
  client changes in the same release.
- New `categories` field must be hand-curated per farm. Acceptable — there
  are 4 farms.

### Migration plan
See `backend/alembic/versions/0003_categories_and_multi_verification.py`.
Sequence: drop old index → add `verification_levels` JSONB → backfill from
`verification_level` (with `dev_recommended` → `dev_verified` rename) →
drop `verification_level` column → add `categories` JSONB → seed re-runs and
sets categories from `seed_data.json` v0.4.
