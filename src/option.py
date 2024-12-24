from scipy.stats import norm
from math import log, sqrt, exp
import requests


class Option:
    def __init__(self, S, K, T, r, vol, option_type="call"):
        """
        Initializes the object Option
        :param S: Price of Underlying
        :param K: Strike Price
        :param T: Time to maturity (in years)
        :param r: Risk Free Rate (annualized)
        :param vol: Volatility (annualized)
        :param option_type: 'call' or 'put'; default is 'call'
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.vol = vol
        self.option_type = option_type.lower()


        self.d1 = self.get_d1()
        self.d2 = self.get_d2()

    def get_d1(self):
        return (log(self.S / self.K) + (
                self.r + 0.5 * self.vol ** 2) * self.T) / (
                self.vol * sqrt(self.T))

    def get_d2(self):
        return self.get_d1() - self.vol * sqrt(self.T)

    def black_scholes_price(self):
        if self.option_type == "call":
            price = self.S * norm.cdf(self.d1) - self.K * exp(
                -self.r * self.T) * norm.cdf(self.d2)
        elif self.option_type == "put":
            price = self.K * exp(-self.r * self.T) * norm.cdf(
                -self.d2) - self.S * norm.cdf(-self.d1)
        else:
            raise ValueError("Invalid option type. Choose 'call' or 'put'.")

        return price

    def get_delta(self):

        if self.option_type == "call":
            return norm.cdf(self.d1)
        else:
            return norm.cdf(self.d1) - 1

    def get_gamma(self):
        return (norm.pdf(self.d1)) / (self.S * self.vol * sqrt(self.T))

    def get_vega(self):
        return self.S * norm.pdf(self.d1) * sqrt(self.T)

    def get_theta(self):
        if self.option_type == "call":
            return ((- self.S * norm.pdf(self.d1) * self.vol) / (2 * sqrt(self.T))) - self.r * self.K * exp(
                -self.r * self.T) * norm.cdf(self.d2)
        else:
            return ((- self.S * norm.pdf(self.d1) * self.vol) / (2 * sqrt(self.T))) + self.r * self.K * exp(
                -self.r * self.T) * norm.cdf(-self.d2)

    def get_rho(self):
        if self.option_type == "call":
            return self.K * self.T * exp(- self.r * self.T) * norm.cdf(self.d2)
        else:
            return -(self.K * self.T * exp(- self.r * self.T) * norm.cdf(-1 * self.d2))

    def get_greeks(self):
        return {"Delta": self.get_delta(),
                "Gamma": self.get_gamma(),
                "Vega": self.get_vega(),
                "Theta": self.get_theta(),
                "Rho": self.get_rho(),
                }

    @staticmethod
    def fetch_risk_free_rate(T):
        maturities = {0.25: "DGS3MO",
                      0.5: "DGS6MO",
                      1: "DGS1",
                      2: "DGS2",
                      5: "DGS5",
                      10: "DGS10"
                      }

        closest_maturity = min(maturities.keys(), key=lambda x: abs(x -
                                                                    T))
        series_id = maturities[closest_maturity]
        api_key = "246b57b6f48a3fe94b2e8b2e707df8af"
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json"

        response = requests.get(url)
        data = response.json()
        latest_rate = float(data['observations'][-1]['value']) / 100  # Convert to decimal
        return latest_rate

    @staticmethod
    def is_close(rate1, rate2, to1=1e-4):
        return abs(rate1 - rate2) < to1