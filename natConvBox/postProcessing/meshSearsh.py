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
import time


def processIter(N):

    path = f"../case_{N}/"

    formating.createCaseIFromCase(newCasePath=path,
                            baseCasePath="../case2D/")

    formating.setMeshSize(path, N)

    subprocess.run([path + "Allclean"])
    t1 = time.time()
    subprocess.run([path + "Allrun"], check=True)
    dt = time.time() - t1

    T, T_name = formating.find_time(path)

    # Temp = Ofpp.parse_internal_field(path + T_name[-1] + "/T")
    # Cx = Ofpp.parse_internal_field(path + T_name[-1] + "/Cx")
    # Cy = Ofpp.parse_internal_field(path + T_name[-1] + "/Cy")

    np.savetxt(f"case_{N}.txt", np.array([N, dt, int(T[-1])]))

    shutil.rmtree(path)

if __name__ == "__main__":
    # Ns = [40, 80, 120, 160, 200]
    Ns = np.logspace(2, 3, 10, dtype=int)
    Time = np.zeros(len(Ns))
    itNums = np.zeros(len(Ns))

    with Pool(processes=6) as pool:  # По умолчанию использует все ядра CPU
        pool.map(processIter, Ns)

    for i, N in enumerate(Ns):
        _, dt, itNum = np.loadtxt(f"case_{N}.txt")
        Time[i] = dt
        itNums[i] = itNum

        os.remove(f"case_{N}.txt")

    np.savetxt("data.txt", np.array([Ns, Time, itNums]).T)