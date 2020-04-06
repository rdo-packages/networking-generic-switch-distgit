# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif

%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global srcname networking_generic_switch
%global pkgname networking-generic-switch
%global with_doc 1
%global common_summary Pluggable Modular Layer 2 Neutron Mechanism driver


Name:           python-%{pkgname}
Version:        XXX
Release:        XXX
Summary:        %{common_summary}

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{upstream_version}.tar.gz

BuildArch:      noarch
BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
# for unit tests
BuildRequires:  /usr/bin/stestr-%{pyver}
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-netmiko
BuildRequires:  python%{pyver}-neutron-lib
BuildRequires:  python%{pyver}-neutron-tests
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-six
BuildRequires:  python%{pyver}-stevedore
BuildRequires:  python%{pyver}-tenacity
BuildRequires:  python%{pyver}-tooz

%description
Pluggable Modular Layer 2 Neutron Mechanism driver implementing functionality
required for use-cases like OpenStack Ironic multi-tenancy mode.

%prep
%autosetup -n %{pkgname}-%{upstream_version} -S git
%py_req_cleanup

%build
%{pyver_build}
%if 0%{?with_doc}
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%check
PYTHON=%{pyver_bin} stestr-%{pyver} --test-path %{srcname}/tests/unit run

%install
%{pyver_install}


%package -n python%{pyver}-%{pkgname}
Summary:        %{common_summary}
%{?python_provide:%python_provide python%{pyver}-%{pkgname}}

Requires:       openstack-neutron-common >= 1:13.0.0
Requires:       python%{pyver}-netmiko >= 2.0.2
Requires:       python%{pyver}-neutron-lib >= 1.18.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-six >= 1.10.0
Requires:       python%{pyver}-stevedore >= 1.20.0
Requires:       python%{pyver}-tenacity >= 4.4.0
Requires:       python%{pyver}-tooz >= 1.58.0

%description -n python%{pyver}-%{pkgname}
Pluggable Modular Layer 2 Neutron Mechanism driver implementing functionality
required for use-cases like OpenStack Ironic multi-tenancy mode.

This package contains the plugin itself.


%package -n python%{pyver}-%{pkgname}-tests
Summary:        %{common_summary} - tests

Requires:       python%{pyver}-%{pkgname} = %{version}-%{release}
Requires:       python%{pyver}-mock >= 2.0.0
Requires:       python%{pyver}-neutron-tests
Requires:       python%{pyver}-fixtures >= 3.0.0

%description -n python%{pyver}-%{pkgname}-tests
Pluggable Modular Layer 2 Neutron Mechanism driver implementing functionality
required for use-cases like OpenStack Ironic multi-tenancy mode.

This package contains the unit tests.


%if 0%{?with_doc}
%package doc
Summary:        %{common_summary} - documentation

BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx

%description doc
Pluggable Modular Layer 2 Neutron Mechanism driver implementing functionality
required for use-cases like OpenStack Ironic multi-tenancy mode.

This package contains the documentation.
%endif


%files -n python%{pyver}-%{pkgname}
%license LICENSE
%{pyver_sitelib}/%{srcname}
%{pyver_sitelib}/%{srcname}*.egg-info
%exclude %{pyver_sitelib}/%{srcname}/tests

%files -n python%{pyver}-%{pkgname}-tests
%license LICENSE
%{pyver_sitelib}/%{srcname}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif


%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/networking-generic-switch/commit/?id=c2bb1b85a7d2d57c7f5f16f57432da9b48cf7164
