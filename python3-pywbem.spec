#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit/functional tests

Summary:	WBEM client and related utilities, written in pure Python
Summary(pl.UTF-8):	Klient WBEM i powiązane narzędzia, napisane w czystym Pythonie
Name:		python3-pywbem
Version:	1.7.3
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Python
#Source0Download: https://github.com/pywbem/pywbem/releases
Source0:	https://github.com/pywbem/pywbem/archive/%{version}/pywbem-%{version}.tar.gz
# Source0-md5:	a88e93a95ed363003b2f7f504c7662c7
Patch0:		pywbem-no-wheel.patch
URL:		https://github.com/pywbem/pywbem
BuildRequires:	python3-FormEncode >= 2.0.0
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML >= 5.1.1
BuildRequires:	python3-httpretty >= 0.9.5
BuildRequires:	python3-importlib_metadata >= 4.8.3
BuildRequires:	python3-lxml >= 4.6.2
BuildRequires:	python3-packaging >= 16.6
BuildRequires:	python3-ply >= 3.10
BuildRequires:	python3-pytest >= 4.4.0
BuildRequires:	python3-pytz >= 2019.1
BuildRequires:	python3-requests >= 2.25.0
BuildRequires:	python3-six >= 1.16.0
BuildRequires:	python3-testfixtures >= 6.9.0
BuildRequires:	python3-yamlloader >= 0.5.5
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.749
%if %{with doc}
BuildRequires:	python3-autodocsumm >= 0.2.12
BuildRequires:	python3-sphinx_git >= 10.1.1
BuildRequires:	python3-sphinxcontrib-fulltoc >= 1.2.0
BuildRequires:	sphinx-pdg-3 >= 4.5
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pywbem is a WBEM client and WBEM indication listener, written in pure
Python.

%description -l pl.UTF-8
Pywbem to klient WBEM oraz serwis identyfikacji WBEM, napisane w
czystym Pythonie.

%package apidocs
Summary:	API documentation for Python pywbem module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pywbem
Group:		Documentation

%description apidocs
API documentation for Python pywbem module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pywbem.

%prep
%setup -q -n pywbem-%{version}
%patch -P 0 -p1

%{__sed} -i -e 's/\.\. git_changelog::/(missing git changelog)/' docs/changes.rst

%build
%py3_build

%if %{with tests}
PATH=$(pwd):$PATH \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests/unittest tests/functiontest
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/mof_compiler{,-3}
%py3_comp $RPM_BUILD_ROOT%{py3_sitescriptdir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitescriptdir}

cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/python3-pywbem-%{version}
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' $RPM_BUILD_ROOT%{_examplesdir}/python3-pywbem-%{version}/*.py

%{__rm} $RPM_BUILD_ROOT%{_bindir}/*.bat

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md SECURITY.md TODO.md
%attr(755,root,root) %{_bindir}/mof_compiler-3
%{py3_sitescriptdir}/pywbem
%{py3_sitescriptdir}/pywbem_mock
%{py3_sitescriptdir}/pywbem-%{version}-py*.egg-info
%{_examplesdir}/python3-pywbem-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_modules,_static,client,*.html,*.js}
%endif
