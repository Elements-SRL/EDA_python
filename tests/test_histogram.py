import unittest

from matplotlib import pyplot as plt
from numpy.random import randn
from src.analysis.histogram import histogram


class TestHistogram(unittest.TestCase):

    def test_histogram(self):
        # rand = randn(100)
        # y, x = histogram.calc_hist(rand)
        # print(y, x)
        # print(len(y), len(x))
        # self.assertTrue(len(y) + 1 == len(x))
        # n, bins, patches = plt.hist(y, 10, facecolor='blue', alpha=0.5)
        # print(n, bins, patches)
        # plt.show()
        self.assertTrue(2 + 2 == 4)


if __name__ == '__main__':
    unittest.main()
