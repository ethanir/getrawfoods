# ADR 0003: Diet profile system

## Status

Accepted, 2026-04-26

## Context

The directory was originally framed around Aajonus Vonderplanitz's primal-diet
tradition, with farms tagged for whether they appeared in his published
sourcing materials. In practice, the audience for raw animal-food sourcing
spans several overlapping dietary traditions:

- **Raw carnivore** — meat-and-organ-focused, often with raw dairy. Smaller
  but fast-growing community.
- **Aajonus primal** — the original 60% raw dairy, 25-30% raw meat, 5% fruit
  framework. Specific food rules (no salt cheese, no honey with meat, etc.)
- **Weston A. Price / ancestral** — broader: raw dairy, fermented foods,
  organs, bone broths, traditional fats. Largest audience.

Locking the directory's identity to one tradition was both narrowing the
audience and misrepresenting the maintainer's actual diet (raw carnivore,
not Aajonus primal).

## Decision

Add two fields to each farm:

- `diet_profiles: string[]` — which traditions the farm meaningfully serves
- `best_for: string` — short tagline shown inline ("raw bison + organs")

Top-of-page filter: four pills (`All diets` / `Raw carnivore` /
`Aajonus primal` / `Weston A. Price`). Selecting a profile filters the
list to farms tagged with that profile and adjusts the result count.

## Consequences

- The directory becomes honest about being multi-tradition. The maintainer
  can speak to all three profiles without claiming expertise in any.
- Trimmed seed from 21 farms to 6, removing items the maintainer has no
  personal experience with (olive oil, honey, coconut). New farms come in
  via community submissions.
- Aajonus's work remains a key citation source. The verification level
  `aajonus_verified` still means "appears in his published lists" — that's
  a meaningful signal regardless of which profile a user follows.

## Alternatives considered

**Single-profile site.** Pick one (raw carnivore) and run with it. Rejected:
narrows audience, misrepresents the breadth of the source data we have.

**Many profiles.** Aajonus alone has 12+ documented variations (Sport
Formula, Down Diet, Lubrication Formula, etc.). Rejected: the directory
isn't a diet plan, it's a sourcing tool. Profiles are about which farms
fit your eating, not which protocol you're running.
