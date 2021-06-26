============================
*ANTLeRinator* Release Notes
============================

.. start included documentation

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