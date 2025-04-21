%global buildroot_ver  2025.02

Name:           buildroot-mipsel32-o32-uclibc
Epoch:          1
Version:        1.7
Release:        1%{?dist}
Summary:        Buildroot generated MIPSel32 uClibc toolchain

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

Source0:        https://buildroot.org/downloads/buildroot-%{buildroot_ver}.tar.gz
Source1:        mipsel32.config
Source2:        fixes-gcc15.patch

BuildRequires:  perl-ExtUtils-MakeMaker perl-Thread-Queue perl-FindBin perl-English perl-IPC-Cmd
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
Buildroot generated MIPS toolchain targeting MIPS32 (little endian) O32. Uses
uClibc as libc and provides static and shared libraries. Support for C and C++

%prep
%setup -q -c
cd buildroot-%{buildroot_ver}
patch -p1 < %{SOURCE2}
cp %{SOURCE1} .config

%build
cd buildroot-%{buildroot_ver}
%make_build

%install
export QA_RPATHS=$[ 0xFFFF ]
mkdir -p %{buildroot}/opt
cp -r buildroot-%{buildroot_ver}/output/host %{buildroot}/opt/buildroot-mipsel32-o32-uclibc
cd %{buildroot}/opt/buildroot-mipsel32-o32-uclibc/ && ./bin/mipsel-linux-strip -d mipsel-buildroot-linux-uclibc/sysroot/usr/lib/libc.a
# Strip debug symbols from .so files in sysroot
for f in `find %{buildroot}/opt/buildroot-mipsel32-o32-uclibc/mipsel-buildroot-linux-uclibc/sysroot -type f -name "*.so*"`;
do
  if file $f | grep "ELF" | grep "not stripped"; then
    %{buildroot}/opt/buildroot-mipsel32-o32-uclibc/bin/mipsel-linux-strip -d $f
  fi
done

%files
/opt/buildroot-mipsel32-o32-uclibc/*

%changelog
* Mon Apr 21 2025 David Guillen Fandos <david@davidgf.net> - 2025.04.21-1
- Bump to buildroot 2025.02

* Wed May 22 2024 David Guillen Fandos <david@davidgf.net> - 2024.05.22-1
- Bump to buildroot 2024.02.2

* Mon Apr 17 2023 David Guillen Fandos <david@davidgf.net> - 2023.04.17-1
- Bump to buildroot 2023.02

* Fri May 20 2022 David Guillen Fandos <david@davidgf.net> - 2022.05.20-1
- Bump to buildroot 2022.02.1

* Sat Oct 09 2021 David Guillen Fandos <david@davidgf.net> - 2021.10.09-1
- Bump to buildroot 2021.08.1 (and GCC 11)

* Sat Sep 18 2021 David Guillen Fandos <david@davidgf.net> - 2021.09.18-1
- Bump to buildroot 2021.08

* Sat Jun 05 2021 David Guillen Fandos <david@davidgf.net> - 2021.06.05-1
- Bump to buildroot 2021.02.2

* Sun Mar 28 2021 David Guillen Fandos <david@davidgf.net> - 2021.03.28-1
- First version

