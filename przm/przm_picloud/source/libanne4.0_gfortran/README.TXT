README.TXT

                              LIBANNE

        A set of libraries for use with hydrologic applications

                             Version 4.0

                             2002/02/25

                        libraries for:   aide and wdm
                                         graphics
                                         statistics
                                         utility
                                         data analysis
                      utility programs:  wdimex
                                         wdmrx

IMPORTANT NOTE:  If you have n-day data sets that were created using
                 the N-day option in version 3.2 of SWSTAT, you will
                 need to run WDMRX to correct a problem with the
                 SEADBG and SEADND attributes.  WDMRX is distributed
                 with ANNIE (http://water.usgs.gov/software/annie.html)
                 and SWSTAT (http://water.usgs.gov/software/swstat.html)
                 as well as LIBANNE.

Instructions for installation and use are provided below.  After
installation, see libanne.txt in the doc subdirectory for summary
information on LIBANNE.

For assistance, enhancement requests, or to report bugs, contact the
Hydrologic Analysis Software Support Program by sending e-mail to
h2osoft@usgs.gov.



                          TABLE OF CONTENTS

                          A. DISTRIBUTION FILES
                          B. DOCUMENTATION
                          C. EXTRACTING FILES
                          D. COMPILING (optional)
                          E. INSTALLING
                          F. CONTACTS


A. DISTRIBUTION FILES

The following distribution packages (containing the software and
information files) are currently available for UNIX systems:

 libanne4.0.source.tar.gz  - Source code only
 libanne4.0.Solaris.tar.gz - Compiled for Sun UltraSPARC-II under Solaris 2.6


B. DOCUMENTATION

   The libanne libraries are used in various combinations by a number of
   water-resources applications, including ANNIE, IOWDM, SWSTAT, PEAKFQ,
   GLSNET, DR3M, HSPEXP, HSPF, HYSEP, and  PRMS.

   The Watershed Data Management (WDM) library provides a mechanism for
   managing in a single storage file the kinds of data needed to perform
   water-resources investigations.  Time-series, table, text, vector,
   space-time, and descriptive attribute data types are currently supported
   in the WDM file format.  (Requires wdmlib, adwdmlib, and utillib.)

   The ANNIE Interactive Development Environment (AIDE) library provides
   a set of routines for building interactive, character-based interfaces.
   The library contains tools to build a user interface that provides a
   consistent methodology for displaying text and for querying the user
   for (1) menus, (2) forms, (3) tables, and (4) file names.  (Requires
   aidelib, adwdmlib, and utillib.)

   The graphics (GRAPH) library contains a set of routines for drawing
   axes, curves, and symbols.  Requires a user-supplied Graphical Kernel
   System (GKS) library.  (Requires graphlib and utillib.)

   Computer generated documentation for the utillib, graphlib, wdmlib,
   aidelib, and adwdmlib libraries is included in the doc subdirectory.
   See these files:

   utillib.txt   general utility routines
   graphlib.txt  graphics routines
   wdmlib.txt    watershed data management routines
   aidelib.txt   aide user interface
   adwdmlib.txt  routines shared by wdm and aide libraries

Kittle, J.L., Jr., Hummel, P.R., and Imhoff, J.C., 1989, ANNIE-IDE, A
   system for developing interactive user interfaces for environmental
   models (Programmers Guide):  Environmental  Research Laboratory,
   U.S Environmental Protection Agency, Athens, Ga., EPA/600/3-89/034,
   166 p.

Lumb, A.M., Carsel, R.F., and Kittle, J.L., Jr., 1988, Data management
   for water-quality modeling development and use:  Proceedings of the
   International Conference on Interactive Information and Processing
   Systems for Meteorology, Oceanography, and Hydrology.

Kittle, J.L., Jr., Flynn, K.M., Hummel, P.R., and Lumb, A.M.,
   Programmers manual for the watershed data management (wdm) system,
   1991, written communication, 190 p.

See http://water.usgs.gov/software/ordering_documentation.html for
information on ordering printed copies of USGS publications.

For information on ordering printed copies of EPA publications, see

           National Technical Information Service
           5285 Port Royal Road
           Springfield VA 22161

           electronic mail: orders@ntis.fedworld.gov
           Phone:  1-800-553-NTIS (6847) or (703) 605-6000
           Fax: (703) 605-6900
           web:  http://www.ntis.gov/


C. EXTRACTING FILES

Compressed tar files are used to distribute the source code and versions
of the software compiled for selected UNIX operating systems.  All of
the files needed to install and use the libraries are contained in the
file libanne4.0.OS.tar.gz (where OS is a string indicating the intended
operating system.)  If there is not a tar file for your operating system
or you want to compile the software, the source version of the tar file
contains all of the files needed to compile and install the libraries on
a UNIX-based computer.  For all of these distributions, the directory
libanne4.0 is created (or overwritten) when the files are extracted from
the tar file; if this directory already exists, you may want to delete
or rename it before extracting the files.

Follow the steps below to extract the files from a distribution tar file
(assumes libanne will be installed in the /usr/opt/wrdapp directory).

  Steps in extracting files                  explanation
  -----------------------------------------  ---------------------------------
  mv libanne4.0.____.tar.gz /usr/opt/wrdapp  If the tar file is not already in
                                             the directory where you want the
                                             distribution installed, move it
                                             there.

  cd /usr/opt/wrdapp                         If you are not in the directory
                                             where the tar file is located, go
                                             there.

  gunzip libanne4.0.____.tar.gz              Uncompress the distribution file.

  tar -xvpof libanne4.0.____.tar             Extract the distribution files
                                             from the tar file.

This creates the following directory structure (the contents of each
directory are shown to the right):

   libanne4.0                files NOTICE.TXT, RELEASE.TXT, and this README.TXT
     `-----bin               compiled utility programs
     `-----doc               documentation files (see file Contents.txt)
     `-----src               Makefile
             `-----adwdm     --+
             `-----aide        |
             `-----ann         |
             `-----awstat      +-- for each library and program:
             `-----graph       |
             `-----stats       |   1.  makefile
             `-----util        |
             `-----waide       |   2.  source code, if the source tar
             `-----wdimex      |       file is untarred
             `-----wdm         |
             `-----wdmrx     --+
     `-----msg               wdimex.sh script to build message file
             `-----adwdm     --+
             `-----aide        |
             `-----ann         +-- text versions of the message file
             `-----awstat      |   groups for the indicated libraries
             `-----waide     --+
     `-----lib               compiled libraries
     `-----lib_data          unformatted, binary direct access message file

Notes:  a) The lib, lib_data, and bin subdirectories are not included in
           the source distribution; they are created during compilation.
        b) Source code is included only with the source distribution.
        c) It is recommended that no user files be kept in the library
           directory structure.  If you plan to put files in the library
           directory structure, do so only by creating subdirectories.
        d) The software is configured for installation under the
           directory /usr/opt/wrdapp.  The wrdapp directory may be
           a separate file system mounted at /usr/opt/wrdapp.  Most
           programs that use the libanne libraries do not require that
           the libraries be installed under /usr/opt/wrdapp.  If you
           choose to install the library elsewhere and you have programs
           that use the WMSGOP or ANINIT routines,  you will need to
           retrieve the source version of the tar file and compile
           the software.  See the README.TXT files of the individual
           software packages to see if this is necessary.


D. COMPILING (optional)

If you have retrieved a pre-compiled distribution of the software, skip to
the Installing section below.

If a compiled version of the software is not available for your computer
or you want to build the libraries yourself, follow the instructions in
this section.  The source distribution is provided for those users' who
want the source code.  Little or no support can be provided for users
generating their own versions of the software.  In general, to compile a
new version of the software, you will need:

        a) Fortran (77 or later) and C compilers,
        b) a minimal level of knowledge of Make, the compilers, and
           the UNIX operating system,
        c) while not required for compiling the libraries, a Graphical
           Kernel System (GKS) library is required to use the graphlib
           library;  GKS libraries available without fee include Gli/gks
           (available at http://iff001.iff.kfa-juelich.de/gli/) and xgks
           (available at unidata.ucar.edu in /pub/xgks/xgks-2.5.5.tar.Z).

As provided in the source distribution, the software is set up to be
compiled under Solaris in the /usr/opt/wrdapp directory using Gli/gks.
A small number of changes may be needed to compile on other UNIX
platforms, in another directory, or to use a different GKS library.
Additional changes will be required to compile on a PC or other non-UNIX
platform.  The versions.txt file found in the doc subdirectory identifies
items that may need to be changed.

To generate the library archives, utility executables, and message file,
do the following:

1.  The values for the indicated variables in the following files may
    need to be modified (see versions.txt in the doc subdirectory for
    more details):

                                 variables that may need to be modified
                           ---------------------------------------------------
    file name                  version     lib archive   compiler flags & name
    ---------------------  --------------  ------------  ---------------------
    src/Makefile           SeqVrsn
        util/makefile      FFVrsn ObjVrsn  SymTbl ArOpt  FFLAGS FC   CFLAGS CC
        adwdm/makefile     FFVrsn ObjVrsn  SymTbl ArOpt  FFLAGS FC
              fmsgwd.inc   WDNAME
        wdm/makefile       FFVrsn          SymTbl ArOpt  FFLAGS FC
        aide/makefile      FFVrsn ObjVrsn  SymTbl ArOpt  FFLAGS FC
             fmsgwd.inc    WDNAME
        awstat/makefile    FFVrsn          SymTbl ArOpt  FFLAGS FC
        graph/makefile     FFVrsn ObjVrsn  SymTbl ArOpt  FFLAGS FC
        stats/makefile     FFVrsn          SymTbl ArOpt  FFLAGS FC
        waide/makefile     FFVrsn          SymTbl ArOpt  FFLAGS FC
        ann/makefile       FFVrsn          SymTbl ArOpt  FFLAGS FC
        wdimex/makefile    FFVrsn          SymTbl ArOpt  FFLAGS FC
        wdmrx/makefile     FFVrsn          SymTbl ArOpt  FFLAGS FC
              wdmrx.f      RECL

2.  Run make in the src directory to compile the source, build the libraries
    and utility programs, and create the message file:

        cd libanne4.0/src
        make

    make will:

        a.  create the subdirectories lib, bin, and lib_data, if they do
            not already exist,
        b.  run make in each of the subdirectories under src to compile
            the source code and build the libraries and utility programs,
            placing the libraries in lib and the executables in bin,
        c.  run the wdimex.sh script found in the msg subdirectory to
            build the message file and place it in lib_data.

    Note:  This MAY take a while.


E. INSTALLING

To make the libraries and utility programs easy to use, they should be
installed in directories included in the user's library and executable
search paths, respectively.  The Makefile in the libanne src directory
contains instructions to optionally place links in the specified directories
to the libraries and executables contained in the libanne lib and bin
directories.  Change to the libanne src directory and use the following
command:

    make install [LIBDIR=lib_path] [BINDIR=bin_path]

where lib_path and bin_path are the names of directories in the user's
path.  If LIBDIR and BINDIR are specified, the libraries and utility
programs are linked to the specified directories, respectively.  By
default, LIBDIR equals the libanne lib directory and BINDIR equals the
libanne bin directory.

Examples of values for lib_path and bin_path are:

    make install LIBDIR=/usr/local/lib BINDIR=/usr/opt/bin
    make install LIBDIR=$HOME/lib BINDIR=$HOME/bin

Notes:  a) Brackets "[xxx]" are used to indicate optional arguments
           to commands.
        b) The installer must have sufficient access rights to the
           LIBDIR and BINDIR directories to create links to the
           libraries and utility programs and to delete any existing
           libanne libraries or utility programs (see list below).
        c) By setting LIBDIR and BINDIR to directories in the users'
           search path, the libraries can be conveniently loaded from
           any directory on your computer and the programs can be easily
           executed from any directory.

After installation, the following libraries, utility programs, and message
file should be available to the users:

  directory            available files
  -------------------  -----------------------------------
  LIBDIR               adwdmlib.a   aidelib.a   annlib.a
                       awstatlib.a  graphlib.a  statslib.a
                       utillib.a    waidelib.a  wdmlib.a
  BINDIR               wdimex       wdmrx
  libanne4.0/lib_data  message.wdm


F. CONTACTS

Inquiries about this software distribution should be directed to:

  U.S. Geological Survey
  Hydrologic Analysis Software Support Program
  437 National Center
  Reston, VA  20192

  e-mail:  h2osoft@usgs.gov
