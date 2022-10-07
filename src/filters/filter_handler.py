from numpy import ndarray
from scipy import signal
from src.filters.filter_arguments import FilterArguments as FiAr


def filter_preview(filter_arguments: FiAr) -> (ndarray, ndarray):
    cutoff = [filter_arguments.cutoff_frequency,
              filter_arguments.other_cutoff_frequency] if filter_arguments.b_type in ["bandpass", "bandstop"]\
        else filter_arguments.cutoff_frequency
    if filter_arguments.filter_type == "butter":
        return signal.butter(N=filter_arguments.order, Wn=cutoff, btype=filter_arguments.b_type,
                             analog=filter_arguments.analog)
# def filter_signal(filter_arguments: FiAr, x: ndarray, y:ndarray) -> (ndarray, ndarray):

