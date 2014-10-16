%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define lib32dir /usr/lib

Name:           pipelight
License:        LGPL
Group:          Networking/WWW
Version:        0.2.7.1
Release:        2
Epoch:			1
Summary:	MS Silverlight alternative for linux
URL:		http://fds-team.de/cms/index.html
%ifarch x86_64
%define rname %name-x64
%else
%define rname %name
%endif 
Source0:	pipelight-%{version}.tar.xz
Source1:	pipelight-x64-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%rname-%version-build
Source100:      pipelight.rpmlintrc
%ifarch x86_64
Requires:	wine-compholio64
%else
Requires:	wine-compholio
%endif
Requires:	firefox
Requires:   	webcore-fonts
Suggests:	firefox-ext-user_agent_overrider

%description
MS Silverlight alternative for linux

%prep
%ifarch x86_64
%setup -T -b 1 -n %rname-%version
%else
%setup -T -b 0 -n %rname-%version
%endif

%build

%install
cp -R usr %{buildroot}

%post
#!/bin/sh -e


# Source debconf library.
ln -sf /bin/id /usr/bin/id
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
%{_datadir}/man/man1/pipelight-plugin.1.xz
%ifarch x86_64
%{lib32dir}/%{name}
%else
%{_libdir}/%{name}
%endif
