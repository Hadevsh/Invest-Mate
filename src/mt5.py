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
    return True

def fetch_test_data():
    pass