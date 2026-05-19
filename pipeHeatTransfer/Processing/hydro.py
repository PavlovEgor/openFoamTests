import numpy as np
from scipy.optimize import newton


def Lambda(dP, Re, D=0.01, L=0.5, nu=1e-6):
    return (dP / (Re ** 2)) * ((2 * (D ** 3)) / (L * (nu ** 2)))


def ReToU(Re, D=0.01, nu=1e-6):
    return nu * Re / D


def BlasiusLow(Re):
    return 0.3164 / (Re ** 0.25)


def PrandlLow(Re):

    C = 0.8 - 2 * np.log10(Re)
    def PrFunc(x):
        return C + (x ** (-0.5)) - np.log10(x) 
    
    def PrFuncPrime(x):
        return -0.5 * (x ** (-1.5)) - np.log(10) / x
    
    root = newton(PrFunc, BlasiusLow(Re), PrFuncPrime)

    return root


def IdelchikLow(Re, l0, Delta=1e-3):

    a1 = 0
    b1 = 0
    c1 = 0

    if (Delta * Re * np.sqrt(l0) < 10) and (Delta * Re * np.sqrt(l0) > 3.6):
        a1 = -0.8
        b1 = 2.0
        c1 = 0
    elif (Delta * Re * np.sqrt(l0) < 20) and (Delta * Re * np.sqrt(l0) > 10):
        a1 = 0.068
        b1 = 1.13
        c1 = -0.87
    elif (Delta * Re * np.sqrt(l0) > 20) and (Delta * Re * np.sqrt(l0) < 40):
        a1 = 1.538
        b1 = 0.0
        c1 = -2.0
    elif (Delta * Re * np.sqrt(l0) > 40) and (Delta * Re * np.sqrt(l0) < 191.2):
        a1 = 2.471
        b1 = -0.588
        c1 = -2.588
    elif (Delta * Re * np.sqrt(l0) > 191.2):
        a1 = 1.138
        b1 = 0
        c1 = -2.0

        return (1.8 * np.log10(8.3 / Delta)) ** -2
    
    else:
        return PrandlLow(Re)
    
    C = - (a1 + b1 * np.log10(Re) + c1 * np.log10(Delta))

    def PrFunc(x):
        return C + (x ** (-0.5)) - (b1/2) * np.log10(x) 
    
    def PrFuncPrime(x):
        return -0.5 * (x ** (-1.5)) - (b1/2) * np.log(10) / x

    root = newton(PrFunc, BlasiusLow(Re), PrFuncPrime)

    return root

def thetaTheory(r):
    return 0.5 * ((r) ** 2) - 0.125 * ((r) ** 4) - 7/48


# def theta_2(T, T0=773, X=0.48, w=0.03, Cp=147.3, rho=1.05e4, l=17.5, d=0.01, ql=57e3):
#     Pe = Cp * rho * w * d / l
#     # return ((T - T0) / (ql * d)) + 4 * X / (d * Pe)
#     return ((T - np.mean(T)) / (ql * d))

def theta_2(T, u, r, T0=773, X=0.48, w=0.03, Cp=147.3, rho=1.05e4, l=17.5, d=0.01, ql=57e3):
    # Pe = Cp * rho * w * d / l
    # return ((T - T0) / (ql * d)) + 4 * X / (d * Pe)
    # return ((T - np.mean(T)) / (ql * d))

    # T_ave = np.sum(T[:-1] * u[:-1] * r[:-1] * (r[1:] - r[:-1])) / np.sum(u[:-1] * r[:-1] * (r[1:] - r[:-1]))
    # return ((T - T_ave) / (ql * d)) - (0.145-0.133)
    return ((T - T[0]) / (ql * d)) - 0.145

def UTheory(r, w=0.003):
    return 2 * w * (1 - (r ** 2))