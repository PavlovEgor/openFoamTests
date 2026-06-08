import numpy as np
import matplotlib.pyplot as plt

def acc(X, Y):
    return (Y / (np.exp(lgb) * X ** (k))) ** -1

def plot(ax, data, color, label, marker="o", linestyle="--"):

    Ns = data[:, 0]      # первый столбец - ось X
    time = data[:, 1]    # второй столбец - первая ось Y
    itNum = data[:, 2]   # третий столбец - первая ось Y

    ax.plot(Ns**3, time / itNum, color=color, marker=marker, linestyle=linestyle, label=label)

# Загружаем данные из файла
dataCPU = np.loadtxt('data4CPU_3D.txt')
dataCPU6 = np.loadtxt('data6CPU_3D.txt')
dataGPU = np.loadtxt('dataGPU_PETSC_HYPRE_per100.txt')
data4CPU_PETSC = np.loadtxt('data4CPU_3D_PETSC_fgmres.txt')

NsCPU = dataCPU[:, 0]      # первый столбец - ось X
timeCPU = dataCPU[:, 1]    # второй столбец - первая ось Y
itNumCPU = dataCPU[:, 2]   # третий столбец - первая ось Y

X = np.log(NsCPU**3)
Y = np.log(timeCPU/itNumCPU)
k = np.cov(X, Y, ddof=0)[0,1] / np.var(X)
lgb = np.mean(Y) - k * np.mean(X)

# Создаем фигуру и основную ось
fig, ax1 = plt.subplots(figsize=(10, 6))

# Графики для первой оси Y (левая)
color1 = 'tab:red'
color2 = 'tab:blue'
color3 = 'tab:purple'
color4 = 'tab:green'
color5 = 'tab:pink'
ax1.set_xlabel('Количество ячеек на стороне квадрата')
ax1.set_ylabel('Время расчета на одну итерацию, c', color='tab:green')

plot(ax1, dataCPU, color=color1, marker='o', linestyle='-', label=r'time 4xCPU')
plot(ax1, dataCPU6, color=color3, marker='o', linestyle='-', label=r'time 6xCPU')
plot(ax1, dataGPU, color=color2, marker='o', linestyle='--', label=r'time GPU PETSC HYPRE T4')
plot(ax1, data4CPU_PETSC, color=color4, marker='o', linestyle='--', label=r'4xCPU PETSC')
ax1.plot(NsCPU**3, np.exp(lgb) * (NsCPU**3) ** (k), color=color4, marker='o', linestyle='-', label="fit")
# plot(ax1, dataGPU_AMGX_T4, color=color3, marker='o', linestyle='--', label=r'time GPU AmgX T4')
# plot(ax1, dataGPU_AMGX_SPUMA_T4, color=color4, marker='o', linestyle='--', label=r'time GPU SPUMA AmgX T4')

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
ax1.set_yscale('log')  
# ax2.set_yscale('log')
ax1.set_xscale('log') 

# Автоматическая подгонка макета
plt.tight_layout()

# Показываем график
# plt.show()

# (Опционально) сохраняем график
plt.savefig('data.png', dpi=300, bbox_inches='tight')
plt.show()