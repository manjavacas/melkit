import os

from setuptools import find_packages, setup

with open(os.path.join('melkit', 'version.txt'), 'r') as f:
    __version__ = f.read().strip()

with open('requirements.txt') as f:
    reqs = f.read().splitlines()

setup(name='melkit',
      version=__version__,
      packages=[package for package in find_packages() if package.startswith('melkit')],
      license='GPL3',
      author='Antonio Manjavacas',
      author_email='manjavacas@ugr.es',
      description='A toolkit designed to facilitate the handling of MELCOR/MELGEN 1.8.6 files.',
      url='https://github.com/manjavacas/melkit',
      keywords='toolkit, melcor, melcor-fusion, melgen',
      install_requires=reqs,
      include_package_data=True,
      extras_require={
          'doc': [
            'sphinx-autoapi==2.0.1',
            'sphinx-rtd-theme==1.2.0',
            'sphinxcontrib-applehelp==1.0.4',
            'sphinxcontrib-devhelp==1.0.2',
            'sphinxcontrib-htmlhelp==2.0.1',
            'sphinxcontrib-jquery==2.0.0',
            'sphinxcontrib-jsmath==1.0.1',
            'sphinxcontrib-qthelp==1.0.3',
            'sphinxcontrib-serializinghtml==1.1.5'
          ]
      }
      )