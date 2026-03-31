# Eidos Agent Instructions

## Product

Eidos is a desktop-first portfolio intelligence platform with a lightweight web companion.
Prioritize insight-first UX, explainability, performance, and modular analytics.

## Architecture rules

- Desktop app is the primary surface.
- Keep business/domain logic reusable across desktop and web.
- Prefer shared packages over duplicate logic.
- FastAPI owns backend/domain orchestration.
- SQLite is the local-first source of truth in MVP.
- PostgreSQL/cloud sync are future concerns; do not prematurely optimize for them.

## Engineering rules

- Never make broad refactors unless explicitly asked.
- Preserve backwards compatibility when reasonable.
- Keep modules small and composable.
- Prefer typed interfaces and explicit schemas.
- Add or update tests for every non-trivial change.
- Run lint, typecheck, and tests before finishing.

## UX rules

- Desktop-first, keyboard-friendly, data-dense UI.
- Show conclusions before charts.
- Keep drilldowns clear and explainable.
- Avoid clutter and novelty UI.

## Data rules

- Distinguish source-of-truth data from computed data.
- Store timestamps and provenance for market/news/macro data.
- Make calculations reproducible and testable.

## Done criteria

A task is only complete when:

1. Code is implemented
2. Tests are added/updated
3. Lint/typecheck/build pass
4. Migration or schema changes are documented
5. A short changelog summary is produced
