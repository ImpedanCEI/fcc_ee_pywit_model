from lhc_pywit_model.collimators_group import CollimatorsGroup as LHCCollimatorsGroup

from typing import Union, Callable
from pathlib import Path
import numpy as np

from fcc_ee_pywit_model.parameters import DEFAULT_RESONATOR_F_ROI_LEVEL

from lhc_pywit_model.utils import execute_jobs_locally


class CollimatorsGroup(LHCCollimatorsGroup):
    def __init__(self, settings_filename: Union[str, Path], lxplusbatch: str, optics_filename: Union[Path, str],
                 relativistic_gamma: float,
                 f_params_dict: dict, z_params_dict: dict,
                 compute_geometric_impedance: bool, compute_taper_RW_impedance: bool,
                 use_single_layer_approx_for_coated_taper: bool, compute_wake: bool,
                 taper_settings: Union[str, Path], jobs_submission_function: Callable = execute_jobs_locally,
                 normalized_emittance_x: float = None, normalized_emittance_y: float = None, machine: str = 'LHC',
                 name: str = '', f_cutoff_bb: float = 50e9,
                 additional_f_params: dict = None, resonator_f_roi_level: float = DEFAULT_RESONATOR_F_ROI_LEVEL,
                 frequency_parameters_for_taper_rw: dict = None):

        self.normalized_emittance_x = normalized_emittance_x
        self.normalized_emittance_y = normalized_emittance_y

        super().__init__(settings_filename=settings_filename, lxplusbatch=lxplusbatch,
                         optics_filename=optics_filename, relativistic_gamma=relativistic_gamma,
                         f_params_dict=f_params_dict, z_params_dict=z_params_dict,
                         compute_geometric_impedance=compute_geometric_impedance,
                         compute_taper_RW_impedance=compute_taper_RW_impedance,
                         use_single_layer_approx_for_coated_taper=use_single_layer_approx_for_coated_taper,
                         compute_wake=compute_wake, taper_settings=taper_settings,
                         jobs_submission_function=jobs_submission_function,
                         normalized_emittance=None, machine=machine,
                         name=name, f_cutoff_bb=f_cutoff_bb,
                         additional_f_params=additional_f_params, resonator_f_roi_level=resonator_f_roi_level,
                         frequency_parameters_for_taper_rw=frequency_parameters_for_taper_rw)

    def compute_one_sigma_halfgap(self, beta_x, beta_y, angle):
        if self.normalized_emittance_x is None or self.normalized_emittance_y:
            raise ValueError('The normalized emittances must be specified in order to compute the one sigma half-gap')

        if self.relativistic_gamma is None:
            raise ValueError('The relativistic gamma factor must be specified in order to compute the one sigma '
                             'half-gap')

        relativistic_beta = np.sqrt(1-1/self.relativistic_gamma**2)

        emit_x = self.normalized_emittance_x
        emit_y = self.normalized_emittance_y

        return np.sqrt(beta_x*emit_x*np.cos(angle)**2/(relativistic_beta*self.relativistic_gamma) +
                       beta_y*emit_y*np.sin(angle)**2/(relativistic_beta*self.relativistic_gamma))
