from __future__ import annotations

import os
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "eidos.sqlite3"


def get_database_url() -> str:
    if "EIDOS_DATABASE_URL" not in os.environ:
        DEFAULT_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return os.getenv("EIDOS_DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")
