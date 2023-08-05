========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/actor/badge/?style=flat
    :target: https://readthedocs.org/projects/actor
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/actor.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/actor

.. |wheel| image:: https://img.shields.io/pypi/wheel/actor.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/actor

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/actor.svg
    :alt: Supported versions
    :target: https://pypi.org/project/actor

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/actor.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/actor

.. |commits-since| image:: https://img.shields.io/github/commits-since/yasserfarouk/actor/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/yasserfarouk/actor/compare/v0.0.0...master



.. end-badges

A simple actor framework with dynamic parallelism

* Free software: GNU Lesser General Public License v2.1 or later (LGPLv2+)

Installation
============

::

    pip install actor

You can also install the in-development version with::

    pip install https://github.com/yasserfarouk/actor/archive/master.zip


Documentation
=============


https://actor.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
