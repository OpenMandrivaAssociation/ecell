%define major		2
%define libname		%mklibname %{name} %{major}
%define devname		%mklibname -d %{name}

# disable doc build for now as it brokes the build
# (11/2010 wally)
%define build_doc	0

Summary:	A software suite for modeling, simulation, and analysis of biological cells
Name:		ecell
Version:	3.2.1
Release:	4
License:	GPLv2+ and LGPLv2+
Group:		Sciences/Biology
Url:		http://ecell.sourceforge.net/
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-icons.tar.bz2

Buildrequires:	gnome-python-canvas
BuildRequires:	boost-devel
BuildRequires:	gsl-devel
BuildRequires:	python-ply
BuildRequires:	python-devel
BuildRequires:	python-numpy-devel
BuildRequires:	pygtk2.0-libglade
BuildRequires:	libltdl-devel

%if %{build_doc}
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	docbook-utils
BuildRequires:	docbook-dtd42-xml
%endif

Requires:	gnome-python
Requires:	gnome-python-canvas
Requires:	gnome-python-gnomevfs
Requires:	pygtk2.0-libglade
Requires:	python-numpy
Requires:	%{libname} = %{version}-%{release}
# require devel package as it's possibly needed on run-time for the examples (samples),
# see note on description
Requires:	%{devname} = %{version}-%{release}

%description
E-Cell Project is an international research project aiming to model and
reconstruct biological phenomena in silico, and developing necessary
theoretical supports, technologies and software platforms to allow precise
whole cell simulation.

E-Cell System is an object-oriented software suite for modeling, simulation,
and analysis of large scale complex systems such as biological cells. The
first version of E-Cell Simulation Environment (E-Cell SE) was released
in 1999, after which the development of its Windows version, E-Cell
version 2, had started and recently released. Software development has
since shifted to developing version 3, restructuring the system with
an aim to provide the cell simulation community a common, highly
flexible and high performance software environment.

Note that development libraries and headers are also required by this
package because they may be required to create new biological processes
or to run the included examples.

%package -n %{libname}
Summary:	Libraries from Ecell3
Group:		System/Libraries
Obsoletes:	libecell3_2 <= 1.0.103

%description -n %{libname}
This package provides the libraries for %{name}.

%package -n %{devname}
Summary:	Developer package for E-Cell System
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Requires:	python-numpy-devel

%description -n %{devname}
This package provides the development files for %{name}.

%if %build_doc
%package doc
Summary:	Ecell3 extras documentations
Group:		Sciences/Biology
BuildArch:	noarch

%description doc
E-Cell Project is an international research project aiming to model and
reconstruct biological phenomena in silico, and developing necessary
theoretical supports, technologies and software platforms to allow precise
whole cell simulation.

This package contains extra documentation.
%endif

%package session-monitor
Summary:	E-Cell Session Monitor
Group:		Sciences/Biology
Requires:	ecell = %{version}-%{release}
Requires:	pygtk2.0
Requires:	pygtk2.0-libglade

%description session-monitor
E-Cell System is an object-oriented software suite for modeling,
simulation, and analysis of large scale complex systems, particularly focused
on biological details of cellular behavior.

%package model-editor
Summary:	E-Cell Model Editor
Group:		Sciences/Biology
Requires:	ecell = %{version}-%{release}
Requires:	ecell-session-monitor = %{version}-%{release}
Requires:	pygtk2.0
Requires:	pygtk2.0-libglade
Requires:	gnome-python-canvas

%description model-editor
E-Cell System is an object-oriented software suite for modeling,
simulation, and analysis of large scale complex systems, particularly focused
on biological details of cellular behavior.

%prep
%setup -q
%setup -q -T -D -a1 #icons

%build
%configure2_5x --disable-static

#fix build
sed -i -e 's|CXXFLAGS = .*|CXXFLAGS = |g' ecell/dm/Makefile

%make

%install
%makeinstall_std

%multiarch_includes %{buildroot}%{_includedir}/ecell-3.2/ecell_config.h

# desktop files
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-session-monitor.desktop << EOF
[Desktop Entry]
Name=E-Cell Session Monitor
Comment=A software suite for modeling, simulation, and analysis of biological cells
Exec=ecell3-session-monitor
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;Education;Science;Biology;
EOF

cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}-model-editor.desktop << EOF
[Desktop Entry]
Name=E-Cell Model Editor
Comment=A software suite for modeling, simulation, and analysis of biological cells
Exec=ecell3-model-editor
Icon=%{name}
Terminal=false
Type=Application
Categories=GTK;Education;Science;Biology;
EOF

# icons
install -D -m 644 %{name}48.png %{buildroot}/%{_liconsdir}/%{name}.png
install -D -m 644 %{name}32.png %{buildroot}/%{_iconsdir}/%{name}.png
install -D -m 644 %{name}16.png %{buildroot}/%{_miconsdir}/%{name}.png

#fix shebang
sed -i -e 's|/usr/local/bin|%{_bindir}|g' %{buildroot}%{python_sitearch}/ecell/em.py

# let files section handle docs
rm -rf %{buildroot}%{_docdir}

# we don't want these
rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/%{name}-3.2/session-monitor/plugins/Makefile*
rm -rf %{buildroot}%{_libdir}/%{name}-3.2/model-editor/plugins/Makefile.am

#fix rights
chmod 644 %{buildroot}%{_libdir}/%{name}-3.2/session-monitor/plugins/*.xpm
chmod 644 %{buildroot}%{_libdir}/%{name}-3.2/model-editor/plugins/*.py

%if %{build_doc}
#move to a better location
cp -R ecell/model-editor/doc doc/model-editor
%endif

%files
%doc COPYING AUTHORS NEWS README doc/samples
%dir %{_sysconfdir}/ecell-3.2/
%{_bindir}/ecell3-em2eml
%{_bindir}/ecell3-eml2em
%{_bindir}/ecell3-eml2sbml
%{_bindir}/ecell3-python
%{_bindir}/ecell3-sbml2eml
%{_bindir}/ecell3-session
%{_bindir}/ecell3-session-manager
%{_datadir}/ecell-3.2
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

%files -n %{libname}
%doc COPYING AUTHORS NEWS README
%exclude %{_libdir}/ecell-3.2/model-editor
%exclude %{_libdir}/ecell-3.2/session-monitor
%exclude %{python_sitelib}/%{name}/ui
%{_libdir}/ecell-3.2
%{_libdir}/*.so.*
%{python_sitearch}/ecell
%{python_sitearch}/E_Cell-%{version}-py%{py_ver}.egg-info

%files -n %{devname}
%doc AUTHORS COPYING README
%{_bindir}/dmcompile
%{_bindir}/ecell3-dmc
%{_libdir}/*.so
%{_includedir}/dmtool
%{_includedir}/ecell-3.2
%{multiarch_includedir}/ecell-3.2

%files session-monitor
%doc AUTHORS COPYING README
%dir %{_sysconfdir}/ecell-3.2
%config(noreplace) %{_sysconfdir}/ecell-3.2/osogo.ini
%{_bindir}/ecell3-session-monitor
%{_libdir}/ecell-3.2/session-monitor
%dir %{python_sitelib}/%{name}/ui
%{python_sitelib}/%{name}/ui/*.py
%{python_sitelib}/%{name}/ui/osogo
%{python_sitelib}/%{name}.session_monitor-%{version}-py%{pyver}.egg-info
%{_datadir}/applications/mandriva-%{name}-session-monitor.desktop

%files model-editor
%doc AUTHORS COPYING README
%config(noreplace) %{_sysconfdir}/ecell-3.2/model-editor.ini
%{_bindir}/ecell3-model-editor
%{_libdir}/ecell-3.2/model-editor
%{python_sitelib}/%{name}/ui/model_editor
%{python_sitelib}/%{name}.model_editor-%{version}-py%{pyver}.egg-info
%{_datadir}/applications/mandriva-%{name}-model-editor.desktop

%if %{build_doc}
%files doc
%doc doc/refman doc/users-manual doc/model-editor doc/api
%endif

