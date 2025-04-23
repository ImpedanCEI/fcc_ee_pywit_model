import numpy as np
import os 
import json

import_folder = "/home/dogibellieri/fcc_ee_pywit_model/examples/CST_results/Collimator_schematic/Longitudinal_taper_15deg"
output_folder = "/home/dogibellieri/fcc_ee_pywit_model/examples/fcc_ee_collimators_from_cst_long_15deg_wake_unitsTESTTT/collimator_schematic_normalized_long_unitsTESTTT"

for filename in os.listdir(import_folder):
    dict_out = {}
    table = np.loadtxt(f'{import_folder}/{filename}', skiprows=3)
    if filename.startswith("Impedance"):
        table[:, 0] *= 1e9 # to convert freq. from GHz to Hz
        #table[:, 1:3] *= -1e3 no need to normalize Z_long 
        if "long" in filename:
            component = "zlong"
        else: 
            raise ValueError("No long found in filename")
        
        dict_out[component] = {}
        dict_out[component]["frequency"] = table[:, 0].tolist()
        dict_out[component]["real impedance"] = table[:, 1].tolist()
        dict_out[component]["imaginary impedance"] = table[:, 2].tolist()

    elif filename.startswith("Wake"):
        table[:, 0] /= 1e3 # to convert from mm to m
        table[:, 1] *= 1e12 # from V/pC to V/C
        if "long" in filename:
            component = "wlong"
        else: 
            raise ValueError("No long found in filename")
        
        dict_out[component] = {}
        dict_out[component]["distance"] = table[:, 0].tolist()
        dict_out[component]["wake"] = table[:, 1].tolist()
    else:
        raise ValueError("Nor impedance either wake found in filename")
   
    # save the dictionary in a json file
    
    with open(f'{output_folder}/{filename}'.replace("txt", "json"), "w") as f:
        json.dump(dict_out, f, indent=2)

