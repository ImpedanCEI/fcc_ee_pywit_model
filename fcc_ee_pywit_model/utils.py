from typing import Union, Dict
from pathlib import Path
import pyoptics as opt
from pywit.interface import component_names
import json


import numpy as np
from scipy.interpolate import interp1d


def compute_betas_and_lengths(twiss_table,
                              layout_dict: dict,
                              beta_smooth_elements=None, 
                              beta_x_smooth=None,
                              beta_y_smooth=None) -> dict:
    
    if beta_smooth_elements is None:
        beta_smooth_elements = []
    else:
        if beta_x_smooth is None or beta_y_smooth is None:
            raise ValueError("if beta_smooth_elements is specified the smooth beta has to be specified too") 

    all_s = twiss_table.s 
    _, ind = np.unique(all_s, return_index=True)
    all_s = all_s[ind]
    all_betax = twiss_table.betx[ind]
    all_betay = twiss_table.bety[ind]
    # interpolating functions
    fx = interp1d(all_s, all_betax, kind='cubic')
    fy = interp1d(all_s, all_betay, kind='cubic')

    dict_betas_lengths = {}

    for name in layout_dict['betas_lengths_names']:

        if name not in beta_smooth_elements:
            length = 0
            betax = 0
            betay = 0

            for the_beg, the_end_ in zip(layout_dict['sbeg'][name],
                                        layout_dict['send'][name]):
                if the_end_ > twiss_table.summary.length:
                    the_end = twiss_table.summary.length
                else:
                    the_end = the_end_

                length += the_end - the_beg
                the_s = np.arange(the_beg, the_end_, 0.01)
                if the_end not in the_s:
                    the_s = np.hstack((the_s, [the_end]))
                # average beta (through trapz integration)
                betax += np.trapz(fx(the_s), x=the_s)
                betay += np.trapz(fy(the_s), x=the_s)

            if length != 0:
                betax /= length
                betay /= length

            dict_betas_lengths[name] = {
                'beta_x': betax,
                'beta_y': betay,
                'length': length
            }
        else:
            length = 0

            for the_beg, the_end_ in zip(layout_dict['sbeg'][name],
                                        layout_dict['send'][name]):
                if the_end_ > twiss_table.summary.length:
                    the_end = twiss_table.summary.length
                else:
                    the_end = the_end_

                length += the_end - the_beg

                dict_betas_lengths[name] = {
                    'beta_x': beta_x_smooth,
                    'beta_y': beta_y_smooth,
                    'length': length
                }

    return dict_betas_lengths


def create_impedance_wake_json_from_cst(
        filenames_dict: Dict[str, Path],
        output_filename: Path,
        skiprows: int = 3,
):
    # create an empty dictionary
    out_dict = {}

    # open each file, read the data and store it in the dictionary
    for component_name, filename in filenames_dict.items():

        # if the component name is not a valid one, raise an error
        if component_name not in component_names:
            raise ValueError(f"Component name {component_name} not in {component_names.keys()}")

        is_impedance, _, _ = component_names[component_name]

        # read the data and store it in the dictionary
        data = np.loadtxt(filename, skiprows=skiprows)
        out_dict[component_name] = data.tolist()  # to list because json doesn't like np.arrays

        if is_impedance:
            out_dict[component_name] = {
                "frequency": data[:, 0].tolist(),
                "real impedance": data[:, 1].tolist(),
                "imaginary impedance": data[:, 2].tolist(),
            }
        else:
            out_dict[component_name] = {
                "distance": data[:, 0].tolist(),
                "wake": data[:, 1].tolist(),
            }

    # save the dictionary in a json file
    with open(output_filename, "w") as f:
        json.dump(out_dict, f, indent=2)
