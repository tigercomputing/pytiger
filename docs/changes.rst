******************
Changes in pytiger
******************

Release 2.0.1
=============

 * Fix Read the Docs documentation builds.
 * Add EL10 builds.

Release 2.0.0
=============

 * Drop Python 2 compatibility. The minimum supported Python version is now
   3.6.
 * Remove all CentOS 7 packages, including SCL.
 * Remove deprecated :mod:`pytiger.logging.legacy` module.
 * Remove deprecated :mod:`pytiger.nagios` module.
 * Remove deprecated :func:`pytiger.monitoring.MonitoringCheck.warn` method.
 * Fix :mod:`pytiger.logging.config` Python 3.13 compatibility.

Release 1.2.2
=============

 * Add GitLab CI test runs and RPM building.
 * Overhaul the RPM spec file completely.
 * Refactor :mod:`pytiger.utils.plugins` for Python 3.12.

Release 1.2.1
=============

* Correct code examples and formatting in :mod:`pytiger.logging`.
* Remove Debian packaging from the ``master`` branch in preparation for the
  conversion of the Debian package from a native package.

Release 1.2.0
=============

* Add a `separator` parameter to :func:`pytiger.monitoring.MonitoringCheck.exit`
* New module: :mod:`pytiger.logging.syslog`
* Set minimum Python interpreter version to 2.6
* New module: :mod:`pytiger.logging.config`
* New module: :mod:`pytiger.monitoring` (replacing :mod:`pytiger.nagios`)

Release 1.1.1
=============

* Deprecate nagios.NagiosClient.warn(), replace with warning() (#2)

Release 1.1.0
==============

* Python 3 compatibility
* New module: :mod:`pytiger.utils.plugins`
* New decorator: :class:`pytiger.utils.decorators.singleton`

Release 1.0.0
=============

* Initial release.
