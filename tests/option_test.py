import unittest
from src.option import Option
from math import isclose

class TestOption(unittest.TestCase):

    def setUp(self):
        self.call_option = Option(S=100, K=100, T=1, r=0.05, vol=0.2, option_type="call")
        self.put_option = Option(S=100, K=100, T=1, r=0.05, vol=0.2, option_type="put")

    def test_black_scholes_price(self):
        call_price = self.call_option.black_scholes_price()
        put_price = self.put_option.black_scholes_price()
        self.assertTrue(isclose(call_price, 10.4506, rel_tol=1e-4))
        self.assertTrue(isclose(put_price, 5.5735, rel_tol=1e-4))

    def test_get_delta(self):
        self.assertTrue(isclose(self.call_option.get_delta(), 0.6368, rel_tol=1e-4))
        self.assertTrue(isclose(self.put_option.get_delta(), -0.3632, rel_tol=1e-4))

    def test_get_gamma(self):
        call_gamma = self.call_option.get_gamma()
        put_gamma = self.put_option.get_gamma()
        self.assertTrue(isclose(call_gamma, 0.0187, rel_tol=1e-2))
        self.assertTrue(isclose(put_gamma, 0.0187, rel_tol=1e-2))

    def test_get_vega(self):
        call_vega = self.call_option.get_vega()
        put_vega = self.put_option.get_vega()
        self.assertTrue(isclose(call_vega, 37.524, rel_tol=1e-4))
        self.assertTrue(isclose(put_vega, 37.524, rel_tol=1e-4))

    def test_get_theta(self):
        call_theta = self.call_option.get_theta()
        put_theta = self.put_option.get_theta()
        self.assertTrue(isclose(call_theta, -6.414, rel_tol=1e-4))
        self.assertTrue(isclose(put_theta, -1.658, rel_tol=1e-4))

    def test_get_rho(self):
        call_rho = self.call_option.get_rho()
        put_rho = self.put_option.get_rho()
        self.assertTrue(isclose(call_rho, 53.2325, rel_tol=1e-4))
        self.assertTrue(isclose(put_rho, -41.8905, rel_tol=1e-4))

    def test_get_greeks(self):
        greeks = self.call_option.get_greeks()
        self.assertIn("Delta", greeks)
        self.assertIn("Gamma", greeks)
        self.assertIn("Vega", greeks)
        self.assertIn("Theta", greeks)
        self.assertIn("Rho", greeks)


if __name__ == "__main__":
    unittest.main()
