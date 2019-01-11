%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define git 20190106

Summary:	Distribution-independent installer framework
Name:		calamares
Version:	3.2.2
%if "%{git}" != ""
Release:	1.%{git}.5
Source0:	calamares-%{version}-%{git}.tar.xz
%else
Release:	13
# git archive --format=tar --prefix=calamares-1.1.0-$(date +%Y%m%d)/ HEAD | xz -vf > calamares-1.1.0-$(date +%Y%m%d).tar.xz
#Source0:	calamares-%{version}-%{calamdate}.tar.xz
Source0:	https://github.com/calamares/calamares/releases/download/v%{version}/%{name}-%{version}.tar.gz
%endif
Group:		System/Configuration/Other
License:	GPLv3+
URL:		http://calamares.io/
Source2:	%{name}.rpmlintrc
Source3:	%{name}-locale-setup
Source4:	%{name}-locale.service
Source5:	%{name}-post-script
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
Source18:	omv-services-systemd.conf
Source19:	omv-settings.conf
Source20:	omv-unpackfs.conf
Source21:	omv-users.conf
Source22:	omv-partition.conf
Source23:	omv-removeuser.conf
Source24:	omv-webview.conf
Source25:	omv-umount.conf
Source26:	omv-shellprocess.conf
Source50:       49-nopasswd_calamares.rules
Source51:       %{name}-live.sudo
Source99:	openmandriva-install.svg
Source100:	OpenMandriva-adverts.tar.xz
Patch1:		calamares-0.17.0-20150112-openmandriva-desktop-file.patch
# (crazy) why we need this?
Patch2:		calamares-libparted-detection.patch
# (crazy) patches from Frugalware
Patch3:		0001-Try-to-guess-suggested-hostname-from-dmi.patch
Patch4:		0001-locale-fixes.patch
# (crazy) we do some strange things in iso repo , here a way to undo
Patch5:		services-systemd-add-unmask-support.patch
Patch10:	revert-some-lvm-code-causing-crashes.patch
Patch11:	dm-module-do-not-error-out.patch
# For now -- until it starts working properly
Patch12:	disable-lvm-ui.patch
# (crazy) to be removed on next round of snapshots
Patch13:        bug-1043.patch
Patch14:        bug-1070.patch
# (crazy) this really got broken and not needed anyway
# drop the weird unsorted lsblk output
Patch15:        0001-CreatePartitionTableJob-drop-lsblk-and-mount-debug-o.patch


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
BuildRequires:	cmake(KF5Crash)
BuildRequires:	cmake(KF5Solid)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(KF5IconThemes)
BuildRequires:	cmake(KF5KIO)
BuildRequires:	cmake(KF5Service)
BuildRequires:	cmake(KF5Plasma)
BuildRequires:	cmake(KF5Parts)
BuildRequires:	cmake(KPMcore) >= 3.2.1
BuildRequires:	yaml-cpp-devel
BuildRequires:	pkgconfig(python3)
BuildRequires:	boost-devel >= 1.54.0
BuildRequires:	boost-python-devel
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(pwquality)
BuildRequires:	systemd-macros
Requires(post):	distro-release-OpenMandriva
Requires(post):	distro-theme-OpenMandriva
Requires:	coreutils
Requires:	gawk
Requires:	util-linux
Requires:	dracut
Requires:	grub2
%ifarch %{x86_64}
# EFI currently only supported on x86_64
Requires:	grub2-efi
%endif
Requires:	console-setup
# x11 stuff
Requires:	setxkbmap
Requires:	xkbcomp
Requires:	xloadimage
Requires:	NetworkManager
Requires:	os-prober
Requires:	gawk
# (tpg) this requires all the filesystem tools needed to manipulate filesystems
Requires:	partitionmanager >= 3.2.1
Requires:	systemd
Requires:	rsync
Requires:	shadow
Requires:	polkit
Requires:	dnf
Requires:	squashfs-tools
Requires:	dmidecode
# (tpg) needed for webview module
Requires:	qt5-qtwebengine

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
Library for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	cmake

%description -n %{develname}
Development files and headers for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}%{?git:-%{git}}

#delete backup files
rm -f src/modules/*/*.conf.default-settings

%build

%cmake_qt5 -DCALAMARES_BOOST_PYTHON3_COMPONENT="python37" -DWITH_PYTHONQT="OFF"

%make_build

%install
%make_install -C build
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
install -m 644 %{SOURCE18} %{buildroot}%{_sysconfdir}/calamares/modules/services-systemd.conf
install -m 644 %{SOURCE19} %{buildroot}%{_sysconfdir}/calamares/settings.conf
install -m 644 %{SOURCE20} %{buildroot}%{_sysconfdir}/calamares/modules/unpackfs.conf
install -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/calamares/modules/users.conf
install -m 644 %{SOURCE22} %{buildroot}%{_sysconfdir}/calamares/modules/partition.conf
install -m 644 %{SOURCE23} %{buildroot}%{_sysconfdir}/calamares/modules/removeuser.conf
install -m 644 %{SOURCE24} %{buildroot}%{_sysconfdir}/calamares/modules/webview.conf
install -m 644 %{SOURCE25} %{buildroot}%{_sysconfdir}/calamares/modules/umount.conf
install -m 644 %{SOURCE26} %{buildroot}%{_sysconfdir}/calamares/modules/shellprocess.conf

# (crazy) service and wrapper for language/keyboard stuff in the iso
mkdir -p %{buildroot}{%{_unitdir},%{_sbindir}}
install -m 755 %{SOURCE3} %{buildroot}%{_sbindir}/%{name}-locale-setup
install -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}-locale.service
install -m 755 %{SOURCE5} %{buildroot}%{_sbindir}/%{name}-post-script

# (crazy) permission files
mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d
mkdir -p %{buildroot}%{_sysconfdir}/polkit-1/rules.d
install -m 644 %{SOURCE50} %{buildroot}%{_sysconfdir}/polkit-1/rules.d/49-nopasswd_calamares.rules
install -m 440 %{SOURCE51} %{buildroot}%{_sysconfdir}/sudoers.d/%{name}-live

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/90-%{name}-locale.preset << EOF
enable %{name}-locale.service
EOF

# (tpg) install adverts and slideshow
tar xf %{SOURCE100} -C %{buildroot}%{_sysconfdir}/calamares/branding/auto

# (crazy) wipe original icon and use symlink to our one

rm -rf %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
install -m 644 %{SOURCE99} %{buildroot}%{_iconsdir}/hicolor/scalable/apps/openmandriva-install.svg
ln -s %{_iconsdir}/hicolor/scalable/apps/openmandriva-install.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%find_lang %{name} --all-name --with-html

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
    knownIssuesUrl:      "https://wiki.openmandriva.org/en/4.0/Errata"
    releaseNotesUrl:     "https://wiki.openmandriva.org/en/4.0/Release_Notes"

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

%files -f calamares.lang
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
%config(noreplace) %{_sysconfdir}/calamares/settings.conf
%{_presetdir}/90-%{name}-locale.preset
%{_unitdir}/%{name}-locale.service
%{_sbindir}/%{name}-locale-setup
%{_sbindir}/%{name}-post-script
%{_sysconfdir}/polkit-1/rules.d/49-nopasswd_calamares.rules
%{_sysconfdir}/sudoers.d/%{name}-live
%{_bindir}/calamares
%{_sysconfdir}/calamares/modules/*.conf
%{_datadir}/calamares/branding/default/*
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
%{_iconsdir}/hicolor/scalable/apps/*.svg
%{_mandir}/man8/calamares.8.*

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
