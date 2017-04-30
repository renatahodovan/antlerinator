============
ANTLeRinator
============

*ANTLeRinator* is a Python 3 utility package to help keeping components of
ANTLR v4 in sync.


Requirements
============

* Python_ >= 3.4
* pip_ and setuptools Python packages (the latter is automatically installed by
  pip)
* Java_ SE >= 7 JRE or JDK (the latter is optional)

.. _Python: https://www.python.org
.. _pip: https://pip.pypa.io
.. _Java: https://www.oracle.com/java/


Install
=======

The quick way::

    pip install antlerinator

Alternatively, by cloning the project and running setuptools::

    python setup.py install


Usage
=====

A common form of *ANTLeRinator*'s usage:

.. code-block:: python

    import antlerinator
    import argparse
    import subprocess

    parser = argparse.ArgumentParser()
    parser.add_argument('--antlr', default=antlerinator.antlr_default_path)
    args = parser.parse_args()

    if (args.antlr == antlerinator.antlr_default_path):
        antlerinator.install(lazy=True)
    subprocess.call(['java', '-jar', args.antlr])

Should there be need for manual jar installation, a helper script is available::

    antlerinator-install


Copyright and Licensing
=======================

Licensed under the BSD 3-Clause License_.

.. _License: LICENSE.rst
