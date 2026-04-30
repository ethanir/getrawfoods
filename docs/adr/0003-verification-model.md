# ADR 0003: Verification model — per (farm, category) tuple

**Date:** 2026-04-29
**Status:** Accepted

## Context

A farm in the directory carries verification badges that signal trust. The brief defines four tiers, in display order:

1. **Aajonus-verified** — the farm appears in Aajonus Vonderplanitz's published sourcing materials.
2. **Dev-verified** — the maintainer has personally ordered from the farm and stands behind it for the categories listed.
3. **Community-verified** — submitted by community members and confirmed by multiple users (activates in Phase 3 when submissions go live).
4. **Unverified** — submitted but not yet confirmed.

A farm can carry multiple tiers. Miller's Organic Farm is both Aajonus-verified and Dev-verified, for example.

The shape of the verification data decides what the directory can honestly claim. Two options were on the table.

## Decision

Verification is per **(farm, category, tier)** — a row in a join table called `verifications` with foreign keys to `farms`, `categories`, and `tiers`, and a composite unique constraint over the three. A farm with three Aajonus-verified categories and three Dev-verified categories has six rows in this table.

Categories and tiers are both modeled as their own tables (rather than as Postgres enums), so display ordering, descriptions, and any future per-category or per-tier metadata live as data rather than as code. Adding a new category or tier is a single row, not a schema migration.

## Considered alternative

**Verification per farm, not per (farm, category).** A simpler shape: a farm has a set of badges (Aajonus-verified, Dev-verified) that apply to all of its listed categories.

Rejected because it cannot honestly represent the actual data. Frankie's Free Range Meat lists raw butter on its website, but the maintainer has only ordered meat and organs from there — Frankie's is dev-verified for meat and organs, not for dairy. Under the per-farm shape, listing Frankie's at all forces a choice between over-claiming (the dev-verified badge applies to dairy, which is false) and under-claiming (drop dairy entirely, even when the dairy program might be fine for someone else). The per-(farm, category) shape lets the directory list a farm under exactly the categories its verifications cover.

The cost is a join table and one extra select per page. Worth it.

## Consequences

- The home page renders five category sections by joining `farms` to `categories` through `verifications` and grouping. A farm with verifications in three categories appears in three sections, with the badges relevant to each category.
- The farm detail page shows all of a farm's badges grouped by category.
- Adding a new tier (e.g., when community submissions activate) is a row in `tiers`. Adding a new category is a row in `categories`. Neither requires a migration.
- The verifications table grows linearly with farms × verified categories × tiers. For v1 (4 farms, 14 verifications) this is trivial; the shape supports thousands of farms without restructuring.
- The seed script in `backend/app/seed/` is the source of truth for v1 reference data. It is idempotent — re-running on a populated database is a no-op for already-present slugs.
