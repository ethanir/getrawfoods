# ADR 0005: Aesthetic refresh and category-led navigation

**Status**: Accepted
**Date**: 2026-04-29
**Supersedes parts of**: 0002 (aesthetic), 0003 (diet profiles as primary filter)

## Context

ADR 0002 committed to a Hacker News / Craigslist density. Shipped in v0.1 and
v0.2, this read as cramped and lo-fi to the maintainer once it was actually in
use day-to-day. The tradeoff was real but the wrong call for this project: the
audience values trust *and* care, not just trust. Pure utilitarian density
signals "abandoned" before it signals "serious."

ADR 0003 made diet profiles (raw carnivore / Aajonus primal / Weston A. Price)
the primary navigation. With only 4 farms in v0.4 — all of which serve all
three diet profiles — that filter is moot. Users land on the page and have
nothing useful to filter by.

The actual mental model users bring to the directory is by *what they're
shopping for* — raw dairy today, organs next week, oysters when they want them.
That's the navigation that matches intent.

## Decision

### Aesthetic

Refined minimalism. Same bones as ADR 0002 (utilitarian, hairlines, sharp
edges, IBM Plex stack, single oxblood accent) but loosened density and
warmer palette.

- Background: `#F5F0E5` (warm cream, replaces `#FAF8F5`)
- Ink: `#1F1A15` (warm dark, replaces `#1A1A1A`)
- Muted: `#6B6358` (warm gray, replaces `#6B6B6B`)
- Border: `#E0D9CC` (warm hairline, replaces `#D8D2C8`)
- Accent: `#6B1F1F` (oxblood, unchanged)
- Type stack: IBM Plex Serif (headings), IBM Plex Sans (body), IBM Plex Mono
  (small caps labels) — unchanged but `--font-serif` and `--font-mono` tokens
  are now defined in `:root`, fixing the silent-fallback bug from v0.2
- Spacing: `1.25rem` row padding (was `0.875rem`); body line-height `1.65`
  (was `1.5`); `h1` at `2rem` (was `1.75rem`)
- Section labels: mono 11px in muted, letter-spacing `0.12em`,
  text-transform uppercase, hairline rule below
- Drop the dual `.farm-row` / `.ph-farm-row` legacy class system — unify
  on semantic class names without prefix

The signal is "considered reference document" not "abandoned 2010 forum." Every
choice that makes it look more polished without adding noise is welcome; every
choice that adds chrome (gradients, shadows, animations, decorative icons) is
not.

### Navigation

Categories are the primary navigation: **raw dairy / raw meat / raw organs /
oysters**. Page renders one section per category, each section labeled in mono
small caps, listing every farm that serves it. Farms with multiple categories
appear in multiple sections — duplication is intentional, it matches how users
actually browse ("I want raw dairy, who's got it?").

Diet profile filter pills are removed from v0.4 but the schema field
(`diet_profiles`) stays — re-add the filter when the dataset is large enough
that diet variation becomes a meaningful axis.

Search and verification-level dropdown also removed for v0.4 — too few farms
to need them. Re-add when the directory exceeds ~20 entries.

## Consequences

### Positive
- Loses the "is this site maintained?" first impression of pure HN density.
- Category navigation matches user intent better than diet profile filtering.
- Warmer palette reads as deliberate craft, not generic startup.
- Standing `--font-mono` / `--font-serif` bug gets fixed in the same pass.

### Negative
- Some duplication of farm rows across sections (Miller's appears in 3
  sections). Acceptable given the small dataset.
- Users coming from v0.2 will notice the redesign — minor cognitive cost,
  worth it.

### Revisit
- When the directory exceeds 20 farms, re-introduce search and
  verification-level filter at the top.
- When diet profile coverage varies meaningfully across farms (e.g. some are
  carnivore-friendly only), re-introduce the diet pills.
- The map page (paused on `feat/map-page` branch) eventually returns and
  needs a styling pass to match this aesthetic, plus a probable rebuild
  inspired by getrawmilk.com's interaction model.
