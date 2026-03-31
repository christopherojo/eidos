import type {
  ConcentrationSummary,
  PortfolioSnapshot,
} from "@eidos/shared-types";

export function summarizeConcentration(
  snapshot: PortfolioSnapshot
): ConcentrationSummary {
  const totalMarketValue = snapshot.positions.reduce(
    (sum, position) => sum + position.marketValue,
    0
  );

  if (totalMarketValue <= 0) {
    return {
      totalMarketValue: 0,
      largestHoldingWeight: 0,
      holdingCount: snapshot.positions.length,
    };
  }

  const largestHoldingWeight = Math.max(
    ...snapshot.positions.map(
      (position) => position.marketValue / totalMarketValue
    )
  );

  return {
    totalMarketValue,
    largestHoldingWeight,
    holdingCount: snapshot.positions.length,
  };
}
