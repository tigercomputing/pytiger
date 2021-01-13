%{?scl:%scl_package pytiger}
%{!?scl:%global pkg_name %{name}}

%if 0%{?rhel} == 7 && 0%{!?scl:1}
# This flag denotes we want to build python2 and python3 RPMs in one go, which
# only applies on CentOS 7 for Python 2.7 and 3.4/3.6, and only if we are NOT
# building for an SCL Python package.
%global _want_dual_pythons 1
%endif

# The current convention for Python 2.x non-SCL packages is to prefix them
# python2-, so conditionally define a macro we can use to add this tag.
%if 0%{!?scl:1}
%global python2_pkgtag 2
%endif

%global sum Tiger Computing Ltd Python Utilities

Name: %{?scl_prefix}pytiger
Summary: %{sum}
Version: 1.2.1
Release: 4%{?dist}

Group: Development/Libraries
License: BSD-3-clause
Source0: %{pkg_name}-%{version}.tar.gz
Url: https://github.com/tigercomputing/%{pkg_name}

BuildArch: noarch
BuildRequires: epel-rpm-macros

BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools

# Requirements for RHEL7 py2 only
%if 0%{?_want_dual_pythons:1}
BuildRequires: %{?scl_prefix}python-devel
BuildRequires: %{?scl_prefix}python-setuptools
%endif

%description
This is the Tiger Computing Ltd Python Utility library, pytiger.

%package -n python%{python3_pkgversion}-%{pkg_name}
Summary: %{sum}
Requires: python%{python3_pkgversion}-six

%description -n python%{python3_pkgversion}-%{pkg_name}
This is the Tiger Computing Ltd Python Utility library, pytiger.

# For dual pythons, add in the extra binary package
%if 0%{?_want_dual_pythons:1}
%package -n %{?scl_prefix}python%{?python2_pkgtag}-%{pkg_name}
Summary: %{sum}
Requires: %{?scl_prefix}python-six
%if 0%{!?scl:1}
%{?python_provide:%python_provide python%{?python2_pkgtag}-%{pkg_name}}
%endif

%description -n %{?scl_prefix}python%{?python2_pkgtag}-%{pkg_name}
This is the Tiger Computing Ltd Python Utility library, pytiger.
%endif

%prep
%setup -n %{pkg_name}-%{version} -q

%build
%if 0%{?scl:1}
%{?scl:scl enable %{scl} "}
%{__python} setup.py build
%{?scl:"}
%else
%py3_build
%{?_want_dual_pythons:%py_build}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?scl:1}
%{?scl:scl enable %{scl} "}
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT \
  --install-data=%{_datadir}
%{?scl:"}
%else
%py3_install
%{?_want_dual_pythons:%py_install}
%endif

%files -n python%{python3_pkgversion}-%{pkg_name}
%{python3_sitelib}/*

%if 0%{?_want_dual_pythons:1}
%files -n %{?scl_prefix}python%{?python2_pkgtag}-%{pkg_name}
%{python_sitelib}/*
%endif

%changelog
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
