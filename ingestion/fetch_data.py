import yfinance as yf
import pandas as pd
import logging
from .market_api import MarketDataProvider

logger = logging.getLogger(__name__)

class YahooFinanceProvider(MarketDataProvider):
    """
    Implementation of MarketDataProvider using yfinance.
    """
    
    def fetch_ohlcv(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        logger.info(f"Fetching data for {symbol} from {start_date} to {end_date} via yfinance")
        try:
            df = yf.download(symbol, start=start_date, end=end_date, progress=False, auto_adjust=True)
            
            if df.empty:
                logger.warning(f"No data returned for {symbol}")
                return pd.DataFrame()
            
            # Ensure standard column names if needed, though yfinance is usually good.
            # yfinance returns 'Open', 'High', 'Low', 'Close', 'Volume'
            # We want to make sure it's clean.
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            return df
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            raise
