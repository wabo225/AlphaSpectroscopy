from gc import callbacks
from scipy.constants import *
import numpy as np
from matplotlib import pyplot as plt
import mca
from arealDensity import τ

path = ('datafiles', 'spectrum')


# τ_p | E_p | FWHM | R
table1 = np.zeros((mca.trials(*path), 5))

i = 0
def callback(data, i):
    table1[i, 0] = τ(data['pressure'], data['temperature'], 0.2)(4)
    table1[i, 1] = data['E_p']
    table1[i, 2] = data['FWHM']
    table1[i, 3] = data['R']
    table1[i, 4] = data['σ_E_p']

mca.map_folder(*path, callback) # this is not garanteed to iterate through the files in alphabetical order

table1 = table1[table1[:,0].argsort()] # sort the table by the τ column.

# τ_m | E_m | dE/dτ
table2 = np.zeros((mca.trials(*path)-1, 3)) # create a new table with 1 less row

for i in range(len(table2)):
    table2[i, 0] = np.mean(table1[i:i+2, 0])
    table2[i, 1] = np.mean(table1[i:i+2, 1])
    table2[i, 2] = (table1[i, 1] - table1[i+1, 1])/(table1[i, 0] - table1[i+1, 0])

np.savetxt('table1.txt', table1)
np.savetxt('table2.txt', table2)

# plt.style.use(['science', 'ieee'])
# plt.plot(table2[:,1], - table2[:,2], '.')
# plt.ylabel(r'Energy loss $-\frac{dE_p}{d\tau}$ MeV cm${}^2/g$')
# plt.xlabel(r'Alpha energy $E_p$ MeV')
# plt.savefig('EnergyLoss.png')
# plt.show()

plt.errorbar(table1[:,0], table1[:,1], yerr=table1[:,4], fmt='.')
plt.ylabel(r'Energy $E_p$ MeV')
plt.xlabel(r'Areal Density $\tau$ g/cm${}^2$')
plt.savefig('Energy.png')

