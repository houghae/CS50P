import pytest
import pandas as pd
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import project
from project import (
    get_data,
    user_input,
    validate_ticker,
    run_strategy,
    Indicator,
    SMA,
    EMA,
    ATR,
    STD_DEV,
    BB,
    KC,
    Squeeze,
    MACD,
    Anchor,
    Anchor_Plot,
)

# Note about pytest: running pytest with the -s flag allows print statements to be shown for debugging.

# Mock constants
# Set up a fixture to reuse objects, @pytest.fixture. Could use this for indicators or maybe for API data or dataframes.
MOCK_TICKER = "QQQ"
MOCK_DATA = {
    "open": [100, 102, 104, 103, 105],
    "high": [102, 104, 106, 105, 107],
    "low": [99, 101, 103, 102, 104],
    "close": [101, 103, 105, 104, 106],
}
MOCK_DF = pd.DataFrame(MOCK_DATA, index=pd.date_range("2023-01-01", periods=len(MOCK_DATA["open"])))

# Use copy so each value is representing a unique df. This should make the test more robust in case there's an issue with one df but not all.
MOCK_DATA_DICT = {
    "1-Hour": MOCK_DF.copy(),
    "4-Hour": MOCK_DF.copy(),
    "Daily": MOCK_DF.copy(),
    "Weekly": MOCK_DF.copy(),
}

# Notes on mocking:
# The patch decorator tells pytest the path of the thing being mocked.
# The function argument defines the name of the mock.
# .return_value is like instantiating an object and returning that instance every time.
# When calling a method on a mocked return value, you should call .return_value after that method.
# This creates a mocked value for the method call instead of forcing the method call to become an attribute.
# mock_datetime.return_value.now.return_value vs mock_datetime.return_value.now.
# .side_effect is similar but returns an iterable in a list, an exeption, or some different return value.
# Pytest will throw an error if you run out of iterables before ending a loop. See user_input() and run_strategy().

@patch("project.datetime")
@patch("project.os.path.join")
@patch("project.os.path.exists")
@patch("project.pd.read_csv")
@patch("project.hist_data_client.get_stock_bars")
def test_get_data(
    mock_get_stock_bars,
    mock_read_csv,
    mock_path_exists,
    mock_path_join,
    mock_datetime,
):
    # Mock all of the patches
    mock_datetime.return_value.now.return_value = datetime(1969, 7, 20)

    # Create file paths for each mocked tf
    mock_path_join.side_effect = lambda *args: "/".join(args)

    mock_path_exists.side_effect = [True, True, True, False]

    mock_read_csv.return_value = MOCK_DF

    mock_get_stock_bars.return_value.df.return_value = MOCK_DF

    # Call the function
    result = get_data(MOCK_TICKER)

    # Assertions
    # Assert four timeframes
    assert len(result) == 4

    # Assert first 3 timeframes were loaded from csv b/c path.exists was true for first 3
    mock_read_csv.assert_called()
    assert result["1-Hour"].equals(MOCK_DF)
    assert result["4-Hour"].equals(MOCK_DF)
    assert result["Daily"].equals(MOCK_DF)

    # Assert last tf was fetched via Alpaca client
    mock_get_stock_bars.assert_called_once()
    assert result["Weekly"].equals(MOCK_DF)


@patch("project.validate_ticker")
@patch("builtins.input")
def test_user_input(mock_input, mock_val_tick):
    # Mock user ticker scrubbing
    mock_input.side_effect = ["AAPL", "aapl", "aApl ", "  aapL", " aapl "]
    
    # Mock successful ticker validation
    mock_val_tick.return_value = True
    
    # Assert tickers are returned properly
    for _ in range(5):
        assert user_input() == "AAPL"

    # Mock unsuccessful ticker validation, then exit command
    mock_input.side_effect = ["INVALID", "EXIT"]
    mock_val_tick.return_value = False

    # assert_any_call asserts that the mock was called with the defined string
    with patch("builtins.print") as mock_print:
        with pytest.raises(SystemExit):
            user_input()
            mock_print.assert_any_call("Invalid ticker. Please enter a valid ticker symbol.\n")    


@patch("project.trade_client.get_asset")
def test_validate_ticker(mock_get_ticker):
    # Mock successful ticker validation
    mock_ticker = MagicMock()
    mock_ticker.tradable = True
    mock_get_ticker.return_value = mock_ticker

    assert validate_ticker(MOCK_TICKER) is True

    # Mock unsuccessful ticker validation
    mock_get_ticker.side_effect = Exception("Invalid ticker")

    assert validate_ticker("INVALID") is False


@patch("project.Anchor_Plot")
@patch("project.get_data")
@patch("project.user_input")
def test_run_strategy(mock_user_input, mock_get_data, mock_Anchor_Plot):
    # Mock user input
    # SystemExit ensures the test won't get stuck in the while loop
    mock_user_input.side_effect = ["QQQ", SystemExit]
    
    # Mock get data
    mock_get_data.return_value = {
        "1-Hour": ["TimeFrameUnit.Hour", 1],
        "4-Hour": ["TimeFrameUnit.Hour", 4],
        "Daily": ["TimeFrameUnit.Day", 1],
        "Weekly": ["TimeFrameUnit.Week", 1],
    }

    # Mock anchor plot
    mock_ap_instance = mock_Anchor_Plot.return_value
    mock_ap_instance.plot.return_value = None

    # Call the function, catch SystemExit so it doesn't throw an error
    with pytest.raises(SystemExit):
        run_strategy()

    # Assert that user input is called
    mock_get_data.assert_called_once_with("QQQ")

    # Assert that get data provides a dict with 1hr, 4hr, daily, and weekly keys
    mock_Anchor_Plot.assert_called_once_with(
        {
            "1-Hour": ["TimeFrameUnit.Hour", 1],
            "4-Hour": ["TimeFrameUnit.Hour", 4],
            "Daily": ["TimeFrameUnit.Day", 1],
            "Weekly": ["TimeFrameUnit.Week", 1],
        },
        "QQQ"
    )

    # Assert that anchor_plot.plot plots some charts in a browser window
    mock_ap_instance.plot.assert_called_once_with()


def test_Indicator():
    test_ind = Indicator(MOCK_DF)

    assert test_ind.df is MOCK_DF


def test_SMA():
    # Create instance
    sma = SMA(MOCK_DF, 5)
    # Run method
    sma.calc()

    # Assert that the indicator's column name has been added
    assert "SMA 5" in sma.df.columns
    # Assert that the data within the column is numerical
    assert pd.api.types.is_numeric_dtype(sma.df["SMA 5"])

def test_EMA():
    ema = EMA(MOCK_DF, 5)
    ema.calc()

    assert "EMA 5" in ema.df.columns
    assert pd.api.types.is_numeric_dtype(ema.df["EMA 5"])

def test_ATR():
    atr = ATR(MOCK_DF, 5)
    atr.calc()

    assert "TR" in atr.df.columns
    assert "ATR 5" in atr.df.columns
    assert pd.api.types.is_numeric_dtype(atr.df["ATR 5"])


def test_STD_DEV():
    std_dev = STD_DEV(MOCK_DF, 5)
    std_dev.calc()

    assert "Std Dev 5" in std_dev.df.columns
    assert pd.api.types.is_numeric_dtype(std_dev.df["Std Dev 5"])


def test_BB():
    bb = BB(MOCK_DF, 5)
    bb.calc()

    assert "Upper BB" in bb.df.columns
    assert pd.api.types.is_numeric_dtype(bb.df["Upper BB"])
    assert "Lower BB" in bb.df.columns
    assert pd.api.types.is_numeric_dtype(bb.df["Lower BB"])

def test_KC():
    kc = KC(MOCK_DF, 5)
    kc.calc()

    assert "Upper KC" in kc.df.columns
    assert pd.api.types.is_numeric_dtype(kc.df["Upper KC"])
    assert "Lower KC" in kc.df.columns
    assert pd.api.types.is_numeric_dtype(kc.df["Lower KC"])


def test_Squeeze():
    sq = Squeeze(MOCK_DF)
    sq.calc()

    assert "Squeeze Fired" in sq.df.columns
    assert pd.api.types.is_bool_dtype(sq.df["Squeeze Fired"])
    assert "Sqz Delta" in sq.df.columns
    assert pd.api.types.is_numeric_dtype(sq.df["Sqz Delta"])
    assert "Sqz Hist" in sq.df.columns
    assert pd.api.types.is_numeric_dtype(sq.df["Sqz Hist"])


def test_MACD():
    macd = MACD(MOCK_DF)
    macd.calc()

    assert "MACD" in macd.df.columns
    assert pd.api.types.is_numeric_dtype(macd.df["MACD"])
    assert "MACD Wave" in macd.df.columns
    assert pd.api.types.is_numeric_dtype(macd.df["MACD Wave"])
    assert "MACD Signal" in macd.df.columns
    assert pd.api.types.is_numeric_dtype(macd.df["MACD Signal"])


def test_Anchor():
    for df in MOCK_DATA_DICT.values():
        squeeze = Squeeze(df)
        squeeze.calc()

    anchor = Anchor(MOCK_DATA_DICT)
    anchor.calc()

    for df in anchor.data_dict.values():
        assert "Anchor Fired" in df.columns
        assert pd.api.types.is_bool_dtype(df["Anchor Fired"])


def test_Anchor_plot():
    # This test validates that the plot method plots something and doesn't crash. That is all.
    # A future version could show that the correct number of plots are plotted, the correct number of columns are present in the data dict, and all the plots are populated with data.

    plot = Anchor_Plot(MOCK_DATA_DICT, MOCK_TICKER)
    try:
        plot.plot()
    except Exception as e:
        pytest.fail(f"Anchor_Plot.plot() raised {e}")


def main():
    test_get_data()
    test_user_input()
    test_validate_ticker()
    test_run_strategy()
    test_Indicator()
    test_SMA()
    test_EMA()
    test_ATR()
    test_STD_DEV()
    test_KC()
    test_BB()
    test_Squeeze()
    test_MACD()
    test_Anchor()
    test_Anchor_plot()


if __name__ == "__main__":
    main()
