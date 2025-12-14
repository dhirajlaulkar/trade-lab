# TradeLab

## Overview
TradeLab is a modular, institutional-grade trading analytics system engineered for quantitative research. It features a scalable Python backend for vectorized backtesting and a Next.js frontend with a "Neobrutalist" design for real-time visualization.

## Architecture
### Backend (Python/FastAPI)
- **`ingestion/`**: Abstracted market data providers.
- **`pipeline/`**: strict schema validation and ETL processing.
- **`strategies/`**: Signal generation logic (-1, 0, 1).
- **`backtesting/`**: Vectorized simulation engine.
- **`automation/`**: Workflow orchestration.
- **`api/`**: Serverless-ready FastAPI endpoints.

### Frontend (Next.js)
- **`frontend/`**: React-based dashboard using Tailwind CSS and Recharts.
- **AI Analyst**: Integrated Groq (Llama 3) for automated performance insights.

## features
- **High-Performance Simulation**: Vectorized pandas operations for sub-second backtesting.
- **Interactive Dashboard**: Real-time Equity Curve visualization and parameter tuning.
- **AI-Powered Insights**: Automated text summaries of portfolio metrics.
- **Production-Ready**: Type-hinted, modular codebase designed for Vercel deployment.

## Setup
### Backend
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
uvicorn api.index:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables
Create a `.env` file in the root:
```
GROQ_API_KEY=your_api_key_here
```

## Example Output
```text
Running Momentum Strategy on SPY...
[INFO] Data fetched and processed.
[INFO] Backtest complete.
--- Performance Report ---
Total Return: 25.4%
Sharpe Ratio: 1.2
Max Drawdown: -15.2%
```
