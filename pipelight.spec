%define _enable_debug_packages %{nil}
%define debug_package %{nil}
%define lib32dir /usr/lib


Name:           pipelight
License:        LGPLv2.1+
Group:          Networking/WWW
Version:        0.2.8.2
Release:        1
Epoch:		1
Summary:	MS Silverlight alternative for linux
URL:		http://pipelight.net
Source0:	pipelight-%{version}.tar.bz2
Source1:	pipelight-x64-%{version}.tar.bz2
Source100:      pipelight.rpmlintrc
Patch0:		pipelight-0.2.8.2-distro-version.patch
Patch1:		pipelight-0.2.8.2-id-path.patch
# Not auto-detected, likely used via dlopen
Requires:	%{_lib}capi20_3
# Used in library check
Requires:	pkgconfig(netapi)
Requires:	webcore-fonts
# Even 64 bit version uses 32 bit wine and some libraries for main plugins
Requires:	libudev1
Requires:	wine32
%ifarch x86_64
Requires:	wine64
%endif
Requires(post,preun):	gnupg
Requires(post,preun):	wget
Suggests:	firefox-ext-user_agent_overrider

%description
MS Silverlight alternative for linux.

Make sure to enable plugins by running pipelight-plugin from your user account.
For example: pipelight-plugin --enable silverlight5.1

Enabling plugins requires to accept Microsoft's license so it has to be done
manually.

If something goes wrong run: pipelight-plugin --system-check

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

%post
#!/bin/sh -e
mkdir -p /usr/lib/mozilla/plugins
pipelight-plugin --update
pipelight-plugin --remove-mozilla-plugins
pipelight-plugin --create-mozilla-plugins

%preun
#!/bin/sh -e
# Keep the previous configuration on an update
if [ $1 = 0 ]; then
    pipelight-plugin --remove-mozilla-plugins
    pipelight-plugin --disable-all
fi


#----------------------------------------------------------------------------

%prep
%setup -c -T
%ifarch x86_64
tar -xf %{SOURCE1}
%else
tar -xf %{SOURCE0}
%endif
pushd %{name}-*
%patch0 -p1
%patch1 -p1
popd
%build

%install
cp -R %{name}-*/usr %{buildroot}/

chmod 0755 %{buildroot}%{_prefix}/lib/%{name}/*.so

pushd %{buildroot}%{_datadir}/%{name}
rm -f wine
ln -s %{_bindir}/wine wine
%ifarch x86_64
rm -f wine64
ln -s %{_bindir}/wine64 wine64
%endif
popd
