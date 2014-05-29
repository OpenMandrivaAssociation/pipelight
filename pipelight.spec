%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define lib32dir /usr/lib

Name:           pipelight
License:        LGPL
Group:          Networking/WWW
Version:        0.2.6
Release:        2
Summary:	MS Silverlight alternative for linux
URL:		http://fds-team.de/cms/index.html
Source:         %name-%version.tar.bz2
Source1:        %name-x64-%version.tar.bz2
BuildRoot:      %{_tmppath}/%name-%version-build
Requires:	wine-compholio
Requires:	firefox
Suggests:	webcore-fonts

%description
MS Silverlight alternative for linux

%prep
%ifarch x86_64
 %setup -T -a 1 -n %name-%version
%else
 %setup -n %name-%version
%endif

%build


%install
cp -R usr $RPM_BUILD_ROOT

%post
#!/bin/sh -e


# Source debconf library.
ln -s /bin/id /usr/bin/id
pipelight-plugin --update
pipelight-plugin --create-mozilla-plugins

%preun
#!/bin/sh -e


pipelight-plugin --remove-mozilla-plugins

# Keep the previous configuration on an update
if [ "$1" != "upgrade" ]; then
	pipelight-plugin --disable-all
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/pipelight-plugin
%{_datadir}/%{name}
%{_datadir}/doc/%{name}-multi
%{_datadir}/man/man1/pipelight-plugin.1.xz
%ifarch x86_64
%{lib32dir}/%{name}
%else
%{_libdir}/%{name}
%endif

%changelog
* Wed May 27 2014 kyndek <kyndek@gmail.com> 
- prepared for Openmandriva Lx 

* Mon Apr 07 2014 Stan8 <stasiek0000@poczta.onet.pl> 0.2.6-Stan8
- new version

* Sun Mar 30 2014 Stan8 <stasiek0000@poczta.onet.pl> 0.2.5-Stan8
- first build