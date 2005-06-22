# TODO
# - mandir should be passed in build not install (pmk bug?)
Summary:	Pre Make Kit
Name:		pmk
Version:	0.9.3
Release:	0.2
Epoch:		0
License:	BSD
Group:		Development/Building
Source0:	http://dl.sourceforge.net/pmk/%{name}-%{version}.tar.gz
# Source0-md5:	6f117a9282ee92f2f973c6973f6f822f
URL:		http://pmk.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The pmk project tries to provide an alternative to GNU autoconf, GNU
libtool and pkg-config. It also provides a basic BSD install like tool
and a source scanner to help building of pmkfiles.

Goals:
- Make it easy to use for both users and developers.
- Let the configure stage as secure as possible
- Keep the number of needed dependencies as low as possible (actually
  only libc).
- Provide the package in a free and usable license for everybody
  (three clauses BSD).
- Limit the changes in sources for a transition from autoconf.

%prep
%setup -q

%build
SYSCONFDIR=%{_sysconfdir} \
DATADIR=%{_datadir} \
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
sh pmkcfg.sh -p %{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
%{__make} install \
	MANDIR=%{_mandir} \
	DESTDIR=$RPM_BUILD_ROOT

> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/%{name}.conf

%post
# due HW specific vars, need to do it on target host
%{_bindir}/pmksetup -u PREFIX=%{_prefix} > /dev/null

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BONUS README BUGS STATUS CREDITS TODO Changelog INSTALL LICENSE
%doc doc/ samples/
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*

%attr(755,root,root) %{_bindir}/pmk
%attr(755,root,root) %{_bindir}/pmkinstall
%attr(755,root,root) %{_bindir}/pmkpc
%attr(755,root,root) %{_bindir}/pmkscan
%attr(755,root,root) %{_bindir}/pmksetup
%{_mandir}/man[158]/*
%dir %{_datadir}/pmk
%{_datadir}/pmk/pmkcfgtool.dat
%{_datadir}/pmk/pmkcomp.dat
%{_datadir}/pmk/pmkcpu.dat
%{_datadir}/pmk/pmkfile.sample
%{_datadir}/pmk/pmkscan.dat
