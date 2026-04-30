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
                        baseCasePath):

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
    
def get_last_simulation_time(log_file):
    """Извлекает последние значения Time и ExecutionTime из лог-файла"""
    
    with open(log_file, 'r') as f:
        content = f.read()
    
    # Ищем все вхождения Time = X
    time_pattern = r'^Time\s*=\s*(\d+)' 
    times = re.findall(time_pattern, content, re.MULTILINE)
    # Ищем все вхождения ExecutionTime
    exec_pattern = r'ExecutionTime\s*=\s*([\d.]+)\s*s'
    exec_times = re.findall(exec_pattern, content)
    
    if times and exec_times:
        last_time = int(times[-1])
        last_exec_time = float(exec_times[-1])
        return last_time, last_exec_time
    else:
        return None, None