import pandas as pd
import logging

logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        logger.warning("Empty DataFrame passed to clean_data")
        return df

    initial_rows = len(df)
    
    df = df.sort_index()

    df = df[~df.index.duplicated(keep='first')]

    df = df.ffill().bfill()
    
    if df.isnull().values.any():
        logger.warning("Data still contains NaNs after filling, dropping remaining NaN rows.")
        df = df.dropna()

    final_rows = len(df)
    logger.info(f"Data cleaned. Rows: {initial_rows} -> {final_rows}")
    
    return df
