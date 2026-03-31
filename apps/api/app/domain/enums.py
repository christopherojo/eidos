from __future__ import annotations

from enum import Enum


class AssetType(str, Enum):
    EQUITY = "equity"
    ETF = "etf"
    BOND = "bond"
    CASH = "cash"
    CRYPTO = "crypto"
    OTHER = "other"


class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    FEE = "fee"


class AlertSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    OPEN = "open"
    DISMISSED = "dismissed"
    RESOLVED = "resolved"
