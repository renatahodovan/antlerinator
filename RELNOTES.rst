============================
*ANTLeRinator* Release Notes
============================

.. start included documentation

1!3.0.1
=======

Summary of changes:

* Improved code internals of setuptools extension (remove reference to
  deprecated Distutils).
* Improved testing (on Python 3.12, 3.13, and on PyPy 3.11; also linting tests;
  bumped ANTLR version in tests to 4.13.2; editable installs via development
  mode).
* Improved package metadata.
* Improved documentation (switched to furo theme).
* Dropped support for Python 3.6, 3.7, and 3.8.


1!3.0.0
=======

Summary of changes:

* Changed setuptools extension not to clean generated lexer/parser before
  creating an sdist.
* Dropped support for Python 3.5, bumped minimum Python requirement to 3.6.
* Internal refactorings (to make use of new language features).
* Improved testing infrastructure (testing Python 3.11; maintenance changes).


1!2.1.0
=======

Summary of changes:

* Enabled use of recursive wildcard patterns in the output option of the
  setuptools extension.
* Extended/fixed setuptools extension to also handle editable wheels.
* Improved testing (linting).
* Improved metadata.


1!2.0.1
=======

Summary of changes:

* Fixed SSL context creation.
* Internal refactorings (to access package metadata).
* Improved testing (on Python 3.10).
* Improved documentation.


1!2.0.0
=======

Summary of changes:

* Dropped support for Python 2.
* Changed API, introduced keyword-only arguments.
* Improved documentation.
* Improved testing (on PyPy).


1!1.1.0
=======

Summary of changes:

* Implemented setuptools extension to help lexer/parser generation at
  build-time.
* Moved from flat layout to src layout.
* Improved testing (linting, coverage information).
* Improved documentation.


1!1.0.0
=======

First release of *ANTLeRinator* in the new Epoch 1.

Summary of main features:

* Helps downloading any version of the ANTLR v4 tool jar, especially the one in
  sync with the antlr4-python?-runtime package, if installed (both from API and
  CLI).
* Helps adding and processing ANTLR-specific CLI option.

Summary of changes compared to Epoch 0 (4.6-4.9.2):

* Broke away from ANTLR's versioning and started a new epoch where versions
  reflect the evolution of the API of the *ANTLeRinator* package.
* Removed antlr4-python?-runtime as an install dependency.
* Changed API and CLI to use the term 'download' instead of 'install'.
* Made the handling of CLI options similar to and based on the *inators*
  package.
* Moved to pyproject.toml & setup.cfg-based packaging.
