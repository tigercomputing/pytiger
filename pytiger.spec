%{?scl:%scl_package pytiger}
%{!?scl:%global pkg_name %{name}}

%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%if 0%{?scl:1}

%if "%{scl}" == "python27"
%global _want_python2 1
%endif

%if "%{scl}" == "rh-python34"
%global _want_python3 1
%endif

%if "%{scl}" == "rh-python35"
%global _want_python3 1
%endif

%if 0%{!?_want_python2:1} && 0%{!?_want_python3:1}
%{error: dont know SCL %{scl}}
%endif

%else
%global _want_python2 1
%if 0%{?rhel} && 0%{?rhel} >= 7
%global _want_python3 1
%endif
%endif

%global _pkg_name pytiger
%global sum Tiger Computing Ltd Python Utilities

Name: %{?scl_prefix}%{_pkg_name}
Summary: %{sum}
Version: 1.1.0
Release: 2%{?dist}

Group: Development/Libraries
License: BSD-3-clause
Source0: %{pkg_name}-%{version}.tar.gz
Url: https://github.com/tigercomputing/%{_pkg_name}

BuildArch: noarch
BuildRequires: epel-rpm-macros

# Common requirements for all python2 packages
%if 0%{?_want_python2:1}
BuildRequires: %{?scl_prefix}python2-devel
BuildRequires: %{?scl_prefix}python-setuptools
%endif

# Common requirements for all python3 packages
%if 0%{?_want_python3:1}
BuildRequires: python3-rpm-macros
%endif

# Requirements for SCL packages only
%if 0%{?scl:1}
BuildRequires: %{?scl_prefix}python-devel
Requires: %{?scl_prefix}python-six
%endif

# Requirements for RHEL7 non-SCL only
%if 0%{?rhel} && 0%{?rhel} >= 7 && 0%{!?scl:1}
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: python%{python3_pkgversion}-setuptools
%endif

%description
This is the Tiger Computing Ltd Python Utility library, pytiger.

%if 0%{?rhel} && 0%{!?scl:1}
%package -n python2-%{_pkg_name}
Summary: %{sum}
%{?python_provide:%python_provide python2-%{_pkg_name}}
Requires: python-six

%description -n python2-%{_pkg_name}
This is the Tiger Computing Ltd Python Utility library, pytiger.

%if 0%{?rhel} >= 7
%package -n python%{python3_pkgversion}-%{_pkg_name}
Summary: %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{_pkg_name}}
Requires: python%{python3_pkgversion}-six

%description -n python%{python3_pkgversion}-%{_pkg_name}
This is the Tiger Computing Ltd Python Utility library, pytiger.
%endif

%endif

#%check
#%{?scl:scl enable %{scl} - << \EOF}
#%{__python2} setup.py nosetests
#%{?scl:EOF}

%prep
%setup -n %{pkg_name}-%{version} -q

%build
%if 0%{?rhel} && 0%{?scl:1}
%{?scl:scl enable %{scl} - << \EOF}
%{?_want_python2:%{__python2} setup.py build ;}
%{?_want_python3:%{__python3} setup.py build ;}
%{?scl:EOF}
%else
%{?_want_python2:%py2_build}
%{?_want_python3:%py3_build}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if 0%{?rhel} && 0%{?scl:1}
%{?scl:scl enable %{scl} - << \EOF}
%{?_want_python2:%{__python2} setup.py install -O1 --root=$RPM_BUILD_ROOT}
%{?_want_python3:%{__python3} setup.py install -O1 --root=$RPM_BUILD_ROOT}
%{?scl:EOF}
%else
%{?_want_python2:%py2_install}
%{?_want_python3:%py3_install}
%endif

%if 0%{?rhel} && 0%{?scl:1}

%files
%{?_want_python2:%{python2_sitelib}/*}
%{?_want_python3:%{python3_sitelib}/*}

%else

%files -n python2-%{_pkg_name}
%{python2_sitelib}/*

%if 0%{?rhel} >= 7
%files -n python%{python3_pkgversion}-%{_pkg_name}
%{python3_sitelib}/*
%endif

%endif

%changelog
* Fri Feb 16 2018 Jonathan Wiltshire <jmw@tiger-computing.co.uk> - 1.1.1-1
- Replace nagios.NagiosCheck.warn() with warning().

* Thu Nov 30 2017 Chris Boot <crb@tiger-computing.co.uk> - 1.1.0-2
- Add support for rh-python35 SCL. Make SCL selection a bit more generic.

* Tue Nov 01 2016 Chris Boot <crb@tiger-computing.co.uk> - 1.1.0-1
- First real RPM release for CentOS 6 and 7, plus 6+sclpy27 and 6+sclpy34.

* Tue Sep 08 2015 Chris Boot <crb@tiger-computing.co.uk> - 1.0.0-0.1.a
- Initial RPM release
