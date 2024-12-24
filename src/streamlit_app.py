import option
import streamlit as st
import seaborn as sns
import numpy as np
import heatmap_funcs
import pandas as pd
import yfinance as yf


st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.title("Black-Scholes Option Pricing")
st.sidebar.header('Option Parameters')

st.sidebar.subheader("Stock Price Source")
use_live_data = st.sidebar.toggle("Fetch Live Data (Yahoo Finance)",
                                value=False)

if use_live_data:
    stock_ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
    try:
        stock_data = yf.Ticker(stock_ticker)
        live_price = stock_data.history(period="1d")['Close'].iloc[-1]
        st.sidebar.write(f"Live Spot Price: ${live_price:.2f}")
        S = live_price
    except Exception as e:
        st.sidebar.error(f"Error fetching data for {stock_ticker}: {e}")
        S = st.sidebar.number_input("Fallback Spot Price", value=100.0, step=0.01)
else:
    S = st.sidebar.number_input("Spot Price", value=100.0, step=0.01)

K = st.sidebar.number_input("Strike Price (K)", value=100.0, step=0.01)
T = st.sidebar.number_input("Time to Maturity (in years)", value=1.0, step=0.25)

use_gov_bond_rate = st.sidebar.toggle("Use Government Bond Rate for "
                                      "Risk-Free Rate", value=True)
if use_gov_bond_rate:
    temp_option = option.Option(S, K, T, 0.0001, 0.0001, "call")

    try:
        r = temp_option.fetch_risk_free_rate(T) * 100  # Convert to percentage
        st.sidebar.write(f"Fetched government rate: {r:.2f}%")
    except Exception as e:
        st.sidebar.error(f"Error fetching rate: {e}")
        r = 0.05  # Default fallback rate
else:
    r = st.sidebar.number_input("Input Risk-Free Rate (in percent)",
                                value=5.00, step=0.01)

vol = st.sidebar.number_input("Volatility (in percent)", value=20.00,
                              step=0.01)

call_option = option.Option(S, K, T, r / 100, vol / 100, "call")
put_option = option.Option(S, K, T, r / 100, vol / 100, "put")
call_price = call_option.black_scholes_price()
put_price = put_option.black_scholes_price()

st.markdown(
    """
    <style>
    .container {
        padding: 10px;
        background-color: #f9f9f9;
        border: 1px solid #333030;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 10px;
    }
    .call-container {
        padding: 10px;
        background-color: #d4edda; /* Light green for Call Price */
        border: 1px solid #333030;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 10px;
    }
    .put-container {
        padding: 10px;
        background-color: #edd4dc; /* Light red for Put Price */
        border: 1px solid #333030;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 10px;
    }
    .centered-header {
        text-align: center;
        font-weight: bold;
        font-size: 22px;
        margin-bottom: 10px;
    }
    .value {
        font-size: 19px;
        font-weight: normal;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(' ### Values')
col1, col2, col3, col4, col5 = st.columns(5)

# Displaying headers and values in styled containers
with col1:
    st.markdown(
        '<div class="container"><p class="centered-header">Spot Price</p><p class="value">${:.2f}</p></div>'.format(S),
        unsafe_allow_html=True)

with col2:
    st.markdown(
        '<div class="container"><p class="centered-header">Strike Price (K)</p><p class="value">${:.2f}</p></div>'.format(
            K), unsafe_allow_html=True)

with col3:
    st.markdown(
        '<div class="container"><p class="centered-header">Time to Maturity (T)</p><p class="value">{:.2f} years</p></div>'.format(
            T), unsafe_allow_html=True)

with col4:
    st.markdown(
        '<div class="container"><p class="centered-header">Risk-Free Rate</p><p class="value">{:.2f}%</p></div>'.format(
            r), unsafe_allow_html=True)

with col5:
    st.markdown(
        '<div class="container"><p class="centered-header">Volatility</p><p class="value">{:.2f}%</p></div>'.format(
            vol), unsafe_allow_html=True)

# Prices Section
st.subheader("Prices")
col_call, col_put = st.columns(2)

with col_call:
    st.markdown(
        '<div class="call-container"><p class="centered-header">Call Price</p><p class="value">${:.2f}</p></div>'.format(
            call_price), unsafe_allow_html=True)

with col_put:
    st.markdown(
        '<div class="put-container"><p class="centered-header">Put Price</p><p class="value">${:.2f}</p></div>'.format(
            put_price), unsafe_allow_html=True)

st.sidebar.divider()
st.sidebar.subheader("PnL Parameters")
num_contracts = st.sidebar.number_input("Number of Contracts", value=1, step=1)
purchase_price = st.sidebar.number_input("Purchase Price per Contract", value=call_price, step=0.01)
pnl = num_contracts * (call_price - purchase_price)

range_offset = 50  # Adjustable range offset for visualization
num_points = 11    # Number of points
S_min, S_max = S - range_offset, S + range_offset
K_min, K_max = K - range_offset, K + range_offset

S_range = np.linspace(S_min, S_max, num_points)
K_range = np.linspace(K_min, K_max, num_points)

call_pnl_surface = np.zeros((num_points, num_points))
put_pnl_surface = np.zeros((num_points, num_points))

for i, S_val in enumerate(S_range):
    for j, K_val in enumerate(K_range):
        # Call option PnL
        temp_call_option = option.Option(S_val, K_val, T, r / 100, vol / 100, "call")
        call_option_price = temp_call_option.black_scholes_price()
        call_pnl_surface[i, j] = num_contracts * (call_option_price - purchase_price)

        # Put option PnL
        temp_put_option = option.Option(S_val, K_val, T, r / 100, vol / 100, "put")
        put_option_price = temp_put_option.black_scholes_price()
        put_pnl_surface[i, j] = num_contracts * (put_option_price - purchase_price)

# Custom colormap
custom_cmap = sns.diverging_palette(0, 145, as_cmap=True)
st.divider()
# Display heatmaps in two Streamlit columns
col_call_pnl, col_put_pnl = st.columns(2)

# Call PnL heatmap
with col_call_pnl:
    heatmap_funcs.generate_heatmap(
        "Call Option PnL Heatmap",
        call_pnl_surface,
        K_range,
        S_range,
        custom_cmap,
        heatmap_funcs.dynamic_annotation_format
    )

# Put PnL heatmap
with col_put_pnl:
    heatmap_funcs.generate_heatmap(
        "Put Option PnL Heatmap",
        put_pnl_surface,
        K_range,
        S_range,
        custom_cmap,
        heatmap_funcs.dynamic_annotation_format
    )

st.divider()
st.subheader("Greeks")
call_greeks = call_option.get_greeks()
put_greeks = put_option.get_greeks()
col_call_greeks, col_put_greeks = st.columns(2)

with col_call_greeks:
    st.markdown("#### Call Option Greeks")
    data = {
        "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
        "Values": [f"{value:.4f}" for value in call_greeks.values()]}
    call_greeks_df = pd.DataFrame(data)
    st.table(call_greeks_df)

with col_put_greeks:
    st.markdown("#### Put Option Greeks")
    data = {
        "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
        "Values": [f"{value:.4f}" for value in put_greeks.values()]}
    put_greeks_df = pd.DataFrame(data)
    st.table(put_greeks_df)

call_pnl_df = pd.DataFrame(call_pnl_surface, index=S_range, columns=K_range)
put_pnl_df = pd.DataFrame(put_pnl_surface, index=S_range, columns=K_range)

# Provide download options
st.sidebar.download_button(
    label="Download Call PnL Data",
    data=call_pnl_df.to_csv(index=True),
    file_name="call_pnl_data.csv",
    mime="text/csv"
)

st.sidebar.download_button(
    label="Download Put PnL Data",
    data=put_pnl_df.to_csv(index=True),
    file_name="put_pnl_data.csv",
    mime="text/csv"
)