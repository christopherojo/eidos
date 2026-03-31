import { summarizeConcentration } from "@eidos/analytics";
import type { PortfolioSnapshot } from "@eidos/shared-types";
import { Panel } from "@eidos/shared-ui";

const demoSnapshot: PortfolioSnapshot = {
  asOf: "2026-03-28T00:00:00Z",
  baseCurrency: "USD",
  positions: [
    { symbol: "MSFT", quantity: 8, marketValue: 3400, assetClass: "equity" },
    {
      symbol: "VGIT",
      quantity: 12,
      marketValue: 2600,
      assetClass: "fixed_income",
    },
  ],
};

const summary = summarizeConcentration(demoSnapshot);

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
            title="Sample analytics contract"
            description={`Largest holding weight: ${(summary.largestHoldingWeight * 100).toFixed(1)}%`}
          >
            <dl className="space-y-3 text-sm text-slate-700">
              <div className="flex items-center justify-between gap-4">
                <dt>Total market value</dt>
                <dd className="font-medium">
                  ${summary.totalMarketValue.toLocaleString()}
                </dd>
              </div>
              <div className="flex items-center justify-between gap-4">
                <dt>Holdings</dt>
                <dd className="font-medium">{summary.holdingCount}</dd>
              </div>
              <div className="flex items-center justify-between gap-4">
                <dt>As of</dt>
                <dd className="font-medium">
                  {demoSnapshot.asOf.slice(0, 10)}
                </dd>
              </div>
            </dl>
          </Panel>
        </div>
      </div>
    </main>
  );
}
