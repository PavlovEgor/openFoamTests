import numpy as np
import re
import subprocess
from scipy.optimize import newton
from multiprocessing import Pool
import shutil
import os
import itertools
import formating, hydro


kwallFunctions = [
    "kqRWallFunction",
    "kLowReWallFunction"
]

epsilonWallFunctions = [
    "epsilonWallFunction"
]

nutWallFunctions = [
    "nutLowReWallFunction",
    "nutkWallFunction",
    "nutUWallFunction",
    "nutUSpaldingWallFunction"
]

WallFunctionsComb = list(itertools.product(kwallFunctions, epsilonWallFunctions, nutWallFunctions))

n = 22
Re = np.logspace(3.8, 6.2, n)

def processIter(i, meshType=1):
    p = np.zeros(n)
    yPlus = np.zeros((3, n))

    path = f"../case_{i}/"

    formating.createCaseIFromCase(newCasePath=path, 
                                  baseCasePath="../case/", 
                                  meshType=meshType)


    formating.setTurbModel(path, "kEpsilon")
    formating.setWallFunctions(path, "k",       WallFunctionsComb[i][0])
    formating.setWallFunctions(path, "epsilon", WallFunctionsComb[i][1])
    formating.setWallFunctions(path, "nut",     WallFunctionsComb[i][2])
    
    result_filename = f"Data/mesh{meshType}_" + WallFunctionsComb[i][0] + "_" + WallFunctionsComb[i][1] + "_" + WallFunctionsComb[i][2] + ".txt"

    for i in range(n):

        formating.setU(path, hydro.ReToU(Re[i]))

        subprocess.run([path + "Allclean"])
        subprocess.run([path + "Allrun"], check=True)
    
        p_data = np.loadtxt(path + "postProcessing/probes/0/p", comments='#')
        yPlus_data = np.loadtxt(path + "postProcessing/yPlus/0/yPlus.dat",     
                                comments='#',  # Пропускаем строки, начинающиеся с #
                                usecols=(0, 2, 3, 4)
                                )
        
        p[i] = p_data[-1][1]
        yPlus[0, i] = yPlus_data[-1][1]
        yPlus[1, i] = yPlus_data[-1][2]
        yPlus[2, i] = yPlus_data[-1][3]

        np.savetxt(result_filename, np.array([Re[:i+1], hydro.Lambda(p, Re)[:i+1], yPlus[0, :i+1], yPlus[1, :i+1], yPlus[2, :i+1]]).T)

    shutil.rmtree(path)

if __name__ == "__main__":
    with Pool(processes=6) as pool:  # По умолчанию использует все ядра CPU
        pool.map(processIter, range(len(kwallFunctions) * len(epsilonWallFunctions) * len(nutWallFunctions)))