from fcc_ee_pywit_model.fcc_ee_pywit_model import FCCEEModel
import os

example_folder = '/Users/lorenzogiacomel/fcc_ee_pywit_model/examples/dummy_example'

collimator_settings_filename = os.path.join(example_folder,
                                            'dummy_collimator_settings.json')
taper_settings_filename = os.path.join(example_folder,
                                       'dummy_taper_settings.json')
elliptic_elements_settings_filename = os.path.join(example_folder,
                                                   'dummy_elliptic_elements_settings.json')
broadband_resonators_list = [os.path.join(example_folder,
                                          'dummy_broadband_resonators.json')]
resonators_list = [os.path.join(example_folder,
                                'dummy_resonators.json')]

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

model = FCCEEModel(
    energy=45.6e9, #80e9, 120e9, 175e9, 182.5e9
    collimator_settings_filename=collimator_settings_filename,
    taper_settings_filename=taper_settings_filename,
    elliptic_elements_settings_filename=elliptic_elements_settings_filename,
    broadband_resonators_list=broadband_resonators_list,
    resonators_list=resonators_list,
    f_params_dict=f_params_dict,
    z_params_dict=z_params_dict,
    additional_f_params=additional_f_params,
    normalized_emittance_for_coll=3.5,   #?
    compute_geometric_impedance_collimators=True,
    compute_taper_RW_impedance_collimators=True,
    use_single_layer_approx_for_coated_taper=True,
    frequency_parameters_for_taper_rw=frequency_parameters_for_taper_rw,
    f_cutoff_broadband=50e9,    #?
    compute_wake=False,     #?
)

print('a')
