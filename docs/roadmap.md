# Roadmap

## Phase 0: Foundation

- Establish monorepo structure.
- Standardize linting, formatting, testing, and CI.
- Create shared packages for types, UI, and analytics.

## Phase 1: Local Portfolio Model

- Introduce SQLite-backed portfolio entities and migrations.
- Add ingestion for holdings, accounts, and transactions.
- Define reproducible analytics inputs and outputs.

## Phase 2: Insight Workbench

- Build desktop workflows for overview, risk, and exposure summaries.
- Add explainable drilldowns from conclusions to underlying calculations.
- Expand shared UI primitives for data-dense portfolio screens.

## Phase 3: Companion Surfaces

- Reuse shared logic for a lightweight web companion.
- Add sync-ready contracts without making cloud a hard dependency.
- Separate source-of-truth data from derived aggregates and caches.
