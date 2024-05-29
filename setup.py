from setuptools import setup, find_packages
from setuptools.command.install import install
from os import makedirs
import pickle
import pathlib

class PostInstallCommand(install):
    def run(self):
        install.run(self)


setup(
    name='fcc_ee_pywit_model',
    version='0.1.0',
    packages=['fcc_ee_pywit_model'],
    url='https://github.com/ImpedanCEI/fcc_ee_pywit_model',
    license='MIT',
    author='Lorenzo Giacomel, Dora Gibellieri, Carlo Zannini',
    author_email='lorenzo.giacomel@cern.ch, dora.gibellieri@cern.ch, carlo.zannini@cern.ch',
    description='Impedance model of the FCC-ee',
    cmdclass={'install': PostInstallCommand},
    include_package_data=True,
    package_data={'lhc_pywit_model': ['data/*', 'data/resonators/*',
                                      'data/broadband_resonators/*', 'data/elliptic_elements/*',
                                      'data/machine_layouts/*',
                                      'data/collimators/*',
                                      'data/optics/*']},
    install_requires = ["numpy", "scipy", "matplotlib","pyoptics"]
)
