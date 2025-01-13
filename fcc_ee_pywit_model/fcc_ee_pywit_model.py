from pywit.model import Model

from lhc_pywit_model.elliptic_elements_group import EllipticElementsGroup
from lhc_pywit_model.resonators_group import ResonatorsGroup
from lhc_pywit_model.broadband_resonators_group import BroadbandResonatorsGroup
from lhc_pywit_model.utils import execute_jobs_locally

from pywit.component import Component
from pywit.interface import component_names
from pywit.element import Element
from pywit.elements_group import ElementsGroup

from fcc_ee_pywit_model.package_paths import base_dir
from fcc_ee_pywit_model.parameters import DEFAULT_RESONATOR_F_ROI_LEVEL
from fcc_ee_pywit_model.utils import compute_betas_and_lengths
from fcc_ee_pywit_model.data.machine_layouts.fcc_ee_layout_b1 import layout_dict
from fcc_ee_pywit_model.collimators_group import CollimatorsGroup

from typing import List, Union, Callable, Dict
from pathlib import Path
import os
import json
from cpymad.madx import Madx
from scipy.constants import physical_constants, c as c_light
from scipy.interpolate import interp1d
import numpy as np


class FCCEEModel(Model):
    def __init__(self,
                 energy,  #45.6e9, 80e9, 120e9, 175e9, 182.5e9
                 collimator_settings_filename: Union[str, Path] = None,
                 taper_settings_filename: Union[str, Path] = None,
                 elliptic_elements_settings_filename: Union[str, Path] = None,
                 broadband_resonators_list: List[Union[str, Path]] = None,
                 resonators_list: List[Union[str, Path]] = None,
                 table_filenames_dict: Dict[str, Path] = None,
                 lxplusbatch: str = None,
                 f_params_dict: dict = None,
                 z_params_dict: dict = None, additional_f_params: dict = None,
                 jobs_submission_function: Callable = execute_jobs_locally,
                 rms_emittance_x_for_coll: float = None,
                 rms_emittance_y_for_coll: float = None,
                 compute_taper_RW_impedance_collimators: bool = False,
                 compute_geometric_impedance_collimators: bool = False,
                 use_single_layer_approx_for_coated_taper: bool = True,
                 frequency_parameters_for_taper_rw: dict = None,
                 resonator_f_roi_level: float = DEFAULT_RESONATOR_F_ROI_LEVEL,
                 f_cutoff_broadband: float = 50e9,
                 compute_wake: bool = False,
                 optics_filename: Union[str, Path] = 'twiss_fccee_b1.tfs',
                 markers_dict: Dict[str, float] = None,
                 beta_smooth_elements: List[str] = None
                 ):

        self.machine = 'FCCee'
        self.optics_filename = optics_filename

        e0 = physical_constants['electron mass energy equivalent in MeV'][0]*1e6

        self.relativistic_gamma = energy/e0
        self.relativistic_beta = np.sqrt(1-1/self.relativistic_gamma**2)

        mad = Madx()

        sequence_name = 'fccee_p_ring'

        ''''
        if energy <= 80:
            mad.call(os.path.join(optics_directory, 'lattices/z/fccee_z.seq'))
        else:
            mad.call(os.path.join(optics_directory, 'lattices/t/fccee_t.seq'))

        mad.input(f'beam, particle=POSITRON,energy={energy};'
                  f'use sequence={sequence_name};')
        '''

        sequence_name = 'ring'
        mad.call(os.path.join(base_dir, './fccee_collimation_lattice_forimpedance/FCCee_z_V23_tridodo572_colloptics_thin.seq'))
        if markers_dict is not None:
            for marker_name, s in markers_dict.items():
                mad.input(f'M: marker;')
                mad.input(f'{marker_name}: M;')
                mad.input(f'seqedit, sequence={sequence_name};')
                mad.input(f'install, element={marker_name}, at={s};')
                mad.input(f'endedit;')

        mad.input(f'beam, particle=POSITRON,energy={energy};use sequence={sequence_name};')
        mad.twiss(sequence=sequence_name, file=optics_filename)

        self.twiss = mad.table.twiss

        self.circ = self.twiss.summary.length
        radius = self.circ / (2 * np.pi)
        self.q_x = self.twiss.summary.q1
        self.q_y = self.twiss.summary.q2

        self.beta_x_smooth = radius / self.q_x
        self.beta_y_smooth = radius / self.q_y

        self.betas_lengths_dict = compute_betas_and_lengths(
            twiss_table=self.twiss,
            layout_dict=layout_dict,
            beta_smooth_elements=beta_smooth_elements,
            beta_x_smooth=self.beta_x_smooth,
            beta_y_smooth=self.beta_y_smooth
        )

        self.resonator_f_roi_level = resonator_f_roi_level

        elements_list = []

        if collimator_settings_filename is not None:
            self.normalized_emittance_x_for_coll = self.relativistic_gamma * self.relativistic_beta * rms_emittance_x_for_coll
            self.normalized_emittance_y_for_coll = self.relativistic_gamma * self.relativistic_beta * rms_emittance_y_for_coll

            elements_list.append(CollimatorsGroup(
                settings_filename=collimator_settings_filename,
                lxplusbatch=lxplusbatch,
                relativistic_gamma=self.relativistic_gamma,
                normalized_emittance_x=self.normalized_emittance_x_for_coll,
                normalized_emittance_y=self.normalized_emittance_y_for_coll,
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
                relativistic_gamma=self.relativistic_gamma,
                machine=self.machine,
                compute_wake=compute_wake,
                #yokoya_factors_beam_screen_filename=os.path.join(
                #    data_directory, 'elliptic_elements',
                #    'Yokoya_factors_elliptic.dat'),
                name='beam pipe',
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

        if table_filenames_dict is not None:
            group_element_list = []
            for group_name, group_dict in table_filenames_dict.items():
                # for each element, load the table and create the components
                for element_name, table_filename in group_dict.items():
                    # load the table
                    with open(table_filename) as table_file:
                        table_dict = json.load(table_file)

                    # extract the frequencies for the impedance and the distances for the wake

                    components_list = []

                    # for each component, create the component object
                    for component_name, component_dict in table_dict.items():
                        if component_name == 'frequency' or component_name == 'distance':
                            continue

                        # get the component properties from the component name
                        is_impedance, plane, exponents = component_names[component_name]

                        source_expoents = exponents[:2]
                        test_exponents = exponents[2:]

                        # create the impedance or wake functions
                        if is_impedance:
                            frequencies = np.array(component_dict['frequency'])
                            real_impedance = np.array(component_dict['real impedance'])
                            imaginary_impedance = np.array(component_dict['imaginary impedance'])
                            component_array = real_impedance + 1j*imaginary_impedance
                            impedance_func = interp1d(frequencies, component_array, bounds_error=False, fill_value=0)
                            wake_func = None
                        else:
                            distances = np.array(component_dict['distance'])
                            component_array = np.array(component_dict['wake'])
                            times = distances/(self.relativistic_beta*c_light)

                            wake_func = interp1d(times, component_array, bounds_error=False, fill_value=0)
                            impedance_func = None

                        # create the component object
                        components_list.append(Component(impedance=impedance_func, wake=wake_func, plane=plane,
                                                            source_exponents=source_expoents, test_exponents=test_exponents,
                                                            name=component_name))

                    # get the beta functions at the element
                    element_mask = self.twiss.name == element_name
                    beta_x = self.twiss.betx[element_mask][0]
                    beta_y = self.twiss.bety[element_mask][0]

                    # use almost zero length for the element since it is alrady taken into account in CST
                    length = 1e-12

                    # create the element object and append it to the elements list
                    group_element_list.append(Element(
                        components=components_list,
                        beta_x=beta_x,
                        beta_y=beta_y,
                        length=length,
                        name=element_name
                    ))
                
                elements_list.append(ElementsGroup(elements_list=group_element_list, name=group_name))

        os.remove(self.optics_filename)

        super().__init__(elements=elements_list, lumped_betas=(self.beta_x_smooth, self.beta_y_smooth))
