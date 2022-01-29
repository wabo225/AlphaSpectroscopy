from os import walk

import mca
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

peaks = [44, 87, 109, 216, 431]
attentuation = [0.1, 0.2, 0.25, 0.5, 1]

path = 'datafiles'
filenames = next(walk(path), (None, None, []))[2]

for filename in filenames:
    if filename.startswith("MCAlibration"):
        data = mca.extract_data(path + '/' + filename)
        channels = data['data']/data['meas_live']
        # rolling average
        channels = np.convolve(channels, np.hamming(5))
        derivative = np.gradient(channels)
        plt.plot(channels)

pars, cov = curve_fit(lambda a, b, x : a*x + b, attentuation, peaks)

plt.show()