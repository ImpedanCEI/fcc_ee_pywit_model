# <img src="CEI_section_meeting/4_Full_Impedance_Model/logo/cei_logo.png" alt="CEI Logo" width="50"/>  FCC-ee PyWIT Model 

*This repository contains the Impedance/Wake (I/W) model of the FCC-ee collider.*

The intent of this package is to provide the infrastructure needed to develop and maintain the model.

---

## 🌀 Overview

This repository contains the necessary tools to develop the **FCC-ee Impedance/Wake Model** for the FCC-ee project.  

---
## 🚀 Getting Started

### 🛠️ PyWIT / xwakes 

*Toolbox to build and manipulate impedance and wake function models, usable in **Xsuite**, **DELPHI**, and others.*

#### 📦 Installation

Under a conda environment with Python 3.8+, install via **PyPI**: 

```bash
pip install xwakes
```

#### 🔗 Coupling Xwakes to IW2D
Xwakes can be coupled to IW2D using the executables obtained from compiling the C++ code.
Once the Python interface for IW2D is completed, this will no longer be necessary.

Some folders need to be created in the user’s home directory. This can be automatically done after installing Xwakes:

```bash
python -c 'import xwakes; xwakes.initialize_pywit_directory()'
```
#### ⚙️ Building IW2D Executables

Follow the IW2D README.md (https://gitlab.cern.ch/IRIS/IW2D/) to produce the executables:
- **flatchamber.x** 
- **roundchamber.x** 
- **wake_flatchamber.x** 
- **wake_roundchamber.x** 

After building, copy them to your PyWIT IW2D bin folder:

```bash
cp /path/to/iw2d/IW2D/cpp/*.x ~/pywit/IW2D/bin
```


## 📂 Get the FCC-ee Repository

```bash
git clone https://github.com/ImpedanCEI/fcc_ee_pywit_model/fcc_ee_pywit_model
```

## 📚 Examples & Hands-on Material

```bash
git clone https://github.com/ImpedanCEI/fcc_ee_pywit_model/tree/main/CEI_section_meeting
```


## 📁 Contents

- **Different optics have been analyzed:**
    - 📄**GHC V23 by K. Oide**: [FCCWeek_Optics_Oide_230606](https://indico.cern.ch/event/1202105/contributions/5408583/attachments/2659051/4608141/FCCWeek_Optics_Oide_230606.pdf)
    - 📄**GHC V24.4 by K. Oide**: [Optics_Oide_241106](https://indico.cern.ch/event/1471642/contributions/6210189/attachments/2961576/5209132/Optics_Oide_241106.pdf)
    - 📄**GHC V23 by K. Oide**: [Optics_Oide_bx*:techi_250424](https://indico.cern.ch/event/1509196/contributions/6480794/attachments/3055731/5402860/Optics_Oide_bx*_techi_250424.pdf)
    - 📄**LCC by P. Raimondi**: [LCC optics developments.pdf ](https://indico.cern.ch/event/1566197/contributions/6605749/attachments/3106610/5506004/LCC%20optics%20developments.pdf)


- 💡 Various examples demonstrating how the code works are available,

- 🎯 The collimators group has been specialized to give the possibility to have different emittances in x/y.

# <img src="CEI_section_meeting/4_Full_Impedance_Model/logo/fcc.png"  alt="CEI Logo" width="250"/> 







