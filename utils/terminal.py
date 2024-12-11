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

        self.auto_refresh = False  # Flag to track auto-refresh state
        self.refresh_interval = 120  # Default refresh interval in seconds

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
        symbol_entry.insert(0, "BTCUSD")  # Default value

        tk.Label(self.root, text="Timeframe: ").grid(row=1, column=0, sticky=tk.W)
        timeframe_entry = tk.Entry(self.root)
        timeframe_entry.grid(row=1, column=1, sticky=tk.W)
        timeframe_entry.insert(0, "M30")  # Default value

        tk.Label(self.root, text="Number of candles: ").grid(row=2, column=0, sticky=tk.W)
        candles_num_entry = tk.Entry(self.root)
        candles_num_entry.grid(row=2, column=1, sticky=tk.W)
        candles_num_entry.insert(0, "100")  # Default value

        tk.Label(self.root, text="Refresh Interval (seconds):").grid(row=3, column=0, sticky=tk.W)
        refresh_interval_entry = tk.Entry(self.root)
        refresh_interval_entry.grid(row=3, column=1, sticky=tk.W)
        refresh_interval_entry.insert(0, str(self.refresh_interval))  # Default value

        # Initial dummy chart
        dummy_data = load_candlestick_data()  # Load candlestick data with default data
        fig, ax = self.create_chart(dummy_data)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_title(f"BTCUSD - 100 candles (M30)")  # Set the title for the chart with default settings

        # Canvas for the chart
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, sticky="nsew")

        # Toolbar frame
        toolbar_frame = tk.Frame(self.root)
        toolbar_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()

        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Load button
        def on_load():
            symbol = symbol_entry.get()
            timeframe = timeframe_entry.get()
            candles_num = candles_num_entry.get()
            self.refresh_chart(symbol, timeframe, candles_num)

        load_button = tk.Button(self.root, text="Load Data", command=on_load)
        load_button.grid(row=6, column=0, columnspan=2)

        # Auto-refresh toggle button
        def toggle_auto_refresh():
            self.auto_refresh = not self.auto_refresh  # Toggle the flag
            if self.auto_refresh:
                try:
                    self.refresh_interval = int(refresh_interval_entry.get())
                    logger.info(f"Auto-refresh enabled with interval: {self.refresh_interval} seconds")
                    auto_refresh_button.config(text="Stop Auto-Refresh")
                    symbol = symbol_entry.get()
                    timeframe = timeframe_entry.get()
                    candles_num = candles_num_entry.get()
                    self.schedule_refresh(symbol, timeframe, candles_num)
                except ValueError:
                    logger.error("Invalid refresh interval")
                    self.auto_refresh = False  # Disable auto-refresh if there's an error
            else:
                logger.info("Auto-refresh disabled")
                auto_refresh_button.config(text="Start Auto-Refresh")

        auto_refresh_button = tk.Button(self.root, text="Start Auto-Refresh", command=toggle_auto_refresh)
        auto_refresh_button.grid(row=7, column=0, columnspan=2)

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
            self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, sticky="nsew")

            # Add the new toolbar
            toolbar_frame = tk.Frame(self.root)
            toolbar_frame.grid(row=5, column=0, columnspan=2, sticky="nsew")
            self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
            self.toolbar.update()

            ax.grid(True, linestyle='--', alpha=0.5)
            ax.set_title(f"{symbol} - {candles_num} candles ({timeframe})")

            logger.info(f"Successfully updated chart for {symbol}, {candles_num} candles ({timeframe})")
        except ValueError as ve:
            logger.error(f"Validation error: {ve}")
        except RuntimeError as re:
            logger.error(f"Runtime error: {re}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    def schedule_refresh(self, symbol, timeframe, candles_num):
        if self.auto_refresh:
            self.refresh_chart(symbol, timeframe, candles_num)
            # Schedule the next refresh
            self.root.after(self.refresh_interval * 1000, lambda: self.schedule_refresh(symbol, timeframe, candles_num))
