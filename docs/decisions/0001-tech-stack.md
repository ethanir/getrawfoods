# ADR 0001: Tech Stack

**Status**: Accepted
**Date**: 2026-04-26

## Context

We're building a community knowledge base for a niche health movement. Audience is small but passionate (~50k–200k worldwide). Traffic at MVP will be tiny; could grow to ~10k DAU within a year if soft launch goes well. Single developer (initially), part-time, prioritizing both shippability and resume value.

## Decision

| Layer        | Choice                              |
|--------------|-------------------------------------|
| Backend      | FastAPI + SQLAlchemy 2.x + Alembic  |
| Database     | PostgreSQL 16 + PostGIS             |
| Frontend     | React 18 + Vite + Tailwind 3        |
| Map          | Leaflet + OpenStreetMap             |
| Hosting (FE) | Vercel                              |
| Hosting (BE) | Fly.io or Railway                   |
| Hosting (DB) | Neon or Supabase                    |
| CI           | GitHub Actions                      |

## Considered alternatives

### Backend
- **Next.js full-stack**: Faster to ship, BUT couples the API to the UI and makes mobile/CLI clients painful later. Also less portfolio-impressive for a developer trying to demonstrate full-stack range.
- **Django + DRF**: Mature, batteries-included. Heavier and less idiomatic for type-safe async APIs. Migrations less ergonomic than Alembic for this scale.
- **Express/Fastify (Node)**: Fine choice. Picked Python over Node because the developer is more proficient in Python and FastAPI's auto-OpenAPI is genuinely useful.

### Database
- **MongoDB**: Easier for unstructured data, but our domain is highly relational (farms ↔ products ↔ tips ↔ reviews ↔ users) and we need geographic queries. Postgres + PostGIS wins on every dimension.
- **SQLite**: Fine for prototyping, doesn't scale to multi-instance backend. Postgres in Docker is one extra container.

### Search
- **Elasticsearch / MeiliSearch**: Premature. Postgres `tsvector` + `pg_trgm` handles full-text search well into the millions of rows. Add only if it becomes a bottleneck.

### Frontend
- **Next.js**: Good SSR/SEO story, but adds complexity. We can add SSR later via separate prerender service or migrate to Next when SEO becomes the bottleneck.
- **SvelteKit / SolidStart**: Slick but smaller ecosystem; more friction for a contributor pool that defaults to React.

### Map
- **Mapbox**: Beautiful, free tier exists, but rate-limited and requires account/API keys. Lock-in risk.
- **Google Maps**: Same issues as Mapbox plus pricier.

## Consequences

### Positive
- Free or near-free hosting at MVP scale (~$0–10/mo).
- Single language (Python) on the backend; mainstream language (JS) on the frontend — easy to find contributors.
- All choices are battle-tested and well-documented.
- Auto-generated OpenAPI docs are a free feature.
- PostGIS handles every geographic query we'll need at scale.

### Negative
- More moving parts than a Next.js monolith — three deployments to coordinate.
- React + Vite + Tailwind has churn; lock dependency versions and document upgrades.
- PostGIS adds Docker image size; mitigated by using `postgis/postgis` image directly.

## Revisit

If by Phase 5 we have:
- > 100k farms or > 1M forum posts → consider Elasticsearch
- SEO not ranking despite content → consider migrating frontend to Next.js for SSR
- > 10k DAU → re-evaluate hosting tiers
