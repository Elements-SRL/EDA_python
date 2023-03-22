import unittest
from src.logics.logics import Logics
from src.analysis.dwell.dwell import ThresholdModality


class DwellAnalysisTest(unittest.TestCase):
    path_to_abf = "res/EventsDetection/Flowcell 19_external electrodes_PS200 and 350_CH001_000.abf"

    def test_zipped_result(self):
        logics = Logics()
        logics.open(self.path_to_abf)
        results = logics.dwell_analysis(0.001, 0.100, 0.3, ThresholdModality.RELATIVE)
        a, d, b, e = zip(*results)
        assert (len(a) == len(d))
        assert (len(a) == len(b))
        assert (len(a) == len(e))

    def test_get_amplitudes(self):
        logics = Logics()
        logics.open(self.path_to_abf)
        dg = logics.metadata.selected_data_group
        logics.dwell_analysis(0.001, 0.100, 1.3, ThresholdModality.STD_DEV_BASED)
        # TODO is there a better way to test it?
        assert (len(dg.data_groups) == 0)


if __name__ == '__main__':
    unittest.main()
