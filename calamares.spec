%define major 2
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Distribution-independent installer framework
Name:		calamares
Version:	2.4.5
Release:	3
Group:		System/Configuration/Other
License:	GPLv3+
URL:		http://calamares.io/
# git archive --format=tar --prefix=calamares-1.1.0-$(date +%Y%m%d)/ HEAD | xz -vf > calamares-1.1.0-$(date +%Y%m%d).tar.xz
#Source0:	calamares-%{version}-%{calamdate}.tar.xz
Source0:	%{name}-%{version}.tar.gz
Source2:	calamares.rpmlintrc
Source3:	%{name}.service
Source4:	%{name}.target
Source5:	%{name}-install-start
Source6:	%{name}-install-setup
Source7:	omv-bootloader.conf
Source8:	omv-displaymanager.conf
Source9:	omv-finished.conf
Source10:	omv-fstab.conf
Source11:	omv-grubcfg.conf
Source12:	omv-keyboard.conf
Source13:	omv-locale.conf
Source14:	omv-machineid.conf
Source15:	omv-mount.conf
Source16:	omv-packages.conf
Source17:	omv-welcome.conf
Source18:	omv-services.conf
Source19:	omv-settings.conf
Source20:	omv-unpackfs.conf
Source21:	omv-users.conf
Source22:	omv-partition.conf
Source23:	omv-removeuser.conf
Source24:	omv-webview.conf
Source99:	openmandriva-install.svg
Source100:	OpenMandriva-adverts.tar.xz
Patch1:		calamares-0.17.0-20150112-openmandriva-desktop-file.patch
Patch2:		calamares-libparted-detection.patch
# 2.2.2 introduced a change where the partition module loading (including scanning)
# is run in a separate thread, this causes crashes for us so temporarily reverting
# until a full solution is found
# Patch3:		calamares-2.3-revert_async_partition_module_loading.patch
# (tpg) here is the candidate for a real solution
#Patch4:		0000-Rearrange-asynchronous-scan-in-PartitionCoreModule-a.patch
#Patch5:		0001-Init-filesystems-asynchronously.patch
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5WebEngine)
BuildRequires:	pkgconfig(Qt5WebEngineWidgets)
BuildRequires:	pkgconfig(Qt5Test)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Quick)
BuildRequires:	pkgconfig(Qt5QuickWidgets)
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
BuildRequires:	cmake(KF5IconThemes)
BuildRequires:	cmake(KF5KIO)
BuildRequires:	cmake(KF5Service)
BuildRequires:	cmake(KF5Parts)
BuildRequires:	cmake(KPMcore) >= 2.2.0
BuildRequires:	yaml-cpp-devel
BuildRequires:	pkgconfig(python3)
BuildRequires:	boost-devel >= 1.54.0
BuildRequires:	boost-python3-devel
BuildRequires:	pkgconfig(libcrypto)
Requires(post):	distro-release-OpenMandriva
Requires(post):	distro-theme-OpenMandriva
Requires:	coreutils
Requires:	gawk
Requires:	util-linux
Requires:	dracut
Requires:	grub2
%ifarch x86_64
# EFI currently only supported on x86_64
Requires:	grub2-efi
%endif
Requires:	console-setup
# x11 stuff
Requires:	setxkbmap
Requires:	xkbcomp
Requires:	xli
Requires:	NetworkManager
Requires:	os-prober
Requires:	gawk
# (tpg) this requires all the filesystem tools needed to manipulate filesystems
Requires:	partitionmanager >= 2.2.0
Requires:	systemd
Requires:	rsync
Requires:	shadow
Requires:	polkit
Requires:	urpmi
Requires:	squashfs-tools
Requires:	dmidecode
# (tpg) needed for webview module
Requires:	qt5-qtwebengine
# (tpg) needed for calamares-install-setup
Requires:	openbox
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
%setup -qn %{name}-%{version}
%apply_patches

#delete backup files
rm -f src/modules/*/*.conf.default-settings

%build
%cmake_qt5 -DWITH_CRASHREPORTER:BOOL="OFF"

%make

%install
%makeinstall_std -C build

#own the local settings directories
mkdir -p %{buildroot}%{_sysconfdir}/calamares/modules
mkdir -p %{buildroot}%{_sysconfdir}/calamares/branding/auto
touch %{buildroot}%{_sysconfdir}/calamares/branding/auto/branding.desc

# (tpg) settings specific for OMV
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/calamares/modules/bootloader.conf
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/calamares/modules/displaymanager.conf
install -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/calamares/modules/finished.conf
install -m 644 %{SOURCE10} %{buildroot}%{_sysconfdir}/calamares/modules/fstab.conf
install -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/calamares/modules/grubcfg.conf
install -m 644 %{SOURCE12} %{buildroot}%{_sysconfdir}/calamares/modules/keyboard.conf
install -m 644 %{SOURCE13} %{buildroot}%{_sysconfdir}/calamares/modules/locale.conf
install -m 644 %{SOURCE14} %{buildroot}%{_sysconfdir}/calamares/modules/machineid.conf
install -m 644 %{SOURCE15} %{buildroot}%{_sysconfdir}/calamares/modules/mount.conf
install -m 644 %{SOURCE16} %{buildroot}%{_sysconfdir}/calamares/modules/packages.conf
install -m 644 %{SOURCE17} %{buildroot}%{_sysconfdir}/calamares/modules/welcome.conf
install -m 644 %{SOURCE18} %{buildroot}%{_sysconfdir}/calamares/modules/services.conf
install -m 644 %{SOURCE19} %{buildroot}%{_sysconfdir}/calamares/settings.conf
install -m 644 %{SOURCE20} %{buildroot}%{_sysconfdir}/calamares/modules/unpackfs.conf
install -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/calamares/modules/users.conf
install -m 644 %{SOURCE22} %{buildroot}%{_sysconfdir}/calamares/modules/partition.conf
install -m 644 %{SOURCE23} %{buildroot}%{_sysconfdir}/calamares/modules/removeuser.conf
install -m 644 %{SOURCE24} %{buildroot}%{_sysconfdir}/calamares/modules/webview.conf

# (tpg) service files
mkdir -p %{buildroot}{%{_unitdir},%{_sbindir},%{_sysconfdir}/systemd/system/calamares.target.wants}
install -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}.target
install -m 755 %{SOURCE5} %{buildroot}%{_sbindir}/%{name}-install-start
install -m 744 %{SOURCE6} %{buildroot}%{_sbindir}/%{name}-install-setup
ln -sf %{_unitdir}/%{name}.service %{buildroot}%{_sysconfdir}/systemd/system/calamares.target.wants/%{name}.service

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/90-%{name}.preset << EOF
enable %{name}.service
EOF

# (tpg) install adverts and slideshow
tar xf %{SOURCE100} -C %{buildroot}%{_sysconfdir}/calamares/branding/auto

# (tpg) install icon
mkdir -p %{buildroot}%{_iconsdir}
install -m 644 %{SOURCE99} %{buildroot}%{_iconsdir}/openmandriva-install.svg

%post
# generate the "auto" branding
. %{_sysconfdir}/os-release

cat > %{_sysconfdir}/calamares/branding/auto/branding.desc <<EOF
# THIS FILE IS AUTOMATICALLY GENERATED! ANY CHANGES TO THIS FILE WILL BE LOST!
---
componentName:  auto

strings:
    productName:         "$NAME"
    shortProductName:    "$NAME"
    version:             "$VERSION"
    shortVersion:        "$VERSION"
    versionedName:       "$NAME $VERSION"
    shortVersionedName:  "$NAME $VERSION"
    bootloaderEntryName: "openmandriva"
    productUrl:          "$HOME_URL"
    supportUrl:          "$BUG_REPORT_URL"
    knownIssuesUrl:      "https://wiki.openmandriva.org/en/3.0/New"
    releaseNotesUrl:     "https://wiki.openmandriva.org/en/3.0/Release_Notes"

images:
    productLogo:         "%{_iconsdir}/openmandriva.svg"
    productIcon:         "%{_iconsdir}/openmandriva.svg"
# (tpg) need to decide what show here
#    productWelcome:      "languages.png"

slideshow:               "omv-ads.qml"

style:
   sidebarBackground:    "#263039"
   sidebarText:          "#FFFFFF"
   sidebarTextSelect:    "#292F34"
EOF

%files
%doc LICENSE AUTHORS
%dir %{_sysconfdir}/systemd/system/calamares.target.wants
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
%{_sysconfdir}/systemd/system/calamares.target.wants/%{name}.service
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.target
%{_sbindir}/%{name}-install-start
%{_sbindir}/%{name}-install-setup
%{_bindir}/calamares
%optional %{_libexecdir}/calamares_crash_reporter
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
%{_iconsdir}/openmandriva-install.svg
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

%files -n %{libname}
%{_libdir}/libcalamares.so.%{major}*
%{_libdir}/libcalamaresui.so.%{major}*

%files -n %{develname}
%dir %{_includedir}/libcalamares
%dir %{_libdir}/cmake/Calamares
%{_includedir}/libcalamares/*
%{_libdir}/libcalamares.so
%{_libdir}/libcalamaresui.so
%{_libdir}/cmake/Calamares/*
