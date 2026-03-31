from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Alert, Holding, Note, PortfolioSnapshot, Transaction
from app.domain.enums import AlertSeverity, AlertStatus, AssetType, TransactionType
from app.repositories.source import (
    AlertRepository,
    NoteRepository,
    PortfolioRepository,
    SecurityRepository,
    TransactionRepository,
)
from app.schemas.source import (
    AlertCreate,
    NoteCreate,
    PortfolioCreate,
    SecurityCreate,
    TransactionCreate,
)
from app.services.recompute import rebuild_holdings, snapshot_portfolio


def test_repositories_and_computed_entities_cover_crud_basics(session: Session) -> None:
    portfolio_repo = PortfolioRepository(session)
    security_repo = SecurityRepository(session)
    transaction_repo = TransactionRepository(session)
    note_repo = NoteRepository(session)
    alert_repo = AlertRepository(session)

    portfolio = portfolio_repo.create(
        PortfolioCreate(name="Long Term", base_currency="usd", description="Retirement sleeve")
    )
    security = security_repo.create(
        SecurityCreate(
            symbol="AAPL",
            name="Apple Inc.",
            asset_type=AssetType.EQUITY,
            currency="usd",
            exchange="NASDAQ",
            isin="US0378331005",
        )
    )

    first_buy = transaction_repo.create(
        TransactionCreate(
            portfolio_id=portfolio.id,
            security_id=security.id,
            transaction_type=TransactionType.BUY,
            quantity=Decimal("10"),
            price=Decimal("150"),
            gross_amount=Decimal("1500"),
            fees=Decimal("1"),
            currency="usd",
            occurred_at=datetime(2026, 3, 10, 12, 0, tzinfo=UTC),
            external_ref="txn-001",
        )
    )
    transaction_repo.create(
        TransactionCreate(
            portfolio_id=portfolio.id,
            security_id=security.id,
            transaction_type=TransactionType.SELL,
            quantity=Decimal("2"),
            price=Decimal("170"),
            gross_amount=Decimal("340"),
            fees=Decimal("1"),
            currency="usd",
            occurred_at=datetime(2026, 3, 12, 12, 0, tzinfo=UTC),
            external_ref="txn-002",
        )
    )

    note = note_repo.create(
        NoteCreate(
            portfolio_id=portfolio.id,
            security_id=security.id,
            title="Conviction",
            body="Keep position sized below concentration limits.",
        )
    )
    alert = alert_repo.create(
        AlertCreate(
            portfolio_id=portfolio.id,
            security_id=security.id,
            severity=AlertSeverity.WARNING,
            status=AlertStatus.OPEN,
            rule_type="drawdown",
            message="Price fell 10% from recent high.",
            triggered_at=datetime(2026, 3, 13, 12, 0, tzinfo=UTC),
        )
    )

    holdings = rebuild_holdings(
        session,
        portfolio.id,
        computed_at=datetime(2026, 3, 14, 12, 0, tzinfo=UTC),
    )
    snapshot = snapshot_portfolio(
        session,
        portfolio.id,
        snapshot_date=date(2026, 3, 14),
        computed_at=datetime(2026, 3, 14, 12, 0, tzinfo=UTC),
    )
    session.commit()

    assert portfolio_repo.get(portfolio.id) is not None
    assert security_repo.get(security.id) is not None
    assert first_buy.id is not None
    assert note.id is not None
    assert alert.id is not None
    assert len(holdings) == 1
    assert holdings[0].quantity == Decimal("8.000000")
    assert holdings[0].net_invested_amount == Decimal("1162.000000")
    assert holdings[0].average_cost == Decimal("145.250000")
    assert snapshot.holdings_count == 1
    assert snapshot.total_quantity == Decimal("8.000000")
    assert snapshot.total_net_invested_amount == Decimal("1162.000000")

    refreshed_snapshot = snapshot_portfolio(
        session,
        portfolio.id,
        snapshot_date=date(2026, 3, 14),
        computed_at=datetime(2026, 3, 15, 12, 0, tzinfo=UTC),
    )
    session.commit()

    assert refreshed_snapshot.id == snapshot.id
    assert refreshed_snapshot.computed_at == datetime(2026, 3, 15, 12, 0, tzinfo=UTC)

    session.delete(portfolio)
    session.commit()

    assert session.scalar(select(Transaction)) is None
    assert session.scalar(select(Note)) is None
    assert session.scalar(select(Alert)) is None
    assert session.scalar(select(Holding)) is None
    assert session.scalar(select(PortfolioSnapshot)) is None


def test_integrity_constraints_block_duplicate_security_symbols(session: Session) -> None:
    security_repo = SecurityRepository(session)
    security_repo.create(
        SecurityCreate(
            symbol="BND",
            name="Vanguard Total Bond Market ETF",
            asset_type=AssetType.ETF,
            currency="USD",
            exchange="NASDAQ",
            isin="US9219378356",
        )
    )
    session.commit()

    with pytest.raises(IntegrityError):
        security_repo.create(
            SecurityCreate(
                symbol="BND",
                name="Duplicate Symbol",
                asset_type=AssetType.ETF,
                currency="USD",
                exchange="NASDAQ",
                isin="US0000000001",
            )
        )

    session.rollback()
