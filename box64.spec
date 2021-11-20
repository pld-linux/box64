# Conditional build:
%bcond_with	larch64		# target Loongarch64 device
%bcond_with	phytium		# target Phytium (D2000 or FT2000/4) device
%bcond_with	rk3326		# target Rockchip RK3326 device
%bcond_with	rk3399		# target Rockchip RK3399 device
%bcond_with	rpi4		# target Raspberry Pi 4
%bcond_with	sd845		# target Snapragon 845 device
%bcond_with	tegrax1		# target Tegra X1

Summary:	Linux Userspace x86_64 Emulator
Name:		box64
Version:	0.1.6
Release:	1
License:	MIT
Group:		Applications
Source0:	https://github.com/ptitSeb/box64/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	caf23020c1c5e823ac2f2155d82d1d4a
URL:		https://box86.org
BuildRequires:	cmake >= 3.4
BuildRequires:	python3
BuildRequires:	rpmbuild(macros) >= 1.605
ExclusiveArch:	aarch64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprov	libgcc_s.so libstdc\\+\\+.so
%define		_noautostrip	.*x86_64.*

%description
Box64 lets you run x86_64 Linux programs (such as games) on non-x86_64
Linux systems, like ARM (host system needs to be 64bit little-endian).

%prep
%setup -q

%build
%cmake -B build \
	%{?with_larch64:-DLARCH64=ON} \
	%{?with_phytium:-DPHYTIUM=ON} \
	%{?with_rk3326:-DRK3326=ON} \
	%{?with_rk3399:-DRK3399=ON} \
	%{?with_rpi4:-DRPI4ARM64=ON} \
	%{?with_sd845:-DSD845=ON} \
	%{?with_tegrax1:-DTEGRAX1=ON}
%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/{CHANGELOG.md,README.md,USAGE.md}
%{_sysconfdir}/binfmt.d/box64.conf
%attr(755,root,root) %{_bindir}/box64
%dir /usr/lib/x86_64-linux-gnu
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libstdc++.so.6
