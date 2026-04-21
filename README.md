# Eidos

A desktop-first portfolio intelligence platform with a lightweight web companion.

## Prerequisites

- Node.js 22+
- npm 10+
- Python 3.14+
- Rust/Cargo and Microsoft Visual Studio Build Tools with MSVC/Windows SDK for `npm run dev:tauri`

## Quick Start

1. Install workspace dependencies:
   `npm install`
2. Install the API dependencies with Python 3.14:
   `py -3.14 -m pip install -e ./apps/api[dev]`
3. Apply the local SQLite schema:
   `npm run migrate`
4. Seed local development data:
   `npm run seed`

The default SQLite database lives at `apps/api/data/eidos.sqlite3`.

## Repository Layout

- `apps/desktop`: React, TypeScript, Tailwind, and Tauri shell scaffold.
- `apps/api`: FastAPI backend foundation with SQLite persistence, migrations, and seed data.
- `packages/shared-types`: shared TypeScript contracts.
- `packages/shared-ui`: reusable React primitives.
- `packages/analytics`: reusable, testable analytics helpers.

## Run The Program

- Start the desktop UI:
  `npm run dev`
- Start only the desktop app shell:
  `npm run dev:desktop`
- Start the FastAPI backend:
  `npm run dev:api`
- Start the Tauri desktop shell:
  `npm run dev:tauri`

The desktop and API are scaffolded as separate processes right now. Run them in separate terminals when you need both active.

## Database Commands

- Apply migrations:
  `npm run migrate`
- Seed local development data:
  `npm run seed`

Set `EIDOS_DATABASE_URL` if you want to point the API at a different SQLite file.

## Verification Commands

- Run formatting checks:
  `npm run format:check`
- Run lint:
  `npm run lint`
- Run type checks:
  `npm run typecheck`
- Run the full test suite:
  `npm run test`
- Build the TypeScript packages, desktop app, and API bytecode check:
  `npm run build`

## Notes

- Python checks and scripts are configured to prefer Python `3.14` on Windows.
- The API test suite covers validation, migrations, seed behavior, CRUD basics, and integrity constraints.
- The desktop test suite remains a lightweight smoke layer until product workflows are added.

## Docs

- [architecture.md](./architecture.md)
- [roadmap.md](./roadmap.md)
- [testing-strategy.md](./testing-strategy.md)

## Phase 1A Architecture Checklist

The initial architecture design is documented in [docs/architecture.md](./docs/architecture.md) and covers:

- Architecture summary
- Full folder structure
- Frontend, backend, service, shared type, shared UI, and analytics boundaries
- Tauri-to-backend communication model
- Environment variable strategy
- Local development workflow
- Text data flow diagram
- Key decisions and constraints

## Phase 1B Foundation Checklist

Phase 1B is the runnable project foundation:

- Repo structure: `apps/desktop`, `apps/api`, `packages/*`, `docs`, and `tools`
- Tauri shell: `apps/desktop/src-tauri`
- React frontend: `apps/desktop/src`
- FastAPI backend: `apps/api/app`
- SQLite connection: `apps/api/app/db`
- Health check: `GET /health`
- Base UI layout: `apps/desktop/src/App.tsx`
- Environment config: `.env.example`, `apps/api/.env.example`, `apps/desktop/.env.example`, and `apps/desktop/src/config/env.ts`

Expected local outputs:

- `npm run dev:desktop` serves the frontend through Vite.
- `npm run dev:api` starts FastAPI and `GET http://127.0.0.1:8000/health` returns `{"status":"ok"}`.
- `npm run dev:tauri` opens the desktop shell when Rust/Cargo and MSVC Build Tools are installed.
- `npm run test`, `npm run lint`, and `npm run typecheck` should pass before handoff.
