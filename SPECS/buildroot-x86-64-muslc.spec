%global buildroot_ver  2021.02

Name:           buildroot-x86-64-muslc
Epoch:          1
Version:        1.0
Release:        2%{?dist}
Summary:        Buildroot generated x86-64 musl libc toolchain

# Most of the sources are licensed under GPLv3+ with these exceptions:
# LGPLv2+ libquadmath/ libjava/libltdl/ gcc/testsuite/objc.dg/gnu-encoding/generate-random 
#         libgcc/soft-fp/ libffi/msvcc.sh
# LGPLv3+ gcc/prefix.c
# BSD libgo/go/regexp/testdata/testregex.cz zlib/example.c libffi/ 
#     libjava/classpath/external/relaxngDatatype/org/relaxng/datatype/helpers/DatatypeLibraryLoader.java
# GPLv2+ libitm/testsuite/libitm.c/memset-1.c libjava/
# Public Domain libjava/classpath/external/sax/org/xml/sax/ext/EntityResolver2.java
#               libjava/classpath/external/sax/org/xml/sax/ext/DeclHandler.java
# BSL zlib/contrib/dotzlib/DotZLib/GZipStream.cs
License:        GPLv2+ and GPLv3+ and LGPLv2+ and BSD
URL:            https://buildroot.org

Source0:        https://buildroot.org/downloads/buildroot-%{buildroot_ver}.tar.bz2
Source1:        x86-64-muslc.config

BuildRequires:  perl-ExtUtils-MakeMaker perl-Thread-Queue
BuildRequires:	autoconf
BuildRequires:	make ncurses-devel wget bc rsync
BuildRequires:  gcc-c++
BuildRequires:  zlib-devel
BuildRequires:  make
Requires: glibc
Requires: libgcc
AutoReqProv: no

%if 0%{?fedora} > 32
BuildRequires:  perl-FindBin
%endif

%undefine _missing_build_ids_terminate_build
%global debug_package %{nil}
%global __strip /bin/true
%global _build_id_links alldebug

%description
Buildroot generated x86-64 toolchain targeting small sizes. Uses
musl as libc and provides static and shared libraries. Support for C and C++

%prep
%setup -q -c
cp %{SOURCE1} buildroot-%{buildroot_ver}/.config

%build
cd buildroot-%{buildroot_ver} && %make_build

%install
export QA_RPATHS=$[ 0xFFFF ]
mkdir -p %{buildroot}/opt
cp -r buildroot-%{buildroot_ver}/output/host %{buildroot}/opt/buildroot-x86-64-muslc
cd %{buildroot}/opt/buildroot-x86-64-muslc/ && ./bin/x86_64-buildroot-linux-musl-strip -d x86_64-buildroot-linux-musl/sysroot/lib/libc.a

%files
/opt/buildroot-x86-64-muslc/*

%changelog
* Sun Mar 28 2021 David Guillen Fandos <david@davidgf.net> - 2021.03.28-1
- First version
