import re
import os
import shutil
import time
from multiprocessing import Pool

import hydro, formating
import subprocess

import numpy as np


def runCase(casePath):
    subprocess.run([casePath + "Allclean"])
    subprocess.run([casePath + "Allrun"], check=True)
    

class Processing:
    def __init__(self, casePath, tmpDir):

        self.casePath = casePath
        self.tmpDir = tmpDir

        if os.path.exists(tmpDir):
            shutil.rmtree(tmpDir)
        os.makedirs(tmpDir)


    def makeSearch(self, preFunc, postFunc, finalFunc, params, searchDirName, processes=1):

        nParams = len(params)
        for i in range(nParams):
            params[i] = (i, params[i])

        searchDir = self.tmpDir + searchDirName + "/"

        if os.path.exists(searchDir):
            shutil.rmtree(searchDir)
        os.makedirs(searchDir)

        def func(param):
            newCasePath=searchDir + f"case_{param[0]}"

            formating.createCaseIFromCase(newCasePath=newCasePath, baseCasePath=self.casePath)

            preFunc(newCasePath, param)

            runCase(newCasePath)

            postFunc(newCasePath)

            shutil.rmtree(newCasePath)
        
        with Pool(processes=processes) as pool:
            pool.map(func, params)

        finalFunc()

def preTurbulentFlow(casePath, Re):
    formating.setU(casePath, hydro.ReToU(Re))

def preStretch(casePath, Re, stretch):
    formating.setU(casePath, hydro.ReToU(Re))
    formating.setStretch(casePath, stretch)

def preRelaxationFactorsU(casePath, Re, relaxationFactor):
    formating.setU(casePath, hydro.ReToU(Re))
    formating.setrelaxationFactors(casePath, relaxationFactor)

def preTurbulenceModels(casePath, Re, turbulenceModel):
    formating.setU(casePath, hydro.ReToU(Re))
    formating.setTurbModel(casePath, turbulenceModel)

def preWallFunctions(casePath, Re, WallFunctionsComb):

    formating.setU(casePath, hydro.ReToU(Re))
    
    formating.setTurbModel(casePath, "kEpsilon")
    formating.setWallFunctions(casePath, "k",       WallFunctionsComb[0])
    formating.setWallFunctions(casePath, "epsilon", WallFunctionsComb[1])
    formating.setWallFunctions(casePath, "nut",     WallFunctionsComb[2])

def getDP(casePath):
    p_data = np.loadtxt(casePath + "postProcessing/probes/0/p", comments='#')
    return p_data[-1][1]

def getYPlus(casePath):
    yPlus_data = np.loadtxt(casePath + "postProcessing/yPlus/0/yPlus.dat",     
                            comments='#',  # Пропускаем строки, начинающиеся с #
                            usecols=(0, 2, 3, 4)
                            )
    
    return yPlus_data[-1][1], yPlus_data[-1][2], yPlus_data[-1][3]

if __name__ == "__main__":
    Re = 100_000
    proc = Processing("../case/", "./tmp/")

    preTurbulentFlow(proc.casePath, Re)

    runCase(proc.casePath)

    print(hydro.Lambda(getDP(proc.casePath), Re))
    print(hydro.PrandlLow(Re))
    print(getYPlus(proc.casePath))
    print(formating.get_last_simulation_time(proc.casePath + "log.simpleFoam"))