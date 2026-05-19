import numpy as np
import matplotlib.pyplot as plt

# Загружаем данные из файла
data = np.loadtxt('dataCPU.txt')
dataU = np.loadtxt('dataUSERPC.txt')
dataGPU = np.loadtxt('dataGPU.txt')


# Разделяем на колонки
NsCPU = data[:, 0]      # первый столбец - ось X
timeCPU = data[:, 1]    # второй столбец - первая ось Y
itNumCPU = data[:, 2]   # третий столбец - первая ось Y

NsCPU2 = dataU[:, 0]      # первый столбец - ось X
timeCPU2 = dataU[:, 1]    # второй столбец - первая ось Y
itNumCPU2 = dataU[:, 2]   # третий столбец - первая ось Y

NsGPU = dataGPU[:, 0]      # первый столбец - ось X
timeGPU = dataGPU[:, 1]    # второй столбец - первая ось Y
itNumGPU = dataGPU[:, 2]   # третий столбец - первая ось Y

# Создаем фигуру и основную ось
fig, ax1 = plt.subplots(figsize=(10, 6))

# Графики для первой оси Y (левая)
color1 = 'tab:red'
color2 = 'tab:blue'
ax1.set_xlabel('Количество ячеек на стороне квадрата')
ax1.set_ylabel('Время расчета, c', color='tab:green')
ax1.plot(NsCPU, timeCPU, color=color1, marker='o', linestyle='-', label=r'time CPU')
ax1.plot(NsCPU2, timeCPU2, color=color2, marker='o', linestyle='-', label=r'time 2xCPU')
ax1.plot(NsGPU, timeGPU, color=color2, marker='o', linestyle='--', label=r'time GPU')
ax1.tick_params(axis='y', labelcolor='tab:green')
ax1.legend(loc='upper left')
ax1.set_xlim(1e2, 
             1e3)
# Создаем вторую ось Y (правая)
ax2 = ax1.twinx()
color3 = 'tab:purple'
color4 = 'tab:green'
color5 = 'tab:yellow'
ax2.set_ylabel('Количество итераций, c', color=color3)
ax2.plot(NsCPU, itNumCPU, color=color3, marker='^', linestyle='-.', label='iters')
ax2.plot(NsCPU2, itNumCPU2, color=color4, marker='^', linestyle='-.', label='iters')
ax2.plot(NsGPU, itNumGPU, color=color5, marker='^', linestyle='-.', label='iters')
ax2.tick_params(axis='y', labelcolor=color3)
ax2.legend(loc='upper right')

# Создаем верхнюю ось X
ax3 = ax1.twiny()
ax3.set_xlabel('Общее количество ячеек', fontsize=12)
ax3.set_xlim(ax1.get_xlim())  # Устанавливаем те же границы, что и у нижней оси

ax3.set_xlim((ax1.get_xlim()[0] ** 2), 
             (ax1.get_xlim()[1] ** 2))
# Добавляем заголовок
# plt.title('График с двумя осями Y')

# Добавляем сетку для лучшей читаемости
ax1.grid(True, alpha=0.3)
ax1.set_yscale('log')  
ax2.set_yscale('log')
ax1.set_xscale('log') 
ax3.set_xscale('log') 

# Автоматическая подгонка макета
plt.tight_layout()

# Показываем график
# plt.show()

# (Опционально) сохраняем график
plt.savefig('data.png', dpi=300, bbox_inches='tight')