%define	name	exmap-console
%define kernelname exmap
%define	version	0.4.1
%define	release	%mkrel 1

Summary:	Memory analysis tool
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
Source:		http://projects.o-hand.com/sources/exmap-console/%{name}-%{version}.tgz
Patch0:		exmap-console-0.4.1-no_module.patch
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
