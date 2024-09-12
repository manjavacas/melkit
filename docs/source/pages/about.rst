About MELKIT
============

**MELKIT** is a multi-purpose Python toolkit designed to easily edit and query `MELCOR 1.8.6 <https://en.wikipedia.org/wiki/MELCOR>`_ models.

The aim of MELKIT is to facilitate the reading, processing, editing and visualisation of MELCOR input/output files, allowing basic CRUD (*Create*, *Remove*, *Update*, *Delete*) operations and additional functionalities through its **Toolkit** class.

Some of the operations that can be performed are:

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

.. warning:: The MELGEN and MELCOR executables are **NOT INCLUDED** in this package, as they are not freely distributable. Access to this MEGEN/MELCOR exectuables can be requested via the `Sandia National Laboratories website <https://www.sandia.gov/MELCOR/code-distribution/>`_.

.. note:: This project includes the maintenance of the **MLS** (*MELCOR Language Support*) VSCode extension. MLS is a MELCOR 1.8.6 syntax highlighter for Visual Studio Code.
    
    It is publicly available at VS Marketplace. Just search for MLS or download it from `here <https://marketplace.visualstudio.com/items?itemName=manjavacas.mls>`_.

.. tip:: Following this introduction, go to :ref:`examples` to look at different usage examples.