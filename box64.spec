# Conditional build:
%bcond_with	adlink		# target ADLink AmpereAltra device
%bcond_with	larch64		# target Loongarch64 device
%bcond_with	lx2160a		# target LX2160A device
%bcond_with	odroidn2	# target Odroid N2 device
%bcond_with	phytium		# target Phytium (D2000 or FT2000/4) device
%bcond_with	rk3326		# target Rockchip RK3326 device
%bcond_with	rk3399		# target Rockchip RK3399 device
%bcond_with	rk3588		# target Rockchip RK3588 device
%bcond_with	rpi3		# target Raspberry Pi 3
%bcond_with	rpi4		# target Raspberry Pi 4
%bcond_with	rpi5		# target Raspberry Pi 5
%bcond_with	sd845		# target Snapragon 845 device
%bcond_with	sd888		# target Snapragon 888 device
%bcond_with	sd8g2		# target Snapragon 8 Gen 2 device
%bcond_with	tegra_t194	# target Tegra Xavier device
%bcond_with	tegra_t234	# target Tegra Orin device
%bcond_with	tegrax1		# target Tegra X1

Summary:	Linux Userspace x86_64 Emulator
Name:		box64
Version:	0.3.0
Release:	1
License:	MIT
Group:		Applications
Source0:	https://github.com/ptitSeb/box64/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	408ee0d22fb796b25b417759719a840e
URL:		https://box86.org
BuildRequires:	cmake >= 3.13
BuildRequires:	python3
BuildRequires:	rpmbuild(macros) >= 1.605
ExclusiveArch:	aarch64 ppc64le riscv64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoprov	libcrypto.so libgcc_s.so libmbed.*\\.so libssl.so libstdc\\+\\+.so libpng12.so libunwind.so
%define		_noautoreqfiles	.*x86_64.*
%define		_noautostrip	.*x86_64.*

%description
Box64 lets you run x86_64 Linux programs (such as games) on non-x86_64
Linux systems, like ARM (host system needs to be 64bit little-endian).

%prep
%setup -q

%build
%cmake -B build \
%ifarch aarch64
	-DARM64:BOOL=ON \
%endif
	%{?with_adlink:-DADLINK:BOOL=ON} \
	%{?with_larch64:-DLARCH64:BOOL=ON} \
	%{?with_lx2160a:-DLX2160A:BOOL=ON} \
	%{?with_odroidn2:-DODROIDN2:BOOL=ON} \
	%{?with_phytium:-DPHYTIUM:BOOL=ON} \
%ifarch ppc64le
	-DPPC64LE:BOOL=ON \
%endif
%ifarch riscv64
	-DRV64:BOOL=ON \
%endif
	%{?with_rk3326:-DRK3326:BOOL=ON} \
	%{?with_rk3399:-DRK3399:BOOL=ON} \
	%{?with_rk3588:-DRK3588:BOOL=ON} \
	%{?with_rpi3:-DRPI3ARM64:BOOL=ON} \
	%{?with_rpi4:-DRPI4ARM64:BOOL=ON} \
	%{?with_rpi5:-DRPI5ARM64:BOOL=ON} \
	%{?with_sd845:-DSD845:BOOL=ON} \
	%{?with_sd888:-DSD888:BOOL=ON} \
	%{?with_sd8g2:-DSD8G2:BOOL=ON} \
	%{?with_tegra_t194:-DTEGRA_T194:BOOL=ON} \
	%{?with_tegra_t234:-DTEGRA_T234:BOOL=ON} \
	%{?with_tegrax1:-DTEGRAX1:BOOL=ON}
%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md docs/{CHANGELOG.md,USAGE.md}
%{_sysconfdir}/binfmt.d/box64.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/box64.box64rc
%attr(755,root,root) %{_bindir}/box64
%dir /usr/lib/x86_64-linux-gnu
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libcrypto.so.1.0.0
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libcrypto.so.1.1
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libgcc_s.so.1
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libmbedcrypto.so.3
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libmbedcrypto.so.7
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libmbedtls.so.12
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libmbedtls.so.14
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libmbedx509.so.0
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libmbedx509.so.1
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libpng12.so.0
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libssl.so.1.0.0
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libssl.so.1.1
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libstdc++.so.5
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libstdc++.so.6
%attr(755,root,root) /usr/lib/x86_64-linux-gnu/libunwind.so.8
