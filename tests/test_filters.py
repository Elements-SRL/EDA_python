import unittest
from src.analysis.filters.filter_arguments import FilterArguments
import src.analysis.filters.filter_handler as fh


class TestFilters(unittest.TestCase):

    def test_butter_filter_preview(self):
        filter_args = FilterArguments(filter_type="butter",
                                      order=4,
                                      b_type="highpass",
                                      cutoff_frequency=500,
                                      analog=False,
                                      fs=2000)
        b, a = fh.calc_filter(filter_args)
        self.assertTrue(len(b) == len(a))


if __name__ == '__main__':
    unittest.main()
