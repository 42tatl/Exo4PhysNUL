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
    '''Extracts the parameters from the dictionary'''
    tFin = params.get("tFin", 0.0)
    m1 = params.get("m1", 0.0)
    m2 = params.get("m2", 0.0)
    x0 = params.get("x0", 0.0)
    v0x = params.get("v0x", 0.0)
    v0y = params.get("v0y", 0.0)
    a = params.get("a", 0.0)
    tol = params.get("tol", 0.0)
    return tFin, m1, m2, x0, v0x, v0y, a, tol

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

    # Check result
    if os.path.exists(output_filename):
        print(f" SUCCESS: Output file '{output_filename}' was created!")
    else:
        print(f" ERROR: The output file '{output_filename}' was NOT created!")

    return output_filename, result

def run_param_sweep(executable, input_filename, param_name, values, fixed_params):
    outputs = []
    param_list = []
    for val in values:
        params = fixed_params.copy()
        params[param_name] = val
        output_template = f"output_{param_name}_{{{param_name}}}.out"
        outname, result = run_simulation(executable, input_filename, output_template, **params)
        outputs.append(outname)
        param_list.append(params.copy())  # Store each individual param set
    return outputs, param_list


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

def read_output_file(filename):
    data = np.loadtxt(filename)
    a = data[:, 0]
    b = data[:, 3]
    c = data[:, 4]
    d = data[:, 1]
    e = data[:, 2]
    f = data[:, 5]
    g = data[:, 6] #j'ai besoin des nsteps
    return a,b,c,d,e,f,g
