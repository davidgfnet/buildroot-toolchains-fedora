%global buildroot_ver  2021.02.2

Name:           buildroot-armv6el-eabi-uclibc
Epoch:          1
Version:        1.1
Release:        1%{?dist}
Summary:        Buildroot generated ARMv6el uClibc toolchain

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
Source1:        armv6el.config

BuildRequires:  perl-ExtUtils-MakeMaker perl-Thread-Queue perl-FindBin
BuildRequires:	autoconf
BuildRequires:	make ncurses-devel wget bc rsync
BuildRequires:  gcc-c++
BuildRequires:  zlib-devel
BuildRequires:  make
Requires: glibc
Requires: libgcc
AutoReqProv: no

%undefine _missing_build_ids_terminate_build
%global debug_package %{nil}
%global __strip /bin/true
%global _build_id_links alldebug

%description
Buildroot generated ARM toolchain targeting ARMv6 (little endian) EABI Uses
uClibc as libc and provides static and shared libraries. Support for C and C++

%prep
%setup -q -c
cp %{SOURCE1} buildroot-%{buildroot_ver}/.config

%build
cd buildroot-%{buildroot_ver} && %make_build

%install
export QA_RPATHS=$[ 0xFFFF ]
mkdir -p %{buildroot}/opt
cp -r buildroot-%{buildroot_ver}/output/host %{buildroot}/opt/buildroot-armv6el-eabi-uclibc
cd %{buildroot}/opt/buildroot-armv6el-eabi-uclibc/ && ./bin/arm-linux-strip -d arm-buildroot-linux-uclibcgnueabi/sysroot/usr/lib/libc.a

%files
/opt/buildroot-armv6el-eabi-uclibc/*

%changelog
* Sat Jun 05 2021 David Guillen Fandos <david@davidgf.net> - 2021.06.05-1
- Bump to buildroot 2021.02.2

* Sun Mar 28 2021 David Guillen Fandos <david@davidgf.net> - 2021.03.28-1
- First version

