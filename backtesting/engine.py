import pandas as pd
import logging

logger = logging.getLogger(__name__)

class BacktestEngine:
    def __init__(self, initial_capital: float = 100000.0, commission: float = 0.0):
        self.initial_capital = initial_capital
        self.commission = commission
        
    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        if 'Signal' not in data.columns:
            raise ValueError("Data must must contain 'Signal' column")
            
        df = data.copy()
        
        df['Position'] = df['Signal'].shift(1).fillna(0)
        
        df['Market_Return'] = df['Close'].pct_change()
        df['Strategy_Return'] = df['Position'] * df['Market_Return']
        
        df['Trades'] = df['Position'].diff().abs()
        df['Transaction_Cost'] = df['Trades'] * self.commission
        
        df['Strategy_Return_Net'] = (df['Strategy_Return'] - df['Transaction_Cost']).fillna(0)
        
        df['Equity_Curve'] = (1 + df['Strategy_Return_Net']).cumprod() * self.initial_capital
        
        return df
