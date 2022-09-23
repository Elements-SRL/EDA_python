import scipy
from numpy import ndarray
from scipy import signal
from scipy.signal import qspline1d, qspline1d_eval, cspline1d, cspline1d_eval


def butter(y, fs, wn, btype) -> ndarray:
    b, a = signal.iirfilter(4, Wn=wn, fs=fs, btype=btype, ftype="butter")
    return signal.filtfilt(b, a, y)


# reduce and smooth out high frequency noise with a quadratic spline
def quadratic_spline(x, y) -> ndarray:
    return qspline1d_eval(qspline1d(y), x)


# reduce and smooth out high frequency noise with a quadratic spline
def cubic_spline(x, y) -> ndarray:
    return cspline1d_eval(cspline1d(y), x)


def autocorrelation(values) -> ndarray:
    return signal.fftconvolve(values, values[::-1], mode="full")


def fft(y: ndarray, frequency) -> (ndarray, ndarray):
    yf = scipy.fft.fft(y)
    number_of_points = y.size
    xf = scipy.fft.fftfreq(number_of_points, 1/frequency)[:number_of_points//2]
    return xf, yf
