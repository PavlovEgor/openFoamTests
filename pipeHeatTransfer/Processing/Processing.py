import numpy as np
import matplotlib.pyplot as plt

import openfoamparser_mai as Ofpp
from scipy.interpolate import LinearNDInterpolator

import formating, hydro


path = "../cases/laminarCase/"

T, T_name = formating.find_time(path)
X = 0.48
R = 0.005
W = 0.015

U = Ofpp.parse_internal_field(path + T_name[-1] + "/U") 
T = Ofpp.parse_internal_field(path + T_name[-1] + "/T") 
Cx = Ofpp.parse_internal_field(path + T_name[-1] + '/Cx')  # x-координата элементов сетки | shape = (n, 1)
Cy = Ofpp.parse_internal_field(path + T_name[-1] + '/Cy')  # y-координата элементов сетки
Cz = Ofpp.parse_internal_field(path + T_name[-1] + '/Cz')  # z-координата элементов сетки

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

mask = ~np.isnan(T_line)

T_line = T_line[mask]
r_line = r_line[mask]
U_line = U_line[mask]

plt.plot(r_line/R, hydro.theta_2(T_line, U_line, r_line, X=X, w=W), 'o')
# plt.plot(r_line, T_line, 'o')

plt.plot(r_grid_an, hydro.thetaTheory(r_grid_an))

plt.show()

plt.plot(r_line/R, U_line, 'o')
plt.plot(r_grid_an, hydro.UTheory(r_grid_an, w=W))

plt.show()
