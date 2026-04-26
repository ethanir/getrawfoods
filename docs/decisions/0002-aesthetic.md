# ADR 0002: Visual Design Direction

**Status**: Accepted
**Date**: 2026-04-26

## Context

The product is a knowledge base / directory for a serious-minded niche audience (people researching their food sources carefully, typically already past the "shiny new thing" phase). They use Hacker News, Reddit's old design, Wikipedia, the Weston A. Price directory, eatwild.com, realmilk.com — sites that prioritize *information density* over *visual polish*.

Building a typical 2026 SaaS-startup UI here (rounded cards, soft shadows, gradients, animated hero sections, generous padding, marketing-y copy) would *signal wrong* to this audience. They'd read it as "another health-tech grift."

## Decision

We commit to a **utilitarian / reference-document** aesthetic. Specifically:

- **Typography**: IBM Plex family across the board — Plex Sans for UI/headings, Plex Serif for prose, Plex Mono for codes/prices/tags. One coherent typographic system.
- **Color**: Off-white background (`#FAF8F5`), near-black text (`#1A1A1A`), single accent color of deep oxblood (`#6B1F1F`). Used for links, key actions, verification badges. No gradients. No secondary brand colors.
- **Layout**: Dense lists and tables, not "cards." Sharp corners (no border-radius). Hairline borders (`1px solid`), no shadows. Wide content + narrow margins on desktop.
- **Motion**: None. No fade-ins, no hover animations beyond color/underline changes, no scroll-triggered effects.
- **Imagery**: Minimal. Farm photos when uploaded. No stock imagery, no decorative illustrations, no hero images.
- **Density**: A single-screen homepage shows 15–20 farm rows. A farm detail page fits on one screen for most farms.

Reference points: Hacker News, old Reddit, Craigslist, Wikipedia, drudgereport.com, news.ycombinator.com, the eatwild.com directory.

## Why this and not "modern startup UI"

- **Trust signaling.** This audience equates polish with marketing, marketing with deception. Utilitarian = honest.
- **Speed.** No animations, no images = fast page loads. Real benefit on mobile.
- **Maintainability.** No animation libraries, no design system to maintain, no Figma round-trips. Just CSS.
- **Differentiation.** Every other site in this space is either ancient (aajonus.net, weston a price) or generic-startup. We can stand apart by being *deliberately* old-internet.
- **Aging.** This look will age better than 2026 design trends. Hacker News looks the same now as 2010.

## Implementation notes

The full design tokens live in [`frontend/src/index.css`](../../frontend/src/index.css). Tailwind config consumes those tokens so utility classes match the system.

Dark mode is **not** in scope for v1. Many users on this diet are skeptical of screen blue light; light mode is the better default.

## Consequences

### Positive
- Faster development (less CSS to write, no animation choreography).
- Faster page loads (no animations, minimal images).
- Honest signaling to target audience.
- Cheap to maintain.

### Negative
- Will look "boring" on first glance to anyone outside the target audience (e.g., someone judging this on Dribbble).
- Won't go viral on design Twitter.
- Some users may interpret the lack of polish as the project being abandoned. Mitigation: clear "Last updated" timestamps everywhere.

## Revisit

When we have real users, do qualitative interviews. If they say the UI feels stale or untrustworthy (rather than serious or focused), revisit. Don't pre-emptively soften based on outside design opinion.
