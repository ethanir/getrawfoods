# Contributing

GetRawFoods is solo-maintained. This document records the conventions the repo follows so future contributors (or future me) can work consistently.

## Workflow

Direct commits to `main` are the default. Branches exist for genuinely risky changes — large schema rewrites, dependency upgrades, exploratory rewrites — not for routine feature work. There is no PR ceremony, no required review, no CI gating. CI may exist as informational signal but never as a blocker.

## Commit conventions

Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `style:`, `perf:`. One concern per commit. The first `-m` is a single-line subject in imperative mood. Subsequent `-m` flags are paragraphs explaining what changed and why — the *why* is the part that earns its keep months later.

Example subject and body:

```
feat: add per-category verification join table

Verification is per (farm, category) pair, not farm-wide. Frankie's
Free Range Meat is dev-verified for meat and organs but not for
dairy; Miller's Organic Farm is Aajonus-verified across dairy, meat,
and organs. Modeling this farm-wide would either over-claim or
under-claim.

The join table is farm_category_verifications(farm_id, category_id,
tier_id), with a composite unique constraint on (farm, category,
tier). The API returns badges grouped by category in the tier order
documented in ADR-0003.
```

## Code style

**Python.** Ruff and Black, configured in `backend/pyproject.toml`. Type hints everywhere. SQLAlchemy 2.x `Mapped[...]` declarative style — no legacy `Column(...)` declarations. Pydantic v2 for all request and response schemas.

**TypeScript.** ESLint and Prettier, configured in `frontend/`. Strict mode on. Functional components and hooks; no class components.

Linters are not gating. They are a courtesy to the next reader.

## Comments

Comments explain *why*, not *what*. The code already says what. If a comment paraphrases the code on the next line, delete it.

## Architecture decisions

Significant architectural choices land as ADRs in `docs/adr/`, written the same session the decision is made. The format is light: context, decision, alternatives considered, consequences. The point is to capture the reasoning while it is fresh, not to produce a polished document.
