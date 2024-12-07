import MetaTrader5 as mt5
import logging
import os

def init_logging(name="main"):
    """
    Sets-up the logging library - save logs to a file
    """
    logging.basicConfig(encoding='UTF-8', level=logging.INFO,
                       format="%(asctime)s %(name)s %(levelname)s: %(message)s", datefmt='%I:%M:%S',
                       handlers=[logging.FileHandler(f"{name}.log", mode='w', encoding='UTF-8')])
    logging.info("Set-up logging successfully")

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