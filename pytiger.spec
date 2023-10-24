%if 0%{?scl:1}
%scl_package pytiger
%global py_prefix %{scl_prefix}python
%else
%global pkg_name pytiger
%global py_prefix python%{python3_pkgversion}
%endif

%if 0%{?rhel} == 7 && 0%{!?scl:1}
# This flag denotes we want to build python2 and python3 RPMs in one go, which
# only applies on CentOS 7 for Python 2.7 and 3.6, and only if we are NOT
# building for an SCL Python package.
%global _want_python2 1
%endif

%global sum Tiger Computing Ltd Python Utilities

Name: %{?scl_prefix}%{pkg_name}
Summary: %{sum}
Version: 1.2.2
Release: 1%{?dist}

Group: Development/Libraries
License: BSD-3-clause
Source0: %{pkg_name}-%{version}.tar.gz
Url: https://github.com/tigercomputing/%{pkg_name}

BuildArch: noarch
BuildRequires: epel-rpm-macros
%{?scl:BuildRequires: %{scl_prefix}build}
BuildRequires: %{py_prefix}-devel
BuildRequires: %{py_prefix}-setuptools

# Requirements for RHEL7 py2 only
%if 0%{?_want_python2:1}
BuildRequires: python-devel
BuildRequires: python-setuptools
%endif

%description
This is the Tiger Computing Ltd Python Utility library, pytiger.

%package -n %{py_prefix}-%{pkg_name}
Summary: %{sum}
Requires: %{py_prefix}-six

%description -n %{py_prefix}-%{pkg_name}
This is the Tiger Computing Ltd Python Utility library, pytiger.

# For dual pythons, add in the extra binary package
%if 0%{?_want_python2:1}
%package -n python2-%{pkg_name}
Summary: %{sum}
Requires: python-six

%description -n python2-%{pkg_name}
This is the Tiger Computing Ltd Python Utility library, pytiger.
%endif

%prep
%setup -n %{pkg_name}-%{version} -q

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python3} setup.py build
%{?scl:EOF}
%{?_want_python2:%{__python} setup.py build}

%install
rm -rf $RPM_BUILD_ROOT
%{?scl:scl enable %{scl} - << \EOF}
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
%{?scl:EOF}
%{?_want_python2:%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT}

%files -n %{py_prefix}-%{pkg_name}
%{python3_sitelib}/*

%if 0%{?_want_python2:1}
%files -n python2-%{pkg_name}
%{python_sitelib}/*
%endif

%changelog
* Tue Oct 24 2023 Chris Boot <crb@tiger-computing.co.uk> - 1.2.2-1
- Add GitLab CI test runs and RPM building.
- Overhaul the RPM spec file completely.
- Refactor pytiger.utils.plugins for Python 3.12.

* Wed Jan 13 2021 Jonathan Wiltshire <jmw@tiger-computing.co.uk> - 1.2.1-4
- Build for Python 3 by default, and Python 2 as an option.

* Fri Apr 05 2019 Chris Boot <crb@tiger-computing.co.uk> - 1.2.1-3
- Rename python-pytiger back to python2-pytiger for native Python 2.x builds.

* Thu Apr 04 2019 Chris Boot <crb@tiger-computing.co.uk> - 1.2.1-2
- Overhaul the RPM spec file completely.

* Mon Jul 30 2018 Chris Boot <crb@tiger-computing.co.uk> - 1.2.1-1
- Correct code examples and formatting in pytiger.logging.

* Tue Mar 06 2018 Jonathan Wiltshire <jmw@tiger-computing.co.uk> - 1.2.0-1
- Add a `separator` parameter to :func:`pytiger.monitoring.MonitoringCheck.exit`
- New module: :mod:`pytiger.logging.syslog`
- Set minimum Python interpreter version to 2.6
- New module: :mod:`pytiger.logging.config`
- New module: :mod:`pytiger.monitoring` (replacing :mod:`pytiger.nagios`)

* Fri Feb 16 2018 Jonathan Wiltshire <jmw@tiger-computing.co.uk> - 1.1.1-1
- Replace nagios.NagiosCheck.warn() with warning().

* Thu Nov 30 2017 Chris Boot <crb@tiger-computing.co.uk> - 1.1.0-2
- Add support for rh-python35 SCL. Make SCL selection a bit more generic.

* Tue Nov 01 2016 Chris Boot <crb@tiger-computing.co.uk> - 1.1.0-1
- First real RPM release for CentOS 6 and 7, plus 6+sclpy27 and 6+sclpy34.

* Tue Sep 08 2015 Chris Boot <crb@tiger-computing.co.uk> - 1.0.0-0.1.a
- Initial RPM release
