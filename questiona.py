import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
import os
import functions as fct

executable = './Exe'  # Remove .exe for Mac
repertoire = r"/Users/lilimouelle/Desktop/PHYSNUM/Exo4PhysNUL"  # Modify for correct directory
output_template = "output.out"
os.chdir(repertoire)

input_filename = "configa.in"

params = fct.read_in_file(input_filename)
R, r1, epsilon_a, epsilon_b, uniform_rho_case, VR, rho0, N1, N2 = fct.get_params(params)

output = fct.run_simulation(executable, input_filename,output_template) #je comprends pas comment je dois utiliser les fonctions lol
r, phi = fct.read_output_file_phi("outputs/output.out_phi.out")


plt.figure()
plt.plot(r, phi, marker='o')
plt.xlabel(r'r [m]')
plt.ylabel(r'$\phi$ [V]')
plt.grid(True)
plt.tight_layout()
fct.save_figure("phi_vs_r.png")
plt.show()