.SUFFIXES: .exe .o .mod .f90 .f95 .f .f9x .res .rc .rcx
FC = gfortran
XREF = -g # -info
# Debug: Compile and link flags
DEBUGcf = -chk -g -pca -stchk -trace -w -winconsole

# OPTIMIZE: Compile and link flags
OPTIMIZEcf = -nap -nchk -ndal -ng -o1 -npca -ntrace -nsav -nstchk -nw

SRC_Path =
ModuleList = .


# [production options]
ldflags = $(XREF)
f95flags = $(XREF)

# Rules:
.f9x.f90 :
	$(FC) $(f95flags)  $@ $<
.f90.o :
	$(FC) $(f95flags) -c $< -o $*.o

# pfam_pi.exe
f90code = NonInputVariables.F90 \
 					Variables.F90 \
 					allocations.F90 \
 					CoreCalculations.F90 \
					degradation.f90 \
					omega_mass_xfer.f90 \
					solute_holding_capacity.f90 \
					utilities_module.F90 \
					flood_control.F90 \
					mass_inputs.f90 \
					metfileprocessing.f90 \
					outputprocessing.F90 \
					plantgrowth.F90 \
					ChemicalTransformation.f90 \
					PrimarySubroutine.F90 \
					PFAMFortran.f90					
 					

target : pfam_pi.exe
pfam_pi.exe : $(f90code)
	$(FC) $(ldflags) -fbacktrace -o $@ $(f90code)

### Dependencies for .f files:


#End-of-File Makefile

clean:
	rm -f *.o *.mod pfam_pi.exe
