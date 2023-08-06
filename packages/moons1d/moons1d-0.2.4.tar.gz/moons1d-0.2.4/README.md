moons1D
==============================

1D simulator for MOONS/VLT

Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Science templates and instrumental parameters
    │
    ├── notebooks          <- Jupyter notebooks.
    │   ├── MOONS Simulation - Single source
    |   ├── MOONS Simulation - Single source_allBands
    |   ├── MOONS Simulation - Multiple sources
    |   ├── Atmospheric_difraction
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── moons1d                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── spectra.py     <- Spectra module  
    │   ├── catalogue.py   <- Catalogue module 
    │   ├── simulator.py   <- Simulator module
    │
    ├── test               <- Unit tests and notebooks
	├── scripts            <- scripts to run directly throught the terminal 


--------

####Install Moons1d
	
```
git clone https://gitlab.obspm.fr/mrodrigues/moons1d.git
cd moons1d/
sudo python setup.py install
```
	

####Run scripts

```
cd scripts
python MultipleSource.py 
```


####Run notebooks
Use your favorite jupyter notebook server, e.g. https://nteract.io, to open the notebooks (with a python3 kernel

