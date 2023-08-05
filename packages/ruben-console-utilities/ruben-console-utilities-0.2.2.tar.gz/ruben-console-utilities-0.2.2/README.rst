Python Console Utilities
========================

.. image:: https://travis-ci.com/Ruben9922/python-console-utilities.svg?branch=master
    :target: https://travis-ci.com/Ruben9922/python-console-utilities
    :alt: Build Status

.. image:: https://readthedocs.org/projects/python-console-utilities/badge/?version=latest
    :target: https://python-console-utilities.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/ruben-console-utilities
    :target: https://pypi.org/project/ruben-console-utilities/
    :alt: PyPI

.. image:: https://img.shields.io/github/license/Ruben9922/python-console-utilities
    :target: https://github.com/Ruben9922/python-console-utilities/blob/master/LICENSE
    :alt: GitHub

This is a package containing utility functions for command-line applications.

.. Warning:: As this library is still in version 0.y.z, keep in mind that the API may change at any time. See Item 4 of the Semantic Versioning Specification: https://semver.org/#spec-item-4.

Features
--------

* Inputting an integer, float or boolean
* Selecting from a list of options (by entering an integer or character)

Goals
-----

* **Simplicity**: Straightforward, high-level functions with sensible defaults. Most parameters are optional, so you can
  hit the ground running.
* **Flexible**: An extensive range of options are provided, making the library useful in a wide range of situations.

Installation
------------

Install as usual::

    pip install ruben-console-utilities

You may wish to `create a virtual environment <https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments>`_ beforehand.

Usage
-----

Here a few examples:

>>> import consoleutilities as cu
>>> cu.input_option_int(["Export as PDF", "Export as HTML", "Export as TeX"])
[0]: Export as PDF
[1]: Export as HTML
[2]: Export as TeX
Enter integer [0..2]: >? 0
0
>>> cu.input_int("Pick a number between 1 and 10: ", 1, 10, include_max=True)
Pick a number between 1 and 10: >? 8
8
>>> cu.input_boolean("Specify whether to trust this host")
Specify whether to trust this host [y/N]: >? abc123
False
>>> cu.input_boolean("Specify whether to enable HTTPS", default=True)
Specify whether to enable HTTPS [Y/n]: >?
True
