from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
import json

# Add project root to path so we can import modules
sys.path.append(os.getcwd())

from dotenv import load_dotenv
load_dotenv()

from automation.runner import Runner
from llm.summarize_results import generate_summary

app = FastAPI()

class SummaryRequest(BaseModel):
    metrics: dict
    strategy: str
    symbol: str

class BacktestRequest(BaseModel):
    symbol: str
    strategy: str
    start_date: str = "2020-01-01"
    end_date: str = "2023-12-31"

@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/api/ai_summary")
def get_ai_summary(req: SummaryRequest):
    summary = generate_summary(req.metrics, req.strategy, req.symbol)
    return {"summary": summary}

@app.post("/api/run_backtest")
def run_backtest(req: BacktestRequest):
    try:
        # Initialize Runner
        # We might need to override config paths if running in serverless env
        runner = Runner()
        
        # Run Backtest
        metrics, results_df = runner.run(
            symbol=req.symbol,
            strategy_name=req.strategy,
            start_date=req.start_date,
            end_date=req.end_date
        )
        
        # Convert results for JSON response
        # We'll return the Equity Curve for charting
        chart_data = []
        if 'Equity_Curve' in results_df.columns:
            # Filter out the initial period where no trades have happened (Equity stays at initial capital)
            # This avoids the long flat line at the start due to strategy warm-up
            initial_cap = results_df['Equity_Curve'].iloc[0]
            mask = results_df['Equity_Curve'] != initial_cap
            
            # If we have any trades, filter. If no trades at all, we keep it as is (flat)
            if mask.any():
                # Find first index where it changes
                first_change_idx = mask.idxmax()
                # Slice from that index onwards
                results_df = results_df.loc[first_change_idx:]
            
            # Downsample if too large? 3 years of daily data is ~750 points, which is fine.
            results_df.index = results_df.index.astype(str) # Date to string
            chart_data = results_df['Equity_Curve'].reset_index().to_dict(orient='records')
            
        return {
            "metrics": metrics,
            "chart_data": chart_data
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
