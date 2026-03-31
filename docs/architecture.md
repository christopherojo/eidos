# Architecture

Eidos uses a minimal monorepo with one JavaScript workspace and one Python application:

- `apps/desktop`: desktop-first React UI prepared for a Tauri shell.
- `apps/api`: FastAPI service for orchestration and local domain endpoints.
- `packages/shared-types`: shared TypeScript interfaces for app and analytics boundaries.
- `packages/shared-ui`: shared React primitives for desktop and future web surfaces.
- `packages/analytics`: reusable portfolio analysis helpers kept separate from UI concerns.

## Why This Structure

- Keeps domain and presentation logic decoupled from the desktop shell.
- Makes analytics reusable across desktop and a future web companion.
- Avoids introducing task runners or remote caching before the repo needs them.
- Uses conventional tooling: npm workspaces, Vite, Vitest, ESLint, Prettier, FastAPI, Ruff, mypy, and pytest.

## Execution Model

- Desktop is the primary UX surface and owns user workflows.
- FastAPI owns orchestration boundaries and data-serving contracts.
- Shared TypeScript packages keep desktop and future web work aligned.
- SQLite is the local-first persistence choice for MVP.

## Data Modeling

- Source-of-truth entities live separately from computed entities.
- Source-of-truth tables capture user-entered or imported records such as portfolios, securities, transactions, notes, and alert instances.
- Computed tables store reproducible derivatives such as holdings and portfolio snapshots.
- UUID identifiers and UTC timestamps are used across both categories to ease later PostgreSQL migration.

## Running The Stack

- Install Node dependencies with `npm install`.
- Install API dependencies with `py -3.14 -m pip install -e ./apps/api[dev]`.
- Run `npm run migrate` to create or update the local SQLite schema.
- Run `npm run seed` to load sample development data into `apps/api/data/eidos.sqlite3`.
- Run `npm run dev:desktop` for the UI and `npm run dev:api` for the backend.

## Persistence Layout

- Alembic migrations live in `apps/api/alembic`.
- SQLAlchemy models live in `apps/api/app/db/models`.
- Repositories live in `apps/api/app/repositories`.
- Recompute services for derived tables live in `apps/api/app/services`.

## Extension Points

- Add Tauri commands in `apps/desktop/src-tauri` when the Rust toolchain is available.
- Add database modules under `apps/api/app` once local persistence begins.
- Grow `packages/analytics` around deterministic, testable calculations.
- Keep shared UI intentionally small and portable.
