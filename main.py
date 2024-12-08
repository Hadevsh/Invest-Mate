from utils.logger import init_logger
import utils.mt5 as mt5

logger = init_logger() # Global main.log logger

def main():
    mt5.init()
    logger.info("Starting program...")
    mt5.fetch_symbol_price()

if __name__ == "__main__":
    main()