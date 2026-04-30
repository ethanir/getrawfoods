# ADR 0002: Monorepo with backend and frontend split

**Date:** 2026-04-29
**Status:** Accepted

## Context

GetRawFoods has a Python backend and a TypeScript frontend (see [ADR-0001](./0001-stack.md)). They are independently runnable and will deploy to separate hosts. The repo can be organized as a monorepo with two top-level directories or as two separate repos.

## Decision

Single monorepo. Two top-level application directories: `backend/` and `frontend/`. Each has its own dependency manifest (`pyproject.toml`, `package.json`), its own Dockerfile, and its own test suite. Cross-cutting documentation (architecture, ADRs, schema reference) lives at the repo root under `docs/`.

```
getrawfoods/
├── backend/
├── frontend/
├── docs/
├── docker-compose.yml
└── README.md
```

## Considered alternatives

**Two repos (`getrawfoods-api`, `getrawfoods-web`).** Cleaner deploy boundaries, separate issue trackers. Rejected because the two halves change together — a schema change requires a coordinated frontend change, and forcing that across two repos adds friction without gain at this scale. A single commit capturing both sides of a change is more honest than two coordinated ones.

**Polyglot single root (no `backend/` or `frontend/`).** Files at the top level, distinguished by extension or convention. Rejected — the runtimes have incompatible tooling assumptions (`node_modules` vs `.venv`, `package.json` vs `pyproject.toml`) and mingling them at the root breaks every IDE's project root inference.

## Consequences

- Docker Compose mounts each application directory into its respective container. Service boundaries match directory boundaries.
- CI, when added, will need separate jobs for backend and frontend. Acceptable.
- A future third application (a worker, a CLI) gets its own top-level directory under the same convention.
