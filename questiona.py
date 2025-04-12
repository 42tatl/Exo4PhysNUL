import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
import os
import functions as fct

executable = './Exe2'  # Remove .exe for Mac
repertoire = r"/Users/lilimouelle/Desktop/PHYSNUM/Exo4PhysNUL"  # Modify for correct directory
output_template = "output.out"
os.chdir(repertoire)

input_filename = "configa.in"

params = fct.read_in_file(input_filename)
R, r1, epsilon_a, epsilon_b, uniform_rho_case, VR, rho0, N1, N2, epsilon_0 = fct.get_params(params)

'''
output = fct.run_simulation(executable, input_filename,output_template) #je comprends pas comment je dois utiliser les fonctions lol
r, phi = fct.read_output_file_phi("outputs/output.out_phi.out")
'''

phi_file, E_file, D_file, _= fct.run_simulation(executable, input_filename, output_template)
r, phi, r_E, E, r_D, D = fct.read_output_files(phi_file, E_file, D_file)


plt.figure()
plt.plot(r, phi, marker='o')
plt.xlabel(r'r [m]')
plt.ylabel(r'$\phi$ [V]')
plt.grid(True)
plt.tight_layout()
fct.save_figure("phi_vs_r.png")
plt.show()

#Analytical solution
def phi_analytique(r):
    return 0.25 * (R**2 - r**2)
r_vals = np.linspace(0, R, 100)
phi_vals = phi_analytique(r_vals)
plt.figure()
plt.plot(r_vals, phi_vals, label=r"Analytical solution for $\phi(r)$", color='red')
plt.xlabel("r [m]")
plt.ylabel(r"$\phi(r)$ [V]")
plt.grid(True)
plt.legend()
plt.tight_layout()
fct.save_figure("phi_analytique.png")
plt.show()

#Comparaison with analytical solution
plt.figure()
plt.plot(r, phi, 'o-', label="Numerical", color='blue')
plt.plot(r_vals, phi_vals, '--', label="Analytical", color='red')
plt.xlabel("r [m]")
plt.ylabel(r"$\phi(r)$ [V]")
plt.grid(True)
plt.legend()
plt.tight_layout()
fct.save_figure("phi_comparaison.png")
plt.show()
