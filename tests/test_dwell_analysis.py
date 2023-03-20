import unittest
from src.logics.logics import Logics
from src.analysis.dwell import dwell

class DwellAnalysisTest(unittest.TestCase):
    path_to_abf = "../res/EventsDetection/Flowcell 19_external electrodes_PS200 and 350_CH001_000.abf"

    def test_something(self):
        logics = Logics()
        dg = logics.metadata.selected_data_group
        logics.open(self.path_to_abf)
        logics.dwell_analysis(10, 90)
        # TODO is there a better way to test it?
        assert(len(dg.data_groups) == 1)

    def test_get_amplitudes(self):
        logics = Logics()
        dg = logics.metadata.selected_data_group
        logics.open(self.path_to_abf)
        logics.dwell_analysis(10, 90)
        # TODO is there a better way to test it?
        assert(len(dg.data_groups) == 1)


if __name__ == '__main__':
    unittest.main()
