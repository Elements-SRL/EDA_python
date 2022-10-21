import unittest
from src.analysis.fitting import fitting


class TestFitting(unittest.TestCase):

    def test_curve_fitting(self):
        fitting.try_exponential_fitting()

    def test_power_law_fitting(self):
        fitting.try_power_law_fitting()

    def test_gaussian_peak_fitting(self):
        fitting.try_gaussian_peak_fitting()


if __name__ == '__main__':
    unittest.main()
