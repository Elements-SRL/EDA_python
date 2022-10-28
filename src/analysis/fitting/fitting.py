from typing import Iterable, Tuple

import numpy as np
from numpy import ndarray
from scipy.optimize import curve_fit


def linear_fitting(x: ndarray, y: ndarray, measuring_unit_x: str = "*", measuring_unit_y: str = "*") -> (ndarray, Iterable[Tuple[str, float]]):
    a = "a[" + measuring_unit_y + "/" + measuring_unit_x + "]"
    return _compute_curve_fit(x, y, _linear, [a, "b[*]"])


def quadratic_fitting(x: ndarray, y: ndarray, measuring_unit_x: str = "*", measuring_unit_y: str = "*") -> (ndarray, Iterable[Tuple[str, float]]):
    a = "a[" + measuring_unit_y + "/" + measuring_unit_x + "^2]"
    b = "b[" + measuring_unit_y + "/" + measuring_unit_x + "]"
    return _compute_curve_fit(x, y, _quadratic, [a, b, "c[*]"])


def exponential_fitting(x: ndarray, y: ndarray, measuring_unit_x: str = "*", measuring_unit_y: str = "*") -> (ndarray, Iterable[Tuple[str, float]]):
    b = "b[" + measuring_unit_x + "^-1]"
    return _compute_curve_fit(x, y, _exponential, ["a[" + measuring_unit_y + "]", b])


def power_law_fitting(x: ndarray, y: ndarray, measuring_unit_x: str = "*", measuring_unit_y: str = "*") -> (ndarray, Iterable[Tuple[str, float]]):
    return _compute_curve_fit(x, y, _power_law, ["a[" + measuring_unit_y + "/" + measuring_unit_x + "^b]", "b[*]"])


def gaussian_fitting(x: ndarray, y: ndarray, measuring_unit_x: str = "*", measuring_unit_y: str = "*") -> (ndarray, Iterable[Tuple[str, float]]):
    return _compute_curve_fit(x, y, _gaussian, ["a[" + measuring_unit_y + "]", "b[" + measuring_unit_x + "]",
                                                "c[" + measuring_unit_x + "]"], [y.max(), x[x.size // 2], x.size / 4])


def boltzmann_fitting(x: ndarray, y: ndarray, measuring_unit_x: str = "*", measuring_unit_y: str = "*") -> (ndarray, Iterable[Tuple[str, float]]):
    s = "s[" + measuring_unit_y + "/" + measuring_unit_x + "]"
    return _compute_curve_fit(x, y, _boltzmann, ["t[" + measuring_unit_y + "]", "b[" + measuring_unit_y + "]",
                                                 s, "m[" + measuring_unit_x + "]"])


def _linear(x: ndarray, a: float, b: float):
    """Function to calculate the linear with constants a and b"""
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


def _boltzmann(x: ndarray, t: float, b: float, s: float, m: float):
    """Function to calculate the boltzmann sigmoid with constants t, b, s and m"""
    return b + (t - b) / (1 + np.exp(4 * s * (m - x) / (t - b)))


def _compute_curve_fit(x: ndarray, y: ndarray, func, constants: Iterable[str], p0=None) -> (ndarray, Iterable[Tuple[str, float]]):
    popt, pcov = curve_fit(f=func, xdata=x, ydata=y, p0=p0)
    perr: ndarray = np.sqrt(np.diag(pcov))
    if np.inf in perr:
        raise Exception("Couldn't optimize this function")
    constants_to_values = zip(constants, popt)
    return func(x, *popt), constants_to_values
