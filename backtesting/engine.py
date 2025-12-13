import pandas as pd
import logging

logger = logging.getLogger(__name__)

class BacktestEngine:
    """
    Vectorized backtesting engine.
    Assumes execution at the Open price of the NEXT bar after the signal is generated.
    """
    
    def __init__(self, initial_capital: float = 100000.0, commission: float = 0.0):
        self.initial_capital = initial_capital
        self.commission = commission
        
    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Executes the backtest.
        
        Args:
            data (pd.DataFrame): DataFrame with 'Signal', 'Open', 'Close'.
            
        Returns:
            pd.DataFrame: Data with 'Portfolio_Value' and trade details.
        """
        if 'Signal' not in data.columns:
            raise ValueError("Data must must contain 'Signal' column")
            
        df = data.copy()
        
        # Calculate positions
        # Signal=1 means Target Postion=1 (Long), Signal=-1 means Target Position=-1 (Short)
        # We assume 100% equity allocation for simplicity in this version
        
        # Shift signals by 1 to avoid lookahead bias; we trade at Open of next bar based on Close signal
        df['Position'] = df['Signal'].shift(1).fillna(0)
        
        # Calculate Returns
        # Strategy Return = Position * (Pct Change of Price)
        # using 'Open' to 'Open' returns or 'Close' to 'Close'?
        # If we enter at Open (t), and hold till Open (t+1), the return is (Open(t+1) - Open(t)) / Open(t)
        # Standard vectorized approach often uses Close-to-Close returns * lagged position.
        
        df['Market_Return'] = df['Close'].pct_change()
        df['Strategy_Return'] = df['Position'] * df['Market_Return']
        
        # Apply commission cost (simplified approximation)
        # Commission is paid when position changes
        df['Trades'] = df['Position'].diff().abs()
        df['Transaction_Cost'] = df['Trades'] * self.commission
        
        df['Strategy_Return_Net'] = df['Strategy_Return'] - df['Transaction_Cost']
        
        # Cumulative Returns
        df['Equity_Curve'] = (1 + df['Strategy_Return_Net']).cumprod() * self.initial_capital
        
        return df
