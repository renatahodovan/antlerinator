============
ANTLeRinator
============

.. image:: https://img.shields.io/pypi/v/antlerinator?logo=python&logoColor=white
   :target: https://pypi.org/project/antlerinator/
.. image:: https://img.shields.io/pypi/l/antlerinator?logo=open-source-initiative&logoColor=white
   :target: https://pypi.org/project/antlerinator/
.. image:: https://img.shields.io/github/workflow/status/renatahodovan/antlerinator/main/master?logo=github&logoColor=white
   :target: https://github.com/renatahodovan/antlerinator/actions
.. image:: https://img.shields.io/coveralls/github/renatahodovan/antlerinator/master?logo=coveralls&logoColor=white
   :target: https://coveralls.io/github/renatahodovan/antlerinator

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

To use *ANTLeRinator*, it can be added to ``setup.cfg`` as an install
requirement:

.. code-block:: ini

    [options]
    install_requires =
        antlerinator
        antlr4-python2-runtime==4.9.2; python_version~="2.7"  # optional
        antlr4-python3-runtime==4.9.2; python_version>="3.0"  # optional

Note that *ANTLeRinator* has no direct dependency on the *ANTLRv4* runtime.

To install *ANTLeRinator* manually, e.g., into a virtual environment, go the
quick way::

    pip install antlerinator

Alternatively, clone the project and perform a local install::

    pip install .


Usage
=====

Downloading the ANTLRv4 tool jar file at run-time
-------------------------------------------------

If the *ANTLRv4* runtime is installed, *ANTLeRinator* can be used to download
the corresponding version of the tool jar file:

.. code-block:: python

    import antlerinator

    assert antlerinator.__antlr_version__ is not None  # alternatively: import antlr4

    path = antlerinator.download(lazy=True)

If the *ANTLRv4* runtime is not installed or a different version of the tool jar
is needed, the required version must/can be specified:

.. code-block:: python

    import antlerinator

    path = antlerinator.download(version='4.9.2', lazy=True)

By default, these approaches download files to a ``~/.antlerinator`` directory,
and only if necessary (i.e., the jar file has not been downloaded yet).

Downloading the ANTLRv4 tool jar manually
-----------------------------------------

Should there be need for downloading the ANTLR v4 tool jar manually, a helper
script is available::

    antlerinator-download --help

Adding ANTLRv4 support to the command line interface
----------------------------------------------------

If an application has an ``ArgumentParser``-based command line interface,
*ANTLeRinator* can be used to add a CLI argument to specify which *ANTLRv4* tool
jar to use. The default processing of the argument, also provided by
*ANTLeRinator*, is to download the tool jar version corresponding to the
*ANTLRv4* runtime if necessary:

.. code-block:: python

    import antlerinator
    import argparse
    import subprocess

    assert antlerinator.__antlr_version__ is not None

    parser = argparse.ArgumentParser()
    antlerinator.add_antlr_argument(parser)
    args = parser.parse_args()

    antlerinator.process_antlr_argument(args)

    subprocess.call(['java', '-jar', args.antlr])

.. end included documentation


Copyright and Licensing
=======================

Licensed under the BSD 3-Clause License_.

.. _License: LICENSE.rst
