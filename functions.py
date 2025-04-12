import numpy as np
import subprocess
import matplotlib.pyplot as plt
import os

def read_in_file(filename): 
    '''Reads in a file and returns the data as a list of floats'''
    variables = {}
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):  
                key, value = line.split("=")
                key = key.strip()
                value = value.split("//")[0].strip()  
                
                try:
                    if "." in value:
                        variables[key] = float(value)
                    else:
                        variables[key] = int(value)
                except ValueError:
                    print(f"Warning: Could not convert '{value}' to number. Check {filename}.")
    return variables

def get_params(params):
    '''Extracts the physical and numerical parameters from the dictionary'''
    R = params.get("R", 1.0)
    r1 = params.get("r1", 0.5)
    epsilon_a = params.get("epsilon_a", 1.0)
    epsilon_b = params.get("epsilon_b", 1.0)
    uniform_rho_case = params.get("uniform_rho_case", True)
    VR = params.get("VR", 0.0)
    rho0 = params.get("rho0", 1.0)
    N1 = params.get("N1", 10)
    N2 = params.get("N2", 10)
    epsilon_0 = params.get("epsilon_0", 8.854187817e-12)

    return R, r1, epsilon_a, epsilon_b, uniform_rho_case, VR, rho0, N1, N2, epsilon_0

#TEST
def run_simulation(executable, input_filename, output_template, **params):
    '''Runs the simulation with the given parameters'''

    # Ensure outputs/ subfolder exists
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Create the output filename from template
    raw_filename = output_template.format(**params)
    output_filename = os.path.join(output_dir, raw_filename)  # Save in subfolder

    # Build the command string
    param_str = " ".join(f"{key}={value:.15g}" for key, value in params.items())
    cmd = f'"{executable}" {input_filename} {param_str} output={output_filename}'

    print(f"\n Running command: {cmd}")

    # Run the command
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    print("----- STDOUT -----")
    print(result.stdout)

    print("----- STDERR -----")
    print(result.stderr)

    phi_file = output_filename + "_phi.out"
    E_file   = output_filename + "_E.out"
    D_file   = output_filename + "_D.out"

    return phi_file, E_file, D_file, result







def run_param_sweep_qa(executable, input_filename, param_name, values, fixed_params): #ATTENTION: cette fonction est seulement pour la question a car ca ecrase N2!!!!!
    phi_outputs = []
    E_outputs = []
    D_outputs = []
    param_list = []
    for val in values:
        params = fixed_params.copy()
        params[param_name] = val
        params["N2"] = val # Ensure N2 is set to the same value as N1
        output_template = f"output_{param_name}_{{{param_name}}}.out"
        phi_file, E_file, D_file, result = run_simulation(executable, input_filename, output_template, **params)
        phi_outputs.append(phi_file)
        E_outputs.append(E_file)
        D_outputs.append(D_file)
        param_list.append(params.copy())  # Store each individual param set
    return phi_outputs, E_outputs, D_outputs, param_list


def run_param_sweep(executable, input_filename, param_name, values, fixed_params): 
    phi_outputs = []
    E_outputs = []
    D_outputs = []
    param_list = []
    for val in values:
        params = fixed_params.copy()
        params[param_name] = val
        output_template = f"output_{param_name}_{{{param_name}}}.out"
        phi_file, E_file, D_file, result = run_simulation(executable, input_filename, output_template, **params)
        phi_outputs.append(phi_file)
        E_outputs.append(E_file)
        D_outputs.append(D_file)
        param_list.append(params.copy())  # Store each individual param set
    return phi_outputs, E_outputs, D_outputs, param_list





def save_figure(filename, fig=None, subfolder="figures", dpi=300, tight=True):
    """
    Saves a Matplotlib figure to a specified subfolder.

    Parameters:
        fig       : Matplotlib figure object
        filename  : Name of the file (e.g. 'plot.png')
        subfolder : Name of the subfolder to save into
        dpi       : Resolution in dots per inch
        tight     : Whether to use bbox_inches='tight'
    """
    if fig is None:
        fig = plt.gcf()  # get current figure *at call time*
    # Ensure the subfolder exists
    os.makedirs(subfolder, exist_ok=True)

    # Build full path
    filepath = os.path.join(subfolder, filename)

    # Save figure
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight' if tight else None)

    print(f"Figure saved to {filepath}")

def read_output_file_phi(filename):
    '''Reads output_phi.out and returns r, phi'''
    data = np.loadtxt(filename)
    r = data[:, 0]
    phi = data[:, 1]
    return r, phi

def read_output_files(phi_file, E_file, D_file):

    data_phi = np.loadtxt(phi_file)
    r = data_phi[:, 0]
    phi = data_phi[:, 1]

  
    data_E = np.loadtxt(E_file)
    r_E = data_E[:, 0]
    E = data_E[:, 1]

   
    data_D = np.loadtxt(D_file)
    r_D = data_D[:, 0]
    D = data_D[:, 1]

    return r, phi, r_E, E, r_D, D