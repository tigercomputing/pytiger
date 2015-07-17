************
Contributing
************

Contributions to pytiger are welcome, but should follow some guidelines.

Versioning
==========

pytiger uses the
`semantic versioning scheme v2.0.0 <http://semver.org/spec/v2.0.0.html>`_
for version numbering.

Briefly, that means:

    Given a version number MAJOR.MINOR.PATCH, increment the:

    * MAJOR version when you make incompatible API changes,
    * MINOR version when you add functionality in a backwards-compatible manner, and
    * PATCH version when you make backwards-compatible bug fixes.

    Additional labels for pre-release and build metadata are available as
    extensions to the MAJOR.MINOR.PATCH format.

The primary version number is stored in *setup.py* but is used in other
places, such as build system control files.

Style
=====

At a minimum, all code should be compliant with :pep:`8`. The
:program:`flake8` tool provides additional code style hints.

Tests
=====

A basic test should always be included. Tests are not expected to be
comprehensive, but should evolve as bugs are detected. High code coverage
is encouraged.
