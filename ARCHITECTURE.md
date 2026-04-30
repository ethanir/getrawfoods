# Architecture

## Goals

GetRawFoods is a read-mostly directory. The expensive operations are catalog browsing and farm lookups; writes are rare (eventually moderator approvals, eventually user submissions). The architecture optimizes for that shape — a normal relational database, a clean read API, a static-feeling SPA — and explicitly avoids infrastructure complexity that does not serve the actual workload.

## Stack

**Backend.** FastAPI on Python 3.12, SQLAlchemy 2.x (declarative `Mapped[...]` style), Alembic for migrations, Pydantic v2 for request and response schemas. Postgres 16 as the database. PostGIS is on the roadmap for geographic search but is deliberately deferred from v1 — there is no map yet, and adding the dependency before it is needed creates ops surface for no benefit.

**Frontend.** React 18 with Vite and TypeScript (strict). Tailwind for styling. React Router for the two routes in v1 (home, farm detail). No state-management library — server state is fetched per route, UI state is local.

**Auth and email.** Outsourced when the time comes: Supabase Auth for JWT and email verification (the Postgres stays ours), Resend for transactional mail. Neither is wired up in v1.

**Local dev.** Docker Compose, three services: `db`, `backend`, `frontend`. Hot reload on backend and frontend.

**Hosting target.** Frontend on Vercel, backend on Fly.io or Railway, database on Neon. Not deployed yet.

## Repo layout

A monorepo with a hard split between `backend/` and `frontend/`. The split is real — they are independently runnable, independently tested, and would deploy to separate hosts. They communicate over HTTP through a typed API. See [ADR-0002](./docs/adr/0002-monorepo-layout.md) for the reasoning.

```
getrawfoods/
├── backend/      FastAPI app, SQLAlchemy models, Alembic migrations, seed data
├── frontend/     React SPA, Vite build, Tailwind styles
├── docs/         Architecture (this file), ADRs, schema reference
└── docker-compose.yml
```

## Data model

The directory is shaped around three concepts: **farms**, **categories**, and **verifications**. Categories are a fixed enum for v1 (raw dairy, raw meat, raw organs, oysters, wild seafood). Verification is **per (farm, category) pair**, not per farm — a farm can be Aajonus-verified for meat but not for dairy if Aajonus's published materials only spoke to its meat program. This shape keeps the directory honest at the cost of a join table; it is the right tradeoff. The full schema reference will live at `docs/schema.md` once the models are written.

## What is intentionally out of scope for v1

- User accounts, submissions, moderation
- Reviews, voting, comments
- Forum
- Geographic search and map
- Curated source library

These are real features, planned, and the schema and architecture will accommodate them — but adding them now would dilute the v1 milestone. v1 is a clean read-only directory of four seeded farms.
