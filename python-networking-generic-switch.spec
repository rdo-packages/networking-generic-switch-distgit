%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

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
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pkgname}/%{pkgname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
# for unit tests
BuildRequires:  /usr/bin/stestr-3
BuildRequires:  python3-mock
BuildRequires:  python3-fixtures
BuildRequires:  python3-netmiko
BuildRequires:  python3-neutron-lib
BuildRequires:  python3-neutron-tests
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-oslo-log
BuildRequires:  python3-stevedore
BuildRequires:  python3-tenacity
BuildRequires:  python3-tooz

%description
Pluggable Modular Layer 2 Neutron Mechanism driver implementing functionality
required for use-cases like OpenStack Ironic multi-tenancy mode.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pkgname}-%{upstream_version} -S git
%py_req_cleanup

%build
%{py3_build}
%if 0%{?with_doc}
sphinx-build-3 -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%check
PYTHON=%{__python3} stestr-3 --test-path %{srcname}/tests/unit run

%install
%{py3_install}


%package -n python3-%{pkgname}
Summary:        %{common_summary}
%{?python_provide:%python_provide python3-%{pkgname}}

Requires:       openstack-neutron-common >= 1:13.0.0
Requires:       python3-netmiko >= 4.1.1
Requires:       python3-neutron-lib >= 1.18.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-utils >= 3.40.2
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-tenacity >= 6.0.0
Requires:       python3-tooz >= 2.5.1

%description -n python3-%{pkgname}
Pluggable Modular Layer 2 Neutron Mechanism driver implementing functionality
required for use-cases like OpenStack Ironic multi-tenancy mode.

This package contains the plugin itself.


%package -n python3-%{pkgname}-tests
Summary:        %{common_summary} - tests

Requires:       python3-%{pkgname} = %{version}-%{release}
Requires:       python3-mock >= 2.0.0
Requires:       python3-neutron-tests
Requires:       python3-fixtures >= 3.0.0

%description -n python3-%{pkgname}-tests
Pluggable Modular Layer 2 Neutron Mechanism driver implementing functionality
required for use-cases like OpenStack Ironic multi-tenancy mode.

This package contains the unit tests.


%if 0%{?with_doc}
%package doc
Summary:        %{common_summary} - documentation

BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinxcontrib-apidoc

%description doc
Pluggable Modular Layer 2 Neutron Mechanism driver implementing functionality
required for use-cases like OpenStack Ironic multi-tenancy mode.

This package contains the documentation.
%endif


%files -n python3-%{pkgname}
%license LICENSE
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}*.egg-info
%exclude %{python3_sitelib}/%{srcname}/tests

%files -n python3-%{pkgname}-tests
%license LICENSE
%{python3_sitelib}/%{srcname}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif


%changelog
