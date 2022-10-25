from typing import Iterable, Tuple

import numpy as np
from numpy import ndarray
from scipy.optimize import curve_fit


def linear_fitting(x: ndarray, y: ndarray) -> (ndarray, Iterable[Tuple[str, float]]):
    return _compute_curve_fit(x, y, _linear, ["a", "b"])


def quadratic_fitting(x: ndarray, y: ndarray) -> (ndarray, Iterable[Tuple[str, float]]):
    return _compute_curve_fit(x, y, _quadratic, ["a", "b", "c"])


def exponential_fitting(x: ndarray, y: ndarray) -> (ndarray, Iterable[Tuple[str, float]]):
    return _compute_curve_fit(x, y, _exponential, ["a", "b"])


def power_law_fitting(x: ndarray, y: ndarray) -> (ndarray, Iterable[Tuple[str, float]]):
    return _compute_curve_fit(x, y, _power_law, ["a", "b"])


def gaussian_fitting(x: ndarray, y: ndarray) -> (ndarray, Iterable[Tuple[str, float]]):
    return _compute_curve_fit(x, y, _gaussian, ["a", "m", "s"])


def boltzmann_fitting(x: ndarray, y: ndarray) -> (ndarray, Iterable[Tuple[str, float]]):
    new_y, popt = _compute_curve_fit(x, y, _boltzmann, ["t", "b", "s", "m"])
    return new_y, [9]


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


def _compute_curve_fit(x: ndarray, y: ndarray, func, constants: Iterable[str]) -> (ndarray, Iterable[Tuple[str, float]]):
    popt, _ = curve_fit(f=func, xdata=x, ydata=y)
    constants_to_values = zip(constants, popt)
    return func(x, *popt), constants_to_values
