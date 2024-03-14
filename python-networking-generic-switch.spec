%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global srcname networking_generic_switch
%global pkgname networking-generic-switch
%global with_doc 1
%global common_summary Pluggable Modular Layer 2 Neutron Mechanism driver


Name:           python-%{pkgname}
Version:        7.3.0
Release:        1%{?dist}
Summary:        %{common_summary}

License:        Apache-2.0
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
BuildRequires:  pyproject-rpm-macros
BuildRequires:  /usr/bin/stestr-3
BuildRequires:  python3-neutron-tests
%description
Pluggable Modular Layer 2 Neutron Mechanism driver implementing functionality
required for use-cases like OpenStack Ironic multi-tenancy mode.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pkgname}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel
%if 0%{?with_doc}
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%check
%tox -e %{default_toxenv}

%install
%pyproject_install


%package -n python3-%{pkgname}
Summary:        %{common_summary}

Requires:       openstack-neutron-common >= 1:13.0.0
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

%description doc
Pluggable Modular Layer 2 Neutron Mechanism driver implementing functionality
required for use-cases like OpenStack Ironic multi-tenancy mode.

This package contains the documentation.
%endif


%files -n python3-%{pkgname}
%license LICENSE
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}*.dist-info
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
* Thu Mar 14 2024 RDO <dev@lists.rdoproject.org> 7.3.0-1
- Update to 7.3.0

