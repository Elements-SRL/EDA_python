import unittest
from src.logics.logics import Logics


class DwellAnalysisTest(unittest.TestCase):
    path_to_abf = "res/EventsDetection/Flowcell 19_external electrodes_PS200 and 350_CH001_000.abf"

    def test_something(self):
        logics = Logics()
        logics.open(self.path_to_abf)
        logics.dwell_analysis(10, 90)
        # TODO is there a better way to test it?
        assert(len(logics.metadata.selected_data_group.basic_data) == 0)


if __name__ == '__main__':
    unittest.main()
