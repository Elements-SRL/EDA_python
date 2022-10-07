import unittest
from src.filters.filter_arguments import FilterArguments
import src.filters.filter_handler as fh


class TestFilters(unittest.TestCase):

    # TODO not analog filters need cutoff freq normalized between 0 and 1
    def test_butter_filter_preview(self):
        filter_args = FilterArguments(filter_type="butter",
                                      order=4,
                                      b_type="highpass",
                                      cutoff_frequency=500,
                                      analog=True)
        b, a = fh.filter_preview(filter_args)
        self.assertTrue(len(b) == len(a))


if __name__ == '__main__':
    unittest.main()
