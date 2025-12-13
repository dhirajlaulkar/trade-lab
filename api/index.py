from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
import json

# Add project root to path so we can import modules
sys.path.append(os.getcwd())

from automation.runner import Runner

app = FastAPI()

class BacktestRequest(BaseModel):
    symbol: str
    strategy: str
    start_date: str = "2020-01-01"
    end_date: str = "2023-12-31"

@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

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
