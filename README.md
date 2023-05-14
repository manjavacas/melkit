[![Release](https://badgen.net/github/release/manjavacas/melkit)]() ![License](https://img.shields.io/badge/license-GPLv3-blue) [![Contributors](https://badgen.net/github/contributors/manjavacas/melkit)]() [![Documentation Status](https://readthedocs.org/projects/melkit/badge/?version=latest)](https://melkit.readthedocs.io/en/latest/?badge=latest)

# MELKIT

A multi-purpose Python toolkit designed to facilitate the handling of MELCOR 1.8.6 files.

<p align="center">
    <img src="./img/logo.png" alt="drawing" width="150"/>
</p>

## ⚙️ Utilities

- Control Volumes (CVs), Flow Paths (FLs) and Control Functions (CFs) querying and edition.
- PTF and EDF visualization tools.
- Extraction of CVs and FL connections for a given CV.
- Extraction of CFs associated with a given FL, including recursive extraction of inter-dependent CFs.
- Auxiliary tools (comments deletion, duplicates checking...).
- And more!

## ▶️ Installation

Install MELKIT via [PyPI](https://pypi.org/project/melkit/):

```bash
pip install melkit
```

## 💻 How to use

The `Toolkit` class is all you need to start working with MELKIT.

```python
from melkit.toolkit import Toolkit

toolkit = Toolkit('file.inp')

cvs = toolkit.read_cvs()
fls = toolkit.read_fls()
```

Check out the [project documentation](https://melkit.readthedocs.io/en/latest/) for additional usage examples.

## 📦 Extensions

The **MELCOR Language Support** (MLS) is a MELCOR 1.8.6 syntax highlighter for Visual Studio Code.

It is publicly available at VS Marketplace. Just search for *MLS* or download it from [**here**](https://marketplace.visualstudio.com/items?itemName=manjavacas.mls).

## 👐 Contributing

Feel free to contribute via _issues_ and _pull requests_. See [CONTRIBUTING](./CONTRIBUTING.md).

## 📃 License 

See [LICENSE](./LICENSE).
