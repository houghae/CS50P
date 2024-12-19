import yfinance as yf
import pandas as pd
import time

def main():
    #filters = user_query()
    #tickers = stock_screener(filters)
    #print(f"Selected tickers: {tickers}")
    get_user_tickers()


def user_query():
    # Welcome the user
    # Ask some questions about a preferred strategy and their goals. Leave room for 'I don't know'.
    # Store inputs for use in how the rest of the program will operate.
    print("Hi! Welcome to my CS50 investment tool. Let's go through a few questions to get a feel for how you'd like to invest. Ready?")
    time.sleep(5)
    user_tolerance = int(input("On a scale of 1-5, how risk tolerant are you? (1 being very risk adverse and 5 being very risk tolerant.)\n"))
    user_goal = input("What are your trading/investment goals?\n") # Consider using argparse to create multiple choice question.
    user_strategy = input("Do you have a preferred trading strategy?\n") # momentum, gap trade, std dev fade, breakout, etc.
    user_indicators = input("What indicators would you like to start with?\n") # MACD, bollinger bands, mov avg, std dev channel, etc.
    user_market = input("Do you prefer to trade trending or sideways markets?\n")
    return {"tolerance": user_tolerance, "goal": user_goal, "strategy": user_strategy, "indicators": user_indicators, "market": user_market}

def stock_screener(filters):
    # Start with multiple markets and narrow down potential tickers to explore based on user questions. 
    print("Running stock screener with the following filters:")
    for key, value in filters.items():
        print(f"{key}: {value}")
    return ["AAPL", "MSFT", "TSLA"]  # Example tickers



def get_data(tickers, period, interval):
    for ticker in get_user_tickers:
        yf.Ticker(ticker)
    #history = tickers.tickers[].history(period=period, interval=interval)
    



def get_user_tickers():
    user_tickers = input("Enter the tickers you'd like to research. Seperate each with a comma:\n")
    return [ticker.strip().upper() for ticker in user_tickers.split(",")]


def get_user_timeframe():
    user_period = input("What history period would you like to look at?\nYou can enter 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max:\n")
    user_interval = input("What interval would you like your chart?\nYou can enter 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo\n")
    return user_period, user_interval

if __name__ == "__main__":
    main()