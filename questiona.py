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

phi_file, E_file, D_file, _= fct.run_simulation(executable, input_filename, output_template)
r, phi, r_E, E, r_D, D = fct.read_output_files(phi_file, E_file, D_file)


plt.figure()
plt.plot(r, phi, marker='o', label=rf"$\phi(r)$ (N1 = N2 = {N1})", color='blue')
plt.xlabel(r'r [m]',fontsize=16)
plt.ylabel(r'$\phi$ [V]',fontsize=16)
plt.xticks(fontsize=12)  
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend()
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
plt.xlabel("r [m]",fontsize=16)
plt.ylabel(r"$\phi(r)$ [V]",fontsize=16)
plt.xticks(fontsize=12)  
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend()
plt.tight_layout()
fct.save_figure("phi_analytique.png")
plt.show()

#Comparaison with analytical solution
plt.figure()
plt.plot(r, phi, 'o-', label="Numerical", color='blue')
plt.plot(r_vals, phi_vals, '--', label="Analytical", color='red')
plt.xlabel("r [m]",fontsize=16)
plt.ylabel(r"$\phi(r)$ [V]",fontsize=16)
plt.xticks(fontsize=12)  
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend()
plt.tight_layout()
fct.save_figure("phi_comparaison.png")
plt.show()

#Convergence study
errors = []
N_values = []
dts = []
dts_squared = []
phi_outputs, E_outputs, D_outputs, param_sets = fct.run_param_sweep_qa(executable, input_filename, "N1", np.linspace(20, 100, 10, dtype=int), params)
phi_anal_0 = 0.25 * (R**2)
for phi_file, E_file, D_file, param_set in zip(phi_outputs, E_outputs, D_outputs, param_sets):
    r, phi = fct.read_output_file_phi(phi_file)
    phi_0 = phi[0]
    error = np.abs(phi_0 - phi_anal_0)
    errors.append(error)
    N_values.append(param_set["N1"])
    dts.append(1/param_set["N1"])
    dts_squared.append(1/(param_set["N1"]**2))

plt.figure()
plt.plot(dts_squared, errors, 'o-', label=r"$|\phi_\mathrm{num}(0) - \phi_\mathrm{anal}(0)|$")
plt.xlabel(r"N$^{-2}$ (N1=N2)", fontsize=16)
plt.ylabel(r"Error on $\phi(0)$ [V]", fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend()
plt.tight_layout()
fct.save_figure("convergence_phi0_dt.png")
plt.show()

plt.figure()
plt.loglog(N_values, errors, 'o-', label=r"$|\phi_\mathrm{num}(0) - \phi_\mathrm{anal}(0)|$")
plt.xlabel(r"N (N1=N2)", fontsize=16)
plt.ylabel(r"Error on $\phi(0)$ [V]", fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend()
plt.tight_layout()
fct.save_figure("convergence_phi0_N.png")
plt.show()