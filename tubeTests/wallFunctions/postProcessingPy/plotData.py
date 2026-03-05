import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.optimize import newton
import itertools


def BlasiusLow(Re):
    return 0.3164 / (Re ** 0.25)


def PrandlLow(Re):

    C = 0.8 - 2 * np.log10(Re)
    def PrFunc(x):
        return C + (x ** (-0.5)) - np.log10(x) 
    
    def PrFuncPrime(x):
        return -0.5 * (x ** (-1.5)) - np.log(10) / x
    
    root = newton(PrFunc, BlasiusLow(Re), PrFuncPrime)

    return root


print(PrandlLow(1e5))
path = "Data/"

n = 100
R = np.logspace(3.8, 6.2, n)
PL = PrandlLow(R)

fig, ax1 = plt.subplots(figsize=(14, 6))
ax2 = ax1.twinx()

ax1.plot(R, PL, label = "закон Прандтля")

kwallFunctions = [
    "kqRWallFunction",
    "kLowReWallFunction"
]

epsilonWallFunctions = [
    "epsilonWallFunction",
    # "epsilonLowReWallFunction"
]

nutWallFunctions = [
    # "nutWallFunction",
    "nutLowReWallFunction",
    "nutkWallFunction",
    "nutUWallFunction",
    "nutUSpaldingWallFunction"
]

WallFunctionsComb = list(itertools.product(kwallFunctions, epsilonWallFunctions, nutWallFunctions))

color_map = cm.get_cmap('tab10', len(WallFunctionsComb))
marker    = ["s", "o", "^", "v"]

for i, modelName in enumerate(WallFunctionsComb):

    result_filename = path + modelName[0] + "_" + modelName[1] + "_" + modelName[2] + ".txt"
    try:
        R_CFD, Lambda_CFD, _, _, yPlusAve = np.loadtxt(result_filename, comments='#').T

        ax1.plot(R_CFD, Lambda_CFD, marker[i % 4], c=color_map(i), label=modelName[0] + "_" + modelName[1] + "_" + modelName[2])
        ax2.plot(R_CFD, yPlusAve, 'x', c=color_map(i), label="y+ " + modelName[0] + "_" + modelName[1] + "_" + modelName[2])
    except:
        pass

# Отображение

ax1.set_ylabel(r'$\lambda$', fontsize=16, color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax1.set_xlabel('$Re$', fontsize=16)
ax1.set_xscale('log')  
ax1.set_yscale('log')  
ax2.set_yscale('log')
ax2.set_ylabel('Average y+', color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:green')

plt.grid(True, which="both", ls="-", alpha=0.5)
plt.tight_layout(rect=[0, 0, 0.6, 1])

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax2.legend(lines_1 + lines_2, labels_1 + labels_2, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.show()




fig, ax1 = plt.subplots(figsize=(14, 6))
ax2 = ax1.twinx()

n = 22
R = np.logspace(3.8, 6.2, n)
PL = PrandlLow(R)

for i, modelName in enumerate(WallFunctionsComb):

    result_filename = path + modelName[0] + "_" + modelName[1] + "_" + modelName[2] + ".txt"
    try:
        R_CFD, Lambda_CFD, _, _, yPlusAve = np.loadtxt(result_filename, comments='#').T

        ax1.plot(R_CFD, np.abs(Lambda_CFD - PL[:Lambda_CFD.shape[0]]), marker[i % 4], c=color_map(i), label=modelName[0] + "_" + modelName[1] + "_" + modelName[2])
        ax2.plot(R_CFD, yPlusAve, 'x', c=color_map(i), label="y+ " + modelName[0] + "_" + modelName[1] + "_" + modelName[2])
    except:
        pass

# Отображение

ax1.set_ylabel(r'$\Delta \lambda$', fontsize=16, color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax1.set_xlabel('$Re$', fontsize=16)
ax1.set_xscale('log')  
ax1.set_yscale('log')  
ax2.set_yscale('log')
ax2.set_ylabel('Average y+', color='tab:green')
ax2.tick_params(axis='y', labelcolor='tab:green')

plt.grid(True, which="both", ls="-", alpha=0.5)
plt.tight_layout(rect=[0, 0, 0.6, 1])

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax2.legend(lines_1 + lines_2, labels_1 + labels_2, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.show()