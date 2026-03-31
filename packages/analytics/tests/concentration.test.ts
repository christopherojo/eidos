import { describe, expect, it } from "vitest";

import type { PortfolioSnapshot } from "@eidos/shared-types";
import { summarizeConcentration } from "../src/concentration";

describe("summarizeConcentration", () => {
  it("calculates total market value and largest holding weight", () => {
    const snapshot: PortfolioSnapshot = {
      asOf: "2026-03-28T00:00:00Z",
      baseCurrency: "USD",
      positions: [
        {
          symbol: "AAPL",
          quantity: 10,
          marketValue: 5000,
          assetClass: "equity",
        },
        {
          symbol: "BND",
          quantity: 20,
          marketValue: 3000,
          assetClass: "fixed_income",
        },
      ],
    };

    expect(summarizeConcentration(snapshot)).toEqual({
      totalMarketValue: 8000,
      largestHoldingWeight: 0.625,
      holdingCount: 2,
    });
  });

  it("handles empty portfolios without division errors", () => {
    const snapshot: PortfolioSnapshot = {
      asOf: "2026-03-28T00:00:00Z",
      baseCurrency: "USD",
      positions: [],
    };

    expect(summarizeConcentration(snapshot)).toEqual({
      totalMarketValue: 0,
      largestHoldingWeight: 0,
      holdingCount: 0,
    });
  });
});
