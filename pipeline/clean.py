import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans market data by handling missing values and ensuring correct format.
    
    Args:
        df (pd.DataFrame): Raw OHLCV data.
        
    Returns:
        pd.DataFrame: Cleaned data.
    """
    if df.empty:
        logger.warning("Empty DataFrame passed to clean_data")
        return df

    initial_rows = len(df)
    
    # Sort by date
    df = df.sort_index()

    # Drop duplicate index
    df = df[~df.index.duplicated(keep='first')]

    # Fill missing values
    # Forward fill strategies are common in finance (assume last price holds)
    df = df.ffill().bfill()
    
    # Ensure no NaNs remain
    if df.isnull().values.any():
        logger.warning("Data still contains NaNs after filling, dropping remaining NaN rows.")
        df = df.dropna()

    final_rows = len(df)
    logger.info(f"Data cleaned. Rows: {initial_rows} -> {final_rows}")
    
    return df
