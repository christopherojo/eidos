# Architecture

Eidos is organized as a modular monolith with a desktop-first Tauri and React shell, a FastAPI backend, SQLite local-first persistence, and shared packages for types, UI, and analytics.

## Phase 1A Coverage

- Architecture summary: covered in [docs/architecture.md](./docs/architecture.md#phase-1a-summary).
- Folder structure: covered in [docs/architecture.md](./docs/architecture.md#folder-structure).
- Data flow diagram: covered in [docs/architecture.md](./docs/architecture.md#tauri-to-backend-communication).
- Run instructions: covered in [docs/architecture.md](./docs/architecture.md#runnable-plan).
- Key decisions: covered in [docs/architecture.md](./docs/architecture.md#key-decisions).

## Phase 1B Coverage

- Project foundation: covered in [docs/architecture.md](./docs/architecture.md#phase-1b-foundation).
- Local commands and expected outputs: covered in [README.md](./README.md#phase-1b-foundation-checklist).
- Verification commands: covered in [testing-strategy.md](./testing-strategy.md).

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
