import openfoamparser_mai as Ofpp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import LinearNDInterpolator


def is_float(value):
    try:
        a = float(value)
        if a > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def find_time(dir_name=''):
    dir_list = os.listdir(dir_name)
    T = []
    T_name = []

    for name in dir_list:
        if is_float(name):
            T.append(float(name))
            T_name.append(name)

    combined = list(zip(T, T_name))
    sorted_combined = sorted(combined, key=lambda x: x[0])

    return zip(*sorted_combined)


def Dirichlet_sol(r, T1=200, T0=300, R1 = 4.5, R0 = 4.0):
    return T1 - (T1 - T0) * np.log(r / R1) / np.log(R0/R1)


def Neuman_sol(r, T0=200, R1 = 4.0e-3, R0 = 4.5, ql = 52e3):
    return T0 + ql * R1 * np.log(R0 / r)

def TheoreticalModel(r, T0=300, R1 = 1.0, R0 = 4.0, ql = 1e8/2.5):
    return T0 + 0.25 * ql * ((R0 * 1e-3) ** 2) * (1 - ((r/R0) ** 2) + 2 * ((R1/R0) ** 2) * np.log(r/R0))

path = "."
T, T_name = find_time(path)

Temp = Ofpp.parse_internal_field(T_name[-1] + "/T") 
Cx = Ofpp.parse_internal_field(T_name[-1] + "/Cx") 
Cy = Ofpp.parse_internal_field(T_name[-1] + "/Cy") 

D = 0.009
delta = 0.0005
center = (D/2 - delta, 0, 0)
point_end = (D/2, 0, 0)


# Создаём интерполятор
points = np.column_stack((Cx, Cy))
interpolatorT = LinearNDInterpolator(points, Temp)

# Генерируем точки на отрезке
num_points = 50
x_line = np.linspace(center[0], point_end[0], num_points)
y_line = np.linspace(center[1], point_end[1], num_points)
line_points = np.column_stack((x_line, y_line))


T_line = interpolatorT(line_points)
r_line = np.sqrt(x_line ** 2 + y_line ** 2)

r_grid_an = np.linspace(D/2 - delta, D/2, 100)

plt.plot(r_line, T_line, 's')
# plt.plot(r_grid_an, Neuman_sol(r_grid_an))
plt.plot(r_grid_an, Dirichlet_sol(r_grid_an * 1e3))
# plt.plot(r_grid_an, TheoreticalModel(r_grid_an))


plt.show()
