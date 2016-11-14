*****************
Building Packages
*****************

PyTiger provides both Debian and RPM packaging configurations. In most cases
the standard build tools can be used to build packages.

Debian
======

Use standard build mechanisms such as ``dpkg-buildpackage``, ``debuild``,
``pbuilder`` or whatever works for you. The ``debian/`` directory is intended
to track the current release of Debian at the time of the release of PyTiger.
At the time of writing, this is Debian 8 (jessie).

For example:

.. code-block:: console

  $ debuild -us -uc
  [...]
  dpkg-genchanges: including full source code in upload
   dpkg-source --after-build pytiger
  dpkg-buildpackage: full upload; Debian-native package (full source is included)
  Now running lintian...
  Finished running lintian.

We strongly recommend using ``pbuilder`` or ``sbuild`` or similar mechanisms in
order that packages are built in a clean, reproducible environment so that no
unexpected dependencies are pulled in and to avoid having to install all build
dependencies on your build systems.

Red Hat & CentOS
================

Packages targetting the "native" python versions for Red Hat or CentOS can be
built using standard tools such as ``rpmbuild`` or `Mock
<https://github.com/rpm-software-management/mock/wiki>`_ with no specific
configuation. The supplied spec file will generate:

* on Red Hat / CentOS 6.x:

  * ``python2-pytiger`` for Python 2.6

* on Red Hat / CentOS 7.x:

  * ``python2-pytiger`` for Python 2.7
  * ``python34-pytiger`` for Python 3.4

For example:

.. code-block:: console

  $ rpmbuild -bs pytiger.spec
  Wrote: /path/to/rpmbuild/SRPMS/pytiger-1.1.0-1.el7.centos.src.rpm
  $ mock -r epel-7-x86_64 --rebuild /path/to/rpmbuild/SRPMS/pytiger-1.1.0-1.el7.centos.src.rpm
  [...]
  Finish: rpmbuild pytiger-1.1.0-1.el7.centos.src.rpm
  Finish: build phase for pytiger-1.1.0-1.el7.centos.src.rpm
  INFO: Done(/path/to/rpmbuild/SRPMS/pytiger-1.1.0-1.el7.centos.src.rpm) Config(epel-7-x86_64) 3 minutes 4 seconds
  INFO: Results and/or logs in: /var/lib/mock/epel-7-x86_64/result
  Finish: run

We strongly recommend using ``mock`` or similar mechanisms in order that
packages are built in a clean, reproducible environment so that no unexpected
dependencies are pulled in and to avoid having to install all build
dependencies on your build systems.

In addition, the same spec file can be used to build RPM packages for Python
versions packaged in `Software Collections
<https://www.softwarecollections.org>`_, but this requires specially prepared
chroots that have the SCL Python packages included in them. The `Red Hat Blog
<http://developers.redhat.com/blog/>`_ has `some instructions about this
<http://developers.redhat.com/blog/2015/01/07/using-mock-to-build-python27-software-collections-packages-for-rhel6/>`_
covering SCL Python 2.7 on CentOS 6. Once you have a specially prepared chroot
for the SCL Python version you require, just build the package in that chroot
using the usual mock commands.

The following configurations are supported:

* on Red Hat / CentOS 6.x:

  * SCL Python 2.7, creating ``python27-pytiger`` (``sclpy27``)
  * SCL Python 3.4, creating ``rh-python34-pytiger`` (``sclpy34``)

The mock configurations we use for these are:

For CentOS 6 with SCL Python 2.7 (``sclpy27``):

.. code-block:: diff

  --- epel-6-x86_64.cfg	2016-09-13 10:10:00.000000000 +0100
  +++ epel-6-sclpy27-x86_64.cfg	2016-10-11 16:03:41.470227420 +0100
  @@ -1,7 +1,7 @@
  -config_opts['root'] = 'epel-6-x86_64'
  +config_opts['root'] = 'epel-6-sclpy27-x86_64'
   config_opts['target_arch'] = 'x86_64'
   config_opts['legal_host_arches'] = ('x86_64',)
  -config_opts['chroot_setup_cmd'] = 'install @buildsys-build'
  +config_opts['chroot_setup_cmd'] = 'install @buildsys-build scl-utils-build python27-build'
   config_opts['dist'] = 'el6'  # only useful for --resultdir variable subst
   # beware RHEL use 6Server or 6Client
   config_opts['releasever'] = '6'
  @@ -61,4 +61,10 @@
   mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=epel-debug-6&arch=x86_64
   failovermethod=priority
   enabled=0
  +
  +[python27scl]
  +name=Python27 - epel-6-x86_64
  +baseurl=https://www.softwarecollections.org/repos/rhscl/python27/epel-6-x86_64
  +enabled=1
  +gpgcheck=0
   """

For CentOS 6 with SCL Python 3.4 (``sclpy34``):

.. code-block:: diff

  --- epel-6-x86_64.cfg	2016-09-13 10:10:00.000000000 +0100
  +++ epel-6-sclpy34-x86_64.cfg	2016-11-14 16:50:34.543356289 +0000
  @@ -1,7 +1,7 @@
  -config_opts['root'] = 'epel-6-x86_64'
  +config_opts['root'] = 'epel-6-sclpy34-x86_64'
   config_opts['target_arch'] = 'x86_64'
   config_opts['legal_host_arches'] = ('x86_64',)
  -config_opts['chroot_setup_cmd'] = 'install @buildsys-build'
  +config_opts['chroot_setup_cmd'] = 'install @buildsys-build scl-utils-build rh-python34-build'
   config_opts['dist'] = 'el6'  # only useful for --resultdir variable subst
   # beware RHEL use 6Server or 6Client
   config_opts['releasever'] = '6'
  @@ -61,4 +61,10 @@
   mirrorlist=http://mirrors.fedoraproject.org/mirrorlist?repo=epel-debug-6&arch=x86_64
   failovermethod=priority
   enabled=0
  +
  +[python34scl]
  +name=Python34 - epel-6-x86_64
  +baseurl=https://www.softwarecollections.org/repos/rhscl/rh-python34/epel-6-x86_64
  +enabled=1
  +gpgcheck=0
   """
