import numpy as np
from numpy import ndarray
from scipy.optimize import curve_fit


def linear_fitting(x: ndarray, y: ndarray) -> (ndarray, ndarray):
    return _compute_curve_fit(x, y, _linear)


def quadratic_fitting(x: ndarray, y: ndarray) -> (ndarray, ndarray):
    return _compute_curve_fit(x, y, _quadratic)


def exponential_fitting(x: ndarray, y: ndarray) -> (ndarray, ndarray):
    return _compute_curve_fit(x, y, _exponential)


def power_law_fitting(x: ndarray, y: ndarray) -> (ndarray, ndarray):
    return _compute_curve_fit(x, y, _power_law)


def gaussian_fitting(x: ndarray, y: ndarray) -> (ndarray, ndarray):
    return _compute_curve_fit(x, y, _gaussian)


def _linear(x: ndarray, a: float, b: float):
    """Function to calculate the quadratic with constants a, b and c"""
    return a * x + b


def _quadratic(x: ndarray, a: float, b: float, c: float):
    """Function to calculate the quadratic with constants a, b and c"""
    return a * np.power(x, 2) + b * x + c


def _exponential(x: ndarray, a: float, b: float):
    """Function to calculate the exponential with constants a and b"""
    return a * np.exp(b * x)


# Function to calculate the power-law with constants a and b
def _power_law(x: ndarray, a: float, b: float):
    """Function to calculate the power law with constants a and b"""
    return a * np.power(x, b)


def _gaussian(x: ndarray, a: float, b: float, c: float):
    """Function to calculate the gaussian with constants a, b and c"""
    return a * np.exp(-np.power(x - b, 2) / (2 * np.power(c, 2)))


def _compute_curve_fit(x: ndarray, y: ndarray, func) -> (ndarray, ndarray):
    popt, _ = curve_fit(f=func, xdata=x, ydata=y)
    return func(x, *popt), popt
