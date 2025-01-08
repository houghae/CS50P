# Dependencies.
# Use matplotlib for charts, mplfinance is a specific module for charting stocks.
# Use Alpaca for stock data. Arguably more robust than yfinance.
# Use pandas for data handling and I/O. pandas is used heavily for data analysis.
# Use os to create dir
import matplotlib.pyplot as plt
import mplfinance as mpf
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


# Classes for indicators
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
        sma_column = f"SMA_{self.period}"
        self.df[sma_column] = self.df["close"].rolling(window=self.period).mean()

class EMA(Indicator):
    def __init__(self, df, period):
        super().__init__(df)
        self.period = period
    
    # Calculation: Closing price x multiplier + EMA (previous day) x (1-multiplier). 
    # Use pandas ewm method. Must calculate from newest to oldest price action. 
    def calc(self):
        ema_column = f"EMA_{self.period}"
        self.df[ema_column] = self.df["close"].ewm(span=self.period, adjust=False).mean()

class ATR(Indicator):
    def __init__(self, df, period):
        super().__init__(df)
        self.period = period

    # TR Calc: max[(H-L), abs(H-prev close), abs(L-prev close)] 
    # FYI: This calc is better for historical data.
    def tr_calc(self):
        self.df["tr"] = self.df[["high", "low", "close"]].apply(
            lambda row: max(row["high"] - row["low"],
                            abs(row["high"] - row["close"].shift(1)),
                            abs(row["low"] - row["close"].shift(1))),
                            axis=1
        )
        self.df[f"ATR_{self.period}"] = self.df["tr"].rolling(window=self.period).mean()

    # Calculation: Calculate the EMA of the TR.
    # FYI: This calc is better for live data, if I use that in the future.
    def calc(self):
            # Must calc tr first.
            self.tr_calc()
            atr_column = f"ATR_{self.period}"
            self.df[atr_column] = self.df["tr"].ewm(span=self.period, adjust=False).mean()

class STD_DEV(Indicator):
    def __init__(self, df, period):
        super().__init__(df)
        self.period = period

    # Calculation: run std method on the period of closing prices.
    def calc(self):
        std_dev_column = f"std_dev_{self.period}"
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
        
        sma_column = f"SMA_{self.period}"
        std_dev_column = f"std_dev_{self.period}"

        self.df["upper_bb"] = self.df[sma_column] + (2 * self.df[std_dev_column])
        self.df["lower_bb"] = self.df[sma_column] - (2 * self.df[std_dev_column])

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
        ema_column = f"EMA_{self.period}"
        atr_column = f"ATR_{self.period}"

        self.df["upper_kc"] = self.df[ema_column] + (1.5 * self.df[atr_column])
        self.df["lower_kc"] = self.df[ema_column] - (1.5 * self.df[atr_column])

class Squeeze(Indicator):
    def __init__(self, df):
        super().__init__(df)
#        self.period = period # I don't think I need a period for this.

    # Calculation: Squeeze fired when both bb close outside of both kc. This calc should return a boolean.
    def calc(self):
        bb = BB(self.df, 20)
        kc = KC(self.df, 20)
        bb.calc()
        kc.calc()

        self.df["squeeze_fired"] = (self.df["lower_bb"] < self.df["lower_kc"]) & (self.df["upper_bb"] > self.df["upper_kc"])

class MACD(Indicator):
    def __init__(self, df):
        super().__init__(df)
    # Moving average convergence divergence. This is the difference between a fast EMA (12), and a slow EMA (26).

    def calc(self):
        fast_ema = EMA(self.df, 12)
        slow_ema = EMA(self.df, 26)
        signal_ema = EMA(self.df, 9)
        fast_ema.calc()
        slow_ema.calc()
        signal_ema.calc()
        
        self.df["MACD"] = self.df["EMA_12"] - self.df["EMA_26"]
        
        # Appends a boolean to easily see the cross, but doesn't show momentum.
        #self.df["MACD Signal Long"] = self.df["MACD"] > self.df["EMA_9"]

        # Appends a float to create a histogram that can show momentum. I think this is what John Carter calls the wave.
        self.df["MACD Wave"] = self.df["MACD"] - self.df["EMA_9"]


# Class for matplotlib visualization
# Plot multiple timeframe charts each with their own indicators.



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
            #print(f"Loading {tf_name} data for {ticker} from CSV...")
            data_dict[tf_name] = pd.read_csv(csv_file, index_col="timestamp", parse_dates=True)
        else:
            #print(f"Fetching {tf_name} data for {ticker} from Alpaca...")
            request = StockBarsRequest(
                symbol_or_symbols=[ticker],
                timeframe=TimeFrame(amount=tf_amount, unit=tf_unit),
                start=now - timedelta(days=1827),
                limit=365,  # Pay attention to this. Too high might trigger an API call rate limit.
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
            #print("Valid ticker. What else you got?")
            break
        elif user_ticker == "EXIT":
            print("Exiting program...\nThis has been Arthur Hough's CS50P technical analysis asset tool. Cheers!\n")
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
    print("This tool will prompt you for a ticker symbol, \nand then present a backtested trading strategy visualization along with an action recommendation.")
    #time.sleep(3)
    print("Whenever you'd like to exit the program, type EXIT.\n\nLet's get started!\n")


def main():
    welcome()
    while True:
        ticker = user_input()
        all_data_dict = get_data(ticker)


        # Plot the data that was requested using the anchor visualization object.

        # Output call to action. Buy, sell, or wait.



if __name__ == "__main__":
    main()
