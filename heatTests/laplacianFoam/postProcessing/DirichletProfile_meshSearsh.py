import openfoamparser_mai as Ofpp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import formating, thermo
import subprocess
import re
from multiprocessing import Pool
import shutil
import glob
from functools import partial
import os
import time


def processIter(rCells):

    path = f"../Dirichlet_{rCells}/"

    mesh_shape = (rCells, 15 * rCells, 150 * rCells)

    formating.createCaseIFromCase(newCasePath=path,
                            baseCasePath="../Dirichlet/")

    formating.setMeshShape(path, mesh_shape=mesh_shape)

    subprocess.run([path + "Allclean"])
    t1 = time.time()
    subprocess.run([path + "Allrun"], check=True)
    dt = time.time() - t1

    T, T_name = formating.find_time(path)

    Temp = Ofpp.parse_internal_field(path + T_name[-1] + "/T")
    Cx = Ofpp.parse_internal_field(path + T_name[-1] + "/Cx")
    Cy = Ofpp.parse_internal_field(path + T_name[-1] + "/Cy")

    r_grid = np.sqrt(Cx ** 2 + Cy ** 2) * 1e3

    deltaFT = np.sum(np.abs(Temp - thermo.Dirichlet_sol(r_grid))) / (mesh_shape[0] * mesh_shape[1] * mesh_shape[2])
    deltaST = np.sqrt(np.sum((Temp - thermo.Dirichlet_sol(r_grid)) ** 2) / (mesh_shape[0] * mesh_shape[1] * mesh_shape[2]))

    np.savetxt(f"Dirichlet_laplacianFoam_{rCells}.txt", np.array([rCells, deltaFT, deltaST, dt]))

    shutil.rmtree(path)

if __name__ == "__main__":
    rCells_ = range(2, 14)
    deltaFTs = np.zeros(len(rCells_))
    deltaSTs = np.zeros(len(rCells_))
    Time = np.zeros(len(rCells_))

    with Pool(processes=6) as pool:  # По умолчанию использует все ядра CPU
        pool.map(processIter, rCells_)

    for rCells in rCells_:
        _, deltaFT, deltaST, dt = np.loadtxt(f"Dirichlet_laplacianFoam_{rCells}.txt")
        deltaFTs[rCells - rCells_[0]] = deltaFT
        deltaSTs[rCells - rCells_[0]] = deltaST
        Time[rCells - rCells_[0]] = dt

        os.remove(f"Dirichlet_laplacianFoam_{rCells}.txt")

    np.savetxt("Dirichlet_laplacianFoam.txt", np.array([rCells_, 
                                          deltaFTs, 
                                          deltaSTs,
                                          Time]).T)