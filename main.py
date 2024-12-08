from utils.logger import init_logger
from utils.mt5 import init_mt5

from strategies.average_crossover import fetch_data

logger = init_logger() # Global main.log logger

def main() -> None:
    # mt5.init()
    logger.info("Starting program...")
    # mt5.fetch_symbol_price()
    fetch_data()

if __name__ == "__main__":
    main()