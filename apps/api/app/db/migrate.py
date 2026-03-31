from __future__ import annotations

import sys
from pathlib import Path

from alembic.config import Config

from alembic import command
from app.db.config import get_database_url


def _build_config() -> Config:
    api_root = Path(__file__).resolve().parents[2]
    config = Config(str(api_root / "alembic.ini"))
    config.set_main_option("script_location", str(api_root / "alembic"))
    config.set_main_option("sqlalchemy.url", get_database_url())
    return config


def upgrade(revision: str = "head") -> None:
    command.upgrade(_build_config(), revision)


def downgrade(revision: str) -> None:
    command.downgrade(_build_config(), revision)


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    command_name = args[0] if args else "upgrade"
    revision = args[1] if len(args) > 1 else "head"

    if command_name == "upgrade":
        upgrade(revision)
        return 0
    if command_name == "downgrade":
        downgrade(revision)
        return 0

    raise SystemExit(f"Unsupported migration command: {command_name}")


if __name__ == "__main__":
    raise SystemExit(main())
