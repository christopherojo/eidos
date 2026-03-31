from __future__ import annotations

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.clock import utc_now
from app.core.ids import generate_id
from app.db.types import UTCDateTime


class IdentifierMixin:
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_id)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(UTCDateTime(), nullable=False, default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        UTCDateTime(), nullable=False, default=utc_now, onupdate=utc_now
    )
