'''
This module defines the methods to calculate the areal density, τ, k of a gas and its uncertainty.
'''


P_sat = lambda T: 610.78*10**((7.5*T-2048.625)/(T-35.85))

def τ(P_torr, T, Φ):
    '''
    @param T: temperature in °C
    @param P_torr: pressure in torr
    @param Φ: humidity in %
    @returns a function of linear distance in centimeters which represents the areal density in mg/cm^2.
    '''
    T = T + 273.15
    P = P_torr * 133.3224
    P_v = P_sat(T)*Φ
    P_d = P - P_v
    R_d = 287.058
    R_v = 461.495
    return lambda L : (L/T)*(P_d/R_d + P_v/R_v)
