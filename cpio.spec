# XXX generate per-os macro to test
%{expand: %%global this_os_is_%{_os} %%{nil}}
%{?this_os_is_linux:%define	_bindir		/bin}
%{?this_os_is_linux:%define	_libexecdir	/sbin}

Summary: A GNU archiving program.
Name: cpio
Version: 2.4.2
Release: 20
Copyright: GPL
Group: Applications/Archiving
Source: ftp://prep.ai.mit.edu/pub/gnu/cpio-2.4.2.tar.gz
Patch0: cpio-2.3-lstat.patch
Patch1: cpio-2.4.2-glibc.patch
Patch2: cpio-2.4.2-mtime.patch
Patch3: cpio-2.4.2-svr4compat.patch
Patch4: cpio-2.4.2-glibc21.patch
Patch5: cpio-2.4.2-longlongdev.patch
Patch6: cpio-2.4.2-emptylink.patch
Patch7: cpio-2.4.2-stdout.patch
Patch8: cpio-2.4.2-fhs.patch
Patch9: cpio-2.4.2-errorcode.patch
Patch10: cpio-2.4.2-man.patch

%ifnos linux
Prereq: /sbin/rmt
%endif
Prereq: /sbin/install-info

Buildroot: %{_tmppath}/%{name}-root

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

%prep
%setup -q
# patch 0 not applied
%patch1 -p1
%patch2 -p1
%patch3 -p1 -b .svr4compat
%patch4 -p1 -b .glibc21
%patch5 -p1 -b .longlongdev
%patch6 -p1 -b .emptylink
# XXX patch7 not applied
#%patch7 -p1 -b .stdout
%patch8 -p1 -b .fhs
%patch9 -p1 -b .errorcode
%patch10 -p1 -b .man

%build

%configure
make

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall

{ cd ${RPM_BUILD_ROOT}

%ifos linux
# XXX these from mt-st
  rm -f .%{_bindir}/mt .%{_mandir}/man1/mt.1
%endif

  gzip -9nf .%{_infodir}/cpio.*
  rm -f .%{_infodir}/dir
}

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/cpio.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/cpio.info.gz %{_infodir}/dir
fi

%files
%defattr(-,root,root)
%doc README NEWS

%ifnos linux
%{_libexecdir}/*
%endif
%{_bindir}/*
%{_mandir}/man*/*

%{_infodir}/*.info*

%changelog
* Tue Aug  8 2000 Jeff Johnson <jbj@redhat.com>
- update man page with decription of -c behavior (#10581).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Preston Brown <pbrown@redhat.com>
- patch from HJ Lu for better error codes upon exit

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- missing defattr.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Fri Dec 17 1999 Jeff Johnson <jbj@redhat.com>
- revert the stdout patch (#3358), restoring original GNU cpio behavior
  (#6376, #7538), the patch was dumb.

* Tue Aug 31 1999 Jeff Johnson <jbj@redhat.com>
- fix infinite loop unpacking empty files with hard links (#4208).
- stdout should contain progress information (#3358).

* Sun Mar 21 1999 Crstian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- longlong dev wrong with "-o -H odc" headers (formerly "-oc").

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to compile on glibc 2.1, where strdup is a macro

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump package.
- Don't include /bin/mt -- use the mt from mt-st package.
- Add prereq's

* Tue Jun 30 1998 Jeff Johnson <jbj@redhat.com>
- fix '-c' to duplicate svr4 behavior (problem #438)
- install support programs & info pages

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot
- removed "(used by RPM)" comment in Summary

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- no longer statically linked as RPM doesn't use cpio for unpacking packages
