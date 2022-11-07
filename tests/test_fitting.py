import unittest
import numpy as np
from src.analysis.fitting import fitting


class TestFitting(unittest.TestCase):

    def test_linear_fitting(self):
        np.random.seed(0)
        x = np.linspace(0, 1000, 1000)
        y = fitting._linear(x, 2, 5)
        noise = np.random.normal(0, 2, y.size)
        y_noise = y + noise
        y_found, _ = fitting.linear_fitting(x, y_noise)
        self.assertTrue(np.allclose(y, y_found, 0.05, 0.01))

    def test_quadratic_fitting(self):
        np.random.seed(0)
        x = np.linspace(0, 1000, 1000)
        y = fitting._quadratic(x, 2, 4, 8)
        noise = np.random.normal(0, 1, y.size)
        y_noise = y + noise
        y_found, _ = fitting.quadratic_fitting(x, y_noise)
        self.assertTrue(np.allclose(y, y_found, 0.05, 0.01))

    def test_exponential_fitting(self):
        np.random.seed(0)
        x = np.linspace(0, 10, 100)
        y = fitting._exponential(x, 1, 1)
        noise = np.random.normal(0, 1, y.size)
        y_noise = y + noise
        y_found, _ = fitting.exponential_fitting(x, y_noise)
        self.assertTrue(np.allclose(y, y_found, 0.05, 0.01))

    def test_power_law_fitting(self):
        np.random.seed(0)
        x = np.linspace(0, 1000, 1000)
        y = fitting._power_law(x, 2, 4)
        noise = np.random.normal(0, 1, y.size)
        y_noise = y + noise
        y_found, _ = fitting.power_law_fitting(x, y_noise)
        self.assertTrue(np.allclose(y, y_found, 0.05, 0.01))

    def test_gaussian_peak_fitting(self):
        np.random.seed(0)
        x = np.linspace(0, 1000, 1000)
        y = fitting._gaussian(x, 10, 50, 300)
        noise = np.random.normal(0, 0.5, y.size)
        y_noise = y + noise
        y_found, _ = fitting.gaussian_fitting(x, y_noise)
        self.assertTrue(np.allclose(y, y_found, 0.05, 0.01))

    @pytest.mark.skip(reason="overflow")
    def test_boltzmann(self):
        np.random.seed(0)
        x = np.linspace(0, 1000, 1000)
        y = fitting._boltzmann(x, 2, 10, 8, 500)
        noise = np.random.normal(0, 0.5, y.size)
        y_noise = y + noise
        y_found, _ = fitting.boltzmann_fitting(x, y_noise)
        self.assertTrue(np.allclose(y, y_found, 0.1, 0.1))


if __name__ == '__main__':
    unittest.main()
