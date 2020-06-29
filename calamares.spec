%define major 3
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define git %{nil}

Summary:	Distribution-independent installer framework
Name:		calamares
Version:	3.2.26.1
%if "%{git}" != ""
Release:	0.%{git}.1
Source0:	calamares-%{version}-%{git}.tar.xz
%else
Release:	1
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
Source50:	49-nopasswd_calamares.rules
Source51:	%{name}-live.sudo
Source99:	openmandriva-install.svg
Patch1:		calamares-0.17.0-20150112-openmandriva-desktop-file.patch
# (crazy) why we need this?
Patch2:		calamares-libparted-detection.patch
# (crazy) patches from Frugalware
Patch4:		0001-locale-fixes.patch
# (crazy) we do some strange things in iso repo , here a way to undo
Patch5:		0001-services-systemd-support-sockets-timers-and-unmask.patch
# (crazy) LVM disabled for now
#  -- until it starts working properly
Patch6:		0003-disable-lvm.patch
Patch7:		calamares-3.2.16-random-seed-location.patch
#Patch12:	http://frugalware.eu/cala-luks-sucker1.patch

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
BuildRequires:	cmake(ECM)
BuildRequires:	qt5-qttools
BuildRequires:	qt5-linguist
# (crazy): fixme need to sort these after unused plasma*
# and *terminal gone
BuildRequires:	cmake(KF5CoreAddons)
BuildRequires:	cmake(KF5Config)
BuildRequires:	cmake(KF5Crash)
BuildRequires:	cmake(KF5Solid)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(KF5IconThemes)
BuildRequires:	cmake(KF5KIO)
BuildRequires:	cmake(KF5Service)
BuildRequires:	cmake(KF5Parts)
BuildRequires:	cmake(KPMcore) >= 4.0.0
BuildRequires:	cmake(AppStreamQt)
BuildRequires:	yaml-cpp-devel
BuildRequires:	pkgconfig(python3)
BuildRequires:	boost-devel >= 1.54.0
BuildRequires:	boost-python-devel
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(pwquality)
BuildRequires:	systemd-macros
Requires:	coreutils
Requires:	kpmcore
Requires:	gawk
Requires:	util-linux
Requires:	dracut
Requires:	grub2
Requires:	distro-release-installer
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
%autosetup -p1

#delete backup files
rm -f src/modules/*/*.conf.default-settings

%build

# (crazy):
# preservefiles fsresizer could be used once we get OEM mode
# plasma* one can just set a theme with an external tool right now.
# the rest cannot be used in OpenMandriva cause these are Gentoo , ArchLinux , Debian/Ubuntu only modules.
%cmake_qt5 \
	-DCALAMARES_BOOST_PYTHON3_COMPONENT="python39" \
	-DWITH_PYTHONQT="OFF" \
	-DSKIP_MODULES="plasmalnf preservefiles openrcdmcryptcfg fsresizer luksopenswaphookcfg tracking services-openrc dummycpp dummyprocess dummypython dummypythonqt initcpio initcpiocfg initramfs initramfscfg interactiveterminal" \
	-DBoost_NO_BOOST_CMAKE=ON \
	-G Ninja

if grep -q "No Python support" CMakeFiles/CMakeOutput.log; then
	printf '%\n' "Python support is disabled."
	printf '%s\n' "Probably boost-python libraries weren't detected."
	exit 1
fi

%ninja_build

%install
%ninja_install -C build
#own the local settings directories
mkdir -p %{buildroot}%{_sysconfdir}/calamares/modules
mkdir -p %{buildroot}%{_sysconfdir}/calamares/branding/auto

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

# (crazy) wipe original icon and use symlink to our one
rm -rf %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
install -m 644 %{SOURCE99} %{buildroot}%{_iconsdir}/hicolor/scalable/apps/openmandriva-install.svg
ln -s %{_iconsdir}/hicolor/scalable/apps/openmandriva-install.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg

#(crazy) we want debug.log
sed -i -e 's|/usr/bin/calamares|/usr/bin/calamares -d|g' %{buildroot}%{_datadir}/applications/calamares.desktop

%find_lang %{name} --all-name --with-html

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
%{_presetdir}/90-%{name}-locale.preset
%{_unitdir}/%{name}-locale.service
%{_sbindir}/%{name}-locale-setup
%{_sbindir}/%{name}-post-script
%{_sysconfdir}/polkit-1/rules.d/49-nopasswd_calamares.rules
%{_sysconfdir}/sudoers.d/%{name}-live
%{_bindir}/calamares
%{_datadir}/calamares/branding/default/*
%{_datadir}/calamares/qml/calamares/slideshow/*.qml
%{_datadir}/calamares/qml/calamares//slideshow/qmldir
%{_datadir}/applications/calamares.desktop
%{_datadir}/polkit-1/actions/com.github.calamares.calamares.policy
%{_libdir}/calamares/*
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
