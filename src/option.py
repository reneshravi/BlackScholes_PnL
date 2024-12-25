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
        """
        Calculates the d1 value in the black scholes model
        :return: float value of d1
        """
        return (log(self.S / self.K) + (
                self.r + 0.5 * self.vol ** 2) * self.T) / (
                self.vol * sqrt(self.T))

    def get_d2(self):
        """
        Calculates the d2 value in the black scholes model
        :return: float value of d1
        """
        return self.get_d1() - self.vol * sqrt(self.T)

    def black_scholes_price(self):
        """
        Calculates call or put price for the Option object
        :return: float value of black scholes price
        """
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
        """
        Calculates delta value of the Option -> how much option's price
        changes for every $1 move in spot price
        :return: numpy.float delta value of an Option
        """
        if self.option_type == "call":
            return norm.cdf(self.d1)
        else:
            return norm.cdf(self.d1) - 1

    def get_gamma(self):
        """
        Calculates gamma value of an Option -> change in option's delta
        :return: numpy.float gamma value of an Option
        """
        return (norm.pdf(self.d1)) / (self.S * self.vol * sqrt(self.T))

    def get_vega(self):
        """
        Calculates vega value of an Option
        :return: numpy.float vega value of an Option
        """
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