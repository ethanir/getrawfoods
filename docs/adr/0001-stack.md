# ADR 0001: Initial tech stack

**Date:** 2026-04-29
**Status:** Accepted

## Context

GetRawFoods is a read-mostly directory with eventual user submissions, moderation, reviews, and a forum. v1 is a static-feeling read API plus a two-page SPA. The stack must support the whole roadmap without rewrites, but should not pay infrastructure cost for features that are not in v1.

The maintainer is solo, on Apple Silicon, with strong familiarity with Python and React. The codebase is portfolio material — it is read by humans as much as it is run.

## Decision

**Backend.** FastAPI on Python 3.12, SQLAlchemy 2.x (`Mapped[...]` declarative style), Alembic, Pydantic v2, Postgres 16. PostGIS deferred until geographic search is built.

**Frontend.** React 18, Vite, TypeScript (strict), Tailwind 3, React Router.

**Local development.** Docker Compose with three services (`db`, `backend`, `frontend`).

**Auth and email.** Supabase Auth and Resend, wired up when needed. Neither is in v1.

**Hosting target.** Vercel (frontend) + Fly.io or Railway (backend) + Neon (Postgres).

## Considered alternatives

**Next.js or T3 (full TypeScript stack).** Single language across the codebase, server components, single deploy target. Rejected because collapsing backend and frontend into one runtime weakens the demonstration of real backend/frontend separation, which is an explicit goal of the project. The Python ecosystem is also a better fit for any future data work (scraping, importing, batch verification) than the Node equivalent.

**Django.** Heavier than FastAPI, batteries-included where this project does not need batteries (admin, forced ORM, templating). FastAPI's Pydantic-native request and response handling is a closer fit to a directory API.

**SQLite for v1.** Tempting for the four-farm seed, but the project will gain users, submissions, and full-text search; a Postgres-shaped data model written against SQLite from day one accumulates compatibility quirks. Postgres in Docker from day one is cheap.

**PostGIS from day one.** Rejected. PostGIS will be added in the migration that introduces geographic search. Adding the extension now buys nothing and complicates the Docker image.

## Consequences

- Two runtimes to operate (Python and Node). Acceptable for a solo developer; the separation is the point.
- Type information is duplicated across Pydantic and TypeScript. v1 keeps the API surface small enough that hand-maintained types are fine. If the surface grows, generating TS types from the OpenAPI schema is a one-command upgrade.
- Tailwind is a strong style commitment. Acceptable — the design direction (clean, restrained, breathing room) is well-served by utility classes plus a small set of semantic component primitives.
