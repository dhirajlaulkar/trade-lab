from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    """
    Abstract Base Class for trading strategies.
    Strategies must take a DataFrame of OHLCV data and return a DataFrame
    with a 'Signal' column.
    
    Signal values:
    1: Long
    -1: Short
    0: Neutral/Exit
    """
    
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Generates trading signals based on the logic.
        
        Args:
            data (pd.DataFrame): OHLCV data.
        
        Returns:
            pd.DataFrame: Original dataframe with 'Signal' column added.
        """
        pass
