# Contributing

GetRawFoods welcomes contributions. The most valuable contributions, in rough order:

1. **Verified farm submissions.** A farm you've personally ordered from, with photos, recent order details, and product quality notes.
2. **Sourcing tips.** A working checkout note, a phone script that gets fresh shipping, an insider trick.
3. **Citations.** A specific Aajonus quote tied to a specific page, book, or Q&A — with the URL on aajonus.net or the book reference.
4. **Bug reports & UI feedback.** Anything broken, ugly, or confusing.
5. **Code contributions.** Once the project is past MVP.

## Submitting a farm

The web UI's "Submit a Farm" form (Phase 3) is the right path once it exists. Until then, open an issue with the farm details using the schema in `docs/seed_data.json`.

## Code contributions

### Setup

See README — `docker compose up` is the whole story.

### Style

- **Python**: `ruff` for linting, `black` for formatting, type hints everywhere.
- **JavaScript**: Plain ESLint + Prettier defaults. No bikeshedding.
- **Commits**: Conventional commits (`feat:`, `fix:`, `docs:`, etc.).
- **Branches**: `feat/short-description` or `fix/short-description`.

### Pull requests

- One concern per PR. Don't bundle unrelated changes.
- Include a description of *why*, not just *what*.
- If it touches the schema, include the migration.
- If it touches the UI, include a screenshot.
- All checks must pass.

## Code of conduct

Be useful. Don't be a dick. The community we're building exists for people genuinely interested in the diet — keep discussions on-topic and respectful, even when disagreeing.

Anything beyond that gets handled case-by-case at maintainer discretion.

## License

By contributing, you agree your contributions are licensed under MIT (the project license).
