# Architecture

Eidos is organized as a small monorepo with a desktop-first React shell, a FastAPI backend, and shared packages for types, UI, and analytics.

## Runbook

- Install JavaScript dependencies:
  `npm install`
- Install Python dependencies:
  `py -3.14 -m pip install -e ./apps/api[dev]`
- Apply the database schema:
  `npm run migrate`
- Seed local data:
  `npm run seed`
- Start the desktop app:
  `npm run dev:desktop`
- Start the API:
  `npm run dev:api`

See [docs/architecture.md](./docs/architecture.md) for the full architecture overview.
