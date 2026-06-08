import openfoamparser_mai as Ofpp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import subprocess
import re
from multiprocessing import Pool
import shutil
import glob
from functools import partial
import os

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

def diff(A="casePETScSPUMA", B="caseCPU"):

    _, T_nameA = find_time(A)
    _, T_nameB = find_time(B)

    TA = Ofpp.parse_internal_field('./'+ A + "/" + T_nameA[-1] + "/T")
    TB = Ofpp.parse_internal_field('./'+ B + "/" + T_nameB[-1] + "/T")

    plt.imshow((TA - TB).reshape(100, 100))
    plt.show()

    return np.max(TA - TB)

print(diff())