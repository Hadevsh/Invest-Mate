import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import importlib.util
import MetaTrader5 as mt5
import logging

from utils.mt5 import load_candlestick_data

logger = logging.getLogger("main") # Get global logger "main.log" from main.py

class Terminal:
    def __init__(self):
        logger.info("Initializing Terminal...")

    # Start function for GUI
    def start(self):
        root = tk.Tk()
        root.title("Trading Terminal")
        root.state('zoomed') 

        # Close program function
        def on_close():
            quit()
        # Handle the close event
        root.protocol("WM_DELETE_WINDOW", on_close)

        # User inputs
        tk.Label(root, text="Symbol:").grid(row=0, column=0, sticky=tk.W)
        symbol_entry = tk.Entry(root)
        symbol_entry.grid(row=0, column=1, sticky=tk.W)

        tk.Label(root, text="Timeframe: ").grid(row=1, column=0, sticky=tk.W)
        timeframe_entry = tk.Entry(root)
        timeframe_entry.grid(row=1, column=1, sticky=tk.W)

        tk.Label(root, text="Number of candles: ").grid(row=2, column=0, sticky=tk.W)
        candles_num_entry = tk.Entry(root)
        candles_num_entry.grid(row=2, column=1, sticky=tk.W)

        # Initial dummy chart
        dummy_data = load_candlestick_data() # Load candlestick data with default data
        fig, ax = self.create_chart(dummy_data)

        # Canvas for the chart
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, sticky="nsew")
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)

        # Load button
        def on_load():
            symbol = symbol_entry.get()
            timeframe = timeframe_entry.get()
            candles_num = candles_num_entry.get()
            ax.set_title(f"{symbol} {candles_num} candles ({timeframe})")
            # script_path = "strategy_line.py"  # Replace with dynamic selection if needed
            self.refresh_chart(canvas, symbol, timeframe, candles_num, ax)

        load_button = tk.Button(root, text="Load Data", command=on_load)
        load_button.grid(row=4, column=0, columnspan=2)

        root.mainloop()

    # Chart creation function using matplotlib
    def create_chart(self, data):
        fig, ax = plt.subplots(figsize=(12, 6))

        # Creatig candlestick chart
        mpf.plot(
            data,
            type='candle',
            ax=ax,
            style='yahoo',
            show_nontrading=False # Skip days with no data
        )
        return fig, ax

    # Refresh chart function
    def refresh_chart(self, canvas, symbol, timeframe, candles_num, ax=None):
        try:
            candles_num = int(candles_num) # Convert to integer
            data = load_candlestick_data(symbol, timeframe, candles_num) # Load new data

            # Creatig candlestick chart
            mpf.plot(
                data,
                type='candle',
                ax=ax,
                style='yahoo',
                show_nontrading=False # Skip days with no data
            )
            logger.info(f"Successfully updated chart for {symbol}, {candles_num} candles ({timeframe})")
            
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
        except RuntimeError as re:
            logger.error(f"Runtime error: {re}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")