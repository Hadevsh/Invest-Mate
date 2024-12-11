import MetaTrader5 as mt5
import logging
import pandas as pd
import datetime as dt
import mplfinance

logger = logging.getLogger("main")  # Get global logger "main.log" from main.py

def init_mt5() -> bool:
    """
    Connects to MetaTrader5
    """
    if not mt5.initialize():
        error_code = mt5.last_error()
        logger.error(f"MetaTrader5 initialization failed. Error code: {error_code}")
        return False
    logger.info("Connected to MetaTrader5")
    account_info()
    return True

# Test funcions
def account_info() -> None:
    try:
        print("Name:", mt5.account_info().name)
        print("Balance:", mt5.account_info().balance)
        logger.info("Successfully logged MT5 account info")  # Logged for testing purposes - ensures that MT5 is connected
    except Exception as e:
        logger.error(f"Couldn't log MT5 account info. Error code: {e}")

def fetch_symbol_price(symbol: str="BTCUSD") -> None:
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        logger.error(f"Failed to retrieve current price of {symbol}")
    current_price = tick.bid
    print(f"Current price of {symbol}: {current_price}")

# Fetch data from MT5
def load_candlestick_data(symbol: str="BTCUSD", timeframe: str="M30", candles_num: int=100) -> pd.DataFrame:
    if not mt5.initialize():
        logger.error("Failed to initialize MT5. Ensure MetaTrader5 is running and properly configured.")
        raise RuntimeError("MT5 initialization failed.")
    
    if not mt5.symbol_select(symbol, True):
        logger.error(f"Symbol '{symbol}' is not available in MT5.")
        raise ValueError(f"Symbol '{symbol}' is unavailable.")
    
    timeframes = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
        "W1": mt5.TIMEFRAME_W1,
        "MN1": mt5.TIMEFRAME_MN1
    }
    
    mt5_timeframe = timeframes.get(timeframe.upper())
    if mt5_timeframe is None:
        logger.error(f"Invalid timeframe '{timeframe}'. Use one of {list(timeframes.keys())}.")
        raise ValueError(f"Invalid timeframe '{timeframe}'.")
    
    rates = mt5.copy_rates_from_pos(symbol, mt5_timeframe, 0, candles_num)
    if rates is None:
        error = mt5.last_error()
        logger.error(f"Failed to retrieve data for {symbol} ({timeframe}, {candles_num} candles). Error: {error}")
        raise RuntimeError(f"Error loading data for {symbol}.")
    
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')  # Convert epoch to datetime
    data.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "tick_volume": "Volume"}, inplace=True)
    data.set_index('time', inplace=True)  # Set 'time' as the index
    
    logger.info(f"Successfully loaded {len(data)} candles for {symbol} ({timeframe}).")
    return data
