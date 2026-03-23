import numpy as np
import matplotlib.pyplot as plt

# Загружаем данные из файла
data = np.loadtxt('Neuman_laplacianFoam.txt')
TO = 200
# Разделяем на колонки
x = data[:, 0]      # первый столбец - ось X
y1 = data[:, 1] / TO    # второй столбец - первая ось Y
y2 = data[:, 2] / TO    # третий столбец - первая ось Y
y3 = data[:, 3]     # четвертый столбец - вторая ось Y

# Создаем фигуру и основную ось
fig, ax1 = plt.subplots(figsize=(10, 6))

# Графики для первой оси Y (левая)
color1 = 'tab:red'
color2 = 'tab:blue'
ax1.set_xlabel('Количество ячеек по толщине')
ax1.set_ylabel('Ошибка, отн. ед', color='tab:green')
ax1.plot(x, y1, color=color1, marker='o', linestyle='-', label=r'$\Delta^{(1)} T$')
ax1.plot(x, y2, color=color2, marker='s', linestyle='--', label=r'$\Delta^{(2)} T$')
ax1.tick_params(axis='y', labelcolor='tab:green')
ax1.legend(loc='upper left')

# Создаем вторую ось Y (правая)
ax2 = ax1.twinx()
color3 = 'tab:purple'
ax2.set_ylabel('Время расчета, c', color=color3)
ax2.plot(x, y3, color=color3, marker='^', linestyle='-.', label='Время расчета, c')
ax2.tick_params(axis='y', labelcolor=color3)
ax2.legend(loc='upper right')

# Создаем верхнюю ось X
ax3 = ax1.twiny()
ax3.set_xlabel('Общее количество ячеек', fontsize=12)
ax3.set_xlim(ax1.get_xlim())  # Устанавливаем те же границы, что и у нижней оси

ax3.set_xlim((150 * 15 * ax1.get_xlim()[0] ** 3), 
             (150 * 15 * ax1.get_xlim()[1] ** 3))

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
plt.savefig('Neuman.png', dpi=300, bbox_inches='tight')