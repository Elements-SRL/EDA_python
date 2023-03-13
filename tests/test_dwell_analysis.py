import unittest
from src.logics.logics import Logics
from src.analysis.dwell import dwell


class DwellAnalysisTest(unittest.TestCase):
    path_to_abf = "../res/ContiguousData/temp.edh"

    def test_something(self):
        logics = Logics()
        logics.open(self.path_to_abf)
        sr = logics.metadata.selected_data_group.sampling_rate
        list_of_events = dwell.detect_events_from_data_group(logics.metadata.selected_data_group, sr,
                                                             min_event_length=10, max_event_length=800)
        # TODO is there a better way to test it?
        assert(len(list_of_events) == 0)


if __name__ == '__main__':
    unittest.main()
