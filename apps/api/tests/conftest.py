from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy.orm import Session, sessionmaker

from app.db.migrate import upgrade
from app.db.session import create_session_factory


@pytest.fixture()
def database_url(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    database_path = tmp_path / "eidos-test.sqlite3"
    url = f"sqlite:///{database_path.as_posix()}"
    monkeypatch.setenv("EIDOS_DATABASE_URL", url)
    upgrade("head")
    return url


@pytest.fixture()
def session_factory(database_url: str) -> sessionmaker[Session]:
    return create_session_factory(database_url)


@pytest.fixture()
def session(session_factory: sessionmaker[Session]) -> Generator[Session, None, None]:
    with session_factory() as db_session:
        yield db_session
        db_session.rollback()
