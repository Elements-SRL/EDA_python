from numpy import ndarray
from scipy import signal


def spectral_analysis(x: ndarray, fs: float) -> (ndarray, ndarray):
    return signal.welch(x=x, fs=fs)
