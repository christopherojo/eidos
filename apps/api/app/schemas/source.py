from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import Field, field_validator

from app.domain.enums import AlertSeverity, AlertStatus, AssetType, TransactionType
from app.schemas.common import (
    CurrencyValidatedModel,
    EidosModel,
    ensure_utc,
    non_negative_decimal,
    positive_decimal,
)


class PortfolioCreate(EidosModel):
    name: str = Field(min_length=1, max_length=200)
    base_currency: str = Field(min_length=3, max_length=3)
    description: str | None = None

    @field_validator("base_currency")
    @classmethod
    def normalize_base_currency(cls, value: str) -> str:
        return value.upper()


class SecurityCreate(CurrencyValidatedModel):
    symbol: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=200)
    asset_type: AssetType
    exchange: str | None = Field(default=None, max_length=64)
    isin: str | None = Field(default=None, min_length=12, max_length=12)

    @field_validator("symbol")
    @classmethod
    def normalize_symbol(cls, value: str) -> str:
        return value.upper()


class TransactionCreate(CurrencyValidatedModel):
    portfolio_id: str
    security_id: str
    transaction_type: TransactionType
    quantity: Decimal
    price: Decimal
    gross_amount: Decimal
    fees: Decimal = Decimal("0")
    occurred_at: datetime
    settled_at: datetime | None = None
    external_ref: str | None = Field(default=None, max_length=100)

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: Decimal) -> Decimal:
        return positive_decimal(value)

    @field_validator("price", "gross_amount", "fees")
    @classmethod
    def validate_non_negative_fields(cls, value: Decimal) -> Decimal:
        return non_negative_decimal(value)

    @field_validator("occurred_at", "settled_at")
    @classmethod
    def normalize_timestamps(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return ensure_utc(value)


class NoteCreate(EidosModel):
    portfolio_id: str
    security_id: str | None = None
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)


class AlertCreate(EidosModel):
    portfolio_id: str
    security_id: str | None = None
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.OPEN
    rule_type: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1)
    triggered_at: datetime
    resolved_at: datetime | None = None

    @field_validator("triggered_at", "resolved_at")
    @classmethod
    def normalize_timestamps(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return ensure_utc(value)
