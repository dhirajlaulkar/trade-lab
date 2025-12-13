import yaml
import logging
from ingestion.fetch_data import YahooFinanceProvider
from pipeline.clean import clean_data
from pipeline.transform import transform_data
from strategies.momentum import MomentumStrategy
from strategies.mean_reversion import MeanReversionStrategy
from backtesting.engine import BacktestEngine
from backtesting.metrics import calculate_metrics

logger = logging.getLogger(__name__)

class Runner:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.market_provider = YahooFinanceProvider()
        
    def run(self, symbol: str, strategy_name: str, start_date: str = None, end_date: str = None):
        """
        Orchestrates the full pipeline.
        """
        # Load defaults from config if not provided
        if not start_date:
            start_date = self.config['data']['start_date']
        if not end_date:
            end_date = self.config['data']['end_date']
            
        logger.info("Step 1: Ingesting Data")
        raw_df = self.market_provider.fetch_ohlcv(symbol, start_date, end_date)
        if raw_df.empty:
            logger.error("No data found. Aborting.")
            return
            
        logger.info("Step 2: Processing Pipeline")
        cleaned_df = clean_data(raw_df)
        final_df = transform_data(cleaned_df)
        
        logger.info(f"Step 3: Executing Strategy: {strategy_name}")
        strategy_config = self.config['strategies'].get(strategy_name, {})
        
        if strategy_name == 'momentum':
            strategy = MomentumStrategy(strategy_config)
        elif strategy_name == 'mean_reversion':
            strategy = MeanReversionStrategy(strategy_config)
        else:
            raise ValueError(f"Unknown strategy: {strategy_name}")
            
        signals_df = strategy.generate_signals(final_df)
        
        logger.info("Step 4: Running Backtest")
        engine = BacktestEngine(
            initial_capital=self.config['backtest']['initial_capital'],
            commission=self.config['backtest']['commission']
        )
        results = engine.run(signals_df)
        
        logger.info("Step 5: Computing Metrics")
        metrics = calculate_metrics(results)
        
        return metrics, results
