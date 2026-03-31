from __future__ import annotations

from sqlalchemy import func, select

from app.db.models import Alert, Holding, Note, Portfolio, PortfolioSnapshot, Security, Transaction
from app.db.seed import seed
from app.db.session import create_session_factory


def test_seed_populates_local_development_data(database_url: str) -> None:
    seed()
    session_factory = create_session_factory(database_url)

    with session_factory() as session:
        assert session.scalar(select(func.count()).select_from(Portfolio)) == 1
        assert session.scalar(select(func.count()).select_from(Security)) == 2
        assert session.scalar(select(func.count()).select_from(Transaction)) == 2
        assert session.scalar(select(func.count()).select_from(Note)) == 1
        assert session.scalar(select(func.count()).select_from(Alert)) == 1
        assert session.scalar(select(func.count()).select_from(Holding)) == 2
        assert session.scalar(select(func.count()).select_from(PortfolioSnapshot)) == 1
