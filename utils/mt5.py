import MetaTrader5 as mt5
import logging
import pandas as pd
import datetime as dt

logger = logging.getLogger("main") # Get global logger "main.log" from main.py

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
        logger.info("Successfully logged MT5 account info") # Logged for testing purposes - ensures that MT5 is connected
    except Exception as e:
        logger.error(f"Couldn't log MT5 account info. Error code: {e}")

def fetch_symbol_price(symbol: str="BTCUSD") -> None:
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        logger.error(f"Failed to retrieve current price of {symbol}")
    current_price = tick.bid
    print(f"Current price of {symbol}: {current_price}")

# Fetch data from MT5
def load_candlestick_data(symbol, start_date, end_date=None):
    # Set default end date to today
    if end_date is None:
        end_date = dt.datetime.now()

    # Convert start and end dates to datetime objects
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = pd.Timestamp(end_date)

    # Request candlestick data
    rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_H1, start_date, end_date)

    if rates is None:
        logger.error(f"Failed to retrieve data for {symbol}. Error: {mt5.last_error()}")
        return None

    # Convert to DataFrame
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    data.set_index('time', inplace=True)

    # Rename columns for mplfinance
    data.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "tick_volume": "Volume"}, inplace=True)
    return data
