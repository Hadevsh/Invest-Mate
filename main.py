from utils.logger import init_logger
import utils.mt5 as mt5

import strategies.average_crossover as averag_crossover

logger = init_logger() # Global main.log logger

def main() -> None:
    mt5.init_mt5() # Initialize MT5 connection for the whole program
    logger.info("Starting program...")
    mt5.fetch_symbol_price() # Testing function - check if (ensure) MT5 is connected
    
    averag_crossover.fetch_data()

if __name__ == "__main__":
    main()