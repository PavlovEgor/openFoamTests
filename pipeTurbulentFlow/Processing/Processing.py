import re
import os
import shutil
import glob
import time
from multiprocessing import Pool

import hydro, formating
import subprocess

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def runCase(casePath):
    subprocess.run([casePath + "Allclean"])
    subprocess.run([casePath + "Allrun"], check=True)
    

class Processing:
    def __init__(self, casePath, tmpDir):

        self.casePath = casePath
        self.tmpDir = tmpDir

        if not os.path.exists(tmpDir):
            # shutil.rmtree(tmpDir)
            os.makedirs(tmpDir)

    def processingFunc(self, param):

        i = param[0] 
        searchDir = param[1] 
        preFunc = param[2]
        postFunc = param[3]
        paramBody = param[4]

        newCasePath = searchDir + f"case_{i}/"

        formating.createCaseIFromCase(newCasePath=newCasePath, baseCasePath=self.casePath)

        preFunc(newCasePath, *paramBody)

        runCase(newCasePath)

        postFunc(searchDir, newCasePath, *paramBody)

        # shutil.rmtree(newCasePath)


    def makeSearch(self, preFunc, postFunc, finalFunc, params, searchDirName, processes=1):

        searchDir = self.tmpDir + searchDirName + "/"

        if os.path.exists(searchDir):
            shutil.rmtree(searchDir)
        os.makedirs(searchDir)

        nParams = len(params)
        for i in range(nParams):
            params[i] = (i, searchDir, preFunc, postFunc, [params[i]])
        
        with Pool(processes=processes) as pool:
            pool.map(self.processingFunc, params)

        finalFunc(searchDir)

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

def postTurbulentFlow(searchDir, casePath, Re):
    result_filename = searchDir + f"Re={round(Re)}" + ".txt"

    data = [Re, 
            hydro.Lambda(formating.getDP(casePath), Re), 
            *formating.getYPlus(casePath),
            *formating.get_last_simulation_time(casePath + "log.simpleFoam")]

    data_array = np.array([data]) 
    
    np.savetxt(result_filename, data_array, fmt='%.6f')
    print(f"Save Re={round(Re)} case in {result_filename}")

def finalTurbulentFlow(searchDir):
    txt_files = glob.glob(os.path.join(searchDir, "*.txt"))

    txt_files.sort()

    if not txt_files:
        print(f"В папке '{searchDir}' не найдено txt файлов.")
        return
    
    output_file = searchDir + "result.txt"
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    if content and not content.endswith('\n'):
                        outfile.write('\n')
            except Exception as e:
                outfile.write(f"Ошибка при чтении файла: {e}\n")
            


if __name__ == "__main__":
    
    Re = list(np.logspace(3.8, 6.2, 6))

    meshes = [(4, 8, 440), 
              (6, 12, 500), 
              (8, 16, 550)]
    
    turbulenceModels = [
        # "LRR", #
        "LamBremhorstKE",
        "LaunderSharmaKE",
        "LienCubicKE",
        "LienLeschziner",
        "RNGkEpsilon",
        # "SSG", #
        "ShihQuadraticKE",
        "SpalartAllmaras",
        "kEpsilon",
        # "kEpsilonLopesdaCosta", #
        # "kEpsilonPhitF", #
        # "kOmega2006", #
        "kOmegaSST",
        # "kOmegaSSTLM",
        # "kOmegaSSTSAS", #
        "kkLOmega",
        "qZeta",
        "realizableKE"
    ]
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
    stretches = list(np.logspace(-1, 1, 6))
    relaxationFactors = np.linspace(0.4, 0.8, 6)

    for i in range(1, 2):

        proc = Processing("../case/", "./tmp/")

        formating.setMeshSize(proc.casePath, *meshes[i])

        proc.makeSearch(preTurbulentFlow, 
                        postTurbulentFlow,
                        finalTurbulentFlow,
                        Re,
                        f"roughnessFlow{i}", 
                        6)

    n = 100
    R = np.logspace(3.8, 6.2, n)
    PL = hydro.PrandlLow(R)
    IL = np.zeros_like(R)

    for i in range(n):
        IL[i] = hydro.IdelchikLow(R[i], l0=hydro.BlasiusLow(R[i]))
        IL[i] = hydro.IdelchikLow(R[i], l0=IL[i])
        IL[i] = hydro.IdelchikLow(R[i], l0=IL[i])
        IL[i] = hydro.IdelchikLow(R[i], l0=IL[i])



    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    ax1.plot(R, PL, label = "закон Прандтля")
    ax1.plot(R, IL, label = "Идельчик")

    color_map = cm.get_cmap('tab10', 3)
    marker    = ["s", "o", "^"]
    annY = [0.6, 0.8, 0.9]
    annX = [0.6, 1.0, 1.3]


    for i in [0, 1, 2]:

        result_filename = proc.tmpDir + f"roughnessFlow{i}/" + "result.txt"

        try:
            R_CFD, Lambda_CFD, _, _, yPlusAve, _, _ = np.loadtxt(result_filename, comments='#').T

            ax1.plot(R_CFD, Lambda_CFD, marker[i], c=color_map(i), label=f"Mesh {i}")
            ax2.plot(R_CFD, yPlusAve, 'x', c=color_map(i), label="y+ Mesh " + f"{i}")

            PL_at_CFD = hydro.PrandlLow(R_CFD)

            abs_error = np.abs(Lambda_CFD - PL_at_CFD)
            rel_error = abs_error / PL_at_CFD * 100
            
            # Find maximum error point
            max_error_idx = np.argmax(abs_error)
            max_error_R = R_CFD[max_error_idx]
            max_error_lambda = Lambda_CFD[max_error_idx]
            max_error_value = abs_error[max_error_idx]
            max_rel_error = rel_error[max_error_idx]
            
            # Determine arrow direction (above or below the curve)
            is_above = Lambda_CFD[max_error_idx] > PL_at_CFD[max_error_idx]
            
            # Calculate arrow endpoint on Prandtl curve
            pl_at_max = PL_at_CFD[max_error_idx]
            
            # Add arrow and text for the first point (i == 0)
            # Arrow properties
            arrow_props = dict(
                arrowstyle='<->', 
                color='red', 
                lw=2,
                connectionstyle='arc3,rad=0.1'
            )
            
            # Add annotation with arrow
            ax1.annotate(
                f'Max error: {max_error_value:.4f}\n({max_rel_error:.2f}%)',
                xy=(max_error_R, max_error_lambda),  # Point on CFD curve
                xytext=(max_error_R * 2.5, max_error_lambda * annY[i]),  # Text position
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5, connectionstyle='angle3,angleA=0,angleB=90'),
                fontsize=9,
                color='red',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7),
                ha='center'
            )
            
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
    plt.tight_layout(rect=[0, 0, 0.8, 1])

    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax2.legend(lines_1 + lines_2, labels_1 + labels_2, bbox_to_anchor=(1.1, 1), loc='upper left', borderaxespad=0.)

    plt.savefig("LambdaRekEpsilon2.png")
    plt.show()