import MetaTrader5 as mt5
from src.utils import logging

def init_mt5():
    """
    Connects to MetaTrader5
    """
    if not mt5.initialize():
        error_code = mt5.last_error()
        logging.error("MetaTrader5 initialization failed. Error code: %s", error_code)
        return False
    logging.info("Connected to MetaTrader5")
    account_info()
    return True

def account_info():
    try:
        print("Name:", mt5.account_info().name)
        print("Balance:", mt5.account_info().balance)
        logging.info("Successfully logged MT5 account info")
    except Exception as e:
        logging.error("Couldn't log MT5 account info. Error %s", e)

def fetch_symbol_price(symbol="BTCUSD"):
    tick = mt5.symbol_info_tick(symbol)
    print(tick)
    if tick is None:
        logging.error(f"Failed to retrieve current price of {symbol}")
    current_price = tick.bid
    print(f"Current price of {symbol}: {current_price}")