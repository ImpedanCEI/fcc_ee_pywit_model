# FCC-ee Impedance model

This repository contains the impedance model of the FCC-ee collider.
The intent of this package is to provide the infrastructure needed to develop the model.

## Status (updated 29.05.2024)

- Added basic elements: 
  - Collimators: RW (IW2D) + geom (flat taper ) + RW of the tapers (very approximated model)
  - Elliptic elements (pipes): IW2D
  - Resonators
  - Broadband resonators

- The optics are taken from `acc-models/fcc/fcc-ee-lattice` but they do not include the collimation optics yet. **Hence 
the collimators cannot be included until the collimation optics are available.**

- A simple example showing how the code works is available

- The collimators group has been specialized to give the possibility to have different emittances in x/y

## TODO (updated 29.05.2024):
- Add collimation optics
