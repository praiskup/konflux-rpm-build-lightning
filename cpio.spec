# XXX generate per-os macro to test
%{expand: %%global this_os_is_%{_os} %%{nil}}
%{?this_os_is_linux:%define	_bindir		/bin}
%{?this_os_is_linux:%define	_libexecdir	/sbin}

Summary: A GNU archiving program.
Name: cpio
Version: 2.6
Release: 18.1
License: GPL
Group: Applications/Archiving
URL: http://www.gnu.org/software/cpio/
Source: ftp://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.gz
Patch0: cpio-2.6-rh.patch
Patch13: cpio-2.5-nolibnsl.patch
Patch14: cpio-2.6-lfs.patch
Patch16: cpio-2.6-lstat.patch
Patch17: cpio-2.6-umask.patch
Patch18: cpio-2.6-chmodRaceC.patch
Patch19: cpio-2.6-dirTraversal.patch
Patch20: cpio-2.6-warnings.patch
Patch21: cpio-2.6-checksum.patch
Patch22: cpio-2.6-writeOutHeaderBufferOverflow.patch
Patch23: cpio-2.6-initHeaderStruct.patch

%ifnos linux
Prereq: /sbin/rmt
%endif
Prereq: /sbin/install-info
BuildRequires: texinfo, autoconf
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
%patch0 -p1 -b .rh
%patch13 -p1 -b .nolibnsl
%patch14 -p1 -b .lfs
%patch16 -p1 -b .lstat
%patch17 -p1 -b .umask
%patch18 -p1 -b .chmodRaceC
%patch19 -p1 -b .dirTraversal
%patch20 -p1 -b .warnings
%patch21 -p1 -b .checksum
%patch22 -p1 -b .bufferOverflow
%patch23 -p1 -b .initHeaderStruct
autoheader

%build

CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -pedantic -Wall" %configure
make

%install
rm -rf ${RPM_BUILD_ROOT}

%makeinstall
%find_lang %{name}

{ cd ${RPM_BUILD_ROOT}

%ifos linux
# XXX these from mt-st
  rm -f .%{_bindir}/mt .%{_mandir}/man1/mt.1
%endif

# XXX Nuke unpackaged files.
  rm -f .%{_infodir}/dir
  rm -f ./sbin/rmt
}

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/install-info %{_infodir}/cpio.info.gz %{_infodir}/dir

%preun
if [ $1 = 0 ]; then
    /sbin/install-info --delete %{_infodir}/cpio.info.gz %{_infodir}/dir
fi

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc AUTHORS ChangeLog NEWS README THANKS TODO

%ifnos linux
%{_libexecdir}/*
%endif
%{_bindir}/*
%{_mandir}/man*/*

%{_infodir}/*.info*

%changelog
* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6-18.1
- rebuild

* Sat Jun 10 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-18
- autoconf was added to BuildRequires, because autoheader is 
  used in prep phase (#194737)

* Tue Mar 28 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-17
- rebuild

* Sat Mar 25 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-15
- fix (#186339) on ppc and s390

* Thu Mar 23 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-14
- init struct  file_hdr (#186339)

* Wed Mar 15 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-13
- merge toAsciiError.patch with writeOutHeaderBufferOverflow.patch
- merge largeFileGrew.patch with lfs.patch
- fix large file support, cpio is able to store files<8GB 
  in 'old ascii' format (-H odc option)
- adjust warnings.patch

* Tue Mar 14 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-12
- fix warn_if_file_changed() and set exit code to #1 when 
  cpio fails to store file > 4GB (#183224)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.6-11.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.6-11.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 23 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-11
- fix previous patch(writeOutHeaderBufferOverflow)

* Wed Nov 23 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-10
- write_out_header rewritten to fix buffer overflow(#172669)

* Mon Oct 31 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-9
- fix checksum error on 64-bit machines (#171649)

* Fri Jul 01 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-8
- fix large file support, archive >4GiB, archive members <4GiB (#160056)
- fix race condition holes, use mode 0700 for dir creation

* Tue May 17 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-7
- fix #156314 (CAN-2005-1229) cpio directory traversal issue
- fix some gcc warnings

* Mon Apr 25 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-6
- fix race condition (#155749)
- use find_lang macro

* Thu Mar 17 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuild 2.6-5

* Mon Jan 24 2005 Peter Vrabec <pvrabec@redhat.com>
- insecure file creation (#145721)

* Mon Jan 17 2005 Peter Vrabec <pvrabec@redhat.com>
- fix symlinks pack (#145225)

* Fri Jan 14 2005 Peter Vrabec <pvrabec@redhat.com>
- new fixed version of lfs patch (#144688)

* Thu Jan 13 2005 Peter Vrabec <pvrabec@redhat.com>
- upgrade to cpio-2.6

* Tue Nov 09 2004 Peter Vrabec <pvrabec@redhat.com>
- fixed "cpio -oH ustar (or tar) saves bad mtime date after Jan 10 2004" (#114580)

* Mon Nov 01 2004 Peter Vrabec <pvrabec@redhat.com>
- support large files > 2GB (#105617)

* Thu Oct 21 2004 Peter Vrabec <pvrabec@redhat.com>
- fix dependencies in spec

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not link against -lnsl

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 14 2003 Jeff Johnson <jbj@redhat.com> 2.5-3
- setlocale for i18n compliance (#79136).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 18 2002 Jeff Johnson <jbj@redhat.com> 2.5-1
- update 2.5, restack and consolidate patches.
- don't apply (but include for now) freebsd and #56346 patches.
- add url (#54598).

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 2.4.2-30
- rebuild from CVS.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.4.2-25
- Fix up extraction of multiply linked files when the first link is
  excluded (Bug #56346)

* Mon Oct  1 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.4.2-24
- Merge and adapt patches from FreeBSD, this should fix FIFO handling

* Tue Jun 26 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add and adapt Debian patch (pl36), fixes #45285 and a couple of other issues

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

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
