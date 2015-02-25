%define calamdate 20150225
%define partdate 20150112

%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Distribution-independent installer framework 
Name:		calamares
Version:	1.0.0
Release:	0.%{calamdate}.2
Group:		System/Configuration/Other
License:	GPLv3+
URL:		http://calamares.io/
# git archive --format=tar --prefix=calamares-0.17.0-20150112/ HEAD | xz -vf > calamares-0.17.0-20150112.tar.xz
Source0:	calamares-%{version}-%{calamdate}.tar.xz
# https://github.com/calamares/partitionmanager
Source1:	calamares-partitionmanager-%{partdate}.tar.xz
Source2:	calamares.rpmlintrc
Source3:	%{name}.service
Source4:	%{name}-install-start
Source5:	omv-bootloader.conf
Source6:	omv-displaymanager.conf
Source7:	omv-finished.conf
Source8:	omv-fstab.conf
Source10:	omv-grubcfg.conf
Source11:	omv-keyboard.conf
Source12:	omv-locale.conf
Source13:	omv-machineid.conf
Source14:	omv-mount.conf
Source15:	omv-packages.conf
Source16:	omv-prepare.conf
Source17:	omv-services.conf
Source18:	omv-settings.conf
Source19:	omv-unpackfs.conf
Source20:	omv-users.conf
Source21:	OpenMandriva-adverts.tar.xz
Patch1:		calamares-0.17.0-20150112-openmandriva-desktop-file.patch
Patch3:		calamares-1.0.0-20150225-upstream-removeUser.patch
Patch4:		calamares-1.0.0-20150203-upstream-displaymanager-explicitautologin.patch
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(libatasmart)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(libparted)
BuildRequires:	pkgconfig(polkit-qt5-1)
BuildRequires:	cmake >= 3.0
BuildRequires:	cmake(ECM)
BuildRequires:	qt5-qttools
BuildRequires:	qt5-linguist
BuildRequires:	cmake(KF5CoreAddons)
BuildRequires:	cmake(KF5Config)
BuildRequires:	cmake(KF5Solid)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	yaml-cpp-devel
BuildRequires:	pkgconfig(python3)
BuildRequires:	boost-devel >= 1.54.0
BuildRequires:	boost-python3-devel
Requires(post):	distro-release-OpenMandriva
Requires(post):	distro-theme-OpenMandriva
Requires:	coreutils
Requires:	util-linux
Requires:	dracut
Requires:	grub2
%ifarch x86_64
# EFI currently only supported on x86_64
Requires:       grub2-efi
%endif
Requires:	console-setup
# x11 stuff
Requires:	setxkbmap
Requires:	xkbcomp
Requires:	NetworkManager
Requires:	os-prober
Requires:	e2fsprogs
Requires:	dosfstools
Requires:	ntfs-3g
Requires:	gawk
#(tpg) needs to be ported to KF5
#Requires:	partitionmanager
Requires:	systemd
Requires:	systemd-units
Requires:	rsync
Requires:	shadow
Requires:	polkit
Requires:	urpmi
Requires:	squashfs-tools
ExclusiveArch:	%{ix86} x86_64

%description
Calamares is a distribution-independent installer framework,
designed to install from a live CD/DVD/USB environment to
a hard disk. It includes a graphical installation
program based on Qt 5.

%package -n %{libname}
Summary:	Calamares runtime libraries
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description -n %{libname}
Librarief for %{name}.


%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C 
Requires:	%{libname} = %{EVRD}
Requires:	cmake

%description -n %{develname}
Development files and headers for %{name}.

%prep
%setup -q -n %{name}-%{version}-%{calamdate} -a 1
rm -rf src/modules/partition/partitionmanager
mv -f calamares-partitionmanager-%{partdate} src/modules/partition/partitionmanager

%apply_patches

#delete backup files
rm -f src/modules/*/*.conf.default-settings

%build
# workaround for broken LLVM
export CC=gcc
export CXX=g++

%cmake_qt5 -DWITH_PARTITIONMANAGER:BOOL="ON" -DWITH_PYTHON:BOOL="ON" -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"

%make

%install
%makeinstall_std -C build

#own the local settings directories
mkdir -p %{buildroot}%{_sysconfdir}/calamares/modules
mkdir -p %{buildroot}%{_sysconfdir}/calamares/branding/auto
touch %{buildroot}%{_sysconfdir}/calamares/branding/auto/branding.desc

# (tpg) settings specific for OMV
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/calamares/modules/bootloader.conf
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/calamares/modules/displaymanager.conf
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/calamares/modules/finished.conf
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/calamares/modules/fstab.conf
install -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/calamares/modules/grubcfg.conf
install -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/calamares/modules/keyboard.conf
install -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/calamares/modules/locale.conf
install -m 644 %{SOURCE13} %{buildroot}%{_sysconfdir}/calamares/modules/machineid.conf
install -m 644 %{SOURCE14} %{buildroot}%{_sysconfdir}/calamares/modules/mount.conf
install -m 644 %{SOURCE15} %{buildroot}%{_sysconfdir}/calamares/modules/packages.conf
install -m 644 %{SOURCE16} %{buildroot}%{_sysconfdir}/calamares/modules/prepare.conf
install -m 644 %{SOURCE17} %{buildroot}%{_sysconfdir}/calamares/modules/services.conf
install -m 644 %{SOURCE18} %{buildroot}%{_sysconfdir}/calamares/settings.conf
install -m 644 %{SOURCE19} %{buildroot}%{_sysconfdir}/calamares/modules/unpackfs.conf
install -m 644 %{SOURCE20} %{buildroot}%{_sysconfdir}/calamares/modules/users.conf

# (tpg) service files
mkdir -p %{buildroot}{%{_unitdir},%{_sbindir}}
install -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -m 755 %{SOURCE4} %{buildroot}%{_sbindir}/%{name}-install-start

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/90-%{name}.preset << EOF
enable %{name}.service
EOF

# (tpg) install adverts and slideshow
tar xf - %{SOURCE21} -C %{_sysconfdir}/calamares/branding/auto

%post
# generate the "auto" branding
. %{_sysconfdir}/os-release

cat >%{_sysconfdir}/calamares/branding/auto/branding.desc <<EOF
# THIS FILE IS AUTOMATICALLY GENERATED! ANY CHANGES TO THIS FILE WILL BE LOST!
---
componentName:  auto

strings:
    productName:         "$NAME"
    shortProductName:    "$NAME"
    version:             "$VERSION"
    shortVersion:        "$VERSION_ID"
    versionedName:       "$NAME $VERSION"
    shortVersionedName:  "$NAME $VERSION_ID"
    bootloaderEntryName: "$NAME"

images:
    productLogo:         "%{_iconsdir}/openmandriva.svg"
    productIcon:         "%{_iconsdir}/openmandriva.svg"

slideshow:		"omv-ads.qml"
EOF

%files
%doc LICENSE AUTHORS
%dir %{_libdir}/calamares
%dir %{_datadir}/calamares
%dir %{_datadir}/calamares/branding
%dir %{_datadir}/calamares/branding/default
%dir %{_sysconfdir}/calamares
%dir %{_sysconfdir}/calamares/modules
%dir %{_sysconfdir}/calamares/branding
%dir %{_sysconfdir}/calamares/branding/auto
%dir %{_datadir}/calamares/qml
%dir %{_datadir}/calamares/qml/calamares
%dir %{_datadir}/calamares/qml/calamares/slideshow
%{_presetdir}/90-%{name}.preset
%{_unitdir}/%{name}.service
%{_sbindir}/%{name}-install-start
%{_bindir}/calamares
%{_datadir}/calamares/settings.conf
%{_datadir}/calamares/branding/default/*
%{_datadir}/calamares/modules/
%{_datadir}/calamares/qml/calamares/slideshow/*.qml
%{_datadir}/calamares/qml/calamares//slideshow/qmldir
%{_datadir}/applications/calamares.desktop
%{_datadir}/polkit-1/actions/com.github.calamares.calamares.policy
%{_sysconfdir}/calamares/*.conf
%{_sysconfdir}/calamares/modules/*.conf
%{_libdir}/calamares/*
%ghost %{_sysconfdir}/calamares/branding/auto/branding.desc
%{_sysconfdir}/calamares/branding/auto/*.qml
%{_sysconfdir}/calamares/branding/auto/*.png

%files -n %{libname}
%{_libdir}/libcalamares.so.%{major}*
%{_libdir}/libcalamaresui.so.%{major}*
%{_libdir}/libcalapm.so

%files -n %{develname}
%dir %{_includedir}/libcalamares
%dir %{_libdir}/cmake/Calamares
%{_includedir}/libcalamares/*
%{_libdir}/libcalamares.so
%{_libdir}/libcalamaresui.so
%{_libdir}/cmake/Calamares/*
