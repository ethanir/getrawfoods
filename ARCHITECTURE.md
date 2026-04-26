# Architecture

This document describes how GetRawFoods is put together and why. For specific decisions and tradeoffs, see [`docs/decisions/`](./docs/decisions/).

## High-level system

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │     │                     │
│   React frontend    │────▶│   FastAPI backend   │────▶│  PostgreSQL +       │
│   (Vite, Tailwind,  │ HTTP│   (REST, async      │ SQL │  PostGIS            │
│    Leaflet)         │     │    SQLAlchemy)      │     │                     │
│                     │     │                     │     │                     │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
        │                            │                           │
        │                            │                           │
        ▼                            ▼                           ▼
   Vercel CDN                  Fly.io / Railway              Neon / Supabase
   (production)                (production)                  (production)
```

In dev: all three run in Docker via `docker-compose.yml`.
In prod: each layer deploys independently to its own provider.

## Why this shape

**Three separate services, not a monolith.** A Next.js full-stack app would be quicker to ship initially, but separating the API from the UI gives us:
- Independent scaling (the API can run on the cheapest tier; the static frontend lives on a CDN)
- Easy to swap either side later (e.g., add a mobile app, the API doesn't change)
- Clean deployment story — frontend is static files, backend is one container, database is managed
- Forces clean API design from day one (resume-grade)

**Postgres + PostGIS, not separate search/geo databases.** At MVP scale (and well past it), Postgres handles full-text search via `tsvector` and geographic queries via PostGIS just fine. Adding Elasticsearch / MeiliSearch / a separate geo service is premature. We can add them in Phase 5+ if search performance becomes a bottleneck.

**Leaflet + OpenStreetMap, not Google Maps or Mapbox.** Both have free tiers but require API keys, billing accounts, and have rate limits that bite under any real traffic. Leaflet + OSM is free forever and the maintainers have no incentive to change that.

## Data model

The database is the heart of the project. Schema lives in [`docs/schema.md`](./docs/schema.md) and is implemented in [`backend/alembic/versions/0001_initial_schema.py`](./backend/alembic/versions/0001_initial_schema.py).

Key entities:

- **`farms`** — the core directory. Has location (PostGIS `GEOGRAPHY` point), verification level, contact info, status.
- **`farm_products`** — what each farm sells (raw butter, ground beef, etc.) with notes on what to specify.
- **`farm_fulfillment`** — how you can buy (in-person, herd-share, ships-nationwide).
- **`farm_tips`** — sourcing tips per farm: checkout notes, phone scripts, insider knowledge, warnings.
- **`farm_citations`** — links to primary sources (aajonus.net pages, book references).
- **`farm_verifications`** — community check-ins keeping data fresh ("still operating as of 2026").
- **`reviews`** — user reviews of farms.
- **`users`**, **`forum_categories`**, **`threads`**, **`posts`**, **`votes`** — the community layer.

The schema deliberately separates *facts about a farm* (one row in `farms`) from *opinions about it* (rows in `reviews`, `tips`, `verifications`). This makes the data resilient: bad reviews don't erase good farm info; good farms can survive temporary stock issues.

## Request flow (example: viewing a farm)

```
1. User clicks farm slug → React Router navigates to /farms/millers-organic-farm
2. <FarmDetail> mounts → calls api.getFarm(slug) → fetch GET /api/farms/millers-organic-farm
3. FastAPI route handler → query DB joining farms, products, fulfillment, tips, citations
4. SQLAlchemy returns ORM objects → Pydantic schema serializes to JSON
5. React receives JSON → renders the page
```

No GraphQL, no tRPC, no fancy stuff. Plain REST with auto-generated OpenAPI docs. Easy to learn, easy to debug, easy to add to a portfolio.

## Authentication (Phase 3)

Not built yet. Plan:
- JWT access tokens (15 min) + refresh tokens (30 days), stored as httpOnly cookies
- Password hashing with bcrypt
- Optional Google OAuth in a later phase
- All write endpoints will require auth; read endpoints stay public for SEO

## Source attribution & copyright posture

Aajonus's writings are still under copyright. The `farm_citations` table stores *links and brief paraphrased context* — never the original text. The "Source Library" feature (Phase 6) is a *navigator* into [aajonus.net](https://aajonus.net), not a copy of it. This is both legally correct and strategically smart: it makes us indispensable as the curator without competing with the source.

## Deployment

| Environment | Frontend          | Backend                | Database         |
|-------------|-------------------|------------------------|------------------|
| Dev         | Vite (local 3000) | Uvicorn (local 8000)   | Postgres in Docker |
| Production  | Vercel            | Fly.io app or Railway  | Neon (managed)   |

CI runs on every push: lint + test + type check. Deploys go automatic on `main`.

## What's intentionally not in v1

- **No CMS.** Admin actions (approving farm submissions, editing tips) happen via direct DB writes or a tiny admin UI later. A full CMS is overkill.
- **No payments.** Phase 1+ stays free. Pro tier comes only after we have ~500 active users.
- **No notifications, no email.** Until we have something worth notifying users about.
- **No real-time anything.** Polling is fine. WebSockets when there's a reason.

Adding these later is straightforward; building them upfront is wasted work.
