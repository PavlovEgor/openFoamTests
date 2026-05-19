import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import newton
import formating, hydro



n = 100
R = np.logspace(3.8, 6.2, n)
PL = hydro.PrandlLow(R)
m = 6
relaxationFactors = np.linspace(0.4, 0.8, m)

for meshType in [1, 2, 3]:

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    ax1.plot(R, PL, label = "закон Прандтля")

    


    color_map = cm.get_cmap('tab10', m)
    marker    = ["s", "o", "^", "v", "*", "d"]

    for i in range(m):

        result_filename = f"Data/Mesh{meshType}/relaxationFactor_" + f"{i}" + ".txt"

        try:
            R_CFD, Lambda_CFD, _, _, yPlusAve, Tim = np.loadtxt(result_filename, comments='#').T

            ax1.plot(R_CFD, Lambda_CFD, marker[i % 4], c=color_map(i), label=f"{i}, {round(relaxationFactors[i], 3)}")
            ax2.plot(R_CFD, Tim, 'x', c=color_map(i), label="Time " + f"{i}, {round(relaxationFactors[i], 3)}")
        except:
            pass

    # Отображение

    ax1.set_ylabel(r'$\lambda$', fontsize=16, color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax1.set_xlabel('$Re$', fontsize=16)
    ax1.set_xscale('log')  
    ax1.set_yscale('log')  
    ax2.set_yscale('log')
    ax2.set_ylabel('Real time, s', color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:green')

    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.tight_layout(rect=[0, 0, 0.8, 1])

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, bbox_to_anchor=(1.1, 1), loc='upper left', borderaxespad=0.)

    plt.savefig("relaxationFactors.png")
    plt.show()