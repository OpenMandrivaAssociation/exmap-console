%define	name	exmap-console
%define kernelname exmap
%define	version	0.4.1
%define release	9

Summary:	Memory analysis tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source:		http://projects.o-hand.com/sources/exmap-console/%{name}-%{version}.tgz
Patch0:		exmap-console-0.4.1-no_module.patch
Patch1:		exmap-console-2.6.26.patch
URL:		http://projects.o-hand.com/exmap-console
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires(post):	dkms
Requires(preun):	dkms
BuildRequires:	readline-devel termcap-devel help2man glib2-devel

%description
Exmap-console is a suite of command line applications developed around the
Exmap memory analysis tool. It is intended for use in situations where running
the Exmap GUI application is not feasible, for example, on embedded devices,
or when memory data needs to be saved for later examination.

The suite contains three applications: exmap client (exmap), exmap daemon
(exampd) and exmap remote server (exmapserver).

%prep
%setup -q 
%patch0 -p1
%patch1 -p2
sed -i 's/-lreadline/-ltermcap -lreadline/' configure.ac

%build
aclocal
autoconf
automake
%configure2_5x --disable-kernel-module
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# DKMS 
######

install -d -m 755 %{buildroot}%{_prefix}/src
cp -a kernel %{buildroot}%{_prefix}/src/%{kernelname}-%{version}

cat > %{buildroot}%{_prefix}/src/%{kernelname}-%{version}/dkms.conf <<EOF

PACKAGE_VERSION="%{version}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{kernelname}"
MAKE[0]="make -C \${kernel_source_dir} SUBDIRS=\${dkms_tree}/\${PACKAGE_NAME}/\${PACKAGE_VERSION}/build modules"
CLEAN="make clean"

BUILT_MODULE_NAME[0]="\$PACKAGE_NAME"
DEST_MODULE_LOCATION[0]="/kernel/3rdparty/\$PACKAGE_NAME/"

AUTOINSTALL=yes
REMAKE_INITRD=no

EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
dkms add -m %{kernelname} -v %{version} --rpm_safe_upgrade ||:
dkms build -m %{kernelname} -v %{version} --rpm_safe_upgrade ||:
dkms install -m %{kernelname} -v %{version} --rpm_safe_upgrade

%preun
dkms remove -m %{kernelname} -v %{version} --rpm_safe_upgrade --all ||:

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL README 
%{_bindir}/*
%{_prefix}/src/%{kernelname}-%{version}


%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.4.1-8mdv2011.0
+ Revision: 618248
- the mass rebuild of 2010.0 packages

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.4.1-7mdv2010.0
+ Revision: 437506
- rebuild

* Sat Mar 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.4.1-6mdv2009.1
+ Revision: 354896
- rebuild for latest readline

* Fri Sep 12 2008 Pascal Terjan <pterjan@mandriva.org> 0.4.1-5mdv2009.0
+ Revision: 284120
- Bump the release and pray
- Add upstream patch to build on new kernel

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.4.1-3mdv2009.0
+ Revision: 245000
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.4.1-1mdv2008.1
+ Revision: 136407
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Pascal Terjan <pterjan@mandriva.org>
    - Fix typo in summary

* Thu Jul 19 2007 Pascal Terjan <pterjan@mandriva.org> 0.4.1-1mdv2008.0
+ Revision: 53610
- BuildRequires glib2-devel
- Import exmap-console

