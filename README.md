
<p align="center">
    <img src="./docs/source/_static/images/logo.png" alt="logo" width="200"/>
</p>


[![Release](https://badgen.net/github/release/manjavacas/melkit)]()
![License](https://img.shields.io/badge/license-GPLv3-blue)
[![Contributors](https://badgen.net/github/contributors/manjavacas/melkit)]() 
[![Documentation Status](https://readthedocs.org/projects/melkit/badge/?version=latest)](https://melkit.readthedocs.io/en/latest/?badge=latest)


**MELKIT** is a multi-purpose Python toolkit designed to easily edit and query [MELCOR 1.8.6](https://melcor.sandia.gov/) files.

## ⚙️ Utilities

- CV, CF and FL search, reading and listing.
- Object creation and removal from a given input file.
- Object update.
- EDF variables/values extraction, including dataframe conversion.
- Query FL connected CVs and CFs.
- CV extraction by group identifier.
- Listing of used/available IDs (and export to external .csv).
- Comment removal.
- Obtaining duplicate IDs
- ...


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

## 🚀 Contributing

See our [contributing](./CONTRIBUTING.md) guidelines.
