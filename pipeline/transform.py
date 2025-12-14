import pandas as pd
import logging

logger = logging.getLogger(__name__)

def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    df.columns = [c.capitalize() for c in df.columns]
    
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        msg = f"Data is missing required columns: {missing}"
        logger.error(msg)
        raise ValueError(msg)
        
    return df[required_columns]

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
        
    df = validate_schema(df)
    
    if df.index.tz is None:
        df.index = df.index.tz_localize('UTC')
    else:
        df.index = df.index.tz_convert('UTC')
        
    return df
