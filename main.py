from src.utils import *
import src.mt5 as mt5

def main():
    init_logging()
    mt5.init_mt5()
    logging.info("Starting program...")
    mt5.fetch_symbol_price()

if __name__ == "__main__":
    main()