import numpy as np
import matplotlib.pyplot as plt
import openfoamparser_mai as Ofpp
import formating
from math import ceil

path_variable = f"../variable/"
path_uniform = f"../uniform/"
type = "250"

H1 = 30
H2 = 70

L1 = 600
L2 = 12600 - L1

T, T_name = formating.find_time(path_variable)

ny1 = 5
ny2 = ceil(ny1 * H2 / H1)
nx1 = ceil(ny1 * L1 / H1)
nx2 = ceil(ny1 * L2 / H1)

shape_block0 = (ny1, nx1)
shape_block1 = (ny2, nx1)
shape_block2 = (ny2, nx2)
shape_block3 = (ny1, nx2)

L_search = 9100 - L1
n_search = ceil(ny1 * L_search / H1)

Cx = Ofpp.parse_internal_field(path_variable + T_name[-1] + "/Cx")
Cy = Ofpp.parse_internal_field(path_variable + T_name[-1] + "/Cy")
U = Ofpp.parse_internal_field(path_variable + T_name[-1] + "/U")

k_variable = Ofpp.parse_internal_field(path_variable + T_name[-1] + "/k")
k_uniform = Ofpp.parse_internal_field(path_uniform + T_name[-1] + "/k")


datapath_variableLow = "ExpData/Low/"
datapath_variableHigh = "ExpData/High/"

def plot_expData(X_name, ax):
    X_exp_low = np.loadtxt(datapath_variableLow + type + "_" + X_name + ".txt", comments="#").T
    X_exp_high = np.loadtxt(datapath_variableHigh + type + "_" + X_name + ".txt", comments="#").T

    ax.plot(X_exp_low[1], X_exp_low[0], "s", c="tab:red", label="experiment")
    ax.plot(X_exp_high[1], (H1 + H2) - X_exp_high[0], "s", c="tab:red")

def plot_Field(Field, ax, label):

    Field_l = get_LSearch_line(Field)
    Cy_l = get_LSearch_line(Cy)

    ax.plot(Field_l, H1 + Cy_l*1000, '-o', label=label)


def get_LSearch_line(Field):

    start_ind_2 = shape_block0[0]*shape_block0[1] + shape_block1[0]*shape_block1[1]
    end_ind_2 = shape_block0[0]*shape_block0[1] + shape_block1[0]*shape_block1[1] + shape_block2[0]*shape_block2[1]

    Field2 = Field[start_ind_2:end_ind_2]
    Field3 = Field[end_ind_2:]

    Field2 = Field2.reshape(shape_block2)
    Field3 = Field3.reshape(shape_block3)

    return np.concatenate((Field3[:, n_search], Field2[:, n_search]))



fig, ax = plt.subplots(figsize=(8, 6))

ax.set_xlabel('k, [$m^2/s^2$]')
# ax.set_xlabel('U, [$m/s$]')

ax.set_ylabel('y, [$mm$]')


plot_Field(k_variable, ax, "variable")
plot_Field(k_uniform, ax, "uniform")
plot_expData("e", ax)


ax.set_xscale('log') 

ax.grid(True, alpha=0.3)
ax.set_ylim(0, H1 + H2)

plt.legend()
plt.show()
