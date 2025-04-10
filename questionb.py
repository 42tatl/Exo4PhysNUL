import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
import os
import functions as fct

executable = './Exe'  # Remove .exe for Mac
repertoire = r"/Users/lilimouelle/Desktop/PHYSNUM/Exo4PhysNUL"  # Modify for correct directory
os.chdir(repertoire)

input_filename = "configa.in"
output_template = "output_{paramstr}_{value}.out"

params = fct.read_in_file(input_filename)
R, r1, epsilon_a, epsilon_b, uniform_rho_case, VR, rho0, N1, N2 = fct.get_params(params)

output_phi = fct.run_simulation(executable, input_filename,"N", [3], {"adapt": 0})
r, phi = fct.read_output_file_phi(output_phi)


plt.figure()
plt.plot(r, phi, marker='o')
plt.xlabel("r (m)")
plt.ylabel("φ(r) (V)")
plt.title("Potentiel φ en fonction de r")
plt.grid(True)
plt.tight_layout()
fct.save_figure("phi_vs_r.png")
plt.show()