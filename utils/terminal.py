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

        # Close program function
        def on_close():
            sys.exit() # Exit the script
        # Handle the close event
        root.protocol("WM_DELETE_WINDOW", on_close)

        # User inputs
        tk.Label(root, text="Symbol:").grid(row=0, column=0, sticky=tk.W)
        symbol_entry = tk.Entry(root)
        symbol_entry.grid(row=0, column=1, sticky=tk.W)

        tk.Label(root, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W)
        start_date_entry = tk.Entry(root)
        start_date_entry.grid(row=1, column=1, sticky=tk.W)

        tk.Label(root, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, sticky=tk.W)
        end_date_entry = tk.Entry(root)
        end_date_entry.grid(row=2, column=1, sticky=tk.W)

        # Initial dummy chart
        dummy_data = pd.DataFrame({
            "Open": [1, 2, 3],
            "High": [2, 3, 4],
            "Low": [0.5, 1.5, 2.5],
            "Close": [1.5, 2.5, 3.5]
        }, index=pd.date_range(start="2023-01-01", periods=3))
        fig, ax = self.create_chart(dummy_data)

        # Canvas for the chart
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().grid(row=3, column=0, columnspan=2)

        # Load button
        def on_load():
            symbol = symbol_entry.get()
            start_date = start_date_entry.get()
            end_date = end_date_entry.get()
            # script_path = "strategy_line.py"  # Replace with dynamic selection if needed
            self.refresh_chart(canvas, symbol, start_date, end_date)

        load_button = tk.Button(root, text="Load Data", command=on_load)
        load_button.grid(row=4, column=0, columnspan=2)

        root.mainloop()

    # Chart creation function
    def create_chart(self, data):
        fig, ax = mpf.plot(data, type='candle', returnfig=True)
        return fig, ax
    
    # Refresh chart
    def refresh_chart(self, canvas, symbol, start_date, end_date):
        try:
            data = load_candlestick_data(symbol, start_date, end_date)
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return

        canvas.figure.clf()
        fig, ax = self.create_chart(data)
        # load_strategy(script_path, data, ax)
        canvas.figure = fig
        canvas.draw()