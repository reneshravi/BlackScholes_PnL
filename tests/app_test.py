import pytest
from unittest.mock import patch
from src.option import Option
import numpy as np
import pandas as pd
from src.heatmap_funcs import dynamic_annotation_format


@pytest.fixture
def mock_option():
    return Option(100, 100, 1, 0.05, 0.2, "call")

def test_black_scholes_calculations(mock_option):
    call_price = mock_option.black_scholes_price()
    assert call_price == pytest.approx(10.4506, 0.0001), "Call price calculation is incorrect."

def test_heatmap_formatting():
    assert dynamic_annotation_format(1500000) == "1.5M"
    assert dynamic_annotation_format(10000) == "10.0K"
    assert dynamic_annotation_format(250.5) == "250.5"
    assert dynamic_annotation_format(-50) == "-50.0"

def test_live_data_fetching():
    with patch("yfinance.Ticker") as mock_ticker:
        mock_ticker.return_value.history.return_value = pd.DataFrame({"Close": [150.0]})
        stock_data = mock_ticker("AAPL")
        live_price = stock_data.history(period="1d")['Close'].iloc[-1]
        assert live_price == 150.0, "Live price fetching failed."

def test_heatmap_surface():
    range_offset = 50
    num_points = 11
    S, K, T, r, vol = 100, 100, 1, 0.05, 0.2

    S_range = np.linspace(S - range_offset, S + range_offset, num_points)
    K_range = np.linspace(K - range_offset, K + range_offset, num_points)

    pnl_surface = np.zeros((num_points, num_points))

    for i, S_val in enumerate(S_range):
        for j, K_val in enumerate(K_range):
            temp_call_option = Option(S_val, K_val, T, r, vol, "call")
            call_price = temp_call_option.black_scholes_price()
            pnl_surface[i, j] = call_price

    assert pnl_surface.shape == (11, 11), "PNL surface shape is incorrect."
    assert pnl_surface[0, 0] != 0, "PNL surface values are not being calculated."

def test_sidebar_inputs():
    # Mock Streamlit inputs
    with patch("streamlit.sidebar.number_input") as mock_input:
        mock_input.return_value = 100
        S = mock_input("Spot Price", value=100.0, step=0.01)
        assert S == 100, "Sidebar input for Spot Price failed."

    with patch("streamlit.sidebar.toggle") as mock_toggle:
        mock_toggle.return_value = False
        use_live_data = mock_toggle("Fetch Live Data (Yahoo Finance)", value=False)
        assert not use_live_data, "Sidebar toggle for live data failed."

def test_download_buttons():
    call_pnl_df = pd.DataFrame(np.random.rand(10, 10))

    with patch("streamlit.sidebar.download_button") as mock_download:
        mock_download.return_value = True
        assert mock_download(
            label="Download Call PnL Data",
            data=call_pnl_df.to_csv(index=True),
            file_name="call_pnl_data.csv",
            mime="text/csv"
        ), "Download button for Call PnL Data failed."

if __name__ == "__main__":
    pytest.main()
