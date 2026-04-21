# Architecture

Eidos uses a minimal monorepo with one JavaScript workspace and one Python application:

- `apps/desktop`: desktop-first React UI prepared for a Tauri shell.
- `apps/api`: FastAPI service for orchestration and local domain endpoints.
- `packages/shared-types`: shared TypeScript interfaces for app and analytics boundaries.
- `packages/shared-ui`: shared React primitives for desktop and future web surfaces.
- `packages/analytics`: reusable portfolio analysis helpers kept separate from UI concerns.

## Phase 1A Summary

Eidos is a modular monolith optimized for a local-first desktop MVP. The desktop shell is the primary product surface, React owns interaction and presentation, FastAPI owns domain orchestration and persistence, and SQLite is the local source of truth. Shared TypeScript packages keep frontend contracts and reusable UI/analytics logic portable without introducing cloud assumptions.

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

## Folder Structure

```text
eidos/
  apps/
    desktop/
      src/
        App.tsx
        main.tsx
        index.css
        test/
      src-tauri/
        Cargo.toml
        tauri.conf.json
        src/main.rs
      index.html
      package.json
      tailwind.config.ts
      vite.config.ts
    api/
      alembic/
        env.py
        versions/
      app/
        core/
        db/
          models/
          config.py
          migrate.py
          seed.py
          session.py
          types.py
        domain/
        repositories/
        schemas/
        services/
        main.py
      data/
      tests/
      alembic.ini
      pyproject.toml
  packages/
    analytics/
      src/
      tests/
    shared-types/
      src/
    shared-ui/
      src/
  docs/
    architecture.md
    roadmap.md
    testing-strategy.md
  tools/
    run-python.mjs
  package.json
  tsconfig.base.json
  vitest.config.ts
```

Generated folders such as `node_modules`, `dist`, `.mypy_cache`, `.ruff_cache`, `.pytest_cache`, and local SQLite files are not architecture boundaries and should not be used for source code.

## Boundary Rules

- Frontend: `apps/desktop/src` owns UI composition, routing when added, user interactions, and API client calls. It must not import Python code, know database schema details, or perform persistence directly.
- Tauri shell: `apps/desktop/src-tauri` owns native windowing and future desktop-only capabilities. It should stay thin and delegate portfolio/domain behavior to the frontend and backend.
- Backend: `apps/api/app` owns FastAPI entrypoints, domain orchestration, validation schemas, repositories, migrations, seed data, and SQLite access.
- Services: `apps/api/app/services` owns application workflows and computed data updates such as holdings and portfolio snapshots. Services may coordinate repositories but should not render UI.
- Shared types: `packages/shared-types` owns TypeScript contracts that are safe to share across desktop and future web surfaces. It should not depend on app-specific code.
- Shared UI: `packages/shared-ui` owns reusable React primitives only. It should not call the API directly.
- Analytics: `packages/analytics` owns deterministic TypeScript analytics helpers. Backend computed persistence currently lives in Python services; cross-runtime analytics should be promoted deliberately through shared contracts.

## Data Modeling

- Source-of-truth entities live separately from computed entities.
- Source-of-truth tables capture user-entered or imported records such as portfolios, securities, transactions, notes, and alert instances.
- Computed tables store reproducible derivatives such as holdings and portfolio snapshots.
- UUID identifiers and UTC timestamps are used across both categories to ease later PostgreSQL migration.

## Tauri To Backend Communication

During local development, Tauri loads the Vite dev server and the React frontend calls FastAPI over HTTP on a local loopback URL. In production packaging, the same contract should remain: the desktop shell starts or connects to a local FastAPI process, and the frontend calls its HTTP API through a configured base URL.

Initial communication rules:

- Use HTTP/JSON between React and FastAPI for product data.
- Keep Tauri commands for desktop-native capabilities only, such as file pickers, OS integration, or process lifecycle.
- Do not let Tauri commands bypass FastAPI for portfolio persistence.
- Keep API request and response contracts explicit and mirrored in shared TypeScript types when frontend code needs them.

Text data flow:

```text
User
  -> Tauri window
  -> React + TypeScript UI
  -> local HTTP request using EIDOS_API_BASE_URL or default loopback URL
  -> FastAPI route
  -> Pydantic schema validation
  -> service layer
  -> repository layer
  -> SQLite source-of-truth tables
  -> recompute service when needed
  -> SQLite computed tables
  -> FastAPI response
  -> React UI renders conclusion-first views
```

## Environment Strategy

Environment variables are local-first and optional by default.

- `EIDOS_DATABASE_URL`: optional backend database URL. Defaults to `sqlite:///apps/api/data/eidos.sqlite3` through `apps/api/app/db/config.py`.
- `EIDOS_API_BASE_URL`: planned frontend API base URL. Defaults should target the local FastAPI development server, for example `http://127.0.0.1:8000`.
- `PYTHONPATH`: not required for standard scripts because commands run through `python -m` with the installed editable API package.

Rules:

- Do not commit machine-specific `.env` files.
- Do not introduce cloud credentials or remote service assumptions in Phase 1.
- Keep defaults runnable on a fresh local checkout.
- Prefer explicit environment names over framework-specific magic when adding new variables.

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

## Runnable Plan

1. Install dependencies with `npm install` and `py -3.14 -m pip install -e ./apps/api[dev]`.
2. Apply migrations with `npm run migrate`.
3. Seed development data with `npm run seed`.
4. Start FastAPI with `npm run dev:api`.
5. Start the desktop shell with `npm run dev:desktop`.
6. Start the Tauri shell with `npm run dev:tauri` when Rust/Cargo and MSVC Build Tools are installed.
7. Verify the repo with `npm run format:check`, `npm run lint`, `npm run typecheck`, and `npm run test`.

## Phase 1B Foundation

Phase 1B maps the runnable foundation to concrete files:

- Repo structure: root `package.json`, npm workspaces, `apps`, `packages`, `docs`, and `tools`.
- Tauri desktop app: `apps/desktop/src-tauri/Cargo.toml`, `apps/desktop/src-tauri/tauri.conf.json`, and `apps/desktop/src-tauri/src/main.rs`.
- React frontend: `apps/desktop/src/main.tsx`, `apps/desktop/src/App.tsx`, and `apps/desktop/index.html`.
- FastAPI backend: `apps/api/app/main.py`.
- SQLite connection: `apps/api/app/db/config.py`, `apps/api/app/db/session.py`, and Alembic migrations under `apps/api/alembic`.
- Health check endpoint: `GET /health` in `apps/api/app/main.py`.
- Base UI layout: `apps/desktop/src/App.tsx`.
- Environment config: `.env.example`, `apps/api/.env.example`, `apps/desktop/.env.example`, and `apps/desktop/src/config/env.ts`.

Expected outputs:

- Frontend: Vite prints a local URL and renders the Eidos Foundation screen.
- Backend: FastAPI serves `GET /health` with `{"status":"ok"}`.
- Tauri: desktop window opens after Rust/Cargo and Microsoft Visual Studio Build Tools with MSVC/Windows SDK are available.
- Verification: lint, typecheck, and tests pass locally.

## Key Decisions

- Use a modular monolith so Eidos can move quickly without prematurely introducing distributed systems.
- Keep desktop as the primary surface and treat web as a future companion.
- Keep FastAPI as the single persistence and orchestration boundary.
- Use SQLite for MVP local-first storage and Alembic migrations to preserve a future PostgreSQL path.
- Separate source-of-truth records from computed holdings and snapshots.
- Prefer explicit schemas, UUIDs, and UTC timestamps for portability and reproducibility.
- Avoid cloud assumptions, background sync, accounts, or remote auth in Phase 1.

## Extension Points

- Add Tauri commands in `apps/desktop/src-tauri` when the Rust toolchain is available.
- Add FastAPI routers under `apps/api/app` as product workflows appear.
- Grow `packages/analytics` around deterministic, testable calculations.
- Keep shared UI intentionally small and portable.
