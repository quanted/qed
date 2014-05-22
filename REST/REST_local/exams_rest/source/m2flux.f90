subroutine M2FLUX(Y)
! M2FLUX analyzes and reports a snap-shot of the fate of the chemical. The
! information reported for each process includes the mass flux (kg/time)
! attributable to the process, the percentage of load consumed in the process,
! and a projected decay half-life that would result from each process acting
! in isolation. The processes are also summed by category (chemical,...)
! Created 27 April 1984 by L.A. Burns.
! Revised 04-MAY-1985 (LAB) -- Conversion to F77
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 8/5/91 -- altered output format
use Floating_Point_Comparisons ! Revisions 09-Feb-1999
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
Implicit None
real (kind (0D0)) :: Y(KOUNT,KCHEM)
! Local variables for this subroutine:
real :: BIO, CHE, GNDOUT, HAFLS, HAFLT, HAFLW, PERCET,&
   SOCBIO(2), SOCCHE, SOCDP, SOCHYD, SOCOUT, SOCOX,&
   SOCPHO, SOCSOX, SOCVOL, TOTBIO, SOCRED, TOTFLX, VOL
real :: SURWAT, TEMP, PCTWAT, PCTSED
real, dimension(4) :: TLOCAL = (/1.0,24.0,730.5,8766.0/)
integer :: I, J, K2
logical :: ACTION
character(len=2) :: KOUT ! character representation of chemical number
character(len=7), dimension(4) :: NAMTIM = &    ! NAMTIM is tag for time units
   (/'hours. ','  days.','months.','years. '/)  ! (hour, day, month, or year)
Chemicals: do K2 = 1, KCHEM
! Load character string for transmitting K to table headers:
write (KOUT,fmt='(I2)') K2
if (KOUT(1:1) == ' ') KOUT(1:1) = '0'
! Write page header:
write(RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
write(RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(K2))
write(RPTLUN,5020) ! dashed line
I = int(TENDG)
write (RPTLUN,fmt='(A,I0,1X,A)') ' Table 18.'//KOUT//&
   '.  Sensitivity analysis: after ',I,NAMTIM(TCODEG)
write (RPTLUN,5020) ! dashed line
write (RPTLUN,fmt='(A)')&
   '     Current Value           Mass Flux    % of Total  Half-Life*'
! Analysis of mass fluxes: Calculate mass export rates
! (factor of 1.0E-06 converts mg/hr to kg/hr):
SOCOUT = 0.0
GNDOUT = 0.0
SURWAT = 0.0
do J = 1, KOUNT
   TEMP = 1.0E-06*abs(Y(J,K2))*EXPOKL(J,K2)
   SOCOUT = SOCOUT+TEMP
   if (TYPEG(J) == 'B' .and. TYPEG(J-1) == 'B') then
      GNDOUT = GNDOUT+TEMP
   else
      SURWAT = SURWAT+TEMP
   end if
end do
! Compute volatilization and transformations of chemical,
! accumulate total mass fluxes for ecosystem.
! Initialize mass fluxes: all as kg/hr
SOCVOL    = 0.0   ! Volatilization, kg/hr
SOCCHE    = 0.0   ! Chemical transformation, kg/hr
SOCHYD    = 0.0   ! Hydrolysis
SOCOX     = 0.0   ! Oxidation
SOCDP     = 0.0   ! Direct photolysis
SOCSOX    = 0.0   ! Singlet oxygen photooxidation
SOCBIO(1) = 0.0   ! Biolysis in water column
SOCBIO(2) = 0.0   ! Biolysis in bottom sediments
SOCRED    = 0.0   ! Reductive transformations
Segments: do J = 1, KOUNT        ! Compute process rates for segments
   ! Volatilization: only from epilimnion - mg/L/hr
   VOL = VOLKL(J,K2)*Y(J,K2)
   SOCVOL = SOCVOL+1.0E-06*VOL*WATVOL(J)  ! kg/hr total volatilization
   ! Hydrolysis: 3 limb (acid, base, neutral) process, occurs in all segments.
   CHE = HYDRKL(J,K2)*Y(J,K2)
   SOCCHE = SOCCHE+CHE*WATVOL(J)          ! mg/hr
   SOCHYD = SOCHYD+1.0E-06*CHE*WATVOL(J)  ! kg/hr
   CHE = OXIDKL(J,K2)*Y(J,K2)             ! Oxidation: (mg/L/hr)
   SOCCHE = SOCCHE+CHE*WATVOL(J)          ! mg/hr
   SOCOX = SOCOX+1.0E-06*CHE*WATVOL(J)    ! kg/hr
   CHE = PHOTKL(J,K2)*Y(J,K2)             ! Direct photolysis
   SOCCHE = SOCCHE+CHE*WATVOL(J)          ! mg/hr
   SOCDP = SOCDP+1.0E-06*CHE*WATVOL(J)    ! kg/hr
   CHE = S1O2KL(J,K2)*Y(J,K2)             ! Singlet oxygen photooxidation
   SOCCHE = SOCCHE+CHE*WATVOL(J)          ! mg/hr
   SOCSOX = SOCSOX+1.E-06*CHE*WATVOL(J)   ! kg/hr
   CHE = REDKL(J,K2)*Y(J,K2)              ! Reductive transformations
   SOCCHE = SOCCHE+CHE*WATVOL(J)          ! mg/hr
   SOCRED = SOCRED+1.0E-06*CHE*WATVOL(J)  ! kg/hr
   ! Microbial transformation: depend on aqueous concentration and 
   ! population levels of bacteria
   if (TYPEG(J) == 'B') then              ! Bottom sediments
      BIO = Y(J,K2)*BIOLKL(J,K2)
      SOCBIO(2) = SOCBIO(2)+1.E-06*BIO*WATVOL(J)
   else                                   ! Water column
      BIO = Y(J,K2)*BIOLKL(J,K2)
      SOCBIO(1) = SOCBIO(1)+1.0E-06*BIO*WATVOL(J)
   endif
end do Segments ! End of transformation loop

SOCCHE = SOCCHE*1.0E-06  ! Convert mg/hr to kg/hr
TOTFLX = SOCOUT+SOCVOL+SOCBIO(1)+SOCBIO(2)+SOCCHE ! Compute total flux
! Compute total system-level half-life in hours, allowing for zero entries
if (TOTFLX .NotEqual. 0.0) then              ! if the compound is active,
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/TOTFLX  ! compute the actual halflife
else                                         ! if the compound is not active
   HAFLT = 0.0                               ! Set a nominal half-life of zero
end if

! Complete table heading based on time frame to be used
write (RPTLUN,fmt='(A)') '      by Process              Kg/'//&
   NAMTIM(TCODEG)(1:5)//'       Flux       '//NAMTIM(TCODEG)(1:6)
write (RPTLUN,fmt="(4X,15('-'),10X,10('-'),3X,10('-'),2X,10('-'))")
! Convert mass fluxes and load to kg/(appropriate time unit);
! if working in hours, simply go on:
TFACTR = TLOCAL(TCODEG)
if (TCODEG > 1) then ! Convert mass fluxes by time factor
   SOCHYD = SOCHYD*TFACTR
   SOCOX = SOCOX*TFACTR
   SOCDP = SOCDP*TFACTR
   SOCSOX = SOCSOX*TFACTR
   SOCBIO(1) = SOCBIO(1)*TFACTR
   SOCBIO(2) = SOCBIO(2)*TFACTR
   SOCRED = SOCRED*TFACTR
   SOCVOL = SOCVOL*TFACTR
   SOCOUT = SOCOUT*TFACTR
   SOCCHE = SOCCHE*TFACTR
   GNDOUT = GNDOUT*TFACTR
   SURWAT = SURWAT*TFACTR
   TOTFLX = TOTFLX*TFACTR
end if
! If necessary, enter dummy value of TOTFLX (i.e., allow for entry
! of some chemicals with zero loads or zero baseline for plotting)
if (TOTFLX .GreaterThan. 0.0) then
   ACTION = .true.
else
   TOTFLX = 1.0     ! alias TOTFLX to simplify code,
   ACTION = .false. ! but signal that outcomes should not be printed
endif

! Write out process mass fluxes
! Chemical transformations
if (SOCHYD .GreaterThan. 0.0) then ! report hydrolysis
   PERCET = 100.*SOCHYD/TOTFLX
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCHYD
   write (RPTLUN,fmt='(A,17X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Hydrolysis',SOCHYD,PERCET,HAFLT
else
   write (RPTLUN,fmt='(A)') ' Hydrolysis'
endif

if (SOCRED .GreaterThan. 0.0) then  ! Reductive transformation
   PERCET = 100.*SOCRED/TOTFLX
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCRED
   write (RPTLUN,fmt='(A,18X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Reduction',SOCRED,PERCET,HAFLT
else
   write (RPTLUN,fmt='(A)') ' Reduction'
endif

if (SOCOX .GreaterThan. 0.0) then ! Radical oxidation
   PERCET = 100.*SOCOX/TOTFLX
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCOX
   write (RPTLUN,fmt='(A,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Radical oxidation          ',SOCOX,PERCET,HAFLT
else
   write (RPTLUN,fmt='(A)') ' Radical oxidation'
endif

SOCPHO = SOCDP ! Direct photolysis
! SOCPHO is also available for summing all photochemical processes
if (SOCPHO .GreaterThan. 0.0) then
   PERCET = 100.0*SOCPHO/TOTFLX
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCPHO
   write (RPTLUN,fmt='(A,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Direct photolysis          ',SOCPHO,PERCET,HAFLT
else
   write (RPTLUN,fmt='(A)') ' Direct photolysis'
endif

if (SOCSOX .GreaterThan. 0.0) then ! report singlet oxygen photooxidation
   PERCET = 100.*SOCSOX/TOTFLX
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCSOX
   write (RPTLUN,fmt='(A,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Singlet oxygen oxidation   ',SOCSOX,PERCET,HAFLT
else
   write (RPTLUN,fmt='(A)') ' Singlet oxygen oxidation'
endif

CHEMPC(K2) = 100.0*SOCCHE/TOTFLX  ! Total chemical transformations
if (SOCCHE .GreaterThan. 0.0) then ! report the numbers
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCCHE
   write (RPTLUN,fmt='(A,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      '   All Chemical Processes   ',SOCCHE,CHEMPC(K2),HAFLT
else
   write (RPTLUN,fmt='(A)') '   All Chemical Processes'
endif

! Microbial transformations
if (SOCBIO(1) .GreaterThan. 0.0) then ! report water column
   PERCET = 100.0*SOCBIO(1)/TOTFLX
   HAFLW = 0.69315*(Z(5,K2)+Z(6,K2))/SOCBIO(1)
   write (RPTLUN,fmt='(A,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Bacterioplankton           ',SOCBIO(1),PERCET,HAFLW
else
   write (RPTLUN,fmt='(A)') ' Bacterioplankton'
endif

if (SOCBIO(2) .GreaterThan. 0.0) then ! report bottom sediments
   PERCET = 100.*SOCBIO(2)/TOTFLX
   HAFLS = 0.69315*(Z(5,K2)+Z(6,K2))/SOCBIO(2)
   write (RPTLUN,fmt='(A,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Benthic Bacteria           ',SOCBIO(2),PERCET,HAFLS
else
   write (RPTLUN,fmt='(A)') ' Benthic Bacteria'
endif

! Under the first-order assumptions used in this analysis,
! the derivatives can be summed and related to total mass, so
TOTBIO = SOCBIO(1)+SOCBIO(2) ! Total microbial transformation
BIOPCT(K2) = 100.0*TOTBIO/TOTFLX
if (TOTBIO .GreaterThan. 0.0) then
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/TOTBIO
   write (RPTLUN,fmt='(A,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      '   Total Biolysis           ',TOTBIO,BIOPCT(K2),HAFLT
else
   write (RPTLUN,fmt='(A)') '   Total Biolysis'
endif

EXPPCT(K2) = 100.*SOCOUT/TOTFLX      ! Water-borne export
if (SURWAT .GreaterThan. 0.0) then   ! Report surface water export flux
   PERCET = 100.0*SURWAT/TOTFLX
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SURWAT
   write (RPTLUN,fmt='(A,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Surface Water-borne Export ',SURWAT,PERCET,HAFLT
else
   write (RPTLUN,fmt='(A)') ' Surface Water-borne Export'
endif

if (GNDOUT .GreaterThan. 0.0) then ! Report groundwater export
   PERCET = 100.*GNDOUT/TOTFLX
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/GNDOUT
   write (RPTLUN,fmt='(A,1PG11.4,A,0PF6.2,A,1PG11.4)')&
      ' Seepage export             ',GNDOUT,'    ',PERCET,'    ',HAFLT
else
   write (RPTLUN,fmt='(A)') ' Seepage export'
endif

VOLPCT(K2) = 100.0*SOCVOL/TOTFLX   ! Volatilization
if (SOCVOL .GreaterThan. 0.0) then
   HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCVOL
   write (RPTLUN,fmt='(A,1PG11.4,A,0PF6.2,A,1PG11.4)')&
      ' Volatilization             ',SOCVOL,'    ',VOLPCT(K2),'    ',HAFLT
else
   write (RPTLUN,fmt='(A)') ' Volatilization'
endif

! Loss by all processes combined:
write (RPTLUN,fmt='(A)') & ! table formatting
   '                             =========='
if (ACTION) then
   write (RPTLUN,fmt='(A,1PG11.4)')&
      ' Total mass flux:           ',TOTFLX
else
   write (RPTLUN,fmt='(A)') ' Total mass flux:'
endif
write (RPTLUN,5020) ! dashed line
write (RPTLUN,fmt='(A/A)')&
   ' * Pseudo-first-order estimates based on flux/resident mass;',&
   '   assumes transport delays will not throttle fluxes.'
! Completion of flux analysis.
! The next sector writes a single-page summary of Mode 2 post-
! simulation analysis to FORTRAN LUN RPTLUN.
! Write one page for each chemical:
write(RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(K2))
write (RPTLUN,5020) ! dashed line
! Table title:
I = int(TENDG)
write (RPTLUN,fmt='(A,I0,A)') ' Table 20.'//KOUT//&
   '.  Exposure analysis at the elapse of ',I,' '//NAMTIM(TCODEG)
write (RPTLUN,5020) ! dashed line
! Compute initial mass distribution
QTSAV(K2) = Z(5,K2)+Z(6,K2)
QWSAV(K2) = Z(5,K2)
QSSAV(K2) = Z(6,K2)
if (abs(QTSAV(K2)) .GreaterThan. 0.0) then
   PCTWAT = 100.0*QWSAV(K2)/QTSAV(K2)
   PCTSED = 100.0*QSSAV(K2)/QTSAV(K2)
else    ! Allow for presence of some compounds with zeros
   PCTWAT = 0.0
   PCTSED = 0.0
end if
write (RPTLUN,fmt='(A/A/A)')&  ! Report summary
   ' Exposure Concentrations:',&
   ' =======================',&
   '        Water Column:'
write (RPTLUN,fmt='(A,1PG10.3)')&
   '          Total (mg/L)  . . . . . . . . . . .  ',DOMAX(1,K2)
write (RPTLUN,fmt='(A,1PG10.3)')&
  '          Dissolved (mg/L)  . . . . . . . . .  ',DOMAX(2,K2)
write (RPTLUN,fmt='(A,1PG10.3)')&
   '          Plankton (ug/g dry) . . . . . . . .  ',DOMAX(4,K2)
write (RPTLUN,fmt='(A/A,1PG10.3)')&
   '        Benthic Sediments:',&
   '          Total (mg/kg dry) . . . . . . . . .  ',DOMAX(6,K2)
write (RPTLUN,fmt='(A,1PG10.3)')&
   '          Dissolved (mg/L pore) . . . . . . .  ',DOMAX(7,K2)
write (RPTLUN,fmt='(A,1PG10.3)')&
   '          Benthos (ug/g dry)  . . . . . . . .  ',DOMAX(9,K2)
! Write summary of fate analysis:
write (RPTLUN,fmt='(/A,1PG10.3,2(/A,0PF7.2,A))')&
   ' Fate:  Current Resident Mass -- kg            ',QTSAV(K2),&
   ' ====      Water Column . . . . . . . . . . . .   ',PCTWAT,' %',&
   '           Benthic Sediments  . . . . . . . . .   ',PCTSED,' %'
if (ACTION) then
   write (RPTLUN,fmt='(A,1PG10.3)')&
      '        Total Flux of Chemical -- kg /'//NAMTIM(TCODEG)(1:5)//&
      '    ',TOTFLX
else
   write (RPTLUN,fmt='(A)')&
      '        Total Flux of Chemical -- kg /'//NAMTIM(TCODEG)(1:5)
endif
write (RPTLUN,fmt='(3(A,F8.2,A/),A,F8.2,A)')&
   '           Chemical Transformations:  . . . . .  ',CHEMPC(K2),' %',&
   '           Biological Transformations:  . . . .  ',BIOPCT(K2),' %',&
   '           Volatilization:  . . . . . . . . . .  ',VOLPCT(K2),' %',&
   '           Water-borne Export:  . . . . . . . .  ',EXPPCT(K2),' %'
end do Chemicals
return
5000 format ('1','Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2,/' Ecosystem: ',A)
5020 format (1X,77('-'))
end Subroutine M2FLUX
