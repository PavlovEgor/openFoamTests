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

def setMeshSize(path, N=40):

    setXtoY_inFile(path, 
                   filename="system/blockMeshDict",
                   pattern=r"N (\d+);",
                   replacement=f"N  {N};")


def createCaseIFromCase(newCasePath,
                        baseCasePath="../case/"):

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
    

def is_float(value):
    try:
        a = float(value)
        if a > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def find_time(dir_name=''):
    dir_list = os.listdir(dir_name)
    T = []
    T_name = []

    for name in dir_list:
        if is_float(name):
            T.append(float(name))
            T_name.append(name)

    combined = list(zip(T, T_name))
    sorted_combined = sorted(combined, key=lambda x: x[0])

    return zip(*sorted_combined)