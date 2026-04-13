import numpy as np
import formating
import subprocess


path = f"../uniform/"
ny1 = 5
W1 = 3.0
W2 = 45.4

formating.createCaseIFromCase(newCasePath=path,
                        baseCasePath="../case/")

formating.setDensityToUniform(path, filename="constant/turbulenceProperties")
formating.setMeshSize(path, ny1)
formating.setW(path, "W1", W1)
formating.setW(path, "W2", W2)

subprocess.run([path + "Allclean"])
subprocess.run([path + "Allrun"], check=True)

