############################################
# DO NOT DELETE THIS LINE - used by f90make.
# Everything after the line will be replaced when the Makefile is updated.


.SUFFIXES: .exe .o .mod .f90 .f95 .f .f9x .res .rc .rcx

FC = gfortran

# Debug: Compile and link flags
DEBUGcf = -fbacktrace

# OPTIMIZE: Compile and link flags
OPTIMIZEcf = -nap -nchk -ndal -ng -o1 -npca -ntrace -nsav -nstchk -nw


f95flags = -fcheck=all

# options
# -g -Wall  -fno-bounds-check


# .f9x.f90 :
# 	$(FC) $(f95flags) $(DEBUGcf) $@ $<

# .f90.o :
# 	$(FC) $(f95flags) -c $< -o $*.o

# .f.o :
# 	$(FC) $(f95flags) -c $< -o $*.o


f90code = adamdata.f90 admess.f90 dsply.f90 f2kcli.f90 floatcmp.f90 geardat2.f90 geardata.f90 gintrp.f90 grsub4.f90 helper.f90 ihelp.f90 imbed.f90 inpout.f90 local1.f90 local2.f90 modnam.f90 OZONE.F90 platform.f90 plotx.f90 pondat.f90 prodat.f90 prtmsg.f90 RANKSORT.F90 shoplo.f90 shovar.f90 SIZE.F90 skale.f90 skale2.f90 skan.f90 soldat.f90 solfct.f90 staopt.f90 statvar.f90 stepdata.f90 stifdata.f90 stmess.f90 trans.f90 typopt.f90 unprec.f90 whtcmd.f90 wrkspace.f90 xbar.f90 xvalue.f90 zonopt.f90 bldout.f90 catlg.f90 datopt.f90 decod1.f90 decod2.f90 decod4.f90 desout.f90 dintpt.f90 dintrp.f90 divdif.f90 doit.f90 echoset.f90 ENVSIZ.F90 erase.f90 gear.f90 getarg.f90 getnum.f90 get_file.f90 GLOBALS.F90 help.f90 ifind.f90 inrec.f90 kinet.f90 kinhed.f90 kinlis.f90 kinnum.f90 kinopt.f90 kinplt.f90 kinred.f90 kinsel.f90 list.f90 loadin.f90 loadout.f90 LOCAL.F90 local3.f90 m12bar.f90 m2flux.f90 m3flux.f90 match.f90 newnam.f90 OUTP.F90 paclds.f90 pacpro.f90 pacscr.f90 pak.f90 pakenv.f90 parsum.f90 phox.f90 PRCHEM.F90 pricl.f90 prodin.f90 prprod.f90 prpuls.f90 prtprm.f90 przmin.f90 readsp.f90 recall.f90 reduct.f90 sedadv.f90 setpsw.f90 SetValue.f90 show.f90 singo2.f90 sintrp.f90 solar.f90 STATION.F90 steady.f90 stfint.f90 store.f90 sumup.f90 sunlys.f90 tabe.f90 tab_var.f90 transp.f90 trprod.f90 unpak.f90 unpbar.f90 unpenv.f90 unplds.f90 unppro.f90 unpscr.f90 volat.f90 watadv.f90 WEATHERH.F90 writer.f90 zero.f90 announ.f90 audopt.f90 aveout.f90 beer.f90 biolys.f90 chemin.f90 chksub.f90 chmout.f90 ckicm2.f90 ckicm3.f90 ckload.f90 ckpuls.f90 contin.f90 contrl.f90 datack.f90 disper.f90 distrb.f90 DRIVER.F90 drivm1.f90 drivm2.f90 drivm3.f90 endmon.f90 ENDRSKC.F90 ENDRSKR.F90 envin.f90 envout.f90 ex2fgt.f90 exams.f90 fct.f90 fder.f90 firord.f90 flows.f90 flxout.f90 geock.f90 getvar.f90 ghost.f90 grsub0.f90 grsub2.f90 grsub3.f90 HYDLYS.F90 initl.f90 m2ave.f90 m3ave.f90 prenv.f90 READER.F90 runit.f90 step.f90 stiff.f90 taba.f90 tabb.f90 tabc.f90 tabd.f90 adam.f90 admint.f90 

targets : exams.exe
exams.exe : $(f90code) 
	$(FC) $(f95flags) $(DEBUGcf) -o $@ $(f90code) 

#End-of-File Makefile

clean:
	rm -f *.mod exam.exe

