import openfoamparser_mai as Ofpp
import matplotlib.pyplot as plt
import numpy as np
import formating
from scipy.integrate import simpson


path = f"../case2D/"
n = 80

T, T_name = formating.find_time(path)
Temp = Ofpp.parse_internal_field(path + T_name[-1] + "/T")
Cx = Ofpp.parse_internal_field(path + T_name[-1] + "/Cx")
Cy = Ofpp.parse_internal_field(path + T_name[-1] + "/Cy")
U = Ofpp.parse_internal_field(path + T_name[-1] + "/U")

Temp = Temp.reshape(n, n)
Cx = Cx.reshape(n, n)
Cy = Cy.reshape(n, n)
U = U.reshape(n, n, 3)

Ux = U[:, :, 0]
Uy = U[:, :, 1]
speed = np.sqrt(Ux**2 + Uy**2)

plt.figure(figsize=(10, 8))

plt.imshow(Temp, extent=[Cx.min(), Cx.max(), Cy.min(), Cy.max()], 
           origin='lower', cmap='jet', aspect='auto')
plt.colorbar(label='Temperature')

step = 5  # шаг прореживания, можно изменить в зависимости от плотности сетки

# Создаем сетку координат для стрелок
x_quiver = Cx[::step, ::step]
y_quiver = Cy[::step, ::step]
ux_quiver = Ux[::step, ::step]
uy_quiver = Uy[::step, ::step]
speed_quiver = speed[::step, ::step]

for i in range(x_quiver.shape[0]):
    for j in range(x_quiver.shape[1]):
        # Нормализуем цвет на основе скорости
        norm_speed = (speed_quiver[i, j] - speed.min()) / (speed.max() - speed.min())
        # Выбираем цвет из colormap
        color = plt.cm.plasma(norm_speed)
        
        plt.quiver(x_quiver[i, j], y_quiver[i, j], 
                  ux_quiver[i, j], uy_quiver[i, j],
                  color=color, scale=1, width=0.003, alpha=0.8,
                  headwidth=3, headlength=4)

plt.xlabel('X coordinate')
plt.ylabel('Y coordinate')
plt.title('Temperature Field')
plt.grid(False)  # Можно включить сетку при необходимости
plt.tight_layout()
plt.show()


# Параметры
T_hot = 313            # температура горячей стенки [К]
T_cold = 293           # температура холодной стенки [К]
dT = T_hot - T_cold    # разность температур [К]
L = 0.016823             # характерный размер [м]

lam = 0.02565 
Cp = 1005
rho = 1.2
U0 = lam / (Cp * rho * L)
# Коэффициент перед градиентом
coefficient = L / dT

# Предположим, у вас есть данные:
# Temp - массив температур [n_points_y, n_points_x] или [n_x, n_y] в зависимости от индексации
# Cx - координаты x узлов сетки

# Для левой стенки (x_min)
# Берем первый слой ячеек (индекс 0) и слой ячеек рядом (индекс 1)
# Градиент: (T_wall - T_cell) / (x_wall - x_cell)
dx = Cx[0, 0] - Cx[0, 1]
dTdx_left = -(-3 * Temp[:, 0] + 4 * Temp[:, 1] - Temp[:, 2]) / (2 * dx)

# Для правой стенки (x_max)
# Берем последний слой ячеек (индекс -1) и слой рядом (индекс -2)
dTdx_right = -(-3 * Temp[:, -1] + 4 * Temp[:, -2] - Temp[:, -3]) / (2 * dx)

# Расчет локального числа Нуссельта
Nu_left_local = -coefficient * dTdx_left
Nu_right_local = coefficient * dTdx_right

# Расчет статистик для левой стенки
Nu_left_min = np.min(Nu_left_local)
Nu_left_max = np.max(Nu_left_local)
Nu_left_mean = simpson(Nu_left_local, x=Cx[0, :]) / (L * (1 - 1/n))#  np.mean(Nu_left_local)
Nu_left_std = np.std(Nu_left_local)

# Расчет статистик для правой стенки
Nu_right_min = np.min(Nu_right_local)
Nu_right_max = np.max(Nu_right_local)
Nu_right_mean = simpson(Nu_right_local, x=Cx[0, :]) / (L * (1 - 1/n))#  np.mean(Nu_right_local)
Nu_right_std = np.std(Nu_right_local)

# Вывод результатов
print("=" * 50)
print("ЛЕВАЯ СТЕНКА (горячая, T = {} K)".format(T_hot))
print("-" * 50)
print("Минимальное Nu:     {:.4f}".format(Nu_left_min))
print("Максимальное Nu:    {:.4f}".format(Nu_left_max))
print("Среднее Nu:         {:.4f}".format(Nu_left_mean))
print("Станд. отклонение:  {:.4f}".format(Nu_left_std))
print()
print("ПРАВАЯ СТЕНКА (холодная, T = {} K)".format(T_cold))
print("-" * 50)
print("Минимальное Nu:     {:.4f}".format(Nu_right_min))
print("Максимальное Nu:    {:.4f}".format(Nu_right_max))
print("Среднее Nu:         {:.4f}".format(Nu_right_mean))
print("Станд. отклонение:  {:.4f}".format(Nu_right_std))
print()
print("СКОРОСТИ")
print("-" * 50)
print("Минимальное U:     {:.4f}".format(-np.min(Ux) / U0))
print("Максимальное U:    {:.4f}".format(np.max(Ux) / U0))
print("Минимальное U:     {:.4f}".format(-np.min(Uy) / U0))
print("Максимальное U:    {:.4f}".format(np.max(Uy) / U0))
print("=" * 50)
