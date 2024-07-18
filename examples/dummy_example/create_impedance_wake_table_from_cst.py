import numpy as np
import json
from typing import Dict
from pathlib import Path
from pywit.interface import component_names

from fcc_ee_pywit_model.utils import create_impedance_wake_json_from_cst

create_impedance_wake_json_from_cst(
    filenames_dict={
        "zlong": Path("/home/giacomel/fcc_ee_pywit_model/examples/dummy_example/Z_cells15_teta10_Imm_and_real.txt"),
    },
    output_filename="try_impedance.json",
    skiprows=3
)

