from numpy import ndarray
from scipy import signal

from src.filters.filter_arguments import FilterArguments


def calc_filter(filter_arguments: FilterArguments) -> (ndarray, ndarray):
    cutoff = [filter_arguments.cutoff_frequency,
              filter_arguments.other_cutoff_frequency] if filter_arguments.b_type in ["bandpass", "bandstop"]\
        else filter_arguments.cutoff_frequency
    if filter_arguments.filter_type == "butter":
        return signal.butter(N=filter_arguments.order, Wn=cutoff, btype=filter_arguments.b_type,
                             analog=filter_arguments.analog, fs=filter_arguments.fs)
    elif filter_arguments.filter_type == "bessel":
        return signal.bessel(N=filter_arguments.order, Wn=cutoff, btype=filter_arguments.b_type,
                             analog=filter_arguments.analog, fs=filter_arguments.fs)
    elif filter_arguments.filter_type == "cheby1":
        return signal.cheby1(N=filter_arguments.order, Wn=cutoff, btype=filter_arguments.b_type,
                             analog=filter_arguments.analog, fs=filter_arguments.fs, rp=0.5)
    # elif filter_arguments.filter_type == "cheby2":
    #     return signal.cheby2(N=filter_arguments.order, Wn=cutoff, btype=filter_arguments.b_type,
    #                          analog=filter_arguments.analog, fs=filter_arguments.fs, rs=60.0)


def filter_signal(filter_arguments: FilterArguments, y: ndarray) -> ndarray:
    b, a = calc_filter(filter_arguments)
    return signal.lfilter(b, a, y)
