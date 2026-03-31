export type AssetClass =
  | "equity"
  | "fixed_income"
  | "cash"
  | "commodity"
  | "alternative";

export interface Position {
  readonly symbol: string;
  readonly quantity: number;
  readonly marketValue: number;
  readonly assetClass: AssetClass;
}

export interface PortfolioSnapshot {
  readonly asOf: string;
  readonly baseCurrency: string;
  readonly positions: readonly Position[];
}

export interface ConcentrationSummary {
  readonly totalMarketValue: number;
  readonly largestHoldingWeight: number;
  readonly holdingCount: number;
}
