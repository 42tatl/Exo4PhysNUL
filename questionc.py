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

input_filename = "configc.in"

params = fct.read_in_file(input_filename)
R, r1, epsilon_a, epsilon_b, uniform_rho_case, VR, rho0, N1, N2, epsilon_0 = fct.get_params(params)

phi_file, E_file, D_file, _= fct.run_simulation(executable, input_filename, output_template)
r, phi, r_E, E, r_D, D = fct.read_output_files(phi_file, E_file, D_file)


def compute_div_D(r_D, D):
    #r * D
    rD = r_D * D

    # Derivative of rD with respect to r
    drD = (rD[2:] - rD[:-2]) / (r_D[2:] - r_D[:-2]) 

    # Middles of the middles
    r_midmid = 0.5 * (r_D[2:] + r_D[:-2])  # taille N-2

    #div(D) = (d/dr)(rD) / r
    div_D = drD / r_midmid

    return r_midmid, div_D

def rho_lib_function(r_vals, rho0, r1):
    return np.where(r_vals < r1, rho0 * np.sin(np.pi * r_vals / r1)*epsilon_0, 0)

r_midmid, div_D = compute_div_D(r_D, D)
rho_lib = rho_lib_function(r_midmid, rho0, r1)


plt.figure()
plt.plot(r_midmid, div_D, marker='o', label=fr"$\nabla \cdot \vec{{D}}$ (N1={N1}, N2={N2})", color='blue')
plt.xlabel(r'r [m]',fontsize=16)
plt.ylabel(r'$\nabla \cdot \vec{D}$ [C$ \cdot $m$^{-3}$]',fontsize=16)
plt.xticks(fontsize=12)  
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend(fontsize=16)
plt.tight_layout()
fct.save_figure("div_D.png")
plt.show()

plt.figure()
plt.plot(r_midmid, rho_lib, marker='o', label=r"$\rho_{lib}(r)$", color='blue')
plt.xlabel(r'r [m]',fontsize=16)
plt.ylabel(r'$\rho_{lib}$ [C$ \cdot $m$^{-3}$]',fontsize=16)
plt.xticks(fontsize=12)  
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend(fontsize=16)
plt.tight_layout()
fct.save_figure("rho_lib.png")
plt.show()

#Comparaison
plt.figure()
plt.plot(r_midmid, div_D, marker='o', label=fr"$\nabla \cdot \vec{{D}}$ (N1={N1}, N2={N2})", color='blue')
plt.plot(r_midmid, rho_lib, '--', label=r"$\rho_{lib}(r)$", color='red')
plt.xlabel(r'r [m]',fontsize=16)
plt.ylabel(r'Comparaison of the RHS to the LHS [C$ \cdot $m$^{-3}$]',fontsize=14)
plt.xticks(fontsize=12)  
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend(fontsize=16)
plt.tight_layout()
fct.save_figure("comparaison_divD_rho.png")
plt.show()

#Difference 
errors = []
for i in range(len(r_midmid)):
    errors.append(abs(div_D[i] - rho_lib[i]))

plt.figure()
plt.plot(r_midmid, errors, marker='o', label=fr"$\left| \nabla \cdot \vec{{D}} - \rho_{{lib}} \right|$ (N1={N1}, N2={N2})", color='blue')
plt.xlabel(r'r [m]',fontsize=16)
plt.ylabel(r'$\left| \nabla \cdot \vec{{D}} - \rho_{{lib}} \right|$ [C$ \cdot $m$^{-3}$]',fontsize=14)
plt.xticks(fontsize=12)  
plt.yticks(fontsize=12)
plt.grid(True)
plt.legend(fontsize=14)
plt.tight_layout()
fct.save_figure("erreur_divD_rho.png")
plt.show()











#Charges

#Total free charge
L = 1.0
h = r_D[1:] - r_D[:-1]
Q_lib = np.sum(rho_lib * r_D * h) * 2 * np.pi * L
print(f"Q_lib (charge libre totale) = {Q_lib:.4e} C")

#Total charge 
Q_tot = D[-1] * 2 * np.pi * R * L
print(f"Q_tot (charge totale) = {Q_tot:.4e} C")