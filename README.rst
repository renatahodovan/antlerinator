============
ANTLeRinator
============

.. image:: https://img.shields.io/pypi/v/antlerinator?logo=python&logoColor=white
   :target: https://pypi.org/project/antlerinator/
.. image:: https://img.shields.io/pypi/l/antlerinator?logo=open-source-initiative&logoColor=white
   :target: https://pypi.org/project/antlerinator/
.. image:: https://img.shields.io/github/workflow/status/renatahodovan/antlerinator/main/master?logo=github&logoColor=white
   :target: https://github.com/renatahodovan/antlerinator/actions

.. start included documentation

*ANTLeRinator* is a Python utility package to help keeping components of
ANTLR v4 in sync.


Requirements
============

* Python_ ~= 2.7 or >= 3.5
* pip_
* Java_ SE >= 7 JRE or JDK (the latter is optional)

.. _Python: https://www.python.org
.. _pip: https://pip.pypa.io
.. _Java: https://www.oracle.com/java/


Install
=======

The quick way::

    pip install antlerinator

Alternatively, by cloning the project and performing a local install::

    pip install .


Usage
=====

A common form of *ANTLeRinator*'s usage:

.. code-block:: python

    import antlerinator
    import argparse
    import subprocess

    assert antlerinator.__antlr_version__ is not None

    parser = argparse.ArgumentParser()
    parser.add_argument('--antlr')
    args = parser.parse_args()

    if not args.antlr:
        args.antlr = antlerinator.download(lazy=True)

    subprocess.call(['java', '-jar', args.antlr])

Should there be need for downloading the ANTLR v4 tool jar manually, a helper
script is available::

    antlerinator-download

.. end included documentation


Copyright and Licensing
=======================

Licensed under the BSD 3-Clause License_.

.. _License: LICENSE.rst
