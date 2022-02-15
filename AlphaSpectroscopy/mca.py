import numpy as np
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from os import walk
import re

import cal

trials = lambda folder, startswith: len([
    filename for filename in next(walk(folder), (None, None, []))[2] if filename.startswith(startswith)
    ])
'''returns the number of trials found in the folder'''

T = {
    '01/25/2022': 19.2,
    '01/27/2022': 19.6,
    '02/01/2022': 21.61,
    '02/08/2022': 19.0,
}

σ_T = 0.056

def FWHM(data: np.array) -> float:
    # d = np.convolve(data, np.hamming(20), mode='valid')
    d = data
    try:
        peak_channel = np.argmax(d)
        left = interp1d(d[:peak_channel], np.arange(peak_channel))
        right = interp1d(d[peak_channel:], np.arange(len(d)-peak_channel))
        l = left(0.5*d[peak_channel])
        r = right(0.5*d[peak_channel]) + peak_channel
        return cal.E(r) - cal.E(l)
    except ValueError:
        return 0

def E_p(data: np.array) -> float:
    # d = np.convolve(data, np.hamming(10), mode='valid')
    return cal.E(np.argmax(data))

# def σ_E_p(data: np.array) -> float:
#     d = np.convolve(data, np.hamming(10), mode='valid')
#     return σ_E_p(d)

def map_folder(folder: str, startswith: str, callback: callable):
    # accepts a callback function with a parameter for the data dict defined by extract_data
    filenames = next(walk(folder), (None, None, []))[2]
    trials = len(filenames)
    i = 0
    for filename in filenames:
        if filename.startswith(startswith):
            callback(extract_data(folder +'/' + filename), i)
            i+=1

def extract_data(filename: str) -> dict:
    with open(filename) as f:
        f.readline()
        f.readline()
        for i in range(5):
            f.readline()
        date = f.readline().split()[0]
        f.readline()
        meas_time, meas_live = f.readline().split()
        f.readline()
        shape = f.readline().split()
        data = [int(f.readline()) for i in range(int(shape[1]))]
        data[0:8] = [0,0,0,0,0,0,0,0]
        data = np.array(data)
    
    return {
        'date': date,
        'temperature': T[date],
        'pressure': int(re.findall('\d+', filename)[0]), # uses the filename to find the pressure in torr
        'meas_time': int(meas_time), # total measure time is kinda useless
        'meas_live': int(meas_live),
        'data': data, # perhaps this name needs work
        'peak_channel': np.argmax(data), # this is the channel with the highest counts
        'E_p': E_p(data), # the energy of the peak channel
        'σ_E_p': cal.σ_E(E_p(data)), # the uncertainty in the energy of the peak channel,
        'FWHM': FWHM(data),
        'R': np.sum(data)/int(meas_live) # counts per second
    }

if __name__ == "__main__":    
    filename = 'datafiles/spectrum7.Spe'
    data = extract_data(filename)
    
    print('\n   From file :', filename, '\n')
    print('        Date :', data['date'])
    print('           T :', data['temperature'], '(C)')
    print('           R :', data['R'], '(counts/sec)')
    print('    Pressure :', data['pressure'], '(torr)')
    print('Peak channel :', data['peak_channel']) 
    print('       σ_E_p :', data['σ_E_p'], ('MeV'))
    print(' Peak Energy :', data['E_p'], '(Mev)')
    print('        FWHM :', data['FWHM'], '(Mev)')

    plt.style.use('ieee')
    ch = np.arange(len(data['data']))
    plt.plot(cal.E(ch), data['data']/data['meas_live'], '-')
    plt.fill_between(cal.E(ch), data['data']/data['meas_live'], alpha=0.5)
    plt.show()