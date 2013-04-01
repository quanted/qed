# Makefile for util

include ../make.inc
#
# Usage:  make [libdir=path_to_install_to] [install] [| tee makeout]
#
# Examples:  make 
#            make install libdir=/usr/lib
#            make install libdir=$HOME/lib
#
# History:  95/12/05 kmflynn
#           96/12/10 kmflynn - modified to include/exclude mouse option
#           99/07/30 kmflynn

ObjVrsn = $(ObjSun)         # source Obj[Sun, SGI, DG, AIX, Dec, HP, or 90]
FFVrsn  = $(FFUnix)         # Version FF[Unix, AIX]
SymTbl  = $(BSD)            # symbol table (BSD or SYS_V)

#*******************************************************************
#*****   Some things may need to be changed below this line.   *****
#*******************************************************************

# Compiler flags
#    C - check subranges and array bounds
#    u - default data type for undeclareds is undefined
#    g - generate source level symbolic debug information
# ansi - compile in accordance with rules for ANSI C, flag violations
#    O - optimization
# (NOTES: to generate debug code - set FFLAGS to Dbgf and
#                                  set CFLAGS to DbgC
#            for production code - set FFLAGS to OptM and
#                                  set CFLAGS to OptC
DbgF   = -u -C -g
OptM   = -u -O
DbgC   = -ansi -g
OptC   = -ansi

# compile options, use Unix for default
FFUnix =
FFAIX  = -qxlf77=leadzero        # force leading zero on output

# symbol table for library archive may need to be explicitly built;
# System V ar does this automatically (DG and AIX)
# BSD ar does not (Sun)
BSD    = ranlib $@
SYS_V  = @echo
#        note:  some makes have a problem with SYS_V being blank,
#               use an empty echo.

# library archive options
#    r - replace the named files in the archive file
#    v - give a verbose file-by-file description of the making
#    c - suppress the message that is produced by default when
#        the archive file is created
#    q - quickly append the named files to the end of the
#        archive file
ArOpt = rv

# this description file uses the Bourne shell
SHELL = /bin/sh

# build library with or without mouse option
Mouse_yes = _m
Mouse_no  =
Mouse     = $(Mouse_no)

# Object files, installation specific
# where dttm[dg pc sg sn dc 90].o calls to system routines for date and time
#       utcp(c gn 90].o copy and fill arrays (c, fortran 77, and fortran 90)
#       ckfs[dg pc].o wild card file name matching
#       uscn[vt ux lf90 lh ot pc].o screen addressing
#       utsc[dg lf90 lh ot pc pr vx].o get/put single char from/to screen
#       tty[ux].o get/put single character
ObjScrn = uscnvt.o utscdg$(Mouse).o ttyux.o
ObjFile = ckfsdg.o dirlis_.o getdir_.o Malloc.o FileName.o
#
ObjDG   = utcpc.o  dttmdg.o $(ObjScrn) $(ObjFile)
ObjSun  = utcpc.o  dttmsn.o $(ObjScrn) $(ObjFile)
ObjSGI  = utcpc.o  dttmsg.o $(ObjScrn) $(ObjFile)
ObjAIX  = utcpc.o  dttm90.o $(ObjScrn) $(ObjFile)
ObjDec  = utcpc.o  dttmdc.o $(ObjScrn) $(ObjFile)
ObjHP   = utcpc.o  dttmhp.o $(ObjScrn) $(ObjFile)
Obj90   = utcp90.o dttm90.o $(ObjScrn) $(ObjFile)

#*******************************************************************
#***** You should not need to modify anything below this line. *****
#*******************************************************************

library = util$(Mouse)lib.a
Objects = utchar.o  utdate.o  utgnrl.o utnumb.o utsort.o utscxx.o

libdir  = ../../lib
binary  = ../../lib
libMake = $(binary)/$(library)
libInst = $(libdir)/$(library)

# Rules
all: $(binary) $(libMake) install
	@echo "***"
	@echo "*** Done making all for $(library), files are now up-to-date."
	@echo "***"

# Library and utility dependencies:
$(libMake):   $(Objects) $(ObjVrsn)
	@echo "***"
	@echo "*** making $(libMake)"
	@echo "***"
	ar $(ArOpt) $@ $?
	$(SymTbl)
$(binary):
	@if [ ! -d $(binary) ]   ; then   \
	   mkdir $(binary)  ;             \
	   echo "*** Created $(binary)" ; \
	fi
install:
# Create directory for binary file, if necessary
	@if [ ! -d $(libdir) ]   ; then   \
	   mkdir $(libdir) ;              \
	   echo "*** Created $(libdir)" ; \
	fi
# Link executable to libdir if installing elsewhere
	@if [ ! -s $(libMake) ] ; then                                   \
	   echo "*** library $(libMake) does not exist," ;               \
	   echo "*** use one of the following commands to generate it:"; \
	   echo "***     make" ;  echo "***     make all" ;              \
	else                                                             \
	   if [ $(libdir) != $(binary) ] ; then                          \
	      rm -f $(libInst) ;                                         \
	      cd ../..; ln -s `pwd`/lib/$(library) $(libInst);           \
	      cd ./src/util ;                                            \
	      echo "*** Library $(libInst) has been updated.";           \
	   fi ;                                                          \
	fi
clean:
	@if [ $(libdir) != $(binary) ] ; then rm -f $(libInst) ; fi
	@rm -f *.o $(libMake)
	@echo "***"
	@echo "*** Removed files generated by make for $(library)."
	@echo "***"

# Define object file dependencies:
utchar.o:     const.inc
utnumb.o:     const.inc  fversn.inc
utscxx.o:     color.inc

utscot.o:     color.inc
utscpc.o:     color.inc
utscin.o:     color.inc
utsclf90.o:   color.inc
utsclh.o:     color.inc
utscxxin.o:   color.inc

# system include files
#utcpc.o:     <string.h>
#FileName.o:  <stdlib.h> <string.h>
#Malloc.o:    <stdlib.h>
#dirlis_.o:   <stdlib.h> <string.h> <stdio.h>
#getdir_.o:   <stdlib.h> <string.h> <memory.h>
#ttyux.o:     <signal.h> <stdio.h>  <termios.h>

# end of make
