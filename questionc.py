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

def compute_div_E(r_E, E):
    rE = r_E * E  # r * E

    # Derivative of rE with respect to r (centered difference)
    drE = (rE[2:] - rE[:-2]) / (r_E[2:] - r_E[:-2])

    # Mid-middles of r for plotting (size N-2)
    r_midmid = 0.5 * (r_E[2:] + r_E[:-2])

    # Divergence of E
    div_E = drE / r_midmid

    return r_midmid, div_E


r_midmid, div_D = compute_div_D(r_D, D)
rho_lib = rho_lib_function(r_midmid, rho0, r1)

'''
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
'''





#Charges
r_midmid_E, div_E = compute_div_E(r_E, E)

h_D = r_D[1:] - r_D[:-1]
h_midmid = r_midmid[1:] - r_midmid[:-1]
h_E = r_E[1:] - r_E[:-1]

#Free charges 
Q_lib = 2 * np.pi * np.dot(D[1:] * r_D[1:], h_D) 
print(f"Q_lib = {Q_lib} C")
Q_lib_analytique = 2 * np.pi * epsilon_0 * np.dot(rho_lib[:-1] * r_midmid[:-1], h_midmid)
print(f"Q_lib_analytique = {Q_lib_analytique} C")

#Total charges
Q_total = 2*epsilon_0*np.pi*np.dot(E[1:] * r_E[1:], h_E)
print(f"Q_total = {Q_total} C")

#Polarization charges
i_r1 = np.argmin(np.abs(r_D - r1)) 
rho_pol = epsilon_0*div_E[i_r1]-div_D[i_r1]
print(f"rho_pol = {rho_pol} C/m^3")
