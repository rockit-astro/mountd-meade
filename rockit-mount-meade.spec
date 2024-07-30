Name:      rockit-mount-meade
Version:   %{_version}
Release:   1
Summary:   Meade LX200-GPS mount control
Url:       https://github.com/rockit-astro/mountd-meade
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/mountd/
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/tel %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/meade_mountd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/meade_mountd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/completion/tel %{buildroot}/etc/bash_completion.d/tel
%{__install} %{_sourcedir}/warwick.json %{buildroot}%{_sysconfdir}/mountd/

%package server
Summary:  Meade LX200-GPS mount server
Group:    Unspecified
Requires: python3-rockit-mount-meade python3-astropy python3-pyserial
%description server

%files server
%defattr(0755,root,root,-)
%{_bindir}/meade_mountd
%defattr(0644,root,root,-)
%{_unitdir}/meade_mountd@.service

%package client
Summary:  Meade LX200-GPS mount client
Group:    Unspecified
Requires: python3-rockit-mount-meade python3-astropy
%description client

%files client
%defattr(0755,root,root,-)
%{_bindir}/tel
/etc/bash_completion.d/tel

%package data-warwick
Summary: Meade LX200-GPS mount configuration for Windmill Hill telescope
Group:   Unspecified
%description data-warwick

%files data-warwick
%defattr(0644,root,root,-)
%{_sysconfdir}/mountd/warwick.json

%changelog
