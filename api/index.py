from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
import os
import json

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
        runner = Runner()
        
        metrics, results_df = runner.run(
            symbol=req.symbol,
            strategy_name=req.strategy,
            start_date=req.start_date,
            end_date=req.end_date
        )
        
        chart_data = []
        if 'Equity_Curve' in results_df.columns:
            initial_cap = results_df['Equity_Curve'].iloc[0]
            mask = results_df['Equity_Curve'] != initial_cap
            
            if mask.any():
                first_change_idx = mask.idxmax()
                results_df = results_df.loc[first_change_idx:]
            
            results_df.index = results_df.index.astype(str)
            chart_data = results_df['Equity_Curve'].reset_index().to_dict(orient='records')
            
        return {
            "metrics": metrics,
            "chart_data": chart_data
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
