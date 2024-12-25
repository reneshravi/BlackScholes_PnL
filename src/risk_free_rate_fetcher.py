"""
File: risk_free_rate_fetcher.py
Description: Pulls risk-free rate from government bond data
Created by: Renesh Ravi
"""
import requests
from dotenv import load_dotenv
import os

def configure():
    """
    Loads dotenv to pull api key from .env
    """
    load_dotenv()


def fetch_risk_free_rate(T):
    """
    Given a Time value T, pulls government bond rate for risk-free rate
    value to be used in black scholes model
    :param T: float value of time till expiry of the option
    :return: float value of the fetched risk-free rate in decimal form
    """
    maturities = {0.25: "DGS3MO",
                  0.5: "DGS6MO",
                  1: "DGS1",
                  2: "DGS2",
                  5: "DGS5",
                  10: "DGS10"
                  }

    closest_maturity = min(maturities.keys(), key=lambda x: abs(x - T))
    series_id = maturities[closest_maturity]
    configure()
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={os.getenv("api_key")}&file_type=json"

    response = requests.get(url)
    data = response.json()
    latest_rate = float(data['observations'][-1]['value']) / 100  # Convert to decimal
    return latest_rate