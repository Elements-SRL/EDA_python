from numpy import ndarray
from scipy import signal

from src.filters.filter_arguments import FilterArguments


def calc_filter(filter_arguments: FilterArguments) -> (ndarray, ndarray):
    cutoff = [filter_arguments.cutoff_frequency,
              filter_arguments.other_cutoff_frequency] if filter_arguments.b_type in ["bandpass", "bandstop"]\
        else filter_arguments.cutoff_frequency
    if filter_arguments.filter_type == "butter":
        # TODO change fs
        return signal.butter(N=filter_arguments.order, Wn=cutoff, btype=filter_arguments.b_type,
                             analog=filter_arguments.analog, fs=filter_arguments.fs)


def filter_signal(filter_arguments: FilterArguments, y: ndarray) -> ndarray:
    b, a = calc_filter(filter_arguments)
    return signal.lfilter(b, a, y)