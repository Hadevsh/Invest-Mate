import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import mplfinance as mpf
import numpy as np
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
    
    return df


def moving_average(data_frame: pd.DataFrame, period: int, symbol: str) -> None:
    """
    Calculates a Simple Moving Average (SMA) over a specified period
    Example: 10-period moving average
    """
    data_frame['SMA'] = data_frame['close'].rolling(window=period).mean()

    # Print the data with the SMA
    sma_data = data_frame[['time', 'close', 'SMA']].tail(period) # Last n (period) positions
    
    logger.info(f"Successfully calculated SMA over {period} period for {symbol}")
    return sma_data

def plot_sma(ax, data_frame: pd.DataFrame, symbol: str):
    """
    Plots the Simple Moving Average (SMA) line on the provided axis
    """
    if 'SMA' not in data_frame.columns:
        logger.error(f"SMA not found in the DataFrame for {symbol}. Ensure SMA is calculated.")
        return

    # Drop NaN values to avoid plotting issues
    sma_data = data_frame.dropna(subset=['SMA'])

    if sma_data.empty:
        logger.error("No valid SMA data to plot.")
        return

    # Align SMA with the time axis
    ax.plot(
        sma_data['time'],  # Ensure only valid times are plotted
        sma_data['SMA'],
        label=f"SMA ({len(sma_data)})",
        color='orange',
        linewidth=1.5
    )
    ax.legend(loc='upper left')
    logger.info(f"Successfully plotted SMA for {symbol}")
