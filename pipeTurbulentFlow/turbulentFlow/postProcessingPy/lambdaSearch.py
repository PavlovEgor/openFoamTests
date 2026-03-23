import numpy as np
import re
import subprocess
from scipy.optimize import newton
from multiprocessing import Pool
import shutil
import formating, hydro
import glob
from functools import partial
import os


def extract_Re(file_path):
    match = re.search(r"Re=(\d+)\.txt", file_path)
    if match:
        return int(match.group(1))
    return 0


def processIter(i, meshType=1):

    path = f"../case_{i}/"

    formating.createCaseIFromCase(newCasePath=path, 
                                  baseCasePath="../case/", 
                                  meshType=meshType)
    formating.setU(path, hydro.ReToU(Re=Re[i]))


    subprocess.run([path + "Allclean"])
    subprocess.run([path + "Allrun"], check=True)

    p_data = np.loadtxt(path + "postProcessing/probes/0/p", comments='#')
    yPlus_data = np.loadtxt(path + "postProcessing/yPlus/0/yPlus.dat",     
                            comments='#',  # Пропускаем строки, начинающиеся с #
                            usecols=(0, 2, 3, 4)
                            )
    
    result_filename = f"Data/tmp{meshType}/Re=" + f"{round(Re[i])}" + ".txt"
    
    if not os.path.exists(f"Data/tmp{meshType}/"):
        os.makedirs(f"Data/tmp{meshType}/")

    np.savetxt(result_filename, np.array([Re[i], 
                                          hydro.Lambda(p_data[-1][1], Re[i]), 
                                          yPlus_data[-1][1], yPlus_data[-1][2], yPlus_data[-1][3]]).reshape(1, -1))
 
    shutil.rmtree(path)

if __name__ == "__main__":
    n = 12
    Re = np.logspace(3.8, 6.2, n)

    for i in [1, 2, 3]:
        processIterMeshType = partial(processIter, meshType=i)
        with Pool(processes=6) as pool:  # По умолчанию использует все ядра CPU
            pool.map(processIterMeshType, range(n))

        file_paths = glob.glob(f"Data/tmp{i}/Re=*.txt")
        sorted_files = sorted(file_paths, key=extract_Re)

        with open(f"Data/resultMesh{i}.txt", "w") as output_file:
            for file_path in sorted_files:
                with open(file_path, "r") as input_file:
                    line = input_file.readline().strip()
                    output_file.write(line + "\n")

        shutil.rmtree(f"./Data/tmp{i}")