from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal

from pydantic import Field, field_validator

from app.schemas.common import CurrencyValidatedModel, EidosModel, non_negative_decimal


class HoldingUpsert(CurrencyValidatedModel):
    portfolio_id: str
    security_id: str
    quantity: Decimal
    net_invested_amount: Decimal
    average_cost: Decimal
    last_transaction_at: datetime | None = None
    computed_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    @field_validator("quantity", "net_invested_amount", "average_cost")
    @classmethod
    def validate_non_negative_fields(cls, value: Decimal) -> Decimal:
        return non_negative_decimal(value)


class PortfolioSnapshotUpsert(EidosModel):
    portfolio_id: str
    snapshot_date: date
    holdings_count: int
    total_quantity: Decimal
    total_net_invested_amount: Decimal
    total_market_value: Decimal | None = None
    computed_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
