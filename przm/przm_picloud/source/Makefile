############################################
# DO NOT DELETE THIS LINE - used by f90make.
# Everything after the line will be replaced when the Makefile is updated.
# Section updated on Tue Nov  9 11:52:35 2004.
# Makefile for przm
# e:\5\3przm\7.src\Makefile
#
# nmake /n /u -- generates commands for a batch file

#  6 Jan 2004  3:21 pm
#     * added version.rc stuff
#
# 10 Dec 2002  9:44 am
# Base file created by f90make, then edited by hand:
#     * add the przm libs
#     * source is f77 (without "module" statement), therefore
#       needed to add the objects to the target. See $(f77code)

# DOS>nmake > a.del
# DOS>grep -v 'Fixed form source is an obsolescent feature' a.del > b.del

.SUFFIXES: .exe .o .mod .f90 .f95 .f .f9x .res .rc .rcx

# Fortran preprocessor name: xcoco
# Options:
#    -x :: Read _xcoco.ini
#    -S :: supress final setfile message
# fpp = xcoco
# fpp_opts = -x -S
fpp =
fpp_opts =

# FC = lf95
FC = gfortran

# Lf95 flags
# -dbl -- extend all single precision real items to double precision
# -in -- "Implicit None"
# -info -- variables declared and not used, other stuff
# -nchk -- no checks
# -nconcc -- turn off Fortran carriage control processing for console I/O.
# -pause -- pause after the program terminates
# -wo -- warn obsolescent f90
# -xref -- generate cross-reference information (stored in *.lst)
# XREF = -xref # -info
XREF = -g # -info

# Debug: Compile and link flags
DEBUGcf = -chk -g -pca -stchk -trace -w -winconsole

# OPTIMIZE: Compile and link flags
OPTIMIZEcf = -nap -nchk -ndal -ng -o1 -npca -ntrace -nsav -nstchk -nw

SRC_Path =
ModuleList = .

f95flags =
ldflags =

# [production options]
# f95flags = -in -zero $(XREF) #-info
f95flags = $(XREF)
#f95flags = -fno-range-check

# Rules:
.f9x.f90 :
        $(fpp) $(fpp_opts)  $@ $<

.f90.o :
	$(FC) $(f95flags) -c $< -o $*.o

.f.o :
	$(FC) $(f95flags) -c $< -o $*.o


# przm3123.exe
f90code = canopy.o chem.o cnfuns.o cropdate.o datemod.o \
   debug.o debug_cn.o f2kcli.o floatcmp.o furrow.o \
   general.o i_errchk.o inivar.o ioluns.o \
   iosubs.o lambertw.o m_readvars.o utils.o wind.o

f77code = fcscnc.o przm3.o rsexec.o rsinp1.o rsinp2.o \
   rsinp3.o rsmcar.o rsmisc.o rsprz1.o rsprz2.o \
   rsprz3.o rsprzn.o rsutil.o rsvado.o

przm2_LIBS = -L libanne4.0_gfortran/lib -lwdm -ladwdm -lutil

#-L ../libanne4.0_gfortran/lib -lwdm -ladwdm -lutil

targets : przm3123.exe

przm3123.exe : $(f90code) $(f77code)
	$(FC) $(ldflags) -o $@ $(f90code) $(f77code) $(przm2_LIBS)

### Dependencies for .f90 files:
canopy.o : general.o i_errchk.o wind.o canopy.f90
chem.o : CCROP.INC CHYDR.INC CMET.INC CMISC.INC CPEST.INC PPARM.INC \
   general.o chem.f90
cnfuns.o : CCROP.INC CHYDR.INC PPARM.INC m_readvars.o cnfuns.f90
cropdate.o : CCROP.INC CMISC.INC PPARM.INC datemod.o debug.o cropdate.f90
datemod.o : datemod.f90
debug.o : debug.f90
debug_cn.o : CCROP.INC CHYDR.INC PPARM.INC debug_cn.f90
f2kcli.o : f2kcli.f90
floatcmp.o : floatcmp.f90
furrow.o : CIRGT.INC general.o lambertw.o furrow.f90
general.o : general.f90
i_errchk.o : i_errchk.f90
inivar.o : CMET.INC PPARM.INC general.o wind.o inivar.f90
ioluns.o : general.o ioluns.f90
iosubs.o : general.o iosubs.f90
lambertw.o : general.o lambertw.f90
m_readvars.o :  m_readvars.f90
utils.o : f2kcli.o general.o utils.f90
wind.o : general.o wind.f90

### Dependencies for .f files:
fcscnc.o : CHYDR.INC CIRGT.INC CMET.INC CMISC.INC CPEST.INC \
   PPARM.INC ioluns.o fcscnc.f
przm3.o : CECHOT.INC CFILEX.INC CMCRVR.INC PIOUNI.INC PMXNSZ.INC \
   PMXZON.INC PPARM.INC datemod.o debug.o general.o \
   inivar.o utils.o przm3.f
rsexec.o : CCONTR.INC CCUMUL.INC CECHOT.INC CFILEX.INC CIN2VD.INC \
   CMDATA.INC CPRZST.INC CTRNBC.INC CVADST.INC CVCHMK.INC \
   CVMISC.INC CVNTR1.INC CVVLM.INC CVWRKM.INC CZNWHT.INC \
   PCMPLR.INC PIOUNI.INC PMXMAT.INC PMXNOD.INC PMXNSZ.INC \
   PMXOWD.INC PMXPDT.INC PMXVDT.INC PMXZON.INC cropdate.o rsexec.f
rsinp1.o : CECHOT.INC CFILEX.INC CHYDR.INC CMISC.INC CPEST.INC \
   CTRACE.INC CZNWHT.INC EXAM.INC PIOUNI.INC PMXNSZ.INC \
   PMXYRS.INC PMXZON.INC PPARM.INC TABLE.INC \
   cropdate.o datemod.o general.o ioluns.o iosubs.o rsinp1.f
rsinp2.o : CACCUM.INC CBIO.INC CCROP.INC CECHOT.INC CFILEX.INC \
   CHYDR.INC CIRGT.INC CMCRVR.INC CMET.INC CMISC.INC \
   CNITR.INC CPEST.INC CSPTIC.INC CVNTR1.INC EXAM.INC \
   HLFDUM.INC PMXNSZ.INC PMXZON.INC PPARM.INC \
   cnfuns.o cropdate.o datemod.o debug.o floatcmp.o \
   general.o m_readvars.o utils.o wind.o rsinp2.f
rsinp3.o : CADISC.INC CBACK.INC CBDISC.INC CBSOLV.INC CCONTR.INC \
   CDAOBS.INC CECHOT.INC CIN2VD.INC CMCRVR.INC CMCSTR.INC \
   CMDATA.INC CPCHK.INC CSWHDA.INC CTPDEF.INC CVADST.INC \
   CVMISC.INC CVNTR1.INC CVNTR2.INC CVVLM.INC CVWRKM.INC \
   CWORKN.INC PMXMAT.INC PMXNLY.INC PMXNOD.INC PMXNSZ.INC \
   PMXOWD.INC PMXPRT.INC PMXTIM.INC PMXTMV.INC PMXVDT.INC \
   rsinp3.f
rsmcar.o : rsmcar.f
rsmisc.o : CBIO.INC CHYDR.INC CMET.INC CMISC.INC CONSTP.INC \
   CPEST.INC EXAM.INC PMXYRS.INC PPARM.INC TABLE.INC rsmisc.f
rsprz1.o : CBIO.INC CCROP.INC CECHOT.INC CFILEX.INC CHYDR.INC \
   CIRGT.INC CMET.INC CMISC.INC CNITR.INC CPEST.INC \
   CPRZST.INC CPTAP.INC CSPTIC.INC EXAM.INC PMXNSZ.INC \
   PMXPDT.INC PMXZON.INC PPARM.INC \
   canopy.o chem.o cnfuns.o cropdate.o datemod.o \
   debug.o furrow.o wind.o rsprz1.f
rsprz2.o : CACCUM.INC CCROP.INC CGLBPZ.INC CHYDR.INC CIRGT.INC \
   CMET.INC CMISC.INC CNITR.INC CPEST.INC CSPTIC.INC \
   PMXZON.INC PPARM.INC rsprz2.f
rsprz3.o : CACCUM.INC CCROP.INC CHYDR.INC CIRGT.INC CMET.INC \
   CMISC.INC CNITR.INC CPEST.INC CPTCHK.INC CSPTIC.INC \
   EXAM.INC PMXYRS.INC PPARM.INC TABLE.INC wind.o rsprz3.o
rsprzn.o : CHMSG.INC PHMSG.INC rsprzn.f
rsutil.o : CECHOT.INC CFILEX.INC CTRACE.INC PCMPLR.INC PIOUNI.INC \
   PMXNSZ.INC PMXZON.INC rsutil.f
rsvado.o : CONSTP.INC CADISC.INC CBACK.INC CBSOLV.INC CCONTR.INC \
   CCUMUL.INC CDAOBS.INC CECHOT.INC CFILEX.INC CHYDR.INC \
   CMCSTR.INC CMDATA.INC CMISC.INC CPCHK.INC CSWHDA.INC \
   CTRNBC.INC CVASLV.INC CVCHMK.INC CVNTR1.INC CVNTR2.INC \
   CVVLM.INC CVWRKM.INC CWELEM.INC CWORKA.INC CWORKN.INC \
   PMXMAT.INC PMXNOD.INC PMXNSZ.INC PMXOWD.INC PMXPRT.INC \
   PMXTIM.INC PMXTMV.INC PMXVDT.INC PMXZON.INC PPARM.INC rsvado.f

#End-of-File Makefile

clean:
	rm -f *.o *.mod przm3123.exe
