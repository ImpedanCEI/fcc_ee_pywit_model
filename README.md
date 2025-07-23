# FCC-ee Impedance model for the collimation system

This repository contains the impedance model of the FCC-ee collider.

The intent of this package is to provide the infrastructure needed to develop the model.

## Status (updated 23.07.2025)

- Added elements:
  - Collimators: Geometrical (CST) and RW (IW2D) contributions are considered.
    Approximation using a linear taper.
  - Elliptic elements (pipes): IW2D + numerical form factor for both driving and detuning
    impedance, considering the realistic shape of the vacuum chamber.
  - Resonators
  - Broadband resonators


- Different optics have been analyzed:
    - GHC V23 by K. Oide: [FCCWeek_Optics_Oide_230606](https://indico.cern.ch/event/1202105/contributions/5408583/attachments/2659051/4608141/FCCWeek_Optics_Oide_230606.pdf)
    - GHC V24.4 by K. Oide: [Optics_Oide_241106](https://indico.cern.ch/event/1471642/contributions/6210189/attachments/2961576/5209132/Optics_Oide_241106.pdf)
    - GHC V23 by K. Oide: [Optics_Oide_bx*:techi_250424](https://indico.cern.ch/event/1509196/contributions/6480794/attachments/3055731/5402860/Optics_Oide_bx*_techi_250424.pdf)
    - LCC by P. Raimondi: [LCC optics developments.pdf ](https://indico.cern.ch/event/1566197/contributions/6605749/attachments/3106610/5506004/LCC%20optics%20developments.pdf)


- Various examples demonstrating how the code works are available,

- The collimators group has been specialized to give the possibility to have different
 emittances in x/y.





