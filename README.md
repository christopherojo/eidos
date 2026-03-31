# Eidos

A desktop-first portfolio intelligence platform with a lightweight web companion.

## Prerequisites

- Node.js 22+
- npm 10+
- Python 3.14+

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
