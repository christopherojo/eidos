# Eidos

## Overview

Eidos is a portfolio intelligence platform that transforms fragmented financial data into clear, actionable insights. Instead of simply tracking holdings, Eidos analyzes risk, diversification, macro exposure, and market sentiment to help investors understand what they own, why it matters, and what to do next.

---

## Key Features

* **Portfolio Tracking**
  Monitor holdings, performance, and historical value over time.

* **Diversification & Risk Analysis**
  Identify concentration risks, sector exposure, and hidden correlations.

* **News & Sentiment Intelligence**
  Aggregate relevant news and measure sentiment across your portfolio.

* **Macro Insights**
  Understand how interest rates, inflation, and global trends impact your positions.

* **Stock-Level Analysis**
  Drill into individual holdings with performance, news, and risk context.

* **Alerts & Insights**
  Get notified when meaningful changes occur in your portfolio or the market.

---

## Why Eidos

Most investors rely on scattered tools—broker dashboards, news platforms, and spreadsheets—without a unified system for decision-making. Eidos solves this by consolidating data and delivering structured insights tailored to your portfolio.

---

## Tech Stack

* **Frontend:** Next.js, TypeScript, Tailwind CSS
* **Backend:** FastAPI (Python)
* **Database:** PostgreSQL
* **Caching:** Redis
* **Analytics:** pandas, NumPy, scikit-learn

---

## Project Structure

```
portfolio-intelligence/
  apps/
    web/        # Frontend (Next.js)
    api/        # Backend (FastAPI)
  services/
    analytics/  # Portfolio & risk calculations
    ingestion/  # Market, news, macro data pipelines
  packages/
    ui/         # Shared UI components
    types/      # Shared TypeScript types
  docs/         # Product and technical documentation
```

---

## Getting Started

### Prerequisites

* Node.js (v18+)
* Python (3.10+)
* PostgreSQL
* Redis

### Setup

```bash
# Clone the repo
git clone https://github.com/your-username/eidos.git
cd eidos

# Setup backend
cd apps/api
pip install -r requirements.txt

# Setup frontend
cd ../web
npm install
```

### Run Locally

```bash
# Start backend
cd apps/api
uvicorn app.main:app --reload

# Start frontend
cd apps/web
npm run dev
```

---

## Development Workflow

### Branching Strategy

* `main` → production-ready code
* `develop` → staging branch
* `feature/*` → new features
* `fix/*` → bug fixes

### Example

```bash
git checkout -b feature/portfolio-crud
```

---

## Roadmap

### v0.1 — Core Tracking

* Portfolio CRUD
* Performance dashboard
* Allocation breakdown

### v0.2 — Risk Intelligence

* Diversification score
* Concentration analysis
* Volatility & drawdown metrics

### v0.3 — News & Sentiment

* Portfolio-specific news feed
* Sentiment scoring

### v0.4 — Macro Layer

* Macro dashboard
* Exposure mapping

### v1.0 — Public Release

* Alerts system
* Insight engine
* Polished UI/UX

---

## Contributing

Contributions are welcome. Please open an issue or submit a pull request with a clear description of changes.

---

## License

MIT License

---

## Vision

Eidos is built to evolve from a portfolio tracker into a full decision engine—helping investors move from raw data to informed, confident actions.
