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
    mock_datetime_now = mock_datetime.now
    mock_datetime_now.return_value = datetime(1969, 7, 20)

    mock_path_join.side_effect = lambda *args: "/".join(args)

    mock_path_exists.side_effect = [True, True, True, False]

    mock_read_csv.return_value = MOCK_DF

    mock_df = pd.DataFrame(MOCK_DATA)
    mock_get_stock_bars.return_value.df = mock_df

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
    assert result["Weekly"].equals(mock_df)


@patch("project.validate_ticker")
@patch("builtins.input")
def test_user_input(mock_input, mock_val_tick):
    # Test user ticker scrubbing, use mock input
    # Test successful ticker validation, mock validate_ticker
    mock_input.side_effect = ["AAPL", "aapl", "aApl ", "  aapL", " aapl "]
    mock_val_tick.return_value = True
    for _ in range(5):
        assert user_input() == "AAPL"

    # Test unsuccessful ticker validation, then exit command
    # assert_any_call asserts that the mock was called with the defined string
    mock_input.side_effect = ["INVALID", "EXIT"]
    mock_val_tick.return_value = False
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

    # Call the function
    with pytest.raises(SystemExit):
        run_strategy()

    # Assert that user input has two calls, QQQ and EXIT
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
    ...


def test_SMA():
    ...

def test_EMA():
    ...


def test_ATR():
    ...


def test_STD_DEV():
    ...


def test_BB():
    ...


def test_KC():
    ...


def tet_Squeeze():
    ...


def test_MACD():
    ...


def test_Anchor():
    ...


def test_Anchor_plot():
    ...

def main():
    test_user_input()


if __name__ == "__main__":
    main()
