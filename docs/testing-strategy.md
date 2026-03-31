# Testing Strategy

Eidos favors fast, deterministic tests at the module boundary where logic lives.

## Test Layers

- `packages/analytics`: unit tests for pure calculations and portfolio transforms.
- `packages/shared-ui`: render-level tests for reusable React primitives.
- `apps/desktop`: smoke tests for shell composition and integration with shared packages.
- `apps/api`: API contract tests against FastAPI endpoints using `TestClient`.

## Principles

- Prefer pure functions for calculations and adapter layers for IO.
- Keep source-of-truth models explicit and independently testable.
- Verify behavior close to the boundary that could regress.
- Add integration tests only when unit tests stop providing enough confidence.

## CI Gates

- TypeScript lint, typecheck, tests, and build run in Node CI.
- Python lint, typecheck, tests, and compile checks run in Python CI.
- New non-trivial changes should extend tests in the package they affect.

## Local Verification

- `npm run format:check`
- `npm run lint`
- `npm run typecheck`
- `npm run test`
- `npm run migrate`
- `npm run seed`

The API tests verify schema migration, seed behavior, validation rules, CRUD basics, and integrity constraints against SQLite.
