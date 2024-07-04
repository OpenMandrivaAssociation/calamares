%define major 3
%define oldlibname %mklibname %{name} 3
%define libname %mklibname %{name}
%define develname %mklibname %{name} -d
#define beta alpha6

## !NO JOKE! STOP TOUCHING THAT PACKAGE ##
## ANY COMMIT MADE WITHOUT DISCUSS IN DEVEL CHANELS WILL BE REVERTED ##
## THAT INCLUDES CRAP BUMPS WITHOUT TESTING ###

### STOP IT!! #####

Summary:	Distribution-independent installer framework
Name:		calamares
Version:	3.3.8
Release:	%{?beta:0.%{beta}.}%{?git:0.%{git}.}1
%if 0%{?git:1}
Source0:	https://github.com/calamares/calamares/archive/refs/heads/calamares.tar.gz
%else
Source0:	https://github.com/calamares/calamares/releases/download/v%{version}%{?beta:-%{beta}}/calamares-%{version}%{?beta:-%{beta}}.tar.gz
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
# Detect Plasma 6 on X11, prefer LXQt over Gcruft
Patch3:		calamares-3.3.5-desktops.patch
# (crazy) patches from Frugalware
# (crazy) we do some strange things in iso repo , here a way to undo
# FIXME This may need porting; the code it touches has been rewritten in 3.3.0
#Patch5:	0001-services-systemd-support-sockets-timers-and-unmask.patch

BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6WebEngineCore)
BuildRequires:	cmake(Qt6WebEngineWidgets)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	pkgconfig(libatasmart)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(libparted)
BuildRequires:	pkgconfig(polkit-qt6-1)
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6CoreAddons)
BuildRequires:	cmake(KF6Crash)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(KF6WidgetsAddons)
BuildRequires:	cmake(KF6KIO)
BuildRequires:	cmake(KF6Service)
BuildRequires:	cmake(KF6Parts)
BuildRequires:	cmake(KPMcore) >= 24.01.75
BuildRequires:	cmake(AppStreamQt) >= 1.0.0
BuildRequires:	yaml-cpp-devel
BuildRequires:	pkgconfig(python3)
BuildRequires:	boost-devel >= 1.54.0
BuildRequires:	boost-python-devel
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(pwquality)
BuildRequires:	systemd-macros
BuildRequires:	python%{pyver}dist(jsonschema)
BuildRequires:	python%{pyver}dist(pyyaml)
# cmake needs to find the tools to get their
# location into the binary
BuildRequires:	squashfs-tools
BuildRequires:	gettext
Requires:	coreutils
Requires:	plasma6-kpmcore
Requires:	gawk
Requires:	util-linux
Requires:	dracut
Requires:	grub2
Requires:	distro-release-installer
# The slideshow part uses QML and will fail silently without it
Requires:	qt6-qtdeclarative
%ifarch %{x86_64} %{aarch64}
# EFI currently only supported on x86_64 and aarch64
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
Requires:	qt6-qtwebengine

%description
Calamares is a distribution-independent installer framework,
designed to install from a live CD/DVD/USB environment to
a hard disk. It includes a graphical installation
program based on Qt 5.

%package -n %{libname}
Summary:	Calamares runtime libraries
Group:		System/Libraries
Requires:	%{name} = %{EVRD}
%rename %{oldlibname}

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
%autosetup -p1 -n %{name}-%{version}%{?beta:-%{beta}}

#delete backup files
rm -f src/modules/*/*.conf.default-settings

%build

# (crazy):
# fsresizer could be used once we get OEM mode
# plasma* one can just set a theme with an external tool right now.
# the rest cannot be used in OpenMandriva cause these are Gentoo , ArchLinux , Debian/Ubuntu only modules.
%cmake \
	-DWITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-DWITH_PYTHONQT="OFF" \
	-DWITH_KF5DBus="OFF" \
	-DSKIP_MODULES="plasmalnf openrcdmcryptcfg fsresizer luksopenswaphookcfg tracking services-openrc dummycpp dummyprocess dummypython dummypythonqt initcpio initcpiocfg initramfs initramfscfg interactiveterminal" \
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
sed -i -e 's|pkexec calamares|pkexec calamares -d|g' %{buildroot}%{_datadir}/applications/calamares.desktop

%find_lang %{name} --all-name --with-html

%files -f calamares.lang
%doc AUTHORS
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
%{_datadir}/calamares/qml/calamares/slideshow/qmldir.license
%{_datadir}/applications/calamares.desktop
%{_datadir}/polkit-1/actions/com.github.calamares.calamares.policy
%{_libdir}/calamares/*
%{_iconsdir}/hicolor/scalable/apps/*.svg
%doc %{_mandir}/man8/calamares.8.*

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
