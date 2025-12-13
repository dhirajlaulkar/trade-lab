# TradeLab: Python-Based Trading Analytics & Backtesting Platform

## Overview
TradeLab is a modular, production-grade Python system designed for quantitative research. It simulates an institutional-grade analytics pipeline, capable of ingesting market data, processing it, running signals-based strategies, and generating performance metrics.

**Note**: This project is for educational and simulation purposes only. No real money trading.

## Architecture
The system follows a strict separation of concerns:
- **`ingestion/`**: Handles external APIs (e.g., Yahoo Finance).
- **`pipeline/`**: Data cleaning and transformation. No raw data is ever mutated in place.
- **`strategies/`**: Pure logic classes generating signals (-1, 0, 1).
- **`backtesting/`**: Vectorized engine to simulate portfolio state over time.
- **`automation/`**: Orchestration of the entire flow.

## specific Design Decisions
- **Vectorized Backtesting**: Chosen for performance on large datasets using Pandas.
- **Config-Driven**: All parameters (windows, dates, capital) are in `config.yaml`.
- **Type Hinting**: Used throughout for better developer experience and safety.
- **Data Persistence (ETL Custom)**: The system supports saving raw key data to `data/raw` and cleaned data to `data/processed`. This follows standard ETL patterns to ensure reproducibility and auditability, allowing researchers to debug cleaning logic on static files.

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the main analysis:
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
