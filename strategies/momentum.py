import pandas as pd
from .base import Strategy

class MomentumStrategy(Strategy):
    """
    Moving Average Crossover Strategy.
    """
    
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        
        fast_window = self.config.get('fast_window', 50)
        slow_window = self.config.get('slow_window', 200)
        
        df['SMA_Fast'] = df['Close'].rolling(window=fast_window).mean()
        df['SMA_Slow'] = df['Close'].rolling(window=slow_window).mean()
        
        df['Signal'] = 0
        # Long signal when Fast > Slow
        df.loc[df['SMA_Fast'] > df['SMA_Slow'], 'Signal'] = 1
        # Short signal when Fast < Slow
        df.loc[df['SMA_Fast'] < df['SMA_Slow'], 'Signal'] = -1
        
        return df
