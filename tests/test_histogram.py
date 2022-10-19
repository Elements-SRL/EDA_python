import unittest


from src.analysis.histogram import histogram


class TestHistogram(unittest.TestCase):

    def test_name_strategy(self):
        name = "ciccia ch 0"
        name1 = histogram._name_strategy(name)
        self.assertTrue(name1 == "ciccia ch 0 hist")
        name2 = histogram._name_strategy(name1)
        self.assertTrue(name2 == "ciccia ch 0 hist 1")
        name3 = histogram._name_strategy(name2)
        self.assertTrue(name3 == "ciccia ch 0 hist 2")


if __name__ == '__main__':
    unittest.main()
