from os import walk
from mca import extract_data
import re
from matplotlib import pyplot as plt

# path = input("Enter the path to the folder: ")
path = 'datafiles'

filenames = next(walk(path), (None, None, []))[2]

for filename in filenames:
    if filename.startswith('spectrum'):
        pressure = re.findall('\d+', filename)[0] # torr
        data = extract_data(path + '/' + filename)
        plt.plot(data['data'] / data['meas_live'], label=f"{pressure} torr")

plt.xlabel("Channel")
plt.ylabel(rf"$average \alpha$-particles per second")
plt.legend()
plt.show()  