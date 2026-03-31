from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.models.common import IdentifierMixin, TimestampMixin
from app.db.types import UTCDateTime


class Holding(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = "holdings"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "security_id", name="uq_holdings_portfolio_security"),
    )

    portfolio_id: Mapped[str] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False
    )
    security_id: Mapped[str] = mapped_column(
        ForeignKey("securities.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    net_invested_amount: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    average_cost: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    last_transaction_at: Mapped[datetime | None] = mapped_column(UTCDateTime(), nullable=True)
    computed_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)


class PortfolioSnapshot(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = "portfolio_snapshots"
    __table_args__ = (
        UniqueConstraint(
            "portfolio_id",
            "snapshot_date",
            name="uq_portfolio_snapshots_portfolio_date",
        ),
    )

    portfolio_id: Mapped[str] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False
    )
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    holdings_count: Mapped[int] = mapped_column(Integer, nullable=False)
    total_quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    total_net_invested_amount: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    total_market_value: Mapped[Decimal | None] = mapped_column(Numeric(20, 6), nullable=True)
    computed_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
