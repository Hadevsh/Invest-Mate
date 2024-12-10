import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf
import pandas as pd
import importlib.util
import MetaTrader5 as mt5
import logging
import sys

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
            sys.exit() # Exit the script
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
        dummy_data = load_candlestick_data()
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
            # script_path = "strategy_line.py"  # Replace with dynamic selection if needed
            self.refresh_chart(canvas, symbol, timeframe, candles_num)

        load_button = tk.Button(root, text="Load Data", command=on_load)
        load_button.grid(row=4, column=0, columnspan=2)

        root.mainloop()

    # Chart creation function
    def create_chart(self, data):
        fig, ax = mpf.plot(data, type='candle', returnfig=True)
        return fig, ax
    
    # Refresh chart
    def refresh_chart(self, canvas, symbol, timeframe, candles_num):
        try:
            candles_num = int(candles_num)  # Convert to integer
            data = load_candlestick_data(symbol, timeframe, candles_num)
            canvas.figure.clf()  # Clear the figure
            fig, ax = self.create_chart(data)
            canvas.figure = fig
            canvas.draw()
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
        except RuntimeError as re:
            logger.error(f"Runtime error: {re}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")