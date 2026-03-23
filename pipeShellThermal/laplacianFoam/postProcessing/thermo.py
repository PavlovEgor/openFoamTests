import numpy as np


def Dirichlet_sol(r, T1=200, T0=300, R1 = 4.5, R0 = 4.0):
    return T1 - (T1 - T0) * np.log(r / R1) / np.log(R0/R1)


def Neuman_sol(r, T0=200, R1 = 4.0e-3, R0 = 4.5, ql = 52e3):
    return T0 + ql * R1 * np.log(R0 / r)


def mixedTask_sol(r, T0=300, R1 = 1.0, R0 = 4.0, ql = 1e8/2.5):
    return T0 + 0.25 * ql * ((R0 * 1e-3) ** 2) * (1 - ((r/R0) ** 2) + 2 * ((R1/R0) ** 2) * np.log(r/R0))

