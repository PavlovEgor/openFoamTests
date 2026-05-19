import numpy as np
import matplotlib.pyplot as plt
import re
import subprocess


def Lambda(dP, Re, D=0.01, L=0.5, nu=1e-6):
    return (dP / (Re ** 2)) * ((2 * (D ** 3)) / (L * (nu ** 2)))


def setU(path, U):
    with open(path + "0.orig/U", 'r') as file:
        content = file.read()

    # Ищем строку с value uniform ( ... );
    pattern = r'(value\s+uniform\s*\(\s*[\d\.]+\s+[\d\.]+\s+[\d\.]+\s*\);)'
    replacement = f'value           uniform (0 0 {U});'

    # Заменяем найденное значение
    new_content = re.sub(pattern, replacement, content)

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


def ReToU(Re, D=0.01, nu=1e-6):
    return nu * Re / D


path = "/home/user/OpenFOAM/user-v2412/run/tests/tube/planeSymm/"
result_filename = "planeSymmReLambda.txt"

n = 20
R = np.logspace(4.0, 6.2, n)
R = R[::-1]
p = np.zeros(n)
yPlus = np.zeros((3, n))


for i in range(n):

    U = ReToU(R[i])
    setU(path, U)
    print(i, R[i], U)

    subprocess.run([path + "Allclean"])
    subprocess.run([path + "Allrun"], check=True)
    
    p_data = np.loadtxt(path + "postProcessing/probes/0/p", comments='#')
    yPlus_data = np.loadtxt(path + "postProcessing/yPlus/0/yPlus.dat",     
                            comments='#',  # Пропускаем строки, начинающиеся с #
                            usecols=(0, 2, 3, 4)
                            )

    p[i] = p_data[-1][1]
    yPlus[0, i] = yPlus_data[-1][1]
    yPlus[1, i] = yPlus_data[-1][2]
    yPlus[2, i] = yPlus_data[-1][3]

    np.savetxt(path + "postProcessingPy/" + result_filename, np.array([R[:i+1], Lambda(p, R)[:i+1], yPlus[0, :i+1], yPlus[1, :i+1], yPlus[2, :i+1]]).T)
