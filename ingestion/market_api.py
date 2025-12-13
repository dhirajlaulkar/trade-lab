from abc import ABC, abstractmethod
import pandas as pd
from datetime import datetime

class MarketDataProvider(ABC):
    """
    Abstract base class for market data providers.
    """
    
    @abstractmethod
    def fetch_ohlcv(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch OHLCV data for a given symbol and time range.
        
        Args:
            symbol (str): The ticker symbol.
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.
            
        Returns:
            pd.DataFrame: DataFrame with columns [Open, High, Low, Close, Volume] and DatetimeIndex.
        """
        pass
