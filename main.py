import argparse
import logging
import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from automation.runner import Runner
from llm.summarize_results import generate_summary

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="TradeLab Backtesting CLI")
    parser.add_argument('--symbol', type=str, required=True, help="Ticker symbol (e.g., SPY)")
    parser.add_argument('--strategy', type=str, choices=['momentum', 'mean_reversion'], required=True, help="Strategy to run")
    parser.add_argument('--start', type=str, help="Start Date (YYYY-MM-DD)")
    parser.add_argument('--end', type=str, help="End Date (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    runner = Runner()
    try:
        metrics, _ = runner.run(
            symbol=args.symbol,
            strategy_name=args.strategy,
            start_date=args.start,
            end_date=args.end
        )
        
        print("\n" + "="*40)
        print(f"RESULTS: {args.strategy.upper()} on {args.symbol}")
        print("="*40)
        for k, v in metrics.items():
            print(f"{k}: {v}")
        print("="*40 + "\n")
        
        # LLM Summary
        summary = generate_summary(metrics, args.strategy, args.symbol)
        print(summary)
        
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        # traceback for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
