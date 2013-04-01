# Makefile for libanne libraries and utility programs
#
# Usage:   make [LIBDIR=install_libs_in] [BINDIR=install_binary_in]
#               [install] [clean]  [| tee makeout]
#
# Example:  make
#           make BINDIR=/usr/opt/bin LIBDIR=/usr/lib
#           make BINDIR=$HOME/bin
#
# History:  95/12/05 kmflynn
#           99/07/30 kmflynn

# message file [Gli, Xgks, DG Pc]
SeqVrsn = $(SeqGli)

#*******************************************************************
#*****   Some things may need to be changed below this line.   *****
#*******************************************************************

# installation directories
BINDIR = ../bin
LIBDIR = ../lib

# this description file uses the Bourne shell
SHELL = /bin/sh
shCmd = sh

# Sequential file, installation specific
# where parm[gli xgks pc dg].seq sets computer type, graphics parameters
SeqGli  = gli
SeqXgks = xgks
SeqPc   = pc
SeqDG   = dg

#*******************************************************************
#***** You should not need to modify anything below this line. *****
#*******************************************************************

# library directories
binary = ../bin
library= ../lib
libdata= ../lib_data
Dirs   = $(binary) $(library) $(libdata)

# libraries and programs
Libs = utillib.a      adwdmlib.a  wdmlib.a    \
       aidelib.a      graphlib.a  statslib.a  \
       waidelib.a     awstatlib.a annlib.a
Pgms = wdimex     wdmrx
Msgg = ../lib_data/message.wdm

# sequential files:
SeqAtr = ../msg/adwdm/attr001.seq  ../msg/adwdm/attr051.seq  ../msg/adwdm/attr101.seq \
         ../msg/adwdm/attr151.seq  ../msg/adwdm/attr201.seq  ../msg/adwdm/attr251.seq \
         ../msg/adwdm/attr301.seq  ../msg/adwdm/attr351.seq  ../msg/adwdm/attr401.seq \
         ../msg/aide/message.seq   ../msg/aide/parm$(SeqVrsn).seq
SeqMsg = ../msg/waide/awfeb.seq    ../msg/waide/prwfil.seq   ../msg/waide/atinfo.seq
SeqAwa = ../msg/waide/awfeb.seq    ../msg/waide/tslist.seq   ../msg/waide/agplot.seq  \
         ../msg/awstat/tscmpr.seq  ../msg/awstat/a193.seq    ../msg/awstat/profdr.seq \
         ../msg/ann/pgener.seq     ../msg/ann/qtprnt.seq

# rules
all:  first $(Libs) utility_pgms $(Msgg) install

# make sure all of the libraries and utility programs are current
utillib.a:     ; @cd util     ; make
adwdmlib.a:    ; @cd adwdm    ; make
wdmlib.a:      ; @cd wdm      ; make
aidelib.a:     ; @cd aide     ; make
graphlib.a:    ; @cd graph    ; make
statslib.a:    ; @cd stats    ; make
waidelib.a:    ; @cd waide    ; make
awstatlib.a:   ; @cd awstat   ; make
annlib.a:      ; @cd ann      ; make
utility_pgms:
	@cd wdimex ; make
	@cd wdmrx  ; make

# make sure message files are current
$(Msgg): $(SeqAtr) $(SeqMsg) ../msg/wdimex.sh
	@rm -f $(Msgg)
	@cd ../msg ; rm -f message.out  ; $(shCmd) ./wdimex.sh message $(SeqVrsn) > message.out
	@echo "***"
	@echo "*** Done making message file."
	@echo "***"

# Create directories for libraries, executables, and message files, if needed
first:
	@for dir in $(Dirs) ; do         \
	   if [ ! -d $$dir ] ; then      \
	      mkdir  $$dir ;             \
	      echo "*** Created $$dir" ; \
	   fi ;                          \
	done
install:
	@if [ ! -d $(LIBDIR) ]  ; then   \
	   mkdir $(LIBDIR) ;             \
	   echo "*** Created $(LIBDIR)"; \
	fi
	@for lib in $(Libs) ; do                                    \
	   if [ ! -s ../lib/$$lib ] ; then                          \
	      echo "*** --NOTICE:  library $$lib does not exist"  ; \
	      echo "*** use one of the following to generate it:" ; \
	      echo "***      make"     ;                            \
	      echo "***      make all" ;                            \
	   else                                                     \
	      if [ $(LIBDIR) != $(library) ] ; then                 \
	         rm -f $(LIBDIR)/$$lib ;                            \
	         cd ..; ln -s `pwd`/lib/$$lib $(LIBDIR)/$$lib ;     \
	         cd ./src ;                                         \
	         echo "*** Library $$lib has been updated." ;       \
	      fi ;                                                  \
	   fi                                                       \
	done
	@if [ ! -d $(BINDIR) ]  ; then   \
	   mkdir $(BINDIR) ;             \
	   echo "*** Created $(BINDIR)"; \
	fi
	@for pgm in $(Pgms) ; do                                    \
	   if [ ! -s ../bin/$$pgm ] ; then                          \
	      echo "*** --NOTICE:  program $$pgm does not exist"  ; \
	      echo "*** use one of the following to generate it:" ; \
	      echo "***      make"     ;                            \
	      echo "***      make all" ;                            \
	   else                                                     \
	      if [ $(BINDIR) != $(binary) ] ; then                  \
	         rm -f $(BINDIR)/$$pgm ;                            \
	         cd ..; ln -s `pwd`/bin/$$pgm $(BINDIR)/$$pgm ;     \
	         cd ./src ;                                         \
	         echo "*** Program $$pgm has been updated." ;       \
	      fi ;                                                  \
	   fi                                                       \
	done
clean:
	@cd util   ; make clean ; cd ..
	@cd adwdm  ; make clean ; cd ..
	@cd wdm    ; make clean ; cd ..
	@cd aide   ; make clean ; cd ..
	@cd graph  ; make clean ; cd ..
	@cd stats  ; make clean ; cd ..
	@cd waide  ; make clean ; cd ..
	@cd awstat ; make clean ; cd ..
	@cd ann    ; make clean ; cd ..
	@cd wdimex ; make clean ; cd ..
	@cd wdmrx  ; make clean ; cd ..
	@echo "***"
	@rm -f $(Msgg) ; echo "*** Removed library message file"
	@cd ../msg ; rm -f message.out message.in error.fil ; \
	    echo "***          and associated output files" ; \
	    echo "***          generated by make."          ; \
	    echo "***" ;                                      \
	    cd ../src

# end of make
