def generate_summary(metrics: dict, strategy_name: str, symbol: str) -> str:
    """
    Generates a human-readable summary of the backtest results.
    Can be replaced with an actual LLM call.
    """
    
    prompt_template = f"""
    Performance Summary for {strategy_name} on {symbol}:
    ---------------------------------------------------
    The strategy achieved a Total Return of {metrics['Total Return']} with an Annualized Return of {metrics['Annualized Return']}.
    Risk-adjusted performance was {metrics['Sharpe Ratio']} (Sharpe Ratio).
    The maximum drawdown experienced was {metrics['Max Drawdown']}.
    Win rate for trades was {metrics['Win Rate']}.
    """
    
    return prompt_template
