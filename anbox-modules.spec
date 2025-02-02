#
# spec file for package anbox-modules
#
# copyright (c) 2024 munix9@googlemail.com
#

# needssslcertforbuild

%ifarch x86_64
%if 0%{?suse_version} > 1600
%define kmp_longterm 1
%endif
%endif

Name:           anbox-modules
Version:        20240526.ee4c25f
Release:        0
Summary:        Anbox ashmem and binder kernel module
License:        GPL-2.0-only
URL:            https://github.com/choff/anbox-modules
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-preamble
Patch0:         fix-leap-15_5.patch
BuildRequires:  %{kernel_module_package_buildreqs}
Requires:       anbox-kmp = %{version}
%if 0%{?kmp_longterm}
BuildRequires:  kernel-syms-longterm
%endif
%kernel_module_package -n anbox -p %{SOURCE1}

%description
Anbox ashmem and binder out-of-tree kernel module.

%prep
%autosetup -p1

set -- *
mkdir source
mv "$@" source/
mkdir obj

%build
for flavor in %{flavors_to_build} ; do
    rm -rf obj/$flavor
    cp -r source obj/$flavor
    for _mod in ashmem binder ; do
        %make_build V=1 -C %{kernel_source $flavor} %{?linux_make_arch} modules M=$PWD/obj/$flavor/$_mod
    done
done

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR='%{kernel_module_package_moddir}'

for flavor in %{flavors_to_build} ; do
    for _mod in ashmem binder ; do
        make V=1 -C %{kernel_source $flavor} modules_install M=$PWD/obj/$flavor/$_mod
    done
done

export BRP_PESIGN_FILES='*.ko'

install -D -m 0644 -t %{buildroot}%{_modulesloaddir} source/anbox.conf
install -D -m 0644 -t %{buildroot}%{_udevrulesdir} source/99-anbox.rules

%files
%license source/debian/copyright
%doc source/README.md
%dir %{_modulesloaddir}
%{_modulesloaddir}/anbox.conf
%{_udevrulesdir}/99-anbox.rules

%changelog
