from __future__ import annotations

import sqlalchemy as sa

from alembic import op

revision = "20260331_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "portfolios",
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("base_currency", sa.String(length=3), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_portfolios")),
        sa.UniqueConstraint("name", name=op.f("uq_portfolios_name")),
    )
    op.create_table(
        "securities",
        sa.Column("symbol", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("asset_type", sa.String(length=32), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("exchange", sa.String(length=64), nullable=True),
        sa.Column("isin", sa.String(length=12), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("length(currency) = 3", name=op.f("ck_securities_currency_length")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_securities")),
        sa.UniqueConstraint("isin", name=op.f("uq_securities_isin")),
        sa.UniqueConstraint("symbol", name=op.f("uq_securities_symbol")),
    )
    op.create_table(
        "transactions",
        sa.Column("portfolio_id", sa.String(length=36), nullable=False),
        sa.Column("security_id", sa.String(length=36), nullable=False),
        sa.Column("transaction_type", sa.String(length=32), nullable=False),
        sa.Column("quantity", sa.Numeric(20, 6), nullable=False),
        sa.Column("price", sa.Numeric(20, 6), nullable=False),
        sa.Column("gross_amount", sa.Numeric(20, 6), nullable=False),
        sa.Column("fees", sa.Numeric(20, 6), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("settled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("external_ref", sa.String(length=100), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("fees >= 0", name=op.f("ck_transactions_fees_non_negative")),
        sa.CheckConstraint(
            "gross_amount >= 0",
            name=op.f("ck_transactions_gross_amount_non_negative"),
        ),
        sa.CheckConstraint("length(currency) = 3", name=op.f("ck_transactions_currency_length")),
        sa.CheckConstraint("price >= 0", name=op.f("ck_transactions_price_non_negative")),
        sa.CheckConstraint("quantity > 0", name=op.f("ck_transactions_quantity_positive")),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolios.id"],
            name=op.f("fk_transactions_portfolio_id_portfolios"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["security_id"],
            ["securities.id"],
            name=op.f("fk_transactions_security_id_securities"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_transactions")),
    )
    op.create_table(
        "notes",
        sa.Column("portfolio_id", sa.String(length=36), nullable=False),
        sa.Column("security_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolios.id"],
            name=op.f("fk_notes_portfolio_id_portfolios"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["security_id"],
            ["securities.id"],
            name=op.f("fk_notes_security_id_securities"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_notes")),
    )
    op.create_table(
        "alerts",
        sa.Column("portfolio_id", sa.String(length=36), nullable=False),
        sa.Column("security_id", sa.String(length=36), nullable=True),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("rule_type", sa.String(length=64), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("triggered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolios.id"],
            name=op.f("fk_alerts_portfolio_id_portfolios"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["security_id"],
            ["securities.id"],
            name=op.f("fk_alerts_security_id_securities"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_alerts")),
        sa.UniqueConstraint(
            "portfolio_id",
            "rule_type",
            "triggered_at",
            name=op.f("uq_alerts_rule_window"),
        ),
    )
    op.create_table(
        "holdings",
        sa.Column("portfolio_id", sa.String(length=36), nullable=False),
        sa.Column("security_id", sa.String(length=36), nullable=False),
        sa.Column("quantity", sa.Numeric(20, 6), nullable=False),
        sa.Column("net_invested_amount", sa.Numeric(20, 6), nullable=False),
        sa.Column("average_cost", sa.Numeric(20, 6), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False),
        sa.Column("last_transaction_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("length(currency) = 3", name=op.f("ck_holdings_currency_length")),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolios.id"],
            name=op.f("fk_holdings_portfolio_id_portfolios"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["security_id"],
            ["securities.id"],
            name=op.f("fk_holdings_security_id_securities"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_holdings")),
        sa.UniqueConstraint(
            "portfolio_id",
            "security_id",
            name=op.f("uq_holdings_portfolio_security"),
        ),
    )
    op.create_table(
        "portfolio_snapshots",
        sa.Column("portfolio_id", sa.String(length=36), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("holdings_count", sa.Integer(), nullable=False),
        sa.Column("total_quantity", sa.Numeric(20, 6), nullable=False),
        sa.Column("total_net_invested_amount", sa.Numeric(20, 6), nullable=False),
        sa.Column("total_market_value", sa.Numeric(20, 6), nullable=True),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "holdings_count >= 0",
            name=op.f("ck_portfolio_snapshots_holdings_count_non_negative"),
        ),
        sa.ForeignKeyConstraint(
            ["portfolio_id"],
            ["portfolios.id"],
            name=op.f("fk_portfolio_snapshots_portfolio_id_portfolios"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_portfolio_snapshots")),
        sa.UniqueConstraint(
            "portfolio_id",
            "snapshot_date",
            name=op.f("uq_portfolio_snapshots_portfolio_date"),
        ),
    )


def downgrade() -> None:
    op.drop_table("portfolio_snapshots")
    op.drop_table("holdings")
    op.drop_table("alerts")
    op.drop_table("notes")
    op.drop_table("transactions")
    op.drop_table("securities")
    op.drop_table("portfolios")
