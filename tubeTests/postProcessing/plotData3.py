import numpy as np
import matplotlib.pyplot as plt

# Загружаем данные из файла
dataCPU = np.loadtxt('AMGX_CPU_vs_GPU/Inteli7_vs_RTX2060/dataCPU3.txt')
dataGPU_RTX2060 = np.loadtxt('AMGX_CPU_vs_GPU/Inteli7_vs_RTX2060/dataGPU_AMGX.txt')
dataGPU_SPUMA_RTX2060 = np.loadtxt('AMGX_CPU_vs_GPU/Inteli7_vs_RTX2060/dataGPU_SPUMA_AMGX.txt')
dataGPU_T4 = np.loadtxt('dataGPU_AMGX.txt')
dataGPU_SPUMA_T4 = np.loadtxt('dataGPU_AMGX_SPUMA.txt')



# Разделяем на колонки
NsCPU = dataCPU[:, 0]      # первый столбец - ось X
timeCPU = dataCPU[:, 1]    # второй столбец - первая ось Y
itNumCPU = dataCPU[:, 2]   # третий столбец - первая ось Y

NsGPU = dataGPU_RTX2060[:, 0]      # первый столбец - ось X
timeGPU = dataGPU_RTX2060[:, 1]    # второй столбец - первая ось Y
itNumGPU = dataGPU_RTX2060[:, 2]   # третий столбец - первая ось Y

NsGPUSPUMA = dataGPU_T4[:, 0]      # первый столбец - ось X
timeGPUSPUMA = dataGPU_T4[:, 1]    # второй столбец - первая ось Y
itNumGPUSPUMA = dataGPU_T4[:, 2]   # третий столбец - первая ось Y

NsGPUSPUMA1 = dataGPU_SPUMA_T4[:, 0]      # первый столбец - ось X
timeGPUSPUMA1 = dataGPU_SPUMA_T4[:, 1]    # второй столбец - первая ось Y
itNumGPUSPUMA1 = dataGPU_SPUMA_T4[:, 2]   # третий столбец - первая ось Y

NsGPUSPUMA2 = dataGPU_SPUMA_RTX2060[:, 0]      # первый столбец - ось X
timeGPUSPUMA2 = dataGPU_SPUMA_RTX2060[:, 1]    # второй столбец - первая ось Y
itNumGPUSPUMA2 = dataGPU_SPUMA_RTX2060[:, 2]   # третий столбец - первая ось Y

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
ax1.plot(NsCPU**2, timeCPU / itNumCPU, color=color1, marker='o', linestyle='-', label=r'time 3xCPU')
ax1.plot(NsGPU**2, timeGPU / itNumGPU, color=color4, marker='o', linestyle='--', label=r'time GPU pure AmgX RTX2060')
ax1.plot(NsGPUSPUMA**2, timeGPUSPUMA / itNumGPUSPUMA, color=color5, marker='o', linestyle='--', label=r'time GPU pure AmgX T4')
ax1.plot(NsGPUSPUMA1**2, timeGPUSPUMA1 / itNumGPUSPUMA1, color=color2, marker='o', linestyle='--', label=r'time GPU SPUMA AmgX T4')
ax1.plot(NsGPUSPUMA2**2, timeGPUSPUMA2 / itNumGPUSPUMA2, color=color3, marker='o', linestyle='--', label=r'time GPU SPUMA AmgX RTX2060')


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