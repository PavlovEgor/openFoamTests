import openfoamparser_mai as Ofpp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import formating
import subprocess
import re
from multiprocessing import Pool
import shutil
import glob
from functools import partial
import os


def processIter(N):

    path = f"../case_{N}/"

    formating.createCaseIFromCase(newCasePath=path,
                            baseCasePath="../caseCPU/")

    formating.setMeshSize(path, N)

    subprocess.run([path + "Allclean"])
    subprocess.run([path + "Allrun"], check=True)

    itNum, dt = formating.get_last_simulation_time(path + "log.buoyantBoussinesqSimpleFoam")

    np.savetxt(f"case_{N}.txt", np.array([N, dt, itNum]))

    shutil.rmtree(path)

if __name__ == "__main__":
    # Ns = [40, 80, 120, 160, 200]
    Ns = np.logspace(2, 3, 10, dtype=int)
    Time = np.zeros(len(Ns))
    itNums = np.zeros(len(Ns))

    with Pool(processes=4) as pool:  # По умолчанию использует все ядра CPU
        pool.map(processIter, Ns)
    
    for ns in Ns:
        processIter(ns)

    for i, N in enumerate(Ns):
        _, dt, itNum = np.loadtxt(f"case_{N}.txt")
        Time[i] = dt
        itNums[i] = itNum

    np.savetxt("data.txt", np.array([Ns, Time, itNums]).T)

    for i, N in enumerate(Ns):
        os.remove(f"case_{N}.txt")
