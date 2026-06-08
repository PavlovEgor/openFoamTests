import numpy as np
import matplotlib.pyplot as plt

def acc(X, Y):
    return (Y / (np.exp(lgb) * X ** ( k))) ** -1

def plot(ax, data, color, label, marker="o", linestyle="--"):

    Ns = data[:, 0]      # первый столбец - ось X
    time = data[:, 1]    # второй столбец - первая ось Y
    itNum = data[:, 2]   # третий столбец - первая ось Y

    n = data.shape[0]

    ax.plot(Ns**2, (timeCPU[:n]/itNumCPU[:n]) / (time/ itNum), color=color, marker=marker, linestyle=linestyle, label=label)

def plot2(ax, data, color, label, marker="o", linestyle="--"):

    Ns = data[:, 0]      # первый столбец - ось X
    time = data[:, 1]    # второй столбец - первая ось Y
    itNum = data[:, 2]   # третий столбец - первая ось Y

    ax.plot(Ns**2, acc(Ns**2, time/ itNum), color=color, marker=marker, linestyle=linestyle, label=label)

# Загружаем данные из файла
dataCPU = np.loadtxt('AMGX_CPU_vs_GPU/Inteli7_vs_RTX2060/dataCPU4.txt')
data1CPU_PETSC = np.loadtxt('data1CPU_2D_PETSC.txt')
data4CPU_PETSC = np.loadtxt('data4CPU_2D_PETSC_fgmres.txt')
dataCPU = np.loadtxt('data4CPU_2D_PETSC.txt')



# Разделяем на колонки
NsCPU = dataCPU[:, 0]      # первый столбец - ось X
timeCPU = dataCPU[:, 1]    # второй столбец - первая ось Y
itNumCPU = dataCPU[:, 2]   # третий столбец - первая ось Y

X = np.log(NsCPU**2)
Y = np.log(timeCPU/itNumCPU)
k = np.cov(X, Y, ddof=0)[0,1] / np.var(X)
lgb = np.mean(Y) - k * np.mean(X)


dataGPU_PETSC_HYPER_T4 = np.loadtxt('PETSC_CPU_vs_GPU/Intel_vs_T4/dataGPU_PETSC_HYPER.txt')
dataGPU_PETSC_HYPER_100 = np.loadtxt('PETSC_CPU_vs_GPU/Intel_vs_T4/dataGPU_PETSC_HYPER_SPUMA_auto_periodic_100.txt')
dataGPU_PETSC_HYPER_always = np.loadtxt('PETSC_CPU_vs_GPU/Intel_vs_T4/dataGPU_PETSC_HYPER_SPUMA_always_auto.txt')
dataGPU_PETSC_HYPER_10000 = np.loadtxt('PETSC_CPU_vs_GPU/Intel_vs_T4/dataGPU_PETSC_HYPER_SPUMA_auto_periodic_10000.txt')
dataGPU_PETSC_HYPER_SPUMA_T4 = np.loadtxt('PETSC_CPU_vs_GPU/Intel_vs_T4/dataGPU_PETSC_HYPER_SPUMA.txt')

dataGPU_AMGX_T4 = np.loadtxt('AMGX_CPU_vs_GPU/Intel_vs_T4/dataGPU_AMGX.txt')
dataGPU_AMGX_SPUMA_T4 = np.loadtxt('AMGX_CPU_vs_GPU/Intel_vs_T4/dataGPU_AMGX_SPUMA.txt')
dataGPU_AMGX_SPUMA_T4_c = np.loadtxt('AMGX_CPU_vs_GPU/Intel_vs_T4/dataGPU_AMGX_SPUMA_caching.txt')
dataGPU_AMGX_T4_reuse = np.loadtxt('AMGX_CPU_vs_GPU/Intel_vs_T4/dataGPU_AMGX_reuse.txt')

# Создаем фигуру и основную ось
fig, ax1 = plt.subplots(figsize=(10, 6))

# Графики для первой оси Y (левая)
colors = plt.cm.tab10.colors
ax1.set_xlabel('Количество ячеек')
ax1.set_ylabel('Ускорение', color='tab:green')
ax1.set_title("Зависимость ускорения от размера сетки относительно 4 CPU")

plot2(ax1, dataGPU_AMGX_T4, color=colors[0], marker='o', linestyle='--', label=r'AmgX')
plot(ax1, dataGPU_AMGX_SPUMA_T4, color=colors[1], marker='o', linestyle='--', label=r'SPUMA AmgX')
plot(ax1, dataGPU_AMGX_T4_reuse, color=colors[2], marker='o', linestyle='--', label=r'AmgX reuse')

# plot(ax1, dataGPU_AMGX_SPUMA_T4_c, color=colors[2], marker='o', linestyle='--', label=r'time GPU SPUMA AmgX T4 caching')

plot(ax1, dataGPU_PETSC_HYPER_T4, color=colors[3], marker='o', linestyle='--', label=r'PETSC')
# plot(ax1, dataGPU_PETSC_HYPER_always, color=colors[2], marker='o', linestyle='--', label=r'SPUMA PETSC per-1')
# plot(ax1, dataGPU_PETSC_HYPER_SPUMA_T4, color=colors[4], marker='o', linestyle='--', label=r'SPUMA PETSC per-10')
# plot(ax1, dataGPU_PETSC_HYPER_100, color=colors[5], marker='o', linestyle='--', label=r'SPUMA PETSC per-100')
plot(ax1, dataGPU_PETSC_HYPER_10000, color=colors[6], marker='o', linestyle='--', label=r'SPUMA PETSC per-10000')

plot(ax1, data1CPU_PETSC, color=colors[7], marker='o', linestyle='-', label=r'1xCPU PETSC per-10000')
plot(ax1, data4CPU_PETSC, color=colors[8], marker='o', linestyle='-', label=r'4xCPU PETSC per-10000')

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
plt.savefig('data2.png', dpi=300, bbox_inches='tight')