from __future__ import annotations

from datetime import date

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db.models import Holding, PortfolioSnapshot


class HoldingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def replace_for_portfolio(self, portfolio_id: str, holdings: list[Holding]) -> list[Holding]:
        self.session.execute(delete(Holding).where(Holding.portfolio_id == portfolio_id))
        self.session.add_all(holdings)
        self.session.flush()
        return holdings

    def list_for_portfolio(self, portfolio_id: str) -> list[Holding]:
        stmt = (
            select(Holding)
            .where(Holding.portfolio_id == portfolio_id)
            .order_by(Holding.security_id.asc())
        )
        return list(self.session.scalars(stmt))


class PortfolioSnapshotRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert(self, snapshot: PortfolioSnapshot) -> PortfolioSnapshot:
        existing = self.session.scalar(
            select(PortfolioSnapshot).where(
                PortfolioSnapshot.portfolio_id == snapshot.portfolio_id,
                PortfolioSnapshot.snapshot_date == snapshot.snapshot_date,
            )
        )
        if existing is None:
            self.session.add(snapshot)
            self.session.flush()
            return snapshot

        existing.holdings_count = snapshot.holdings_count
        existing.total_quantity = snapshot.total_quantity
        existing.total_net_invested_amount = snapshot.total_net_invested_amount
        existing.total_market_value = snapshot.total_market_value
        existing.computed_at = snapshot.computed_at
        self.session.flush()
        return existing

    def get_for_date(self, portfolio_id: str, snapshot_date: date) -> PortfolioSnapshot | None:
        return self.session.scalar(
            select(PortfolioSnapshot).where(
                PortfolioSnapshot.portfolio_id == portfolio_id,
                PortfolioSnapshot.snapshot_date == snapshot_date,
            )
        )
