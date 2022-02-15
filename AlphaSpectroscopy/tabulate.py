from scipy.constants import *
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

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


# plt.style.use(['science'])

# def Bethe_Bloch(E):
#     I = 32.5*micro
#     Z_p = 2
#     Z_t = 14.4
#     N = 2 / 14.4 * Avogadro
#     r_e = 2.8179*10**(-15)
#     B = Z_t*np.log(4 * m_e*E / (m_p * I * micro)) - 0.9
#     # print(B)
#     return 2*np.pi*r_e**2 * (0.511)**2 * Z_p**2 * N * m_p/m_e * B / E

# x = np.linspace(0.1, 5.3, 100)
# plt.plot(table2[:,1], - table2[:,2], '.', color = 'black', label='Experimental')
# plt.plot(x, Bethe_Bloch(x), color='red', label='Bethe-Bloch')
# plt.ylabel(r'Energy loss $-\frac{dE_p}{d\tau}$ MeV cm${}^2/$mg')
# plt.xlabel(r'Alpha energy $E_p$ MeV')
# plt.legend()
# plt.savefig('EnergyLoss.png')
# plt.show()

# plt.errorbar(table1[:,0], table1[:,1], yerr=table1[:,4], fmt='.', color='black')
# plt.ylabel(r'Energy $E_p$ MeV')
# plt.xlabel(r'Areal Density $\tau$ mg/cm${}^2$')

linear = lambda x, m, b: m*x + b
pars, cov = curve_fit(linear, table1[13:,0], table1[13:,1], sigma=table1[13:,4])
print(cov)
print(pars)
taus = np.arange(3, 4.5, 0.1)
plt.plot(taus, [linear(x, *pars) for x in taus], 'r-')

# plt.savefig('Energy.png')

# plt.plot(table1[:,0], table1[:,2], '.', color='black')
# plt.ylabel(r'$FWHM$ MeV')
# plt.xlabel(r'Areal Density $\tau$ mg/cm${}^2$')
# plt.savefig('FWHM.png')

plt.plot(table1[:,0], table1[:,3], '.')
plt.ylabel(r'$R$ Counts per second')
plt.xlabel(r'Areal Density $\tau$ mg/cm${}^2$')
plt.savefig('R.png')

print(-pars[1]/pars[0])

print(1/np.abs(pars[0])*np.sqrt(cov[1,1]**2 + pars[1]**2/pars[0]**2*cov[0,0]**2))

