## Readme for Physics
This python package was built on top of the Pint Package by Connor McClellan for introducing units to python floats in the Value class and keeping a list of physical constants.

The main modules are the `Value` class (under value.py) and fundamental_constants (in fundamental_constants.py).

Units are accessed using the `ureg` object in `value.py`.

`Value` arithmetic is compatible with numpy arrays.  

It is recommended to use the Value arithmetic functions instead of python operations (i.e. `+ - / *`)to avoid unexpected behavior:

Example:


#### Working with Python2
Due to various encoding issues with python2, I changed many of the symbols in the doc strings such that the actually symbols will be different when printed.


#### Sphinx Docs

This project uses Sphinx for creating documentation.

To build the docs, create the docs directory and run `sphinx-quickstart --ext-autodoc`


#### Notes On Updated Package
run `python setup.py bdist_wheel` before committing to github