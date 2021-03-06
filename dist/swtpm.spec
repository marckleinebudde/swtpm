# --- swtpm rpm-spec ---

%define name      swtpm
%define version   0.1.0
%define release   1

# Valid crypto subsystems are 'freebl' and 'openssl'
%if "%{crypto_subsystem}" == ""
%define crypto_subsystem freebl
%endif

Summary: TPM Emulator
Name:           %{name}
Version:        %{version}
Release:        %{release}.dev2%{?dist}
License:        BSD
Group:          Applications/Emulators
Source:         %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

# due to gnutls backlevel API:
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 19
    %define with_gnutls    1
%else
    %define with_gnutls    0
%endif

BuildRequires:  automake autoconf bash coreutils libtool sed
BuildRequires:  libtpms-devel fuse-devel glib2-devel gmp-devel
BuildRequires:  expect bash net-tools nss-devel socat python-twisted
%if %{with_gnutls}
BuildRequires:  gnutls >= 3.1.0 gnutls-devel gnutls-utils
BuildRequires:  libtasn1-devel libtasn1
%if 0%{?fedora}
BuildRequires:  libtasn1-tools
%endif
%endif
%if 0%{?fedora} > 16
BuildRequires:  kernel-modules-extra
%endif

Requires:       fuse expect
%if 0%{?fedora} > 16
Requires:       kernel-modules-extra
%endif

%description
TPM emulator built on libtpms providing TPM functionality for QEMU VMs

%package        libs
Summary:        Common libraries for TPM emulators
Group:          System Environment/Libraries
License:        BSD

%description    libs
A library with callback functions for libtpms based TPM emulator

%package        cuse
Summary:        TPM emulator with CUSE interface
Group:          Applications/Emulators
License:        BSD
BuildRequires:  selinux-policy-devel

%description    cuse
TPM Emulator with CUSE interface

%package        devel
Summary:        Include files for the TPM emulator's CUSE interface for usage by clients
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Include files for the TPM emulator's CUSE interface.

%package        tools
Summary:        Tools for the TPM emulator
License:        BSD
Group:          Applications/Emulators
Requires:       swtpm fuse
Requires:       trousers >= 0.3.9 tpm-tools >= 1.3.8-6 expect bash net-tools gnutls-utils

%description    tools
Tools for the TPM emulator from the swtpm package

%files
%defattr(-,root,root,-)
%attr( 755, root, root) %{_bindir}/swtpm
%{_mandir}/man8/swtpm.8*

%files cuse
%defattr(-,root,root,-)
%attr( 755, root, root) %{_bindir}/swtpm_cuse
%{_mandir}/man8/swtpm_cuse.8*
%attr( 755, root, root) %{_datadir}/swtpm/*.pp

%files libs
%{_libdir}/libswtpm_libtpms.so.*

%files devel
%defattr(-, root, root, -)
%{_libdir}/libswtpm_libtpms.so

%dir %{_includedir}/%{name}
%attr(644, root, root) %{_includedir}/%{name}/*.h
%{_mandir}/man3/swtpm_ioctls.3*

%files tools
%defattr(-,root,root,-)
%attr( 755, root, root) %{_bindir}/swtpm_bios
%if %{with_gnutls}
%attr( 755, root, root) %{_bindir}/swtpm_cert
%endif
%attr( 755, root, root) %{_bindir}/swtpm_setup
%attr( 755, tss , tss)  %{_bindir}/swtpm_setup.sh
%attr( 755, root, root) %{_bindir}/swtpm_ioctl
%{_mandir}/man8/swtpm_bios.8*
%{_mandir}/man8/swtpm_cert.8*
%{_mandir}/man8/swtpm_ioctl.8*
%{_mandir}/man8/swtpm-localca.conf.8*
%{_mandir}/man8/swtpm-localca.options.8*
%{_mandir}/man8/swtpm-localca.8*
%{_mandir}/man8/swtpm_setup.8*
%{_mandir}/man8/swtpm_setup.conf.8*
%{_mandir}/man8/swtpm_setup.sh.8*
%config(noreplace) %{_sysconfdir}/swtpm_setup.conf
%config(noreplace) %{_sysconfdir}/swtpm-localca.options
%config(noreplace) %{_sysconfdir}/swtpm-localca.conf
%attr( 755, root, root) %{_datadir}/swtpm/swtpm-localca
%attr( 755, tss, tss) %{_localstatedir}/lib/swtpm-localca


%prep
%setup -q

%build

./bootstrap.sh
%configure \
        --prefix=/usr \
%if %{with_gnutls}
        --with-gnutls \
%endif
%if "%{crypto_subsystem}" == "openssl"
	--with-openssl
%endif

make %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%install

make %{?_smp_mflags} install DESTDIR=${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a ${RPM_BUILD_ROOT}%{_libdir}/*.la

%post cuse
if [ -n "$(type -p semodule)" ]; then
  for pp in /usr/share/swtpm/*.pp ; do
    echo "Activating SELinux policy $pp"
    semodule -i $pp
  done
fi

if [ -n "$(type -p restorecon)" ]; then
  restorecon /usr/bin/swtpm_cuse
fi

%postun cuse
if [ $1 -eq  0 ]; then
  if [ -n "$(type -p semodule)" ]; then
    for p in swtpmcuse_svirt swtpmcuse ; do
      echo "Removing SELinux policy $p"
      semodule -r $p
    done
  fi
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%changelog
