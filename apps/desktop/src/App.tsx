import { Panel } from "@eidos/shared-ui";

import { env } from "./config/env";

export function App() {
  return (
    <main className="min-h-screen bg-slate-100 px-6 py-10 text-slate-950">
      <div className="mx-auto flex max-w-5xl flex-col gap-6">
        <header className="space-y-3">
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-slate-500">
            Eidos Foundation
          </p>
          <div className="space-y-2">
            <h1 className="text-4xl font-semibold tracking-tight">
              Desktop-first portfolio intelligence, scaffolded for shared logic.
            </h1>
            <p className="max-w-3xl text-base text-slate-600">
              This starter shell keeps the product surface intentionally thin
              while shared packages own the reusable types, analytics, and UI
              building blocks.
            </p>
          </div>
        </header>

        <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
          <Panel
            eyebrow="Architecture"
            title="Monorepo foundations are in place"
            description="The desktop shell is wired to shared packages without introducing product workflows yet."
          >
            <ul className="space-y-3 text-sm text-slate-700">
              <li>
                Desktop shell: React, TypeScript, Tailwind, Vite, and Tauri
                scaffolding.
              </li>
              <li>
                Shared logic: analytics and cross-surface types live outside app
                folders.
              </li>
              <li>
                Backend foundation: FastAPI app, test harness, and Python
                quality gates.
              </li>
            </ul>
          </Panel>

          <Panel
            eyebrow="Validation"
            title="Local development targets"
            description="The UI is intentionally minimal while the shell, API, and persistence layers are verified."
          >
            <dl className="space-y-3 text-sm text-slate-700">
              <div className="flex items-center justify-between gap-4">
                <dt>Frontend</dt>
                <dd className="font-medium">Vite dev server</dd>
              </div>
              <div className="flex items-center justify-between gap-4">
                <dt>Backend</dt>
                <dd className="font-medium">{env.apiBaseUrl}</dd>
              </div>
              <div className="flex items-center justify-between gap-4">
                <dt>Storage</dt>
                <dd className="font-medium">SQLite local file</dd>
              </div>
            </dl>
          </Panel>
        </div>
      </div>
    </main>
  );
}
