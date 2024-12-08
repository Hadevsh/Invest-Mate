import utils.logger as log
import logging
import utils.mt5 as mt5

def main():
    log.init()
    mt5.init()
    logging.info("Starting program...")
    mt5.fetch_symbol_price()

if __name__ == "__main__":
    main()