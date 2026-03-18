import openfoamparser_mai as Ofpp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.interpolate import LinearNDInterpolator
import formating, thermo
import subprocess


path = f"../Dirichlet_0/"

D = 0.009
delta = 0.0005
H = 100
rCells = 2

mesh_shape = (rCells, 15 * rCells, 150 * rCells)

formating.createCaseIFromCase(newCasePath=path,
                        baseCasePath="../Dirichlet/")

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


r_grid = np.sqrt(Cx[mesh_shape[0]//2, mesh_shape[1]//2, :] ** 2 + Cy[mesh_shape[0]//2, mesh_shape[1]//2, :] ** 2) * 1e3
r_grid_an = np.linspace(1e3 * (D/2 - delta), 1e3 * D/2, 100)

plt.plot(r_grid, Temp[mesh_shape[0]//2, mesh_shape[1]//2, :], 's')
plt.plot(r_grid_an, thermo.Dirichlet_sol(r_grid_an), label='theory')
plt.xlabel("Радиус, мм")
plt.ylabel("Температура, К")
plt.grid(True, alpha=0.3)
plt.legend()
# plt.show()

plt.savefig('ProfileTDirichlet.png', dpi=300, bbox_inches='tight')

plt.plot(r_grid, np.abs(Temp[mesh_shape[0]//2, mesh_shape[1]//2, :] - thermo.Dirichlet_sol(r_grid)))
plt.show()

