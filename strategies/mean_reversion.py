import pandas as pd
import numpy as np
from .base import Strategy

class MeanReversionStrategy(Strategy):
    """
    Z-Score based Mean Reversion Strategy.
    """
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        window = self.config.get('window', 20)
        std_dev_threshold = self.config.get('std_dev', 2)
        
        # Calculate Rolling Mean and Std
        rolling_mean = df['Close'].rolling(window=window).mean()
        rolling_std = df['Close'].rolling(window=window).std()
        
        # Calculate Z-Score
        df['Z_Score'] = (df['Close'] - rolling_mean) / rolling_std
        
        df['Signal'] = 0
        
        # If Price is significantly below mean, Buy (Signal=1)
        df.loc[df['Z_Score'] < -std_dev_threshold, 'Signal'] = 1
        
        # If Price is significantly above mean, Sell (Signal=-1)
        df.loc[df['Z_Score'] > std_dev_threshold, 'Signal'] = -1
        
        return df
