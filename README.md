# FCC-ee Impedance model

This repository contains the impedance model of the FCC-ee collider.

The intent of this package is to provide the infrastructure needed to develop the model.

## Status (updated 24.02.2025)

- Added elements:
  - Collimators: Geometrical (CST) and RW (IW2D) contributions are considered.
    Approximation using a linear taper.
  - Elliptic elements (pipes): IW2D + numerical form factor for both driving and detuning
    impedance, considering the realistic shape of the vacuum chamber.
  - Resonators
  - Broadband resonators

- Version 2023 of the collimation optics is considered.

- Various examples demonstrating how the code works are available,

- The collimators group has been specialized to give the possibility to have different
 emittances in x/y.

## TODO (updated 24.02.2025):
- Taper geometry and material optimization of collimators.




