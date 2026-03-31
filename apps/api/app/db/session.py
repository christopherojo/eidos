from __future__ import annotations

from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.config import get_database_url


def create_engine_from_url(database_url: str | None = None) -> Engine:
    resolved_url = database_url or get_database_url()
    connect_args = {"check_same_thread": False} if resolved_url.startswith("sqlite") else {}
    engine = create_engine(
        resolved_url,
        future=True,
        connect_args=connect_args,
    )
    if resolved_url.startswith("sqlite"):
        event.listen(engine, "connect", _enable_sqlite_foreign_keys)
    return engine


def _enable_sqlite_foreign_keys(dbapi_connection: Any, _: Any) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_session_factory(database_url: str | None = None) -> sessionmaker[Session]:
    return sessionmaker(
        bind=create_engine_from_url(database_url),
        autoflush=False,
        autocommit=False,
    )


def get_session(database_url: str | None = None) -> Generator[Session, None, None]:
    session_factory = create_session_factory(database_url)
    session = session_factory()
    try:
        yield session
    finally:
        session.close()
