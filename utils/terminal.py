import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import mplfinance as mpf
import matplotlib.pyplot as plt
from utils.mt5 import load_candlestick_data
import logging

logger = logging.getLogger("main")  # Get global logger "main.log" from main.py


class Terminal:
    def __init__(self):
        logger.info("Initializing Terminal...")
        self.canvas = None
        self.toolbar = None
        self.root = None

    def start(self):
        self.root = tk.Tk()
        self.root.title("Trading Terminal")
        self.root.state("zoomed")

        # Close program function
        def on_close():
            quit()

        self.root.protocol("WM_DELETE_WINDOW", on_close)

        # User inputs
        tk.Label(self.root, text="Symbol:").grid(row=0, column=0, sticky=tk.W)
        symbol_entry = tk.Entry(self.root)
        symbol_entry.grid(row=0, column=1, sticky=tk.W)

        tk.Label(self.root, text="Timeframe: ").grid(row=1, column=0, sticky=tk.W)
        timeframe_entry = tk.Entry(self.root)
        timeframe_entry.grid(row=1, column=1, sticky=tk.W)

        tk.Label(self.root, text="Number of candles: ").grid(row=2, column=0, sticky=tk.W)
        candles_num_entry = tk.Entry(self.root)
        candles_num_entry.grid(row=2, column=1, sticky=tk.W)

        # Initial dummy chart
        dummy_data = load_candlestick_data()  # Load candlestick data with default data
        fig, ax = self.create_chart(dummy_data)
        ax.set_title(f"BTCUSD - 100 candles (M30)")

        # Canvas for the chart
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, sticky="nsew")

        # Toolbar frame
        toolbar_frame = tk.Frame(self.root)
        toolbar_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()

        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Load button
        def on_load():
            symbol = symbol_entry.get()
            timeframe = timeframe_entry.get()
            candles_num = candles_num_entry.get()
            self.refresh_chart(symbol, timeframe, candles_num)

        load_button = tk.Button(self.root, text="Load Data", command=on_load)
        load_button.grid(row=5, column=0, columnspan=2)

        self.root.mainloop()

    def create_chart(self, data):
        fig, ax = plt.subplots(figsize=(12, 6))

        # Create candlestick chart
        mpf.plot(
            data,
            type="candle",
            ax=ax,
            style="yahoo",
            show_nontrading=False,  # Skip days with no data
        )
        return fig, ax

    def refresh_chart(self, symbol, timeframe, candles_num):
        try:
            candles_num = int(candles_num)  # Convert to integer
            data = load_candlestick_data(symbol, timeframe, candles_num)  # Load new data

            # Create a new figure and chart
            fig, ax = self.create_chart(data)

            # Destroy the existing canvas and toolbar
            if hasattr(self, "canvas"):
                self.canvas.get_tk_widget().destroy()
            if hasattr(self, "toolbar"):
                self.toolbar.destroy()

            # Add the new canvas
            self.canvas = FigureCanvasTkAgg(fig, master=self.root)
            self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, sticky="nsew")

            # Add the new toolbar
            toolbar_frame = tk.Frame(self.root)
            toolbar_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")
            self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
            self.toolbar.update()

            ax.set_title(f"{symbol} - {candles_num} candles ({timeframe})")

            logger.info(f"Successfully updated chart for {symbol}, {candles_num} candles ({timeframe})")
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
        except RuntimeError as re:
            logger.error(f"Runtime error: {re}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
