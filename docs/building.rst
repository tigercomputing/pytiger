*****************
Building Packages
*****************

PyTiger provides both Debian and RPM packaging configurations. In most cases
the standard build tools can be used to build packages.

Debian
======

Use standard build mechanisms such as ``dpkg-buildpackage``, ``debuild``,
``pbuilder`` or whatever works for you. The ``debian/`` directory is available
in branches prefixed ``debian/`` in Git.

We strongly recommend using ``pbuilder`` or ``sbuild`` or similar mechanisms in
order that packages are built in a clean, reproducible environment so that no
unexpected dependencies are pulled in and to avoid having to install all build
dependencies on your build systems.

Red Hat & CentOS
================

Packages targeting the "native" python versions for Red Hat or CentOS can be
built using standard tools such as ``rpmbuild`` or `Mock
<https://github.com/rpm-software-management/mock/wiki>`_ with no specific
configuration. The supplied spec file will generate the ``python3-pytiger``
RPM.

We strongly recommend using ``mock`` or similar mechanisms in order that
packages are built in a clean, reproducible environment so that no unexpected
dependencies are pulled in and to avoid having to install all build
dependencies on your build systems.
