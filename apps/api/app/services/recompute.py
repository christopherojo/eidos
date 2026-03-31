from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.clock import utc_now
from app.db.models import Holding, PortfolioSnapshot
from app.domain.enums import TransactionType
from app.repositories.computed import HoldingRepository, PortfolioSnapshotRepository
from app.repositories.source import TransactionRepository


@dataclass(slots=True)
class HoldingAggregate:
    security_id: str
    currency: str
    quantity: Decimal = Decimal("0")
    net_invested_amount: Decimal = Decimal("0")
    last_transaction_at: datetime | None = None


def rebuild_holdings(
    session: Session,
    portfolio_id: str,
    computed_at: datetime | None = None,
) -> list[Holding]:
    transactions = TransactionRepository(session).list_for_portfolio(portfolio_id)
    aggregates: dict[str, HoldingAggregate] = {}

    for transaction in transactions:
        aggregate = aggregates.setdefault(
            transaction.security_id,
            HoldingAggregate(security_id=transaction.security_id, currency=transaction.currency),
        )

        if transaction.transaction_type == TransactionType.BUY:
            aggregate.quantity += transaction.quantity
            aggregate.net_invested_amount += transaction.gross_amount + transaction.fees
        elif transaction.transaction_type == TransactionType.SELL:
            aggregate.quantity -= transaction.quantity
            aggregate.net_invested_amount -= transaction.gross_amount - transaction.fees
        elif transaction.transaction_type == TransactionType.DIVIDEND:
            aggregate.net_invested_amount -= transaction.gross_amount
        elif transaction.transaction_type == TransactionType.FEE:
            aggregate.net_invested_amount += transaction.fees or transaction.gross_amount

        aggregate.last_transaction_at = transaction.occurred_at

    timestamp = computed_at or utc_now()
    holdings = [
        Holding(
            portfolio_id=portfolio_id,
            security_id=aggregate.security_id,
            quantity=max(aggregate.quantity, Decimal("0")),
            net_invested_amount=max(aggregate.net_invested_amount, Decimal("0")),
            average_cost=(
                aggregate.net_invested_amount / aggregate.quantity
                if aggregate.quantity > 0
                else Decimal("0")
            ),
            currency=aggregate.currency,
            last_transaction_at=aggregate.last_transaction_at,
            computed_at=timestamp,
        )
        for aggregate in aggregates.values()
        if aggregate.quantity > 0
    ]

    return HoldingRepository(session).replace_for_portfolio(portfolio_id, holdings)


def snapshot_portfolio(
    session: Session,
    portfolio_id: str,
    snapshot_date: date,
    computed_at: datetime | None = None,
) -> PortfolioSnapshot:
    holdings = HoldingRepository(session).list_for_portfolio(portfolio_id)
    timestamp = computed_at or datetime.now(tz=UTC)
    snapshot = PortfolioSnapshot(
        portfolio_id=portfolio_id,
        snapshot_date=snapshot_date,
        holdings_count=len(holdings),
        total_quantity=sum((holding.quantity for holding in holdings), start=Decimal("0")),
        total_net_invested_amount=sum(
            (holding.net_invested_amount for holding in holdings), start=Decimal("0")
        ),
        total_market_value=None,
        computed_at=timestamp,
    )
    return PortfolioSnapshotRepository(session).upsert(snapshot)
