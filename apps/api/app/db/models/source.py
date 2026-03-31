from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.common import IdentifierMixin, TimestampMixin
from app.db.types import UTCDateTime
from app.domain.enums import AlertSeverity, AlertStatus, AssetType, TransactionType


class Portfolio(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = "portfolios"

    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    base_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="portfolio", passive_deletes=True
    )
    notes: Mapped[list["Note"]] = relationship(back_populates="portfolio", passive_deletes=True)
    alerts: Mapped[list["Alert"]] = relationship(back_populates="portfolio", passive_deletes=True)


class Security(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = "securities"

    symbol: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    asset_type: Mapped[AssetType] = mapped_column(
        Enum(AssetType, native_enum=False, length=32), nullable=False
    )
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    exchange: Mapped[str | None] = mapped_column(String(64), nullable=True)
    isin: Mapped[str | None] = mapped_column(String(12), nullable=True, unique=True)

    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="security", passive_deletes=True
    )


class Transaction(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = "transactions"

    portfolio_id: Mapped[str] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False
    )
    security_id: Mapped[str] = mapped_column(
        ForeignKey("securities.id", ondelete="RESTRICT"), nullable=False
    )
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType, native_enum=False, length=32), nullable=False
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    gross_amount: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    fees: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False, default=Decimal("0"))
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    settled_at: Mapped[datetime | None] = mapped_column(UTCDateTime(), nullable=True)
    external_ref: Mapped[str | None] = mapped_column(String(100), nullable=True)

    portfolio: Mapped[Portfolio] = relationship(back_populates="transactions")
    security: Mapped[Security] = relationship(back_populates="transactions")


class Note(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = "notes"

    portfolio_id: Mapped[str] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False
    )
    security_id: Mapped[str | None] = mapped_column(
        ForeignKey("securities.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    portfolio: Mapped[Portfolio] = relationship(back_populates="notes")


class Alert(IdentifierMixin, TimestampMixin, Base):
    __tablename__ = "alerts"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "rule_type", "triggered_at", name="uq_alerts_rule_window"),
    )

    portfolio_id: Mapped[str] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False
    )
    security_id: Mapped[str | None] = mapped_column(
        ForeignKey("securities.id", ondelete="SET NULL"), nullable=True
    )
    severity: Mapped[AlertSeverity] = mapped_column(
        Enum(AlertSeverity, native_enum=False, length=16), nullable=False
    )
    status: Mapped[AlertStatus] = mapped_column(
        Enum(AlertStatus, native_enum=False, length=16), nullable=False
    )
    rule_type: Mapped[str] = mapped_column(String(64), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    triggered_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False)
    resolved_at: Mapped[datetime | None] = mapped_column(UTCDateTime(), nullable=True)

    portfolio: Mapped[Portfolio] = relationship(back_populates="alerts")
