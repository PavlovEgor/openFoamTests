import numpy as np
import matplotlib.pyplot as plt
import re
import subprocess
from scipy.optimize import newton
from multiprocessing import Pool
import shutil
import os
import formating, hydro
from functools import partial


def processIter(i, meshType=1):
    p = np.zeros(n)
    yPlus = np.zeros((3, n))

    path = f"../case_{i}/"

    formating.createCaseIFromCase(newCasePath=path, 
                                  baseCasePath="../case/", 
                                  meshType=meshType)


    formating.setStretch(path, stretch[i])

    if not os.path.exists(f"Data/Mesh{meshType}/"):
        os.makedirs(f"Data/Mesh{meshType}/")

    result_filename = f"Data/Mesh{meshType}/stretch_" + f"{i}" + ".txt"

    for i in range(n):
        formating.setU(path, hydro.ReToU(Re=Re[i]))

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

    n = 12
    m = 6
    Re = np.logspace(3.8, 6.2, n)
    stretch = np.logspace(-1, 1, m)

    for i in [1, 2, 3]:
        processIterMeshType = partial(processIter, meshType=i)
        with Pool(processes=6) as pool:  # По умолчанию использует все ядра CPU
            pool.map(processIterMeshType, range(m))
