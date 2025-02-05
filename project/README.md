# MultiFrame Trader

Technical analysis backtesting tool inspired by John Carter's anchor squeeze setup.

## Table of Contents

- [MultiFrame Trader](#multiframe-trader)
  - [Table of Contents](#table-of-contents)
  - [Video Demo](#video-demo)
  - [About MultiFrame Trader](#about-multiframe-trader)
    - [Why](#why)
    - [What](#what)
    - [Challenges](#challenges)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Running the program](#running-the-program)
      - [Valid ticker request](#valid-ticker-request)
      - [Invalid ticker request](#invalid-ticker-request)
      - [CSV file heirarchy](#csv-file-heirarchy)
      - [Charts](#charts)
      - [Exit command](#exit-command)
      - [Warning message](#warning-message)
    - [Trading Strategy](#trading-strategy)
    - [Indicator Definitions and Explanations](#indicator-definitions-and-explanations)
    - [Future Features](#future-features)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)
  - [Acknowledgements](#acknowledgements)

## Video Demo

  https://www.youtube.com/watch?v=s-9rFnCUGao

## About MultiFrame Trader

### Why

This is my final project for Harvard's CS50P class. I built it to challenge my current knowledge, level up my skillset, and showcase my talents to the world. This project was at the intersection of things I'm interested in (data science/analysis, finance), skills that I've recently aquired (OOP, list comps, generators, file I/O, etc), and a problem I actually wanted solved (backtesting a multi timeframe trading strategy).

### What

MultiFrame Trader is a stock backtesting tool that employs a suite of indicators to analyze stock data. It currently consists of one strategy that was inspired by John Carter's squeeze indicator, but ties in indicators across multiple timeframes to potentially lower the risk to put on a trade. Aligning multiple timeframes can also lead to more explosive volatility, presumably in the direction of whatever trade one may have placed. 

### Challenges

Oh my, there were plenty! Frankly, I think I bit off a bit more than I could chew. The good news is that I was eventually able to overcome all the bugs, tracebacks, and design challenges that I ran into, and learned countless new skills and best practices, albeit by spending way more time than I originally budgeted. Some specific issues I encountered and now know how to solve are:
- Saving API keys in a separate file before pushing your code to Github (seems obvious in hindsight).
- Thoroughly researching libraries for desired functionality before using them. I made the mistake of writing a substantial amount of code with matplotlib only to find out the interactivity I wanted would be achieved easier using Plotly. I also did this with yfinance and switched to Alpaca for futureproofing.
- Creating the code to produce an indicator that read other indicator's values at specific timestamps across a dictionary of dataframes, performed logic using those values, created a new column and value in each of those dataframes, and then created another value based on whether those previous values across specific timestamps were all true. This was the Anchor class, and it taught me about generator expressions.
- Processing data correctly so it has the correct datatypes and values before methods to manipulate it. I ran into an issue in the plot method where my logic wasn't ordered correctly and I was trying to perform actions on dataframes that I thought I had indexed, only to find out they actually had a multi index. My takeaway is to constantly check datatypes to make sure my data is structured correctly.
- Writing unit tests for functions that contained API calls and other dependent variables was new to me. I learned all about mocking constants, variables, and exceptions. One lesson in particular was learning to mock and raise an exception in order to break a loop in the main function. Mocking a return value to break the loop didn't work in this case.

## Installation

You will need an API key from Alpaca Markets, as well as the following dependencies:

1. Get a free API Key at [https://alpaca.markets/](https://alpaca.markets/)
2. Clone the repo
   ```sh
   git clone https://github.com/houghae/CS50P.git
   cd CS50P
   ```
3. Setup a virtual environment
    ```sh
    # For Linux and Mac
    python -m venv venv
    source venv/bin/activate

    # For Windows
    venv\Scripts\activate
    ```
4. Install dependencies
   ```sh
   pip install -r project/requirements.txt
   ```
5. Create a `.env` file and add your API keys
   ```sh
   echo -e "ALPACA_API_KEY=your_api_key_here\nALPACA_API_SECRET=your_secret_key_here" > .env
   ```

## Usage

### Running the program

```sh
cd project
python project.py 
```
- MultiFrame Trader will prompt the user for a stock ticker symbol. It will then validate you input against Alpaca's list of valid tickers. If it's not found it will prompt you again.

#### Valid ticker request

> ![Screenshot of the intro to MultiFrame Trader.](<screenshots/Screenshot from 2025-02-04 16-42-52.png>)

#### Invalid ticker request

> ![Screenshot of invalid ticker response.](<screenshots/Screenshot from 2025-02-05 08-37-40.png>)

- If this is the first time running the program, it'll fetch historical data from the Alpaca API. It will then create a ```historical_data``` directory within the project directory and store the data in four CSV files labeled ```{your_ticker}_{timeframe}.csv```. 

#### CSV file heirarchy

> ![Screenshot of CSV file heirarchy.](<screenshots/Screenshot from 2025-02-05 08-46-52.png>)

- If you've ran the program with for a particular valid ticker before, it will first search the ```historical_data``` directory for the csv files.
- Next, it will open a web browser window and populate it with four timeframes of candlestick charts, and multiple technical indicators. All charts are interactive with panning and zooming capabilities. 

#### Charts

> ![Screenshot of QQQ charts in web browser.](<screenshots/Screenshot from 2025-02-04 17-11-35.png>)

> ![Screenshot of weekly price chart, zoomed in.](<screenshots/Screenshot from 2025-02-04 17-14-46.png>)

- There are a suite of icons in the upper right corner to assist with the interactivity. You can also click and drag the slider under the price chart or click and drag a zoom window on the chart itself. The price charts have a tooltip that shows up whenever you hover over a candlestick. It allows you to see the open, high , low, and close of the bar.
- Once finished with the charts, you may close the window or just go back to the terminal where you will be prompted for another ticker. When finished type ```exit```. 

#### Exit command

> ![Screenshot of the exit command in terminal.](<screenshots/Screenshot from 2025-02-04 16-44-16.png>)

> [!IMPORTANT]
> A potential issue you may run into with heavy usage is an API call limit. I haven't had this problem yet, but I assume at some point the Alpaca API may throttle your calls and it could throw an error.
>
> Also, there is a message that gets thrown in the terminal whenever you enter a ticker. It's a warning that a specific module isn't installed and can be safely ignored.

#### Warning message

> ![Screenshot of warning message to disregard.](<screenshots/Screenshot from 2025-02-04 16-43-44.png>)

### Trading Strategy

The trading strategy for this program is based off of an indicator created by a trader named John Carter who founded Simpler Trading. The indicator is called the "Squeeze" and is a breakout momentum indicator. While working admirably on it's own, it really shines when coupled with multiple timeframes and at least one other directional indicator. This program does exactly that. 

MultiFrame Trader plots a 1 hour, 4 hour, daily, and weekly candlestick chart. Below that it plots:
- A slider to zoom in on the price action.
- The squeeze indicator shown in red and green dots. This tells whether the squeeze has fired or not.
- The squeeze histogram shown in green and red. This shows whether the squeeze fires in a positive or negative direction.
- The wave histogram shown in blue and purple. This compliments/confirms the squeeze histogram.

### Indicator Definitions and Explanations

The following indicators are used in this strategy:
- Simple Moving Average(SMA)
    - The SMA calculates the average price over a specified period of time.
        - SMA = sum of n periods of closing price / n periods
- Exponential Moving Average (EMA)
    - The EMA is a moving average that places a greater weight and significance on the most recent data points.
        - EMA = closing price x multiplier + EMA (previous day) x (1-multiplier)
- Average True Range (ATR)
    - The true range indicator is taken as the greatest of the following: current high less the current low; the absolute value of the current high less the previous close; and the absolute value of the current low less the previous close. The ATR is then a moving average of the true ranges.
        - TR = Max [(H−L), ∣H−C<sub>p</sub>∣, ∣L−C<sub>p</sub>∣]
        - ATR = Previous ATR(n−1)+TR/n
        - where: n=Number of periods, TR=True range
    - When a previous ATR is not available, ATR is calculated this way:
        - (1/n)(sum of TRs in a given period, n)
- Standard Deviation (STD_DEV)
    - Standard deviation is a way to see how far individual points in a dataset are from the mean of the set.
        - STD_DEV is calculated with the std() method in pandas.
- Bollinger Bands (BB)
    - BB creates a price channel with midline. The midline is a 20 period SMA. The upper and lower channels are 2 STD_DEV from the midline.
- Keltner Channels(KC)
    - KC is a channel made up of 2 bands set to 1.5 times the ATR above and below the 20 day EMA.
- Squeeze
    - The squeeze is made up of BB and KC. When BB is inside KC, the market typically has low volatility. When BB expands outside of KC the market typically has a rush of volatility. The switch of the bands indicates a squeeze trade signal. The green dot signals the potential start of high volatility, and the histogram signals the direction of volatility.
- Moving Average Convergence Divergence (MACD)
    - The MACD line is calculated by subtracting a 26 period EMA from a 12 period EMA. There is also a signal line (9 period EMA) plotted against the MACD line. The subtraction of the signal from the MACD creates a histogram that shows momentum and entry/exit points. This is called the MACD Wave. The wave reversal from negative to positive can be useful to time big moves in the asset when being used in conjunction with the squeeze.
- Anchor
    - The anchor indicator ties everything together. This indicator fires a black dot on the high of the candlestick when all four timeframes have a squeeze that fires long. Lining up multiple timeframes provides the potential for an extremely explosive move that can last for a longer time period. By aligning all the timeframes in the same direction, you derisk the trade and increase potential profits. 

> [!CAUTION]
> A word of caution. I am not a financial advisor. Don't rely on this for financial advice. DO YOUR OWN RESEARCH on whether this strategy works for you. ALWAYS BACKTEST WITH PAPER MONEY FIRST.
​
### Future Features

These are some features I'd like to build into the second version when time permits.
- Figure out how to fit the price action vertically to the plot window.
- run a performance test that returns a win ratio, trade frequency, and avg return per trade.
    - Avg return per trade will be based on daily open price after squeeze fires on all 4 timeframes. Exit will be when price crosses the BB midpoint.
- Output call to action. Buy, sell, or wait.
- Expand to using streaming data for realtime trading.
- Consider tying in to Alpaca's trading platform so I could execute trades within the program.

## Contributing

Contributions are welcome and appreciated! To contribute:

1. Fork the repository
2. Create a branch: `git checkout -b feature-branch`
3. Commit your changes: `git commit -m "Add new feature"`
4. Push the branch: `git push origin feature-branch`
5. Submit a Pull Request 

## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.

## Contact

Arthur Hough
- [Github](https://github.com/houghae)
- [Linkedin](https://www.linkedin.com/in/arthurhough/)

## Acknowledgements

I’d like to acknowledge the following for their inspiration and resources that helped me build this project:

- [Simpler Trading/John Carter](https://www.simplertrading.com/) - Inspiration for the trading strategy.
- [ThinkOrSwim](https://toslc.thinkorswim.com/center/reference/Tech-Indicators/studies-library/T-U/TTM-Squeeze) - For defining indicators.
- [Investopedia](https://www.investopedia.com/terms/s/sma.asp) - Also for defining indicators.
- [Jon Krohn](https://github.com/jonkrohn/ML-foundations/) - Jon's ML Foundations videos and notebooks were extremely helpful in learning to work with Pandas DataFrames and ML basics in general.
- [FreeCodeCamp](https://www.freecodecamp.org/) - Countless free resources for all kinds of programming related stuff, like [this one](https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/) I used to construct this readme.
- [CS50P](https://cs50.harvard.edu/python/2022/) - This class was instrumental to me learning Python. I can't begin to express my graditude for David Malan and team.

[**Back to top**](#multiframe-trader)
