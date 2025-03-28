import numpy as np
import os 
import json

import_folder = "collimator_schematic_normalized_dip"
output_folder = "collimator_schematic_normalized_dip_minus"

for filename in os.listdir(import_folder):
    with open(f'{import_folder}/{filename}') as f:
        print(filename)
        dict_out = json.load(f)
    if filename.startswith("Impedance"):

        if "dipX" in filename:
            component = "zxdip"
        elif "dipY" in filename:
            component = "zydip"
        else: 
            raise ValueError("Nor dipX either dipY found in filename")
        
        dict_out[component]['real impedance'] = (np.array(dict_out[component]['real impedance'])*-1).tolist()
        dict_out[component]['imaginary impedance'] = (np.array(dict_out[component]['imaginary impedance'])*-1).tolist()

    elif filename.startswith("Wake"):
        pass
    else:
        raise ValueError("Nor impedance either wake found in filename")
   
    # save the dictionary in a json file
    
    with open(f'{output_folder}/{filename}', "w") as f:
        json.dump(dict_out, f, indent=2)

