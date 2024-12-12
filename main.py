from utils.logger import init_logger
import utils.mt5 as mt5

from utils.terminal import Terminal

# Strategies
import strategies.average_crossover as avg_crossover

logger = init_logger() # Global main.log logger
mt5.init_mt5() # Initialize MT5 connection for the whole program

terminal = Terminal()
terminal.start()

def main() -> None:
    logger.info("Starting program...")
    mt5.fetch_symbol_price() # Testing function - check if (ensure) MT5 is connected

if __name__ == "__main__":
    main()