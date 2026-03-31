from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.domain.enums import AssetType, TransactionType
from app.schemas.source import PortfolioCreate, SecurityCreate, TransactionCreate


def test_portfolio_validation_normalizes_base_currency() -> None:
    portfolio = PortfolioCreate(name="Core", base_currency="usd", description=None)

    assert portfolio.base_currency == "USD"


def test_security_validation_normalizes_symbol() -> None:
    security = SecurityCreate(
        symbol="msft",
        name="Microsoft Corp.",
        asset_type=AssetType.EQUITY,
        currency="usd",
        exchange="NASDAQ",
        isin="US5949181045",
    )

    assert security.symbol == "MSFT"
    assert security.currency == "USD"


def test_transaction_validation_rejects_non_positive_quantity() -> None:
    with pytest.raises(ValidationError):
        TransactionCreate(
            portfolio_id="portfolio-1",
            security_id="security-1",
            transaction_type=TransactionType.BUY,
            quantity=Decimal("0"),
            price=Decimal("10"),
            gross_amount=Decimal("100"),
            fees=Decimal("0"),
            currency="usd",
            occurred_at=datetime(2026, 3, 31, 12, 0, tzinfo=UTC),
        )
