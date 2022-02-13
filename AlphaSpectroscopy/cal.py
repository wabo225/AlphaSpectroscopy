import numpy as np
from matplotlib import pyplot as plt

'''
See \calibration.ipynb for more information about how these functions were generated.
'''

σ_x1 = 0.006000351703899834
σ_x2 = 0.49
x_1 = 6.009578539937767
y_1 = 0
x_2 = 418.60
y_2 = 5.3
σ_c = 2 # calculated as the sample standard deviation

σ_x1 = 1
σ_x2 = 1
σ_c = 4 # calculated as the sample standard deviation



def E(channel: int) -> float:
    '''
    returns the energy (keV) associated with a channel 
    '''
    return y_2*(channel - x_1)/(x_2 - x_1)

def σ_E(channel):
    return np.sqrt(
        y_2**2 * (channel - x_1)**2 / (x_2 - x_1)**4
        * (σ_x1**2 + σ_x2**2) + (y_2/(x_2-x_1)*σ_c)**2
        )

if __name__ == '__main__':
    channels = np.arange(300, 350)
    plt.errorbar(channels, E(channels), σ_E(channels), fmt='.')
    plt.xlabel('Channel')
    plt.ylabel('Energy')
    plt.show()