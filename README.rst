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

* Python_ >= 3.5
* Java_ SE >= 7 JRE or JDK (the latter is optional)

.. _Python: https://www.python.org
.. _Java: https://www.oracle.com/java/


Install
=======

*ANTLeRinator* has both run-time and build-time components, therefore it can be
used both as an install requirement and as a setup requirement.

To use *ANTLeRinator* at run-time, it can be added to ``setup.cfg`` as an
install requirement (if using setuptools_ with declarative config):

.. code-block:: ini

    [options]
    install_requires =
        antlerinator
        antlr4-python3-runtime==4.9.2  # optional

Note that *ANTLeRinator* has no direct dependency on the *ANTLRv4* runtime.

To use *ANTLeRinator* at build-time, it can be added to ``pyproject.toml`` as a
build system/setup requirement (if using PEP517_ builds):

.. code-block:: toml

    [build-system]
    requires = [
        "antlerinator",
        "setuptools",
    ]
    build-backend = "setuptools.build_meta"

To install *ANTLeRinator* manually, e.g., into a virtual environment, use pip_::

    pip install antlerinator

The above approaches install the latest release of *ANTLeRinator* from PyPI_.
Alternatively, for the development version, clone the project and perform a
local install::

    pip install .

.. _setuptools: https://github.com/pypa/setuptools
.. _PEP517: https://www.python.org/dev/peps/pep-0517/
.. _pip: https://pip.pypa.io
.. _PyPI: https://pypi.org/


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

Building lexers/parsers at build-time with ANTLRv4
--------------------------------------------------

*ANTLeRinator* also extends *Setuptools* to allow building lexers/parsers at
build-time from ``.g4`` grammars. It adds two new *Setuptools* commands,
``build_antlr`` and ``clean_antlr``, to perform the building and the cleanup of
lexers/parsers, and also ensures that these new commands are invoked by the
standard ``build`` (``install``), ``develop``, ``clean``, and ``sdist`` commands
as well as by the *Setuptools*-internal ``editable_wheel`` command as
appropriate. The building of lexers/parsers is performed using the *ANTLRv4*
tool and is controlled by the ``[build_antlr]`` section in ``setup.cfg``:

.. code-block:: ini

    [build_antlr]
    commands =
        antlerinator:4.9.2 path/to/Dummy.g4 -Dlanguage=Python2 -o pkg/parser/py2 -Xexact-output-dir
        antlerinator:4.9.2 path/to/Dummy.g4 -Dlanguage=Python3 -o pkg/parser/py3 -Xexact-output-dir
    output =
        pkg/parser/py?/Dummy*.py
    #java =

The ``commands`` option of ``build_antlr`` lists the invocations of the
*ANTLRv4* tool. The first element of each invocation is a so-called provider
specification that defines where to get the *ANTLRv4* tool jar from. Currently,
two providers are supported: ``antlerinator:N.M`` uses *ANTLeRinator* to
download the requested version of the tool jar (if necessary), while
``file:/path/to/antlr.jar`` uses the explicitly given tool jar. The rest of the
elements of each invocation are passed to the tool jar as command line
arguments.

The ``java`` option can be given to explicitly specify which Java VM to use to
run the *ANTLRv4* tool (``java`` is used by default).

The ``output`` option shall list the file names or glob patterns of the output
of the *ANTLRv4* tool invocations. The ``clean_antlr`` command removes these
files on cleanup.

.. end included documentation


Copyright and Licensing
=======================

Licensed under the BSD 3-Clause License_.

.. _License: LICENSE.rst
