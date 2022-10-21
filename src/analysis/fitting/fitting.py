import numpy as np
from matplotlib import pyplot as plt


# Function to calculate the exponential with constants a and b
from scipy.optimize import curve_fit


def exponential(x, a, b):
    return a * np.exp(b * x)


# Function to calculate the power-law with constants a and b
def power_law(x, a, b):
    return a*np.power(x, b)


# Function to calculate the Gaussian with constants a, b, and c
def gaussian(x, a, b, c):
    return a * np.exp(-np.power(x - b, 2) / (2 * np.power(c, 2)))


def try_exponential_fitting():
    # Generate dummy dataset
    x_dummy = np.linspace(5, 15, 50)
    # Calculate y-values based on dummy x-values
    y_dummy = exponential(x_dummy, 0.5, 0.5)
    # Add noise from a Gaussian distribution
    noise = 5 * np.random.normal(size=y_dummy.size)
    y_dummy = y_dummy + noise
    # Plot the noisy exponential data
    fig, ax = plt.subplots()
    ax.scatter(x_dummy, y_dummy, s=20, color='#00b3b3', label='Data')
    # ax.set_yscale('log')
    # plt.show()
    pars, cov = curve_fit(f=exponential, xdata=x_dummy, ydata=y_dummy, p0=[0, 0], bounds=(-np.inf, np.inf))
    # Get the standard deviations of the parameters (square roots of the # diagonal of the covariance)
    stdevs = np.sqrt(np.diag(cov))
    # Calculate the residuals
    res = y_dummy - exponential(x_dummy, *pars)
    ax.plot(x_dummy, exponential(x_dummy, *pars), linestyle='--', linewidth=2, color='black')
    plt.show()


def try_power_law_fitting():
    # Generate dummy dataset
    x_dummy = np.linspace(start=1, stop=1000, num=100)
    y_dummy = power_law(x_dummy, 1, 0.5)
    # Add noise from a Gaussian distribution
    noise = 1.5 * np.random.normal(size=y_dummy.size)
    y_dummy = y_dummy + noise
    fig, ax = plt.subplots()
    # Set the x and y-axis scaling to logarithmic
    ax.set_xscale('log')
    ax.set_yscale('log')
    # # Edit the major and minor tick locations of x and y axes
    # ax.xaxis.set_major_locator(mpl.ticker.LogLocator(base=10.0))
    # ax.yaxis.set_major_locator(mpl.ticker.LogLocator(base=10.0))
    # Set the axis limits
    ax.set_xlim(10, 1000)
    ax.set_ylim(1, 100)
    # Fit the dummy power-law data
    pars, cov = curve_fit(f=power_law, xdata=x_dummy, ydata=y_dummy, p0=[0, 0], bounds=(-np.inf, np.inf))
    # Get the standard deviations of the parameters (square roots of the # diagonal of the covariance)
    stdevs = np.sqrt(np.diag(cov))
    # Calculate the residuals
    res = y_dummy - power_law(x_dummy, *pars)
    ax.scatter(x_dummy, y_dummy, s=20, color='#00b3b3', label='Data')
    ax.plot(x_dummy, power_law(x_dummy, *pars), linestyle='--', linewidth=2, color='black')
    plt.show()


def try_gaussian_peak_fitting():
    # Generate dummy dataset
    x_dummy = np.linspace(start=-10, stop=10, num=100)
    y_dummy = gaussian(x_dummy, 8, -1, 3)
    # Add noise from a Gaussian distribution
    noise = 0.5 * np.random.normal(size=y_dummy.size)
    y_dummy = y_dummy + noise
    # Fit the dummy Gaussian data
    # pars, cov = curve_fit(f=gaussian, xdata=x_dummy, ydata=y_dummy, p0=[0, 0, 0], bounds=(-np.inf, np.inf))

    # Fit the dummy Gaussian data
    pars, cov = curve_fit(f=gaussian, xdata=x_dummy, ydata=y_dummy, p0=[5, -1, 1], bounds=(-np.inf, np.inf))
    fig, ax = plt.subplots()
    # Get the standard deviations of the parameters (square roots of the # diagonal of the covariance)
    stdevs = np.sqrt(np.diag(cov))
    # if stdevs contains inf fitting did not succeed
    # Calculate the residuals
    res = y_dummy - gaussian(x_dummy, *pars)
    ax.scatter(x_dummy, y_dummy, s=20, color='#00b3b3', label='Data')
    ax.plot(x_dummy, gaussian(x_dummy, *pars), linestyle='--', linewidth=2, color='black')
    plt.show()
