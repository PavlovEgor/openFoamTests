import re
import os
import shutil


def setXtoY_inFile(path, 
                   filename,
                   pattern,
                   replacement):
    
    with open(path + filename, 'r') as file:
        content = file.read()

    new_content = re.sub(pattern, replacement, content)

    with open(path + filename, 'w') as file:
        file.write(new_content)


def setU(path, U):

    setXtoY_inFile(path,
                   "0.orig/U",
                   pattern=r'(value\s+uniform\s*\(\s*[\d\.]+\s+[\d\.]+\s+[\d\.]+\s*\);)',
                   replacement=f'value           uniform (0 0 {U});')


def setStretch(path, stretch):

    setXtoY_inFile(path,
                   "system/blockMeshDict",
                   pattern=r'(stretch\s+)[\d\.]+;',
                   replacement=f'stretch        {stretch};')


def setTurbModel(path, modelName):

    setXtoY_inFile(path,
                   "constant/turbulenceProperties",
                   pattern=r'(RASModel\s+)\w+;',
                   replacement=f'RASModel        {modelName};')


def setWallFunctions(path, fieldName, modelName):

    setXtoY_inFile(path,
                   "0.orig/" + fieldName,
                   pattern=r'(pipe { type\s+)\w+;',
                   replacement=rf'pipe {{ type         {modelName};')


def createCaseIFromCase(newCasePath,
                        baseCasePath="../case/",
                        meshType=1):

    if os.path.exists(newCasePath):
        shutil.rmtree(newCasePath)
    os.makedirs(newCasePath)

    for item in os.listdir(baseCasePath):
        source_path = os.path.join(baseCasePath, item)
        dest_path = os.path.join(newCasePath, item)

        if os.path.isdir(source_path):
            shutil.copytree(source_path, dest_path)
        else:
            shutil.copy2(source_path, dest_path)
    
    os.remove(newCasePath + "system/blockMeshDict")
    if meshType not in {1, 2, 3}:
        exit("Wrong meshType, must be 1, 2 or 3")
    os.rename(newCasePath + f"system/blockMeshDict{meshType}", newCasePath + "system/blockMeshDict")


def setrelaxationFactors(path, relaxationFactor):

    setXtoY_inFile(path,
                   "system/fvSolution",
                   pattern=r'(equations { U\s+)[\d\.]+;',
                   replacement=rf'equations {{ U        {relaxationFactor};')