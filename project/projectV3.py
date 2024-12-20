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






# If CSV data exists already, return it. Else run a function to get it from Alpaca.
# def get_data(ticker, timeframe):
#     # create csv var named ticker_timetrame.csv
#     csv_file = os.path.join(HIST_DATA_DIR, f"{ticker}_{timeframe}.csv")
#     # search historical data directory for that file. If it exists, return it. Else run the get alpaca data function.
#     if os.path.exists(csv_file):
#         return pd.read_csv(csv_file) # Prob need to do this later, pd.read_csv(filepath, index_col="timestamp", parse_dates=True)
#     else:
#         alpaca_data = get_alpaca_data(ticker, timeframe)
#         alpaca_data.to_csv(csv_file)
#         return alpaca_data


# # Get Alpaca data function. 
# def get_alpaca_data(ticker):
#     # Get weekly, daily, 4hr, and 1hr data. Max timeframe, candlestick or OHLC data.
#     now = datetime.now(ZoneInfo("America/New_York"))
#     tf_dict = {
#         "1-Hour": [TimeFrameUnit.Hour, 1],
#         "4-Hour": [TimeFrameUnit.Hour, 4],
#         "Daily": [TimeFrameUnit.Day, 1],
#         "Weekly": [TimeFrameUnit.Week, 1],
#     }

#     # Loop through data collection for each timeframe.
#     for tf in tf_dict:
#         request = StockBarsRequest(
#             symbol_or_symbols = [ticker],
#             # TFU can be Hour, Day, Week, Month. Use amount = 4 for 4hr timeframe, 1 for day and week.
#             timeframe = TimeFrame(amount=tf_dict[tf][1], unit=tf_dict[tf][0]),
#             start = now - timedelta(days=1827), # specify start datetime, default=the beginning of the current day.
#             # end_date=None, # specify end datetime, default=now
#             limit = 5, # specify number of data points
#         )
#         return hist_data_client.get_stock_bars(request).df


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
