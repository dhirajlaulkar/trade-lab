# TradeLab: Python-Based Trading Analytics & Backtesting Platform

## Overview
TradeLab is a modular, production-grade Python system designed for quantitative research. It simulates an institutional-grade analytics pipeline, capable of ingesting market data, validating schema, executing signal-based strategies, and visualizing equity curves via a modern web interface.

**Note**: This project is for educational and simulation purposes only. No real money trading.

## Architecture
The system follows a strict separation of concerns, split into a **Python Backend** and **Next.js Frontend**:

### Backend (Python/FastAPI)
- **`ingestion/`**: Handles external APIs (e.g., Yahoo Finance).
- **`pipeline/`**: Data cleaning and transformation.
- **`strategies/`**: Pure logic classes generating signals (-1, 0, 1).
- **`backtesting/`**: Vectorized engine to simulate portfolio state over time.
- **`automation/`**: Orchestration logic.
- **`api/`**: Vercel-ready FastAPI handler acting as the bridge.

### Frontend (Next.js/React)
- **`frontend/`**: A "Mild Neobrutalist" dashboard using Tailwind CSS and Recharts.
- **Features**: Real-time backtest execution, interactive equity curve, and key performance metrics.

## Design Decisions
- **Vectorized Backtesting**: Chosen for performance on large datasets using Pandas.
- **Config-Driven**: All parameters (windows, dates, capital) are in `config.yaml`.
- **Type Hinting**: Used throughout for better developer experience and safety.
- **Data Persistence (ETL Custom)**: The system supports saving raw key data to `data/raw` and cleaned data to `data/processed`.
- **Vercel Architecture**: Designed to be deployed on Vercel, using Python Serverless Functions for the API and Next.js for the UI.

## Setup Instructions

### 1. Backend Setup
```bash
# Create virtual environment
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run API Server locally
uvicorn api.index:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

### 3. CLI Usage (Optional)
You can still run the backtest directly from the terminal:
```bash
python main.py --strategy momentum --symbol SPY
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
