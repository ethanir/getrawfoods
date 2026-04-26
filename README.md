# GetRawFoods

A community-driven sourcing directory for raw meat, organs, dairy, and wild seafood. Built for the raw carnivore, primal, and ancestral health communities.

The web is full of scattered information about where to source raw dairy, grass-fed organs, wild seafood, and other raw food staples — Reddit threads, Telegram groups, decade-old PDFs, half-broken Aajonus directory pages. GetRawFoods consolidates that knowledge: a searchable directory of farms and online suppliers, with sourcing tips, citations to primary sources, and a forum for community contributions.

## What this is

- **Farm directory.** Every entry has products, fulfillment methods (in-person / herd-share / ships), verified standards, and a verification level (Aajonus-verified, dev-recommended, community-verified, unverified).
- **Sourcing tips.** Checkout note templates, phone scripts, shipping tricks, insider knowledge — the practical stuff that turns "I know about Amos Miller" into "I just placed a successful $400 fresh-shipment order."
- **Source library.** Curated links into [aajonus.net](https://aajonus.net) and primary sources (his books, Q&As, interviews) so users can verify claims at the source. We don't reproduce his copyrighted text — we navigate it.
- **Forum.** Categories for sourcing, protocols, experiences, and lineage. Where new tips get generated.
- **Map.** Geographic search across the directory using PostGIS.

## What this isn't

- Not a marketplace. We don't sell anything.
- Not a medical resource. Disclaimers everywhere.
- Not affiliated with Aajonus's estate. This is a community project that respects his work.

## Tech stack

| Layer        | Choice                                           | Why                                                                      |
|--------------|--------------------------------------------------|--------------------------------------------------------------------------|
| Backend      | FastAPI + SQLAlchemy + Alembic                   | Type-safe, async, great DX, free OpenAPI docs                            |
| Database     | PostgreSQL + PostGIS                             | Full-text search + geographic queries, no Elasticsearch needed at scale  |
| Frontend     | React + Vite + Tailwind                          | Fast dev loop, no framework overhead, easy to customize                  |
| Map          | Leaflet + OpenStreetMap                          | Free forever, no API keys, no rate limits                                |
| Auth         | JWT + bcrypt (Google OAuth optional later)       | Standard, no vendor lock-in                                              |
| Hosting      | Vercel (FE) + Fly.io or Railway (BE) + Neon (DB) | Free at MVP scale, scales gracefully                                     |

See [`docs/decisions/`](./docs/decisions/) for full ADRs (Architecture Decision Records).

## Getting started

You need Docker and Docker Compose installed. Nothing else — the whole stack runs in containers.

```bash
git clone <this-repo>
cd getrawfoods
cp .env.example .env             # tweak if you want
docker compose up --build
```

Three services come up:

- `db` — Postgres 16 with PostGIS extension, exposed on `localhost:5432`
- `backend` — FastAPI on `localhost:8000` (auto-reloads on code changes)
- `frontend` — Vite dev server on `localhost:3000` (hot-reload)

Open [http://localhost:3000](http://localhost:3000) — you should see a list of seeded farms.

API docs (Swagger UI) live at [http://localhost:8000/docs](http://localhost:8000/docs).

### Seeding the database

The first time you run `docker compose up`, the migration runs automatically and the seed script loads `docs/seed_data.json`. To reseed:

```bash
docker compose exec backend python scripts/seed.py
```

### Running migrations after schema changes

```bash
docker compose exec backend alembic revision --autogenerate -m "description"
docker compose exec backend alembic upgrade head
```

## Project structure

```
getrawfoods/
├── README.md                  # this file
├── ARCHITECTURE.md            # system overview & data flow
├── CONTRIBUTING.md            # how to contribute
├── docker-compose.yml         # local dev environment
├── .env.example               # env template
├── docs/
│   ├── decisions/             # ADRs — major architecture decisions, why
│   ├── schema.md              # database schema reference
│   └── seed_data.json         # initial farms, products, tips, forum content
├── backend/
│   ├── pyproject.toml         # Python deps
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── alembic/               # database migrations
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── core/              # config, db, auth utilities
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic request/response schemas
│   │   └── api/               # API route handlers
│   └── scripts/
│       └── seed.py            # loads seed_data.json into the database
└── frontend/
    ├── package.json
    ├── Dockerfile
    ├── vite.config.js
    ├── tailwind.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css          # design tokens & base styles
        ├── pages/             # top-level routes
        ├── components/        # reusable UI
        └── lib/api.js         # API client
```

## Roadmap

- [x] Phase 0 — Foundation: schema, seed data, runnable skeleton
- [ ] Phase 1 — Browse: farm directory, filters, farm detail pages, basic search
- [ ] Phase 2 — Map: PostGIS-backed map view with clustering
- [ ] Phase 3 — Auth & community: signup, profiles, submit-a-farm flow with admin review
- [ ] Phase 4 — Reviews: per-farm reviews and community verification
- [ ] Phase 5 — Forum: categories, threads, posts, voting, markdown
- [ ] Phase 6 — Source library: structured links to aajonus.net by topic, citation system
- [ ] Phase 7 — Polish & launch: SEO, mobile, deploy, soft launch in target communities

## Disclaimer

This project is a community resource for educational purposes. Information is presented for reference; nothing on this site constitutes medical, dietary, or legal advice. Raw foods carry inherent risks. Consult appropriate professionals. The maintainers are not affiliated with Aajonus Vonderplanitz, his estate, or any farm listed here.

## License

MIT — see `LICENSE`. Seed data is original work by this project's contributors. Citations link to primary sources rather than reproducing them.
