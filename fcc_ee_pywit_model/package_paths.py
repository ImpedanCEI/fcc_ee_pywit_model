import os
from pathlib import Path

base_dir = Path(__file__).parent.absolute().parent.absolute()
data_directory = os.path.join(Path(__file__).parent.absolute(), 'data')
optics_directory = os.path.join(Path(__file__).parent.parent.absolute(),
                                'fcc-ee-lattice')
