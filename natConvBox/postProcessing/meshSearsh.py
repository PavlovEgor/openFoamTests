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
                            baseCasePath="../caseGPU/")

    formating.setMeshSize(path, N)

    subprocess.run([path + "Allclean"])
    subprocess.run([path + "Allrun"], check=True)

    itNum, dt = formating.get_last_simulation_time(path + "log.buoyantBoussinesqSimpleFoam")

    np.savetxt(f"case_{N}.txt", np.array([N, dt, itNum]))

    shutil.rmtree(path)

if __name__ == "__main__":
    # Ns = [40, 80, 120, 160, 200]
    Ns = np.logspace(2, 3, 10, dtype=int)

    j = 3

    log_step = (np.log10(3) - np.log10(2)) / (10 - 1)

    log_min = np.log10(2)
    log_max = np.log10(3) + j * log_step

    Ns_extended = np.logspace(10**log_min, 10**log_max, 10 + j, dtype=int)

    Time = np.zeros(len(Ns_extended))
    itNums = np.zeros(len(Ns_extended))

    # with Pool(processes=4) as pool:  # По умолчанию использует все ядра CPU
    #     pool.map(processIter, Ns)
    
    for ns in Ns_extended:
        processIter(ns)

    for i, N in enumerate(Ns_extended):
        _, dt, itNum = np.loadtxt(f"case_{N}.txt")
        Time[i] = dt
        itNums[i] = itNum

    np.savetxt("data.txt", np.array([Ns_extended, Time, itNums]).T)

    for i, N in enumerate(Ns_extended):
        os.remove(f"case_{N}.txt")
