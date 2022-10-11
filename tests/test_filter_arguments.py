import unittest
from src.analysis.filters.filter_arguments import FilterArguments


class TestFilterArguments(unittest.TestCase):

    def test_filter_arguments_creation(self):
        filter_args = FilterArguments(filter_type="butter",
                                      order=8,
                                      b_type="highpass",
                                      cutoff_frequency=500,
                                      fs=2000,
                                      )
        self.assertTrue(type(filter_args) == FilterArguments)


if __name__ == '__main__':
    unittest.main()
