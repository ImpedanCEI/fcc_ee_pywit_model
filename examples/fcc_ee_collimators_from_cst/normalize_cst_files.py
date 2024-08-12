import numpy as np
import os 
import json

import_folder = "../CST_results/Collimator_schematic"
output_folder = "collimator_schematic_normalized"

for filename in os.listdir(import_folder):
    dict_out = {}
    table = np.loadtxt(f'{import_folder}/{filename}', skiprows=3)
    if filename.startswith("Impedance"):
        table[:, 0] *= 1e9
        table[:, 1:3] *= 1e3
        if "dipX" in filename:
            component = "zxdip"
        elif "dipY" in filename:
            component = "zydip"
        else: 
            raise ValueError("Nor dipX either dipY found in filename")
        
        dict_out[component] = {}
        dict_out[component]["frequency"] = table[:, 0].tolist()
        dict_out[component]["real impedance"] = table[:, 1].tolist()
        dict_out[component]["imaginary impedance"] = table[:, 2].tolist()

    elif filename.startswith("Wake"):
        table[:, 0] /= 1e3
        table[:, 1] *= 1e3
        if "dipX" in filename:
            component = "wxdip"
        elif "dipY" in filename:
            component = "wydip"
        else: 
            raise ValueError("Nor dipX either dipY found in filename")
        
        dict_out[component] = {}
        dict_out[component]["distance"] = table[:, 0].tolist()
        dict_out[component]["wake"] = table[:, 1].tolist()
    else:
        raise ValueError("Nor impedance either wake found in filename")
   
    # save the dictionary in a json file
    
    with open(f'{output_folder}/{filename}'.replace("txt", "json"), "w") as f:
        json.dump(dict_out, f, indent=2)

