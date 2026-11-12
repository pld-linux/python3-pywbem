#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit/functional tests

Summary:	WBEM client and related utilities, written in pure Python
Summary(pl.UTF-8):	Klient WBEM i powiązane narzędzia, napisane w czystym Pythonie
Name:		python3-pywbem
Version:	1.9.1
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pywbem/
# git archive doesn't contain proper version information, use sdist to build
Source0:	https://files.pythonhosted.org/packages/source/p/pywbem/pywbem-%{version}.tar.gz
# Source0-md5:	377c39ee4c84065122a8e8d80f365e26
# ...but sdist is missing docs dir, use git archive for them
Source1:	https://github.com/pywbem/pywbem/archive/%{version}/pywbem-archive-%{version}.tar.gz
# Source1-md5:	1a53e61443db494d2bc014ad2c46fa8b
URL:		https://github.com/pywbem/pywbem
BuildRequires:	python3-build >= 1.1.1
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.9
BuildRequires:	python3-setuptools >= 1:82.0.0
BuildRequires:	python3-setuptools_scm >= 9.2.0
BuildRequires:	python3-wheel >= 0.46.2
%if %{with tests}
BuildRequires:	python3-FormEncode >= 2.1.1
BuildRequires:	python3-PyYAML >= 6.0.2
BuildRequires:	python3-certifi >= 2024.07.04
BuildRequires:	python3-colorama >= 0.4.5
BuildRequires:	python3-cryptography >= 48.0.1
BuildRequires:	python3-decorator >= 4.0.11
BuildRequires:	python3-easy-server >= 0.8.0
BuildRequires:	python3-easy-vault >= 0.7.0
BuildRequires:	python3-idna >= 3.15
BuildRequires:	python3-importlib_metadata >= 4.8.3
BuildRequires:	python3-jsonschema >= 4.18.0
BuildRequires:	python3-keyring >= 18.0.0
BuildRequires:	python3-lxml >= 6.1.0
BuildRequires:	python3-packaging >= 24.2
BuildRequires:	python3-pluggy >= 1.5.0
BuildRequires:	python3-ply >= 3.10
BuildRequires:	python3-pytest >= 9.0.3
BuildRequires:	python3-pytest-easy-server >= 0.8.0
BuildRequires:	python3-requests >= 2.33.0
BuildRequires:	python3-requests-mock >= 1.6.0
BuildRequires:	python3-requests-toolbelt >= 0.8.0
BuildRequires:	python3-testfixtures >= 6.9.0
BuildRequires:	python3-typing_extensions >= 4.14.1
BuildRequires:	python3-urllib3 >= 2.7.0
BuildRequires:	python3-yagot >= 0.5.0
BuildRequires:	python3-yamlloader >= 0.5.5
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-autodocsumm >= 0.2.12
BuildRequires:	python3-docutils >= 0.18.1
BuildRequires:	python3-sphinx_git >= 10.1.1
BuildRequires:	python3-sphinx_rtd_theme >= 2.0.0
BuildRequires:	python3-sphinxcontrib-fulltoc >= 1.2.0
BuildRequires:	sphinx-pdg-3 >= 7.2.4
%endif
Requires:	python3-modules >= 1:3.9
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
%setup -q -n pywbem-%{version} -a1

%{__mv} pywbem-%{version}/{docs,examples,SECURITY.md,TODO.md} .
%{__rm} -r pywbem-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PATH=$(pwd):$PATH \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m pytest tests/unittest tests/functiontest
%endif

%if %{with doc}
# setuptools_scm cannot detect version without git checkout when in subdir, so give a hint
PYTHONPATH=$(pwd) \
SETUPTOOLS_SCM_PRETEND_VERSION="%{version}" \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/mof_compiler{,-3}

cp -pr examples $RPM_BUILD_ROOT%{_examplesdir}/python3-pywbem-%{version}
%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' $RPM_BUILD_ROOT%{_examplesdir}/python3-pywbem-%{version}/*.py

%{__rm} $RPM_BUILD_ROOT%{_bindir}/*.bat

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.md README.md SECURITY.md TODO.md
%attr(755,root,root) %{_bindir}/mof_compiler-3
%{py3_sitescriptdir}/pywbem
%{py3_sitescriptdir}/pywbem_mock
%{py3_sitescriptdir}/pywbem-%{version}.dist-info
%{_examplesdir}/python3-pywbem-%{version}

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,client,*.html,*.js}
%endif
