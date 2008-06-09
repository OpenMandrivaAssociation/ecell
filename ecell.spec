%define name 		ecell
%define version	 	3.1.105

# when compiling SVN: complete this,
# use %{svn} on line 30, uncomment line 97
%define svn             2632
%define rel		3
%define release 	%mkrel 1.%{svn}.%{rel}

# when compiling stable version
#define rel             1
#define release         %mkrel %{rel}

%define major		2
%define libname		%mklibname %{name}%{major}

%define build_doc 	1

# Macros for in the menu-file.
%define section Applications/Sciences/Biology
%define title   E-cell
%define summary	A software suite for modeling, simulation, and analysis of biological cells

Summary:	%{summary}
Name:		%{name}
Version:	%{version}
Release:	%{release}
# Source0: if stable use %{name}-%{version}.tar.bz2
# if SVN use %{name}-%{version}-%{svn}.tar.bz2
Source0:	%{name}-%{version}-%{svn}.tar.bz2
Source1:	%{name}-icons.tar.bz2
License:	GPL
Group:		Sciences/Biology
Url:		http://ecell.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-buildroot
Prefix:		%{_prefix}
Obsoletes:	ecell3 <= 1.0.103
Buildrequires:	python-numpy gnome-python-canvas boost-devel gsl-devel
Requires:	gnome-python gnome-python-canvas gnome-python-gnomevfs pygtk2.0-libglade python-numpy libsbml
Requires:	%{libname} = %{version}-%{release}
# We do not need anymore xorg-x11-Xvfb to be able to import gnome.canvas python module during compilation
BuildRequires:	python-devel python-numpy-devel pygtk2.0-libglade
BuildRequires:  libltdl-devel
BuildRequires:  doxygen
BuildRequires:  docbook-dtd42-xml

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
Obsoletes:	libecell3_%{major} <= 1.0.103
Requires:	libsbml

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
BuildRequires:  tetex-latex graphviz docbook-utils-pdf

%description doc
E-Cell Project is an international research project aiming to model and
reconstruct biological phenomena in silico, and developing necessary
theoretical supports, technologies and software platforms to allow precise
whole cell simulation.

This package contains extra documentation.
%endif

%prep

%setup -q -n %{name}
%setup -q -n %{name} -T -D -a1 #icons

%build

# SVN version
./autogen.sh
#############

## needed for import gnome.canvas python module
#XDISPLAY=$(i=2; while [ -f /tmp/.X$i-lock ]; do i=$(($i+1)); done; echo $i)
#{_prefix}/X11R6/bin/Xvfb :$XDISPLAY &
#export DISPLAY=:$XDISPLAY
## without it, it will not work ( EE was randomly chosen )
#xauth add $DISPLAY . EE

%configure
%make

# no need, it is not created
# kill $(cat /tmp/.X$XDISPLAY-lock)

# build documentation
%if %build_doc
%make doc
%endif

%install

rm -rf %{buildroot}

%makeinstall
%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/ecell-3.1/ecell_config.h

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}-session-monitor.desktop << EOF
[Desktop Entry]
Name=E-Cell Session Monitor
Comment=A software suite for modeling, simulation, and analysis of biological cells
Exec=%{_bindir}/ecell3-session-monitor
Icon=%{name}
Terminal=false 
Type=Application
Categories=Gtk;Science;Biology;
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}-model-editor.desktop << EOF
[Desktop Entry]
Name=E-Cell Model Editor
Comment=A software suite for modeling, simulation, and analysis of biological cells
Exec=%{_bindir}/ecell3-model-editor
Icon=%{name}
Terminal=false
Type=Application
Categories=Gtk;Science;Biology;
EOF

# icons
%__install -D -m 644 %{name}48.png %{buildroot}/%{_liconsdir}/%{name}.png
%__install -D -m 644 %{name}32.png %{buildroot}/%{_iconsdir}/%{name}.png
%__install -D -m 644 %{name}16.png %{buildroot}/%{_miconsdir}/%{name}.png

rm -fr %buildroot%_datadir/doc/%{name}-%{version}
cp -R ecell/model-editor/doc doc/model-editor

%clean
%__rm -rf %{buildroot}

%post
%{update_menus}

%postun
%{clean_menus}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif


%files -n %{name}
%defattr(0755,root,root,0755)
%{_bindir}/*
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README
#samples (E-Cell examples)
%doc doc/sample/ 
%{_datadir}/ecell-3.1
%{_datadir}/applications/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

%files -n %{libname}
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL NEWS README
%{_libdir}/ecell-3.1
%{_libdir}/*.so.*
%{_libdir}/python%pyver/site-packages/ecell
# Note: leave dev libraries and includes files in %{libname}
# (see %{libname} description), they are needed for the examples (samples)
%{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*

%if %build_doc
%files doc
%defattr(-,root,root)
%doc doc/refman/ doc/users-manual/
%doc doc/model-editor
%doc AUTHORS COPYING INSTALL NEWS README
%endif
