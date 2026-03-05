import numpy as np
import matplotlib.pyplot as plt
import re
import subprocess
from scipy.optimize import newton
from multiprocessing import Pool
import shutil
import os
import time

def Lambda(dP, Re, D=0.01, L=0.5, nu=1e-6):
    return (dP / (Re ** 2)) * ((2 * (D ** 3)) / (L * (nu ** 2)))


def setU(path, U):
    with open(path + "0.orig/U", 'r') as file:
        content = file.read()

    # Ищем строку с value uniform ( ... );
    pattern1 = r'(value\s+uniform\s*\(\s*[\d\.]+\s+[\d\.]+\s+[\d\.]+\s*\);)'
    pattern2 = r'(internalField\s+uniform\s*\(\s*[\d\.]+\s+[\d\.]+\s+[\d\.]+\s*\);)'

    replacement1 = f'value           uniform (0 0 {U});'
    replacement2 = f'internalField   uniform (0 0 {U});'

    # Заменяем найденное значение
    new_content = re.sub(pattern1, replacement1, content)
    new_content = re.sub(pattern2, replacement2, new_content)

    with open(path + "0.orig/U", 'w') as file:
        file.write(new_content)


def setControlDict(path, U, L=0.55):
    with open(path + "system/controlDict", 'r') as file:
        content = file.read()

    T = 0.2 * L / U
    # Ищем строку с value uniform ( ... );
    pattern = r'(endTime\s+)[\d\.]+;'
    replacement = f'endTime         {T};'

    pattern2 = r'(writeInterval\s+)[\d\.]+;'
    replacement2 = f'writeInterval         {T/10};'

    # Заменяем найденное значение
    new_content = re.sub(pattern, replacement, content)
    new_content = re.sub(pattern2, replacement2, new_content)

    with open(path + "system/controlDict", 'w') as file:
        file.write(new_content)


def setrelaxationFactors(path, relaxationFactor):
    with open(path + "system/fvSolution", 'r') as file:
        content = file.read()

    # Ищем строку с value uniform ( ... );
    pattern = r'(fields { p\s+)[\d\.]+;'
    replacement = rf'fields {{ p        {relaxationFactor};'

    # Заменяем найденное значение
    new_content = re.sub(pattern, replacement, content)

    with open(path + "system/fvSolution", 'w') as file:
        file.write(new_content)


def ReToU(Re, D=0.01, nu=1e-6):
    return nu * Re / D


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

n = 22
m = 6
Re = np.logspace(3.8, 6.2, n)
relaxationFactors = np.linspace(0.1, 0.9, m)

def processIter(i):
    p = np.zeros(n)
    yPlus = np.zeros((3, n))
    Tim = np.zeros(n)

    path = f"../case_{i}/"

    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

    for item in os.listdir("../case/"):
        source_path = os.path.join("../case/", item)
        dest_path = os.path.join(path, item)

        if os.path.isdir(source_path):
            shutil.copytree(source_path, dest_path)
        else:
            shutil.copy2(source_path, dest_path)


    setrelaxationFactors(path, relaxationFactors[i])
    result_filename = "Data/relaxationFactor_" + f"{i}" + ".txt"

    for i in range(n):

        
        U = ReToU(Re[i])
        setU(path, U)

        subprocess.run([path + "Allclean"])

        t1 = time.time()
        subprocess.run([path + "Allrun"], check=True)
        Tim[i] = time.time() - t1
    
        p_data = np.loadtxt(path + "postProcessing/probes/0/p", comments='#')
        yPlus_data = np.loadtxt(path + "postProcessing/yPlus/0/yPlus.dat",     
                                comments='#',  # Пропускаем строки, начинающиеся с #
                                usecols=(0, 2, 3, 4)
                                )
        
        p[i] = p_data[-1][1]
        yPlus[0, i] = yPlus_data[-1][1]
        yPlus[1, i] = yPlus_data[-1][2]
        yPlus[2, i] = yPlus_data[-1][3]

        np.savetxt(result_filename, np.array([Re[:i+1], Lambda(p, Re)[:i+1], yPlus[0, :i+1], yPlus[1, :i+1], yPlus[2, :i+1], Tim[:i+1]]).T)

    shutil.rmtree(path)

if __name__ == "__main__":
    with Pool(processes=6) as pool:  # По умолчанию использует все ядра CPU
        pool.map(processIter, range(m))