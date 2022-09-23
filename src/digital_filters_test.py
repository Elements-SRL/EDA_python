import unittest
import numpy as np
from matplotlib import pyplot as plt

from src import digital_filters


class DigitalFiltersTest(unittest.TestCase):

    frequency = 30
    time_sec = np.arange(0, 5, 1.0 / frequency)
    ys = np.sin(2 * np.pi * 1.0 * time_sec)
    y_err = 0.5 * np.random.normal(size=len(time_sec))
    y_raw = ys + y_err
    err_on_raw = np.sum(np.abs(y_raw))

    def debug(self, title, time, raw, filtered):
        plt.title(title)
        plt.plot(time, raw, "-")
        plt.plot(time, filtered, "--")
        plt.show()

    def test_butter(self):
        y_filtered = digital_filters.butter(self.y_raw, self.frequency, 2.5, "lowpass")
        err_on_filtered = np.sum(np.abs(self.y_raw - y_filtered))
        self.debug("butter", self.time_sec, self.y_raw, y_filtered)
        self.assertTrue(err_on_filtered < self.err_on_raw)

    def test_quadratic_spline(self):
        y_filtered = digital_filters.quadratic_spline(self.time_sec, self.y_raw)
        err_on_filtered = np.sum(np.abs(self.y_raw - y_filtered))
        self.debug("quadratic spline", self.time_sec, self.y_raw, y_filtered)
        self.assertTrue(err_on_filtered < self.err_on_raw)

    def test_cubic_spline(self):
        y_filtered = digital_filters.cubic_spline(self.time_sec, self.y_raw)
        err_on_filtered = np.sum(np.abs(self.y_raw - y_filtered))
        self.debug("cubic spline", self.time_sec, self.y_raw, y_filtered)
        self.assertTrue(err_on_filtered < self.err_on_raw)

    def test_autocorrelation(self):
        autocorrelation = digital_filters.autocorrelation(self.y_raw)
        plt.plot(np.arange(-len(self.y_raw)+1, len(self.y_raw)), autocorrelation)
        plt.show()

    def test_fft(self):
        xf, yf = digital_filters.fft(self.y_raw, self.frequency)
        plt.plot(xf,  2.0/5*30 * np.abs(yf[0:5*30//2]))
        plt.show()


if __name__ == '__main__':
    unittest.main()
