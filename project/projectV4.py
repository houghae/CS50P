# Dependencies.
# Use matplotlib for charts, mplfinance is a specific module for charting stocks.
# Use Alpaca for stock data. Arguably more robust than yfinance.
# Use pandas for data handling and I/O. pandas is used heavily for data analysis.
# Use os to create dir
import matplotlib
import matplotlib.pyplot as plt
import tkinter
import mplfinance as mpf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from alpaca.data import StockHistoricalDataClient
from alpaca.trading.client import TradingClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
import sys

# This uses tKinter backend for visuals. Should be able to use this for scrollable figures as well.
matplotlib.use("TkAgg")

# Alpaca trading keys and client.
# Paper trading key only.
# Capitalize vars that are constants, like API keys and dir paths.
# Load environment variables b/c this is best practice. Never hard code keys into codebase.

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
API_SECRET = os.getenv("ALPACA_API_SECRET")

hist_data_client = StockHistoricalDataClient(API_KEY, API_SECRET)
trade_client = TradingClient(API_KEY, API_SECRET)

# Create file path for CSV storage in case there isn't yet a dir. Path is relative to the program's location.
# This enables portability and makes the code more robust if I share it.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HIST_DATA_DIR = os.path.join(BASE_DIR, "historical_data")
os.makedirs(HIST_DATA_DIR, exist_ok=True)


# Prerequisite defs:
# Simple moving avg (SMA): The SMA Calculates the avg price over a specified period of time.

# Exponential moving avg (EMA): Siimilar to the SMA but weights more recent price action more heavily. The EMA is a moving average that places a greater weight and significance on the most recent data points. EMA = Closing price x multiplier + EMA (previous day) x (1-multiplier).

# Avg true range (ATR): The true range indicator is taken as the greatest of the following: current high less the current low; the absolute value of the current high less the previous close; and the absolute value of the current low less the previous close. The ATR is then a moving average, generally using 14 days, of the true ranges.

# Bollinger bands (BB): BB is typically made up of a 20 day SMA and 2 std dev lines that create a channel.

# Keltner channels (KC): KC is a channel made up of 2 bands typically set to twice the ATR above and below the 20 day EMA.

# Squeeze indicator (SQ): SQ is made up of BB and KC. When BB is inside KC, the market typically has low volatility. When BB expands outside of KC the market typically has a rush of volatility. The switch of the bands indicates a squeeze trade signal.

# MACD indicator (MACD): MACD is the moving average convergence divergence indicator. The MACD line is calculated by subtracting a 26 period EMA from a 12 period EMA. There is also a signal line (9 period EMA) plotted against the MACD line. The subtraction of the signal from the MACD can create a histogram that shows momentum and entry/exit points. This is called the MACD Wave.


# Parent class
class Indicator:
    def __init__(self, df):
        self.df = df


class SMA(Indicator):
    def __init__(self, df, period):
        super().__init__(df)
        self.period = period

    # Calculation: sum of all closing prices in n periods, divided by n.
    def calc(self):
        sma_column = f"SMA {self.period}"
        self.df[sma_column] = self.df["close"].rolling(window=self.period).mean()


class EMA(Indicator):
    def __init__(self, df, period):
        super().__init__(df)
        self.period = period

    # Calculation: Closing price x multiplier + EMA (previous day) x (1-multiplier).
    # Use pandas ewm method. Must calculate from newest to oldest price action.
    def calc(self):
        ema_column = f"EMA {self.period}"
        self.df[ema_column] = (
            self.df["close"].ewm(span=self.period, adjust=False).mean()
        )


class ATR(Indicator):
    def __init__(self, df, period):
        super().__init__(df)
        self.period = period

    # TR Calc: max[(H-L), abs(H-prev close), abs(L-prev close)]
    # FYI: This calc is better for historical data.
    def tr_calc(self):
        # self.df["tr"] = self.df[["high", "low", "close"]].apply(
        #     lambda row: max(row["high"] - row["low"],
        #                     abs(row["high"] - row["close"].shift(1)),
        #                     abs(row["low"] - row["close"].shift(1))),
        #                     axis=1
        # )

        h_l_diff = self.df["high"] - self.df["low"]
        h_prev_close_diff = abs(self.df["high"] - self.df["close"].shift(1))
        l_prev_close_diff = abs(self.df["low"] - self.df["close"].shift(1))

        self.df["TR"] = pd.concat(
            [h_l_diff, h_prev_close_diff, l_prev_close_diff], axis=1
        ).max(axis=1)

        self.df[f"ATR {self.period}"] = self.df["TR"].rolling(window=self.period).mean()

    # Calculation: Calculate the EMA of the TR.
    # FYI: This calc is better for live data, if I use that in the future.
    def calc(self):
        # Must calc tr first.
        self.tr_calc()
        atr_column = f"ATR {self.period}"
        self.df[atr_column] = self.df["TR"].ewm(span=self.period, adjust=False).mean()


class STD_DEV(Indicator):
    def __init__(self, df, period):
        super().__init__(df)
        self.period = period

    # Calculation: run std method on the period of closing prices.
    def calc(self):
        std_dev_column = f"Std Dev {self.period}"
        self.df[std_dev_column] = self.df["close"].rolling(window=self.period).std()


class BB(Indicator):
    def __init__(self, df, period):
        super().__init__(df)
        self.period = period

    # Calculation: centerline is SMA, channels are 2 std dev above and below SMA.
    def calc(self):
        sma = SMA(self.df, self.period)
        std_dev = STD_DEV(self.df, self.period)
        sma.calc()
        std_dev.calc()

        sma_column = f"SMA {self.period}"
        std_dev_column = f"Std Dev {self.period}"

        self.df["Upper BB"] = self.df[sma_column] + (2 * self.df[std_dev_column])
        self.df["Lower BB"] = self.df[sma_column] - (2 * self.df[std_dev_column])


class KC(Indicator):
    def __init__(self, df, period):
        super().__init__(df)
        self.period = period

    # Calculation: centerline is EMA, channels are 2 ATR above and below SMA.
    def calc(self):
        ema = EMA(self.df, self.period)
        atr = ATR(self.df, self.period)
        ema.calc()
        atr.calc()

        # For readability I'm creating these variables for use in the calculation below.
        # Alternatively, I could use the f-string in the df calculation itself which would sacrifice readability for two less lines of code.
        ema_column = f"EMA {self.period}"
        atr_column = f"ATR {self.period}"

        self.df["Upper KC"] = self.df[ema_column] + (1.5 * self.df[atr_column])
        self.df["Lower KC"] = self.df[ema_column] - (1.5 * self.df[atr_column])


class Squeeze(Indicator):
    def __init__(self, df):
        super().__init__(df)

    # Calculation: Squeeze fired when both bb close outside of both kc. This calc should return a boolean.
    # Histogram: Delta between 20 SMA and 80 SMA. Delta less or greater than 20 ATR. Delta less than ATR indicates potetial for squeeze. Delta above or below zero line indicates buy or sell.
    def calc(self):
        bb = BB(self.df, 20)
        kc = KC(self.df, 20)
        bb.calc()
        kc.calc()
        fast_sma = SMA(self.df, 20)
        slow_sma = SMA(self.df, 80)
        squeeze_atr = ATR(self.df, 20)
        fast_sma.calc()
        slow_sma.calc()
        squeeze_atr.calc()

        self.df["Squeeze Fired"] = (self.df["Lower BB"] < self.df["Lower KC"]) & (
            self.df["Upper BB"] > self.df["Upper KC"]
        )
        self.df["Sqz Delta"] = self.df["SMA 20"] - self.df["SMA 80"]
        self.df["Sqz Hist"] = self.df["Sqz Delta"] - self.df["ATR 20"]


class MACD(Indicator):
    def __init__(self, df):
        super().__init__(df)

    # Moving average convergence divergence. This is the difference between a fast EMA (12), and a slow EMA (26).

    def calc(self):
        fast_ema = EMA(self.df, 12)
        slow_ema = EMA(self.df, 26)
        fast_ema.calc()
        slow_ema.calc()

        self.df["MACD"] = self.df["EMA 12"] - self.df["EMA 26"]
        self.df["MACD Signal"] = self.df["MACD"].ewm(span=9, adjust=False).mean()
        # Appends a float to create a histogram that can show momentum. I think this is what John Carter calls the wave.
        self.df["MACD Wave"] = self.df["MACD"] - self.df["MACD Signal"]


class Anchor_Plot:
    def __init__(self, data_dict, ticker):
        self.data_dict = data_dict
        self.ticker = ticker

    def plot(self):
        # Create anchor figure. 3 rows, 4 columns.
        fig = make_subplots(
            rows=4,
            cols=4,
            shared_xaxes=True,
            subplot_titles=[f"{tf_name} - Price" for tf_name in self.data_dict.keys()] +
                           [f"{tf_name} - Squeeze" for tf_name in self.data_dict.keys()] +
                           [f"{tf_name} - Squeeze Histogram" for tf_name in self.data_dict.keys()] +
                           [f"{tf_name} - Wave" for tf_name in self.data_dict.keys()],
            vertical_spacing=0.06,
            row_heights=[2, .08, 1, .7],
        )

        # Loop through each tf and plot 3 rows, 1 column.
        for i, (_, df) in enumerate(self.data_dict.items(), start=1):
            df = df.reset_index().set_index("timestamp")
            df.index = pd.to_datetime(df.index)

            # Instantiate and calculate squeeze and MACD wave
            squeeze = Squeeze(df)
            squeeze.calc()
            macd = MACD(df)
            macd.calc()

            # Plot price as candles
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"],
                    name="Price",
                ),
                row=1,
                col=i,
            )

            # Plot squeeze
            squeeze_colors = ["green" if i is True else "red" for i in df["Squeeze Fired"]]
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["Squeeze Fired"],
                    name="Squeeze",
                    marker_color=squeeze_colors,
                    mode="markers",
                    marker_size=5,
                ),
                row=2,
                col=i,
            )

            # Plot squeeze histogram
            squeeze_hist_colors = ["green" if i >= 0 else "red" for i in df["Sqz Hist"]]
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df["Sqz Hist"],
                    marker_color=squeeze_hist_colors,
                ),
                row=3,
                col=i,
            )

            # Plot wave, first create color variable
            macd_colors = ["teal" if i >= 0 else "purple" for i in df["MACD Wave"]]
            fig.add_trace(
                go.Bar(
                    x=df.index,
                    y=df["MACD Wave"],
                    name="MACD Wave",
                    marker_color=macd_colors,
                ),
                row=4,
                col=i,
            )

        fig.update_layout(
            height=950,
            width=1800,
            title_text=f"{self.ticker} Anchor Timeframes",
            showlegend=False,
            margin=dict(l=30, r=30, t=40, b=30),
            hovermode="x unified",
            xaxis=dict(showspikes=True, spikemode="across")
        )
        fig.update_xaxes(rangeslider=dict(visible=True, thickness=0.02), row=1, col=1)
        fig.update_xaxes(rangeslider=dict(visible=True, thickness=0.02), row=1, col=2)
        fig.update_xaxes(rangeslider=dict(visible=True, thickness=0.02), row=1, col=3)
        fig.update_xaxes(rangeslider=dict(visible=True, thickness=0.02), row=1, col=4)
        fig.update_yaxes(tickvals=[], row=2, col=1)
        fig.update_yaxes(tickvals=[], row=2, col=2)
        fig.update_yaxes(tickvals=[], row=2, col=3)
        fig.update_yaxes(tickvals=[], row=2, col=4)
        fig.show()



# Multi timeframe plotting class - MATPLOTLIB. Hard to make interactive
# class Anchor_Plot():
#     def __init__(self, data_dict, ticker):
#         self.data_dict = data_dict
#         self.ticker = ticker

#     # Plot 4 timeframes with squeeze, squeeze fired, MACD wave, and buy/sell indicators.
#     def plot(self):
#         tf_qty = len(self.data_dict)
#         fig, axes = plt.subplots(3, tf_qty, figsize=(19, 8))
#         fig.suptitle(f"{self.ticker} Anchor Charts")

#         for index, (tf_name, df) in enumerate(self.data_dict.items()):
#             ax_price = axes[0, index]
#             ax_squeeze = axes[1, index]
#             ax_wave = axes[2, index]
#             ax_price.set_title(f"{tf_name} Timeframe")
#             ax_squeeze.set_title(f"{tf_name} Squeeze")
#             ax_wave.set_title(f"{tf_name} Wave")

#             # Check for empty dataframes
#             if not df.empty:
#                 # This flattens the multi index data from Alpaca, which is ticker and timestamp.
#                 df = df.reset_index()
#                 # This resets the index so the plots aren't indexed by the ticker.
#                 df = df.set_index("timestamp")
#                 df.index = pd.to_datetime(df.index)

#                 # Instantiate and calculate squeeze and MACD wave
#                 squeeze = Squeeze(df)
#                 squeeze.calc()
#                 macd = MACD(df)
#                 macd.calc()

#                 # Plot price action
#                 mpf.plot(df, ax=ax_price, type="candle", style="yahoo", show_nontrading=True)

#                 # Plot squeeze histogram and squeeze fired indicator.
#                 squeeze_fired = df["Squeeze Fired"]
#                 ax_squeeze.scatter(df.index[squeeze_fired], df["close"][squeeze_fired], color="lightgreen", label="Squeeze Fired", s=10)

#                 # Plot MACD wave.
#                 macd_wave = df["MACD Wave"]
#                 macd_colors = ["teal" if x >= 0 else "purple" for x in macd_wave]
#                 ax_wave.bar(df.index, macd_wave, color=macd_colors, label="MACD Wave")

#             else:
#                 # Return some message about an empty dataframe.
#                 ax_price.text(0.5, 0.5, f"No data for {tf_name}", fontsize=12, ha="center", va="center", transform=ax_price.transAxes)

#         plt.tight_layout()
#         plt.subplots_adjust(top=0.95)
#         plt.show()


def get_data(ticker):
    now = datetime.now(ZoneInfo("America/New_York"))
    tf_dict = {
        "1-Hour": [TimeFrameUnit.Hour, 1],
        "4-Hour": [TimeFrameUnit.Hour, 4],
        "Daily": [TimeFrameUnit.Day, 1],
        "Weekly": [TimeFrameUnit.Week, 1],
    }

    data_dict = {}
    for tf_name, (tf_unit, tf_amount) in tf_dict.items():
        csv_file = os.path.join(HIST_DATA_DIR, f"{ticker}_{tf_name}.csv")
        if os.path.exists(csv_file):
            # print(f"Loading {tf_name} data for {ticker} from CSV...")
            data_dict[tf_name] = pd.read_csv(
                csv_file, index_col="timestamp", parse_dates=True
            )
        else:
            # print(f"Fetching {tf_name} data for {ticker} from Alpaca...")
            request = StockBarsRequest(
                symbol_or_symbols=[ticker],
                timeframe=TimeFrame(amount=tf_amount, unit=tf_unit),
                start=now - timedelta(days=1095),
                limit=1095,  # Pay attention to this. Too high might trigger an API call rate limit.
            )
            df = hist_data_client.get_stock_bars(request).df
            df.to_csv(csv_file)
            data_dict[tf_name] = df

    return data_dict


def user_input():
    # Create while loop to get input from user. Break if input is valid, else print error message and reprompt.
    while True:
        user_ticker = input("What ticker would you like to chart?\n").strip().upper()
        if validate_ticker(user_ticker):
            break
        elif user_ticker == "EXIT":
            print(
                "Exiting program...\nThis has been Arthur Hough's CS50P technical analysis asset tool. Cheers!\n"
            )
            sys.exit()
        else:
            print("Invalid ticker. Please enter a valid ticker symbol.\n")
    return user_ticker


def validate_ticker(ticker):
    # error handling: Use API to check whether asset is tradable.
    try:
        asset = trade_client.get_asset(ticker)
        if asset.tradable:
            return True
    except Exception:
        return False


def welcome():
    print("\nWelcome to Arthur Hough's CS50P technical analysis asset tool.\n")
    time.sleep(1)
    print(
        "This tool will prompt you for a ticker symbol, \nand then present a backtested trading strategy visualization along with an action recommendation."
    )
    # time.sleep(3)
    print("Whenever you'd like to exit the program, type EXIT.\n\nLet's get started!\n")


def run_strategy():
    while True:
        ticker = user_input()
        data_dict = get_data(ticker)
        anchor_plot = Anchor_Plot(data_dict, ticker)
        anchor_plot.plot()
        # run a performance test that returns a win ratio, trade frequency, and avg return per trade.
        # Avg return per trade will be based on daily open price after squeeze fires on all 4 timeframes. Exit will be when price crosses the BB midpoint.


def main():
    welcome()
    run_strategy()

    # Plot the data that was requested using the anchor visualization object.
    # Output call to action. Buy, sell, or wait.


if __name__ == "__main__":
    main()
