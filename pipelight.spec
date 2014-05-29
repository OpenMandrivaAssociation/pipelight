%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define lib32dir /usr/lib

Name:           pipelight
License:        LGPL
Group:          Networking/WWW
Version:        0.2.6
Release:        4
Summary:	MS Silverlight alternative for linux
URL:		http://fds-team.de/cms/index.html
Source:         %name-%version.tar.bz2
Source1:        %name-x64-%version.tar.bz2
Source100:      pipelight.rpmlintrc
Requires:	wine-compholio
Requires:	firefox
Suggests:	webcore-fonts

%description
MS Silverlight alternative for linux

%prep
%ifarch x86_64
 %setup -T -a1 -qn %{name}-x64-%{version}
%else
 %setup -qn %{name}-%{version}
%endif

%build


%install
cp -R usr %{buildroot}

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
