%define name            ecell
%define version         3.2.1  

# when compiling SVN: complete this,
# use %{svn} on line 30, uncomment line 97
#define svn             2632
#define rel            5
#define release        %mkrel 1.%{svn}.%{rel}

# when compiling stable version
%define rel             1
%define release         %mkrel %{rel}

%define major		2
%define libname		%mklibname %{name} %{major}

# disable doc build for now as it brokes the build
# (11/2010 wally)
%define build_doc 	0

Summary:	A software suite for modeling, simulation, and analysis of biological cells
Name:		%{name}
Version:	%{version}
Release:	%{release}
# Source0: if stable use %{name}-%{version}.tar.bz2
# if SVN use %{name}-%{version}-%{svn}.tar.bz2
Source0:	%{name}-%{version}.tar.bz2
Source1:	%{name}-icons.tar.bz2
License:	GPLv2+ and LGPLv2+
Group:		Sciences/Biology
Url:		http://ecell.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-buildroot
Obsoletes:	ecell3 <= 1.0.103
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

%package -n %{libname}
Summary:	Libraries from Ecell3
Group:		System/Libraries
Provides:	%{libname} = %{version}-%{release}
Obsoletes:	libecell3_2 <= 1.0.103

%description -n %{libname}
This package provides the libraries and includes files from Ecell3.
Note that development libraries and headers are also included in this
package because they may be required to create new biological processes
or to run the included examples.
 
# Note : do not create a libecell3-devel package
# (see Note in %{libname} description)

%if %build_doc
%package doc
Summary:	Ecell3 extras documentations
Group:		Sciences/Biology

%description doc
E-Cell Project is an international research project aiming to model and
reconstruct biological phenomena in silico, and developing necessary
theoretical supports, technologies and software platforms to allow precise
whole cell simulation.

This package contains extra documentation.
%endif

%prep
%setup -q
%setup -q -T -D -a1 #icons

%build
%configure2_5x --disable-static

#fix build
sed -i -e 's|CXXFLAGS = .*|CXXFLAGS = |g' ecell/dm/Makefile

%make

%install
rm -rf %{buildroot}
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
sed -i -e 's|/usr/local/bin|%{_bindir}|g' %{buildroot}%{python_sitelib}/ecell/em.py

# let files section handle docs
rm -rf %{buildroot}%{_docdir}

# we don't want these
rm -rf %{buildroot}%{_libdir}/*.la

%if %{build_doc}
#move to a better location
cp -R ecell/model-editor/doc doc/model-editor
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING AUTHORS NEWS README doc/samples
%dir %{_sysconfdir}/ecell-3.2/
%config(noreplace) %{_sysconfdir}/ecell-3.2/*.ini
%{_bindir}/ecell3-*
%{_bindir}/dmcompile
%{_datadir}/ecell-3.2
%{_datadir}/applications/*.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING AUTHORS NEWS README
%{_libdir}/ecell-3.2
%{_libdir}/*.so.*
%{python_sitearch}/ecell
%{python_sitearch}/*.egg-info

# Note: leave dev libraries and includes files in %{libname}
# (see %{libname} description), they are needed for the examples (samples)
%{_libdir}/*.so
%{_includedir}/dmtool
%{_includedir}/ecell-3.2
%{multiarch_includedir}/ecell-3.2

%if %{build_doc}
%files doc
%defattr(-,root,root)
%doc doc/refman doc/users-manual doc/model-editor doc/api
%endif
