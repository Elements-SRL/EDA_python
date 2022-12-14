from typing import Iterable, Tuple, List

import numpy as np
from numpy import ndarray
from scipy.optimize import curve_fit


def _get_measuring_units(measuring_units: Tuple | None = None) -> Tuple[str, str]:
    """
    Get measuring units

    :param measuring_units: tuple containing measuring units for x and y respectively. Default is None
    :return: the input tuple if it is not None else ('*','*')
    """
    return ("*", "*") if measuring_units is None else measuring_units


def linear_fitting(x: ndarray, y: ndarray, m_units: Tuple | None = None) -> Tuple[ndarray,
                                                                                  Iterable[Tuple[str, float]]]:
    """
    Fit the data with linear equation

    :raise exception if the curve fitting can not be calculated
    :param x: x values
    :param y: y values
    :param m_units: measuring units of x and y
    :return: The curve which best fits the data and the list of constants with the associated value
    """
    measuring_unit_x, measuring_unit_y = _get_measuring_units(m_units)
    a = "a[" + measuring_unit_y + "/" + measuring_unit_x + "]"
    return _compute_curve_fit(x, y, _linear, [a, "b[*]"])


def quadratic_fitting(x: ndarray, y: ndarray, m_units: Tuple | None = None) -> Tuple[ndarray,
                                                                                     Iterable[Tuple[str, float]]]:
    """
    Fit the data with a quadratic curve

    :raise exception if the curve fitting can not be calculated
    :param x: x values
    :param y: y values
    :param m_units: measuring units of x and y
    :return: The curve which best fits the data and the list of constants with the associated value
    """
    measuring_unit_x, measuring_unit_y = _get_measuring_units(m_units)
    a = "a[" + measuring_unit_y + "/" + measuring_unit_x + "^2]"
    b = "b[" + measuring_unit_y + "/" + measuring_unit_x + "]"
    return _compute_curve_fit(x, y, _quadratic, [a, b, "c[*]"])


def exponential_fitting(x: ndarray, y: ndarray, m_units: Tuple | None = None) -> Tuple[ndarray,
                                                                                       Iterable[Tuple[str, float]]]:
    """
    Fit the data with exponential curve

    :raise exception if the curve fitting can not be calculated
    :param x: x values
    :param y: y values
    :param m_units: measuring units of x and y
    :return: The curve which best fits the data and the list of constants with the associated value
    """
    measuring_unit_x, measuring_unit_y = _get_measuring_units(m_units)
    b = "b[" + measuring_unit_x + "^-1]"
    return _compute_curve_fit(x, y, _exponential, ["a[" + measuring_unit_y + "]", b])


def power_law_fitting(x: ndarray, y: ndarray, m_units: Tuple | None = None) -> Tuple[ndarray,
                                                                                     Iterable[Tuple[str, float]]]:
    """
    Fit the data with Power law equation

    :raise exception if the curve fitting can not be calculated
    :param x: x values
    :param y: y values
    :param m_units: measuring units of x and y
    :return: The curve which best fits the data and the list of constants with the associated value
    """
    measuring_unit_x, measuring_unit_y = _get_measuring_units(m_units)
    return _compute_curve_fit(x, y, _power_law, ["a[" + measuring_unit_y + "/" + measuring_unit_x + "^b]", "b[*]"])


def gaussian_fitting(x: ndarray, y: ndarray, m_units: Tuple | None = None) -> Tuple[ndarray,
                                                                                    Iterable[Tuple[str, float]]]:
    """
    Fit the data with gaussian peak equation

    :raise exception if the curve fitting can not be calculated
    :param x: x values
    :param y: y values
    :param m_units: measuring units of x and y
    :return: The curve which best fits the data and the list of constants with the associated value
    """
    measuring_unit_x, measuring_unit_y = _get_measuring_units(m_units)
    return _compute_curve_fit(x, y, _gaussian, ["a[" + measuring_unit_y + "]", "b[" + measuring_unit_x + "]",
                                                "c[" + measuring_unit_x + "]"],
                              [y.max(), x[x.size // 2], (x[-1] - x[0]) / 4])


def boltzmann_fitting(x: ndarray, y: ndarray, m_units: Tuple | None = None) -> Tuple[ndarray,
                                                                                     Iterable[Tuple[str, float]]]:
    """
    Fit the data with boltzmann sigmoid equation

    :raise exception if the curve fitting can not be calculated
    :param x: x values
    :param y: y values
    :param m_units: measuring units of x and y
    :return: The curve which best fits the data and the list of constants with the associated value
    """
    measuring_unit_x, measuring_unit_y = _get_measuring_units(m_units)
    s_mu = "s[" + measuring_unit_y + "/" + measuring_unit_x + "]"
    t, b = y.max(), y.min()
    s = (t - b) / (x[-1] - x[0])
    return _compute_curve_fit(x, y, _boltzmann, ["t[" + measuring_unit_y + "]", "b[" + measuring_unit_y + "]",
                                                 s_mu, "m[" + measuring_unit_x + "]"], [t, b, s, x[x.size // 2]])


def _linear(x: ndarray, a: float, b: float):
    """
    Function to calculate the linear with constants a and b

    :param x: x values
    :param a: constant a
    :param b: constant b
    :return: Linear of array x with constants a, b
    """
    return a * x + b


def _quadratic(x: ndarray, a: float, b: float, c: float):
    """
    Function to calculate the quadratic with constants a, b and c

    :param x: x values
    :param a: constant a
    :param b: constant b
    :param c: constant c
    :return: Quadratic of array x with constants a, b and c
    """
    return a * np.power(x, 2) + b * x + c


def _exponential(x: ndarray, a: float, b: float):
    """
    Function to calculate the exponential with constants a and b

    :param x: x values
    :param a: constant a
    :param b: constant b
    :return: Exponential of array x with constants a, b
    """
    return a * np.exp(b * x)


# Function to calculate the power-law with constants a and b
def _power_law(x: ndarray, a: float, b: float):
    """
    Function to calculate the power law with constants a and b

    :param x: x values
    :param a: constant a
    :param b: constant b
    :return: Power law of array x with constants a, b
    """
    return a * np.power(x, b)


def _gaussian(x: ndarray, a: float, b: float, c: float):
    """
    Function to calculate the gaussian with constants a, b and c

    :param x: x values
    :param a: constant a
    :param b: constant b
    :param c: constant c
    :return: Gaussian peak of array x with constants a, b and c
    """
    return a * np.exp(-np.power(x - b, 2) / (2 * np.power(c, 2)))


def _boltzmann(x: ndarray, t: float, b: float, s: float, m: float):
    """Function to calculate the boltzmann sigmoid with constants t, b, s and m

    :param x: x values
    :param t: constant top
    :param b: constant bottom
    :param s: constant slope
    :param m: constant mean
    :return: boltzmann sigmoid of array x with constants a, b and c
    """
    return b + (t - b) / (1 + np.exp(4 * s * (m - x) / (t - b)))


def _compute_curve_fit(x: ndarray, y: ndarray, func, constants: Iterable[str], p0: List[float] | None = None
                       ) -> Tuple[ndarray, Iterable[Tuple[str, float]]]:
    """
    Compute fitting on given curve

    :raise exception if the curve fitting can not be calculated
    :param x: x values
    :param y: y values
    :param func: function to apply to the curve fit algorithm
    :param constants: the constants of the equation
    :param p0: List of initial values. Default is None
    :return: The curve which best fits the data and the list of constants with the associated value
    """
    popt, pcov = curve_fit(f=func, xdata=x, ydata=y, p0=p0)
    perr: ndarray = np.sqrt(np.diag(pcov))
    if np.inf in perr:
        raise Exception("Couldn't optimize this function")
    constants_to_values = list(zip(constants, popt))
    return func(x, *popt), constants_to_values
