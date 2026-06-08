import numpy as np
import matplotlib.pyplot as plt

def acc(X, Y):
    return (Y / (np.exp(lgb) * X ** ( k))) ** -1

def plot(ax, data, color, label, marker="o", linestyle="--"):

    Ns = data[:, 0]      # первый столбец - ось X
    time = data[:, 1]    # второй столбец - первая ось Y
    itNum = data[:, 2]   # третий столбец - первая ось Y

    # ax.plot(Ns**3, (timeCPU/itNumCPU) / (time/itNum), color=color, marker=marker, linestyle=linestyle, label=label)
    ax.plot(Ns**3, acc(Ns**3, time/ itNum), color=color, marker=marker, linestyle=linestyle, label=label)

def plot2(ax, data, color, label, marker="o", linestyle="--"):

    Ns = data[:, 0]      # первый столбец - ось X
    time = data[:, 1]    # второй столбец - первая ось Y
    itNum = data[:, 2]   # третий столбец - первая ось Y

    n = data.shape[0]

    ax.plot(Ns**3, (timeCPU[:n]/itNumCPU[:n]) / (time/ itNum), color=color, marker=marker, linestyle=linestyle, label=label)

# Загружаем данные из файла
dataCPU = np.loadtxt('data4CPU_3D.txt')
dataCPU6 = np.loadtxt('data6CPU_3D.txt')
data4CPU_PETSC = np.loadtxt('data4CPU_3D_PETSC_fgmres.txt')

# Разделяем на колонки
NsCPU = dataCPU[:, 0]      # первый столбец - ось X
timeCPU = dataCPU[:, 1]    # второй столбец - первая ось Y
itNumCPU = dataCPU[:, 2]   # третий столбец - первая ось Y

X = np.log(NsCPU**3)
Y = np.log(timeCPU/itNumCPU)
k = np.cov(X, Y, ddof=0)[0,1] / np.var(X)
lgb = np.mean(Y) - k * np.mean(X)


dataGPU = np.loadtxt('dataGPU_PETSC_HYPRE_per100.txt')
# Создаем фигуру и основную ось
fig, ax1 = plt.subplots(figsize=(10, 6))

# Графики для первой оси Y (левая)
colors = plt.cm.tab10.colors
ax1.set_xlabel('Количество ячеек')
ax1.set_ylabel('Ускорение', color='tab:green')
ax1.set_title("Зависимость ускорения от размера сетки относительно 4 CPU")


plot(ax1, dataCPU, color=colors[1], marker='o', linestyle='-', label=r'4xCPU')
plot(ax1, dataCPU6, color=colors[2], marker='o', linestyle='-', label=r'6xCPU')
plot(ax1, dataGPU, color=colors[3], marker='o', linestyle='--', label=r'SPUMA PETSC (per-100)')
plot2(ax1, data4CPU_PETSC, color=colors[4], marker='o', linestyle='--', label=r'4xCPU PETSC')



ax1.tick_params(axis='y', labelcolor='tab:green')
ax1.legend(loc='upper left')
# ax1.set_xlim(1e2, 
#              1e3)

# Создаем верхнюю ось X
# ax3 = ax1.twiny()
# ax3.set_xlabel('Общее количество ячеек', fontsize=12)
# ax3.set_xlim(ax1.get_xlim())  # Устанавливаем те же границы, что и у нижней оси

# ax3.set_xlim((ax1.get_xlim()[0] ** 2), 
#              (ax1.get_xlim()[1] ** 2))
# Добавляем заголовок
# plt.title('График с двумя осями Y')

# Добавляем сетку для лучшей читаемости
ax1.grid(True, alpha=0.3)
# ax1.set_yscale('log')  
# ax2.set_yscale('log')
ax1.set_xscale('log') 

# Автоматическая подгонка макета
plt.tight_layout()

# Показываем график
# plt.show()

# (Опционально) сохраняем график
plt.savefig('data3.png', dpi=300, bbox_inches='tight')