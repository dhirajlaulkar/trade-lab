from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        pass
