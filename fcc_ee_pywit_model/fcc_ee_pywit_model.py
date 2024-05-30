from pywit.model import Model

from lhc_pywit_model.collimators_group import CollimatorsGroup
from lhc_pywit_model.elliptic_elements_group import EllipticElementsGroup
from lhc_pywit_model.resonators_group import ResonatorsGroup
from lhc_pywit_model.broadband_resonators_group import BroadbandResonatorsGroup

from lhc_pywit_model.utils import execute_jobs_locally

from fcc_ee_pywit_model.package_paths import data_directory, optics_directory
from fcc_ee_pywit_model.parameters import DEFAULT_RESONATOR_F_ROI_LEVEL
from fcc_ee_pywit_model.utils import compute_betas_and_lengths
from fcc_ee_pywit_model.data.machine_layouts.fcc_ee_layout_b1 import layout_dict

from typing import List, Union, Callable
from pathlib import Path
import os
import json
from cpymad.madx import Madx
from scipy.constants import physical_constants
import numpy as np


class FCCEEModel(Model):
    def __init__(self,
                 energy, #45.6e9, 80e9, 120e9, 175e9, 182.5e9
                 collimator_settings_filename: Union[str, Path] = None,
                 taper_settings_filename: Union[str, Path] = None,
                 elliptic_elements_settings_filename: Union[str, Path] = None,
                 broadband_resonators_list: List[Union[str, Path]] = None,
                 resonators_list: List[Union[str, Path]] = None,
                 lxplusbatch: str = None,
                 f_params_dict: dict = None,
                 z_params_dict: dict = None, additional_f_params: dict = None,
                 jobs_submission_function: Callable = execute_jobs_locally,
                 normalized_emittance_for_coll: float = 3.5,
                 compute_taper_RW_impedance_collimators: bool = False,
                 compute_geometric_impedance_collimators: bool = False,
                 use_single_layer_approx_for_coated_taper: bool = True,
                 frequency_parameters_for_taper_rw: dict = None,
                 resonator_f_roi_level: float = DEFAULT_RESONATOR_F_ROI_LEVEL,
                 f_cutoff_broadband: float = 50e9,
                 compute_wake: bool = False,
                 optics_filename: Union[str, Path] = 'twiss_fccee_b1.tfs'
                 ):

        self.machine = 'FCCee'
        self.optics_filename = optics_filename

        e0 = physical_constants['electron mass energy equivalent in MeV'][0]*1e6

        relativistic_gamma = energy/e0

        mad = Madx()

        sequence_name = 'fccee_p_ring'

        if energy <= 80:
            mad.call(os.path.join(optics_directory, 'lattices/z/fccee_z.seq'))
        else:
            mad.call(os.path.join(optics_directory, 'lattices/t/fccee_t.seq'))

        mad.input(f'beam, particle=POSITRON,energy={energy};'
                  f'use sequence={sequence_name};')


        mad.input(f'use sequence={sequence_name};')
        mad.twiss(sequence=sequence_name, file=optics_filename)

        self.twiss = mad.table.twiss

        self.circ = self.twiss.summary.length
        radius = self.circ / (2 * np.pi)
        self.q_x = self.twiss.summary.q1
        self.q_y = self.twiss.summary.q1

        self.beta_x_smooth = radius / self.q_x
        self.beta_y_smooth = radius / self.q_y

        self.betas_lengths_dict = compute_betas_and_lengths(
            twiss_table=self.twiss,
            layout_dict=layout_dict,
        )

        self.resonator_f_roi_level = resonator_f_roi_level

        elements_list = []

        if collimator_settings_filename is not None:
            elements_list.append(CollimatorsGroup(
                settings_filename=collimator_settings_filename,
                lxplusbatch=lxplusbatch,
                relativistic_gamma=relativistic_gamma,
                normalized_emittance=normalized_emittance_for_coll,
                compute_wake=compute_wake,
                f_params_dict=f_params_dict,
                z_params_dict=z_params_dict,
                f_cutoff_bb=f_cutoff_broadband,
                name='collimators', machine=self.machine,
                compute_geometric_impedance=compute_geometric_impedance_collimators,
                compute_taper_RW_impedance=compute_taper_RW_impedance_collimators,
                use_single_layer_approx_for_coated_taper=use_single_layer_approx_for_coated_taper,
                optics_filename=optics_filename,
                additional_f_params=additional_f_params,
                jobs_submission_function=jobs_submission_function,
                taper_settings=taper_settings_filename,
                resonator_f_roi_level=self.resonator_f_roi_level,
                frequency_parameters_for_taper_rw=frequency_parameters_for_taper_rw
            ))

        if elliptic_elements_settings_filename is not None:
            elements_list.append(EllipticElementsGroup(
                lxplusbatch=lxplusbatch,
                parameters_filename=elliptic_elements_settings_filename,
                betas_lengths_dict=self.betas_lengths_dict,
                f_params_dict=f_params_dict, z_params_dict=z_params_dict,
                relativistic_gamma=relativistic_gamma,
                machine=self.machine,
                compute_wake=compute_wake,
                #yokoya_factors_beam_screen_filename=os.path.join(
                #    data_directory, 'elliptic_elements',
                #    'Yokoya_factors_elliptic.dat'),
                name='beam screen',
                f_cutoff=f_cutoff_broadband,
                additional_f_params=additional_f_params,
                jobs_submission_function=jobs_submission_function))

        if broadband_resonators_list is not None and len(broadband_resonators_list) > 0:
            for broadband_resonators_filename in broadband_resonators_list:
                with open(broadband_resonators_filename) as tapers_file:
                    broadband_resonators_filename_dict = json.load(tapers_file)

                elements_list.append(BroadbandResonatorsGroup(
                    betas_lengths_dict=self.betas_lengths_dict,
                    parameters_dict=broadband_resonators_filename_dict,
                    name='a broadband resonator'))

        if resonators_list is not None and len(resonators_list) > 0:
            for resonators_filename in resonators_list:
                with open(resonators_filename) as tapers_file:
                    resonators_filename_dict = json.load(tapers_file)

                elements_list.append(ResonatorsGroup(
                    betas_lengths_dict=self.betas_lengths_dict,
                    parameters_dict=resonators_filename_dict,
                    name=resonators_filename_dict['name']))

        super().__init__(elements=elements_list, lumped_betas=(self.beta_x_smooth, self.beta_y_smooth))
