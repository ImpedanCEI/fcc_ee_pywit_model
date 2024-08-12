from fcc_ee_pywit_model.fcc_ee_pywit_model import FCCEEModel
import os
import matplotlib.pyplot as plt
import numpy as np

example_folder = os. getcwd()

elliptic_elements_settings_filename = os.path.join(example_folder,
                                                   'FCC_ee_vz_elliptic_elements_settings.json')
broadband_resonators_list = [os.path.join(example_folder,
                                          'FCC_ee_vz_broadband_resonators.json')]
resonators_list = [os.path.join(example_folder,
                                'FCC_ee_vz_resonators.json')]

f_params_dict = {'start': 10,
                 'stop': 1e13,
                 'scan_type': 0,
                 'added': '1e-2 0.1 1 1e15',
                 'points_per_decade': 10,
                 'min_refine': 1e11,
                 'max_refine': 5e12,
                 'n_refine': 5000,
                 'sampling_exponent': 1e8,
                 }

additional_f_params = {'long_factor': 100,
                       'freq_lin_bisect': 1e11
                       }

z_params_dict = {'start': 0.01,
                 'stop': 1e13,
                 'scan_type': 2,
                 'added': ''
                 }

frequency_parameters_for_taper_rw = {
    'freq_start': 1e3,
    'freq_stop': 1e15,
    'num_points': 1000
}

collimators_table_dict = {}
folder = "collimator_schematic_normalized"
collimators_list = os.listdir(folder)
for filename in collimators_list:
    collimator_name = filename.split("_")[2]
    if not collimator_name.startswith("tcr"):
        collimators_table_dict[f"{collimator_name}:1"] = f"{folder}/{filename}"

    elif collimator_name.startswith("tcr"):
        collimators_table_dict[f"{collimator_name}:1"] = f"{folder}/{filename}"
        if "c0" in collimator_name:
            collimators_table_dict[collimator_name.replace("c0", "c2")+":1"] = f"{folder}/{filename}"

collimators_name = list(collimators_table_dict.keys())

for collimator_name in collimators_name:
    if collimator_name.startswith("tcr"):
        for ip in ["1", "3", "4"]:
            collimators_table_dict[collimator_name.replace(".2.", f".{ip}.")] = f"{folder}/{filename}"

table_filenames_dict = {'collimators': collimators_table_dict,
               #'bellows': blabla
               }


model = FCCEEModel(
    energy=45.6e9, #80e9, 120e9, 175e9, 182.5e9
    elliptic_elements_settings_filename=elliptic_elements_settings_filename,
    # broadband_resonators_list=broadband_resonators_list,
    # resonators_list=resonators_list,
    table_filenames_dict=table_filenames_dict,
    f_params_dict=f_params_dict,
    z_params_dict=z_params_dict,
    additional_f_params=additional_f_params,
    rms_emittance_x_for_coll=0.71e-9,   #?
    rms_emittance_y_for_coll=1.9e-12,  # ?
    compute_geometric_impedance_collimators=True,
    compute_taper_RW_impedance_collimators=True,
    use_single_layer_approx_for_coated_taper=True,
    frequency_parameters_for_taper_rw=frequency_parameters_for_taper_rw,
    f_cutoff_broadband=50e12,    #?
    compute_wake=False,     #?
)

total_model = model.total

disc_xdip = total_model.get_component('x1000').discretize(10**3, 1, 1e-1, 1e13, freq_precision_factor=0.1)[0]

plt.loglog(disc_xdip[0], (disc_xdip[1].real), '-', linewidth=2, label='real part')
plt.loglog(disc_xdip[0], (disc_xdip[1].imag), '--', linewidth=2, label='imaginary part')
plt.xlabel('frequency [Hz]')
plt.ylabel(r'x-dipolar impedance [$\Omega$/m]')
plt.legend()
plt.show()

disc_xdip = total_model.get_component('y0100').discretize(10**3, 1, 1e-1, 1e13, freq_precision_factor=0.1)[0]

plt.loglog(disc_xdip[0], (disc_xdip[1].real), '-', linewidth=2, label='real part')
plt.loglog(disc_xdip[0], (disc_xdip[1].imag), '--', linewidth=2, label='imaginary part')
plt.xlabel('frequency [Hz]')
plt.ylabel(r'y-dipolar impedance [$\Omega/m$]')
plt.legend()
plt.show()
