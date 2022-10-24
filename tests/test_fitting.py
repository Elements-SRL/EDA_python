import unittest

import numpy as np
from matplotlib import pyplot as plt

from src.analysis.fitting import fitting


class TestFitting(unittest.TestCase):

    def test_linear_fitting(self):
        y, popt = fitting.linear_fitting(np.array([1, 2, 3]), np.array([1, 2, 3]))

    def test_quadratic_fitting(self):
        y, popt = fitting.quadratic_fitting(np.array([1, 2, 3]), np.array([1, 2, 3]))

    def test_exponential_fitting(self):
        y, popt = fitting.exponential_fitting(np.array([1, 2, 3]), np.array([1, 2, 3]))

    def test_power_law_fitting(self):
        y, popt = fitting.power_law_fitting(np.array([1, 2, 3]), np.array([1, 2, 3]))

    def test_gaussian_peak_fitting(self):
        y, popt = fitting.gaussian_fitting(np.array([1, 2, 3]), np.array([1, 2, 3]))

    def test_boltzmann(self):
        x = np.linspace(-100, 100, 1000)
        noise = np.random.normal(size=x.size)
        yr = fitting._boltzmann(x, 5, -5, 1, 0) + noise
        y, popt = fitting.boltzmann_fitting(x, yr)
        fig, ax = plt.subplots()
        ax.plot(x, yr)
        ax.plot(x, y)


if __name__ == '__main__':
    unittest.main()
