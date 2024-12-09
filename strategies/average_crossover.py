import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger("main") # Get global logger "main.log" from main.py

def fetch_data(symbol: str="BTCUSD", timeframe=mt5.TIMEFRAME_M30, num_candles: int=1000) -> None:
    """
    Retrieves historical data for a selected asset (symbol)
    timeframe * num_candles = how far back
    """
    if not mt5.symbol_select(symbol, True):
        logger.error(f"Failed to select {symbol}. Error code: {mt5.last_error()}")

    # Get historical data from the current time backward
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)

    # Convert the result to a pandas DataFrame for easier handling
    if rates is not None:
        df = pd.DataFrame(rates)
        # Convert time in seconds to a datetime format
        df['time'] = pd.to_datetime(df['time'], unit='s')
        logger.info(f"Successfully fetched data for {symbol} - T{timeframe}x{num_candles}")
    else:
        logger.error(f"Failed to retrieve data. Error code: {mt5.last_error()}")

    moving_average(df, 10, symbol)


def moving_average(data_frame: pd.DataFrame, period, symbol) -> None:
    """
    Calculates a Simple Moving Average (SMA) over a specified period
    Example: 10-period moving average
    """
    data_frame['SMA'] = data_frame['close'].rolling(window=period).mean()

    # Print the data with the SMA
    sma_data = data_frame[['time', 'close', 'SMA']].tail(20) # Last 20 positions
    logger.info(f"Successfully calculated SMA over {period} period for {symbol}")