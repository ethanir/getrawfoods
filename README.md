# GetRawFoods

A community-driven sourcing directory for raw meat, organs, dairy, and wild seafood — for people eating in the carnivore and Aajonus primal traditions.

The aim is one place where someone new to raw eating can find verified farms, see exactly what each one sells, and learn the operational details that actually matter — the checkout note that gets fresh shipping, the order window for fresh oysters, the phone script for an Amish farm with no website.

**Status:** early. Building toward v1: a read-only directory of four seeded farms across five categories. User submissions, reviews, and the forum come later.

## Repository

- `backend/` — FastAPI + SQLAlchemy + Postgres API.
- `frontend/` — React + Vite + Tailwind UI. *Not yet scaffolded.*
- `docs/` — Architecture overview, ADRs, schema reference.

For the engineering overview, see [`ARCHITECTURE.md`](./ARCHITECTURE.md). For decisions and their reasoning, see [`docs/adr/`](./docs/adr/). For the database schema, see [`docs/schema.md`](./docs/schema.md). For repo conventions, see [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## Local development

Requires Docker. First-time setup:

```
docker compose up -d
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seed.seed
```

The API is then live at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs` and a health check at `http://localhost:8000/api/health`. After the first setup, `docker compose up -d` is enough.

To run the test suite:

```
docker compose exec backend pytest
```

The frontend service joins this compose stack when the frontend is scaffolded.

## License

MIT. See [`LICENSE`](./LICENSE).

## Disclaimers

GetRawFoods is a sourcing directory, not medical advice. It is not a marketplace — no payments, no order processing. It is not affiliated with the estate of Aajonus Vonderplanitz; the "Aajonus-verified" tier indicates a farm appears in his published sourcing materials, nothing more.
