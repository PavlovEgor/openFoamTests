import numpy as np
import matplotlib.pyplot as plt
import re
import subprocess
import openfoamparser_mai as Ofpp
from scipy.interpolate import LinearNDInterpolator
import os


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


def Lambda(dP, Re, D=0.01, L=0.5, nu=1e-6):
    return (dP / (Re ** 2)) * ((2 * (D ** 3)) / (L * (nu ** 2)))


def setU(path, U):
    with open(path + "0.orig/U", 'r') as file:
        content = file.read()

    # Ищем строку с value uniform ( ... );
    pattern = r'(value\s+uniform\s*\(\s*[\d\.]+\s+[\d\.]+\s+[\d\.]+\s*\);)'
    replacement = f'value           uniform (0 0 {U});'

    # Заменяем найденное значение
    new_content = re.sub(pattern, replacement, content)

    with open(path + "0.orig/U", 'w') as file:
        file.write(new_content)


def setControlDict(path, U, L=0.55):
    with open(path + "system/controlDict", 'r') as file:
        content = file.read()

    T = 0.2 * L / U
    # Ищем строку с value uniform ( ... );
    pattern = r'(endTime\s+)[\d\.]+;'
    replacement = f'endTime         {T};'

    pattern2 = r'(writeInterval\s+)[\d\.]+;'
    replacement2 = f'writeInterval         {T/10};'

    # Заменяем найденное значение
    new_content = re.sub(pattern, replacement, content)
    new_content = re.sub(pattern2, replacement2, new_content)

    with open(path + "system/controlDict", 'w') as file:
        file.write(new_content)


def ReToU(Re, D=0.01, nu=1e-6):
    return nu * Re / D


def thetaTheory(r):
    return 0.5 * ((r) ** 2) - 0.125 * ((r) ** 4) - 7/48


def theta_2(T, T0=773, X=0.48, w=0.03, Cp=147.3, rho=1.05e4, l=17.5, d=0.01, ql=57e3):
    Pe = Cp * rho * w * d / l
    # return ((T - T0) / (ql * d)) + 4 * X / (d * Pe)
    return ((T - np.mean(T)) / (ql * d))



def UTheory(r, w=0.003):
    return 2 * w * (1 - (r ** 2))


print(ReToU(1000, D=0.01, nu=1.5e-7))

path = "."

T, T_name = find_time(path)
X = 0.48
R = 0.005
W = 0.015

U = Ofpp.parse_internal_field(T_name[-1] + "/U") 
T = Ofpp.parse_internal_field(T_name[-1] + "/T") 
Cx = Ofpp.parse_internal_field(T_name[-1] + '/Cx')  # x-координата элементов сетки | shape = (n, 1)
Cy = Ofpp.parse_internal_field(T_name[-1] + '/Cy')  # y-координата элементов сетки
Cz = Ofpp.parse_internal_field(T_name[-1] + '/Cz')  # z-координата элементов сетки

center = (0, 0, X)
point_end = ((R - 0.0002) / np.sqrt(2), (R - 0.0002) / np.sqrt(2), X)


# Создаём интерполятор
points = np.column_stack((Cx, Cy, Cz))
interpolatorT = LinearNDInterpolator(points, T)
interpolatorU = LinearNDInterpolator(points, U[:, 2])

# Генерируем точки на отрезке
num_points = 20
t = np.linspace(0, 1, num_points)
x_line = np.linspace(center[0], point_end[0], num_points)
y_line = np.linspace(center[1], point_end[1], num_points)
z_line = np.linspace(center[2], point_end[2], num_points)
line_points = np.column_stack((x_line, y_line, z_line))


# Интерполируем значения на отрезке
T_line = interpolatorT(line_points)
U_line = interpolatorU(line_points)

r_line = np.sqrt(x_line ** 2 + y_line ** 2)

r_grid_an = np.linspace(0, 1, 100)


plt.plot(r_line/R, theta_2(T_line, X=X, w=W), 'o')
# plt.plot(r_line, T_line, 'o')

plt.plot(r_grid_an, thetaTheory(r_grid_an))

plt.show()

plt.plot(r_line/R, U_line, 'o')
plt.plot(r_grid_an, UTheory(r_grid_an, w=W))

plt.show()
