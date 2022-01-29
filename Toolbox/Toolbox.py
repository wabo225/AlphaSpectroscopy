from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

def get_columns(filename: str, columns = None) -> np.ndarray:
    """
    Returns a numpy array of the columns in the file
    """
    if columns is None:
        return np.genfromtxt(filename, delimiter=',')
    return np.genfromtxt(filename, delimiter=',', usecols=columns)

# 1
def sample_mean(filename):
    data = get_columns(filename, columns = [0])
    return np.mean(data)

def sample_variance(filename):
    data = get_columns(filename, columns = [0])
    return np.var(data)

def sample_std(filename):
    data = get_columns(filename, columns = [0])
    return np.std(data)

# 2
def weighted_mean(filename):
    data = get_columns(filename, columns = [0,1])
    return np.average(data[:,0], weights=data[:,1])

# 3 make a transformation between a measured variable and its uncertainty (y, sigmay) to a new variable and its uncertainty
def transform_log(filename):
    data = get_columns(filename, columns = [0,1])
    # write to a file if you want to
    return np.log(data[:,0]), np.log(data[:,1])

# 4
def linear_plot(filename):
    data = get_columns(filename, columns = [0,1,2])
    plt.errorbar(data[:,0], data[:,1], yerr=data[:,2], fmt='o')
    # formatting should be done after the plot is created

# 5
def semi_log_plot(filename):
    data = get_columns(filename, columns = [0,1,2])
    plt.errorbar(data[:,0], data[:,1], yerr=data[:,2], fmt='o', yscale='log')

# 7 Given a set of data with their associated uncertainties, do a linear regression fit to a function of the form y = ax

def direct_regression(filename):
    data = get_columns(filename, columns = [0,1,2])
    # write to a file if you want to
    
    pars, cov = curve_fit(lambda a, x : a*x, data[0], data[1], sigma=data[2])
    return pars, cov

def linear_regression(filename):
    data = get_columns(filename, columns = [0,1,2])
    # write to a file if you want to
    pars, cov = curve_fit(lambda a, b, x : a*x+b, data[0], data[1], sigma=data[2])
    return pars, cov

def main():
    pass

if __name__ == '__main__':
    main()