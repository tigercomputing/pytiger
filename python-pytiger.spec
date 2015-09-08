Name:		python-pytiger
Summary:	Tiger Computing's Python library
Version:	1.0.0
# Un-comment for release builds:
#Release:	1%{?dist}
# Pre-release alpha/snapshot as per
# https://fedoraproject.org/wiki/Packaging:NamingGuidelines#Pre-Release_packages
Release:	0.1.a%{?dist}

Group:		Development/Languages
License:	BSD-3-clause
URL:		https://git.tiger-computing.co.uk/gitweb/pytiger.git
Source0:	pytiger-%{version}.tar.gz

BuildArch:		noarch
BuildRequires:	python2-devel
BuildRequires:	python-mock
BuildRequires:	python-setuptools
BuildRequires:	python-six
%if 0%{?rhel} && 0%{?rhel} < 7
BuildRequires:	python-unittest2
%else
BuildRequires:	python-coverage
BuildRequires:	python-nose
%endif

%description
This is the Tiger Computing Ltd Python Utility library, pytiger.

%prep
%setup -q -n pytiger-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root %{buildroot} \
		--install-data=%{_datadir}

%check
%if 0%{?rhel} && 0%{?rhel} < 7
unit2 discover -s src -b
%else
%{__python} setup.py nosetests
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/pytiger*

%changelog
* Tue Sep 08 2015 Chris Boot <crb@tiger-computing.co.uk> - 1.0.0-0.1.a
- Initial RPM release
