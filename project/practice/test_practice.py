import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from project import (
    get_data,
    validate_ticker,
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
MOCK_TICKER = "AAPL"
MOCK_DATA = {
    "open": [100, 102, 104, 103, 105],
    "high": [102, 104, 106, 105, 107],
    "low": [99, 101, 103, 102, 104],
    "close": [101, 103, 105, 104, 106],
}
MOCK_DF = pd.DataFrame(MOCK_DATA, index=pd.date_range("2023-01-01", periods=5))


# Test get_data function
@patch("anchor_analysis.StockHistoricalDataClient.get_stock_bars")
@patch("anchor_analysis.os.path.exists")
@patch("anchor_analysis.pd.read_csv")
def test_get_data(mock_read_csv, mock_exists, mock_get_stock_bars):
    # Mock behavior for existing and non-existing CSV
    mock_exists.side_effect = lambda x: "1-Hour" in x  # Only 1-Hour data exists
    mock_read_csv.return_value = MOCK_DF
    mock_get_stock_bars.return_value.df = MOCK_DF

    # Call function
    data_dict = get_data(MOCK_TICKER)

    # Validate structure and data
    assert "1-Hour" in data_dict
    assert "4-Hour" in data_dict
    assert isinstance(data_dict["1-Hour"], pd.DataFrame)
    assert isinstance(data_dict["4-Hour"], pd.DataFrame)


# Test validate_ticker function
@patch("anchor_analysis.TradingClient.get_asset")
def test_validate_ticker(mock_get_asset):
    # Mock successful asset fetch
    mock_asset = MagicMock()
    mock_asset.tradable = True
    mock_get_asset.return_value = mock_asset

    assert validate_ticker(MOCK_TICKER) is True

    # Mock unsuccessful asset fetch
    mock_get_asset.side_effect = Exception("Invalid ticker")
    assert validate_ticker("INVALID") is False


# Test SMA calculation
def test_sma():
    sma = SMA(MOCK_DF.copy(), 3)
    sma.calc()
    assert "SMA 3" in sma.df.columns
    assert not sma.df["SMA 3"].isnull().all()  # Ensure some calculations were made


# Test EMA calculation
def test_ema():
    ema = EMA(MOCK_DF.copy(), 3)
    ema.calc()
    assert "EMA 3" in ema.df.columns
    assert not ema.df["EMA 3"].isnull().all()


# Test ATR calculation
def test_atr():
    atr = ATR(MOCK_DF.copy(), 3)
    atr.calc()
    assert "ATR 3" in atr.df.columns
    assert not atr.df["ATR 3"].isnull().all()


# Test Bollinger Bands calculation
def test_bb():
    bb = BB(MOCK_DF.copy(), 3)
    bb.calc()
    assert "Upper BB" in bb.df.columns
    assert "Lower BB" in bb.df.columns


# Test Keltner Channels calculation
def test_kc():
    kc = KC(MOCK_DF.copy(), 3)
    kc.calc()
    assert "Upper KC" in kc.df.columns
    assert "Lower KC" in kc.df.columns


# Test Squeeze calculation
def test_squeeze():
    sqz = Squeeze(MOCK_DF.copy())
    sqz.calc()
    assert "Squeeze Fired" in sqz.df.columns
    assert "Sqz Delta" in sqz.df.columns
    assert "Sqz Hist" in sqz.df.columns


# Test MACD calculation
def test_macd():
    macd = MACD(MOCK_DF.copy())
    macd.calc()
    assert "MACD" in macd.df.columns
    assert "MACD Signal" in macd.df.columns
    assert "MACD Wave" in macd.df.columns


# Test Anchor calculation
def test_anchor():
    data_dict = {
        "1-Hour": MOCK_DF.copy(),
        "4-Hour": MOCK_DF.copy(),
        "Daily": MOCK_DF.copy(),
        "Weekly": MOCK_DF.copy(),
    }
    for df in data_dict.values():
        df["Squeeze Fired"] = [True, False, True, False, True]

    anchor = Anchor(data_dict)
    anchor.calc()

    for df in data_dict.values():
        assert "Anchor Fired" in df.columns
        assert df["Anchor Fired"].dtype == bool


# Test Anchor_Plot initialization
@patch("anchor_analysis.Anchor_Plot.plot")
def test_anchor_plot(mock_plot):
    data_dict = {
        "1-Hour": MOCK_DF.copy(),
        "4-Hour": MOCK_DF.copy(),
        "Daily": MOCK_DF.copy(),
        "Weekly": MOCK_DF.copy(),
    }
    anchor_plot = Anchor_Plot(data_dict, MOCK_TICKER)
    anchor_plot.plot()
    mock_plot.assert_called_once()


