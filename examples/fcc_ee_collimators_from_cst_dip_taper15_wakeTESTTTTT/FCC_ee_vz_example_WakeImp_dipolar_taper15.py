# Optimized and reorganized version of the original script for clarity and efficiency

from fcc_ee_pywit_model.fcc_ee_pywit_model import FCCEEModel
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

# === Global configuration ===
example_folder = os.getcwd()
folder_images = '/home/dogibellieri/fcc_ee_pywit_model/examples/fcc_ee_collimators_from_cst_dip_taper15_wake/Images_wakeBenchmark'
folder_txt = '/home/dogibellieri/fcc_ee_pywit_model/examples/fcc_ee_collimators_from_cst_dip_taper15_wake/OutputTXT_wakeBenchmark'
os.makedirs(folder_images, exist_ok=True)
os.makedirs(folder_txt, exist_ok=True)

mpl.rcParams.update({'font.size': 18, 'xtick.labelsize': 18, 'ytick.labelsize': 18})

# === Input files for the model ===
elliptic_file = os.path.join(example_folder, 'FCC_ee_vz_elliptic_elements_settings_neg_150nm_Mauro.json')
broadband_list = [os.path.join(example_folder, 'FCC_ee_vz_broadband_resonators.json')]
resonators_list = [os.path.join(example_folder, 'FCC_ee_vz_resonators.json')]

# === Frequency scan parameters ===
f_params_dict = {
    'start': 1e-5, 'stop': 1e14, 'scan_type': 0,
    'added': '1e-6 1e-5 1e-4 1e-2 0.1 1 1e13 1e15',
    'points_per_decade': 30, 'min_refine': 1e10,
    'max_refine': 1e13, 'n_refine': 10000,
    'sampling_exponent': 1e9,
}

additional_f_params = {'long_factor': 100, 'freq_lin_bisect': 1e11}

z_params_dict = {
    'start': 1e-5, 'stop': 1e13, 'scan_type': 2,
    'added': '1e-6 1e-4 1e-2 0.1 1 1e10'
}

frequency_parameters_for_taper_rw = {
    'freq_start': 1e3, 'freq_stop': 1e15, 'num_points': 1000
}

# === Load collimator geometries from folder ===
collimators_dict = {}
collimators_folder = os.path.join(example_folder, 'examples/fcc_ee_collimators_from_cst_dip_taper15_wake/collimator_schematic_normalized')
for fname in os.listdir(collimators_folder):
    cname = fname.split('_')[2]
    key = f"{cname}:1"
    path = os.path.join(collimators_folder, fname)
    collimators_dict[key] = path
    if cname.startswith("tcr") and "c0" in cname:
        collimators_dict[cname.replace("c0", "c2")+":1"] = path

# Add IP-matched collimators for 'tcr' types
collimators_keys = list(collimators_dict.keys())
for cname in collimators_keys:
    if cname.startswith("tcr"):
        for ip in ["1", "3", "4"]:
            collimators_dict[cname.replace(".2.", f".{ip}.")] = collimators_dict[cname]

# === Initialize the model ===
model = FCCEEModel(
    energy=45.6e9,
    elliptic_elements_settings_filename=elliptic_file,
    table_filenames_dict={'collimators': collimators_dict},
    f_params_dict=f_params_dict,
    z_params_dict=z_params_dict,
    additional_f_params=additional_f_params,
    rms_emittance_x_for_coll=0.71e-9,
    rms_emittance_y_for_coll=1.9e-12,
    compute_geometric_impedance_collimators=True,
    compute_taper_RW_impedance_collimators=True,
    use_single_layer_approx_for_coated_taper=True,
    frequency_parameters_for_taper_rw=frequency_parameters_for_taper_rw,
    f_cutoff_broadband=50e12,
    compute_wake=True,
    beta_smooth_elements=['pipe_section_1']
)

# === Wake sampling parameters ===
wake_params = {
    'freq_points': 8000,
    'time_points': 100000,
    'freq_start': 1e-5,
    'freq_stop': 1e14,
    'time_start': 1e-15,
    'time_stop': 1e-5,
    'freq_precision_factor': 0.05
}

# === Utility function for exporting and plotting impedance ===
def export_impedance_and_plot(model, comp, name_suffix):
    freqs = model.total.get_component(comp).discretize(**wake_params)[0][0]
    for idx, element in enumerate(model.elements[:2]):
        Z_re = element.get_component(comp).impedance(freqs).real
        Z_im = element.get_component(comp).impedance(freqs).imag
        tag = 'RW_pipe' if idx == 0 else 'Coll_CST'

        np.savetxt(os.path.join(folder_txt, f"{tag}_Z{comp[1]}_dip_Re_{name_suffix}.txt"),
                   np.column_stack((freqs, Z_re)), header="Frequency (Hz)\tReal Part (Ohm/m)", comments='')
        np.savetxt(os.path.join(folder_txt, f"{tag}_Z{comp[1]}_dip_Im_{name_suffix}.txt"),
                   np.column_stack((freqs, Z_im)), header="Frequency (Hz)\tImaginary Part (Ohm/m)", comments='')

        # Plotting
        for Z, part in zip([Z_re, Z_im], ['Re', 'Im']):
            plt.figure(figsize=(10, 7.5))
            plt.plot(freqs, Z, label=f'{part} Z_{comp[1]}')
            plt.xlabel('Frequency [Hz]')
            plt.ylabel(f'{part}(Z_{comp[1]}^{{dip}}) [Ohm/m]')
            plt.title(f'{tag} {part}(Z_{comp[1]})')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(folder_images, f"{tag}_Z{comp[1]}_dip_{part}_{name_suffix}.png"))
            plt.close()


# === Execute export and plotting for each component ===
for comp in ['x1000', 'y0100']:
    export_impedance_and_plot(model, comp, 'taper15')