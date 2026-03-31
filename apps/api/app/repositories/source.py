from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Alert, Note, Portfolio, Security, Transaction
from app.schemas.source import (
    AlertCreate,
    NoteCreate,
    PortfolioCreate,
    SecurityCreate,
    TransactionCreate,
)


class PortfolioRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: PortfolioCreate) -> Portfolio:
        portfolio = Portfolio(
            name=payload.name,
            base_currency=payload.base_currency,
            description=payload.description,
        )
        self.session.add(portfolio)
        self.session.flush()
        return portfolio

    def get(self, portfolio_id: str) -> Portfolio | None:
        return self.session.get(Portfolio, portfolio_id)


class SecurityRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: SecurityCreate) -> Security:
        security = Security(
            symbol=payload.symbol,
            name=payload.name,
            asset_type=payload.asset_type,
            currency=payload.currency,
            exchange=payload.exchange,
            isin=payload.isin,
        )
        self.session.add(security)
        self.session.flush()
        return security

    def get(self, security_id: str) -> Security | None:
        return self.session.get(Security, security_id)


class TransactionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: TransactionCreate) -> Transaction:
        transaction = Transaction(**payload.model_dump())
        self.session.add(transaction)
        self.session.flush()
        return transaction

    def list_for_portfolio(self, portfolio_id: str) -> list[Transaction]:
        stmt = (
            select(Transaction)
            .where(Transaction.portfolio_id == portfolio_id)
            .order_by(
                Transaction.occurred_at.asc(),
                Transaction.created_at.asc(),
            )
        )
        return list(self.session.scalars(stmt))


class NoteRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: NoteCreate) -> Note:
        note = Note(**payload.model_dump())
        self.session.add(note)
        self.session.flush()
        return note


class AlertRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, payload: AlertCreate) -> Alert:
        alert = Alert(**payload.model_dump())
        self.session.add(alert)
        self.session.flush()
        return alert
