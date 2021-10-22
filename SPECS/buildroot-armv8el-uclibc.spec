%global buildroot_ver  2021.08.1

Name:           buildroot-armv8el-uclibc
Epoch:          1
Version:        1.3
Release:        1%{?dist}
Summary:        Buildroot generated ARMv8el uClibc toolchain

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
Source1:        armv8el.config

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
Buildroot generated ARM toolchain targeting ARMv8 (little endian). Uses
uClibc as libc and provides static and shared libraries. Support for C and C++

%prep
%setup -q -c
cp %{SOURCE1} buildroot-%{buildroot_ver}/.config

%build
cd buildroot-%{buildroot_ver} && %make_build

%install
export QA_RPATHS=$[ 0xFFFF ]
mkdir -p %{buildroot}/opt
cp -r buildroot-%{buildroot_ver}/output/host %{buildroot}/opt/buildroot-armv8el-uclibc
cd %{buildroot}/opt/buildroot-armv8el-uclibc/ && ./bin/aarch64-linux-strip -d aarch64-buildroot-linux-uclibc/sysroot/usr/lib/libc.a
# Strip debug symbols from .so files in sysroot
for f in `find %{buildroot}/opt/buildroot-armv8el-uclibc/aarch64-buildroot-linux-uclibc/sysroot -type f -name "*.so*"`;
do
  if file $f | grep "ELF" | grep "not stripped"; then
    %{buildroot}/opt/buildroot-armv8el-uclibc/bin/aarch64-linux-strip -d $f
  fi
done

%files
/opt/buildroot-armv8el-uclibc/*

%changelog
* Sat Oct 09 2021 David Guillen Fandos <david@davidgf.net> - 2021.10.09-1
- Bump to buildroot 2021.08.1 (and GCC 11)

* Sat Sep 18 2021 David Guillen Fandos <david@davidgf.net> - 2021.09.18-1
- Bump to buildroot 2021.08

* Sat Jun 05 2021 David Guillen Fandos <david@davidgf.net> - 2021.06.05-1
- Bump to buildroot 2021.02.2

* Sun Mar 28 2021 David Guillen Fandos <david@davidgf.net> - 2021.03.28-1
- First version

