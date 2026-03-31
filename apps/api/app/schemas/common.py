from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EidosModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, use_enum_values=False)


class CurrencyValidatedModel(EidosModel):
    currency: str = Field(min_length=3, max_length=3)

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str) -> str:
        return value.upper()


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def non_negative_decimal(value: Decimal) -> Decimal:
    if value < 0:
        raise ValueError("value must be non-negative")
    return value


def positive_decimal(value: Decimal) -> Decimal:
    if value <= 0:
        raise ValueError("value must be positive")
    return value


class SnapshotRequest(EidosModel):
    snapshot_date: date
