from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import delete

from app.db.migrate import upgrade
from app.db.models import Alert, Holding, Note, Portfolio, PortfolioSnapshot, Security, Transaction
from app.db.session import create_session_factory
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


def seed() -> None:
    upgrade("head")
    session_factory = create_session_factory()

    with session_factory.begin() as session:
        for model in (
            PortfolioSnapshot,
            Holding,
            Alert,
            Note,
            Transaction,
            Security,
            Portfolio,
        ):
            session.execute(delete(model))

        portfolio = PortfolioRepository(session).create(
            PortfolioCreate(
                name="Eidos Demo",
                base_currency="USD",
                description="Seeded development portfolio",
            )
        )
        security_repo = SecurityRepository(session)
        msft = security_repo.create(
            SecurityCreate(
                symbol="MSFT",
                name="Microsoft Corp.",
                asset_type=AssetType.EQUITY,
                currency="USD",
                exchange="NASDAQ",
                isin="US5949181045",
            )
        )
        bnd = security_repo.create(
            SecurityCreate(
                symbol="BND",
                name="Vanguard Total Bond Market ETF",
                asset_type=AssetType.ETF,
                currency="USD",
                exchange="NASDAQ",
                isin="US9219378356",
            )
        )

        tx_repo = TransactionRepository(session)
        tx_repo.create(
            TransactionCreate(
                portfolio_id=portfolio.id,
                security_id=msft.id,
                transaction_type=TransactionType.BUY,
                quantity=Decimal("10"),
                price=Decimal("410"),
                gross_amount=Decimal("4100"),
                fees=Decimal("5"),
                currency="USD",
                occurred_at=datetime(2026, 3, 1, 14, 30, tzinfo=UTC),
                external_ref="seed-msft-buy",
            )
        )
        tx_repo.create(
            TransactionCreate(
                portfolio_id=portfolio.id,
                security_id=bnd.id,
                transaction_type=TransactionType.BUY,
                quantity=Decimal("20"),
                price=Decimal("72"),
                gross_amount=Decimal("1440"),
                fees=Decimal("2"),
                currency="USD",
                occurred_at=datetime(2026, 3, 2, 14, 30, tzinfo=UTC),
                external_ref="seed-bnd-buy",
            )
        )

        NoteRepository(session).create(
            NoteCreate(
                portfolio_id=portfolio.id,
                security_id=msft.id,
                title="Watch concentration",
                body="Seed note for local development and explainability flows.",
            )
        )
        AlertRepository(session).create(
            AlertCreate(
                portfolio_id=portfolio.id,
                security_id=msft.id,
                severity=AlertSeverity.WARNING,
                status=AlertStatus.OPEN,
                rule_type="concentration",
                message="Microsoft exceeds the starter concentration threshold.",
                triggered_at=datetime(2026, 3, 3, 14, 30, tzinfo=UTC),
            )
        )

        rebuild_holdings(
            session,
            portfolio.id,
            computed_at=datetime(2026, 3, 4, 14, 30, tzinfo=UTC),
        )
        snapshot_portfolio(
            session,
            portfolio.id,
            snapshot_date=date(2026, 3, 4),
            computed_at=datetime(2026, 3, 4, 14, 30, tzinfo=UTC),
        )


if __name__ == "__main__":
    seed()
