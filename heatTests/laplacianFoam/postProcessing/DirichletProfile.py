import openfoamparser_mai as Ofpp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import LinearNDInterpolator
import formating, thermo
import subprocess


path = f"../Dirichlet/"

D = 0.009
delta = 0.0005
H = 100
rCells = 3

mesh_shape = (rCells, 15 * rCells, 1)

formating.createCaseIFromCase(newCasePath=path,
                        baseCasePath="../case/")

formating.setMeshShape(path, mesh_shape=mesh_shape)

subprocess.run([path + "Allclean"])
subprocess.run([path + "Allrun"], check=True)

T, T_name = formating.find_time(path)

Temp = Ofpp.parse_internal_field(path + T_name[-1] + "/T")
Temp = Temp.reshape(mesh_shape)

Cx = Ofpp.parse_internal_field(path + T_name[-1] + "/Cx")
Cx = Cx.reshape(mesh_shape)

Cy = Ofpp.parse_internal_field(path + T_name[-1] + "/Cy")
Cy = Cy.reshape(mesh_shape)


r_grid = np.sqrt(Cx[:, 1, 0] ** 2 + Cy[:, 1, 0] ** 2) * 1e3
r_grid_an = np.linspace(4.0, 4.5, 100)

plt.plot(r_grid, Temp[:, 1, 0], 's')
plt.plot(r_grid_an, thermo.Dirichlet_sol(r_grid_an))
plt.show()

plt.plot(r_grid, np.abs(Temp[:, 1, 0] - thermo.Dirichlet_sol(r_grid)))
plt.show()

