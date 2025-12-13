import pandas as pd
import numpy as np

def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calculates performance metrics from backtest results.
    
    Args:
        df (pd.DataFrame): Backtest result with 'Strategy_Return_Net'
        
    Returns:
        dict: key metrics.
    """
    daily_returns = df['Strategy_Return_Net'].fillna(0)
    
    total_return = (df['Equity_Curve'].iloc[-1] / df['Equity_Curve'].iloc[0]) - 1
    
    # Annualized Return (assuming daily data, 252 trading days)
    n_days = len(df)
    annualized_return = (1 + total_return) ** (252 / n_days) - 1
    
    # Sharpe Ratio (assuming 0 risk-free rate for simplicity)
    mean_return = daily_returns.mean()
    std_return = daily_returns.std()
    sharpe_ratio = (mean_return / std_return) * np.sqrt(252) if std_return != 0 else 0
    
    # Max Drawdown
    cumulative_returns = (1 + daily_returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()
    
    # Win Rate
    wins = len(daily_returns[daily_returns > 0])
    losses = len(daily_returns[daily_returns < 0])
    total_trades = wins + losses
    win_rate = wins / total_trades if total_trades > 0 else 0
    
    return {
        "Total Return": f"{total_return:.2%}",
        "Annualized Return": f"{annualized_return:.2%}",
        "Sharpe Ratio": f"{sharpe_ratio:.2f}",
        "Max Drawdown": f"{max_drawdown:.2%}",
        "Win Rate": f"{win_rate:.2%}"
    }
