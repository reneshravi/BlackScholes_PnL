# Black-Scholes Option Pricing App

This project is a Streamlit-based web application that calculates the prices and Greeks of European call and put options using the Black-Scholes model. It also includes visualizations of profit and loss (PnL) heatmaps for both call and put options over a range of spot prices and strike prices.

---

## Features

- **Dynamic Spot Price Fetching**:
  - Automatically fetch live stock prices via Yahoo Finance.
  - Option to manually enter spot prices.

- **Risk-Free Rate Integration**:
  - Pull government bond rates as risk-free rates based on the time to maturity.
  - Option to manually input the risk-free rate.

- **Option Pricing**:
  - Compute the prices of European call and put options using the Black-Scholes formula.

- **PnL Heatmaps**:
  - Generate heatmaps to visualize profit and loss for both call and put options across a range of spot and strike prices.

- **Option Greeks**:
  - Calculate and display Delta, Gamma, Vega, Theta, and Rho for both call and put options.

- **Data Export**:
  - Download PnL data for both call and put options in CSV format.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/reneshravi/Black-Scholes-Option-Pricing-App.git
   cd Black-Scholes-Option-Pricing-App
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project directory with the following content:
     ```
     api_key=YOUR_FRED_API_KEY
     ```

4. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

---

## Usage

1. Open the app in your browser (https://blackscholespnl.streamlit.app/).
2. Use the sidebar to input parameters:
   - Spot Price: Enter manually or fetch live data.
   - Strike Price, Time to Maturity, Risk-Free Rate, and Volatility.
   - Specify the number of contracts and purchase price for PnL analysis.
3. View calculated option prices, Greeks, and PnL heatmaps.
4. Download PnL data in CSV format using the sidebar.

---

## File Structure

```
Black-Scholes-Option-Pricing-App/
├── src/
│   ├── option.py                   # Black-Scholes model implementation
│   ├── heatmap_funcs.py            # Heatmap generation utilities
│   ├── risk_free_rate_fetcher.py   # Fetch risk-free rates
│   └── streamlit_app.py            # Main Streamlit app
├── tests/
│   ├── option_test.py              # Unit tests for the Option class
│   ├── heatmap_funcs_test.py       # Unit tests for heatmaps
│   └── rfr_fetcher_test.py         # Unit tests for risk-free rate fetching
│
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
└── .env                            # Environment variables
```

---

## Technologies Used

- **Python**: Core programming language.
- **Streamlit**: Framework for building interactive web apps.
- **NumPy & Pandas**: Numerical and data handling.
- **Matplotlib & Seaborn**: Heatmap and data visualization.
- **Yahoo Finance API (via yfinance)**: Fetch live stock prices.
- **FRED API**: Fetch government bond risk-free rates.

---

## Future Enhancements

- Add support for American options.
- Integrate more complex option models (Heston Model).
- Expand visualizations for more robust user interactivity.

---

## Author

Developed by [Renesh Ravi](https://linkedin.com/in/reneshravi).

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
