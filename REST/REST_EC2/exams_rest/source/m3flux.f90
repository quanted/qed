subroutine M3FLUX
! M3FLUX analyzes and reports the average "fate" of the chemicals. The
! information reported for each process includes: the average mass flux
! (kg/time) attributable to the process, the percentage of total attributable
! to the process, and a projected half-life resulting from each process acting
! in isolation. The processes are also summed by category (chemical,
! biological, transport).
! Created 07 December 1983 (L.A. Burns) from procedure FLXOUT
! Revised 27-DEC-85 (LAB)
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 05/08/1991 -- altered output format
! Revisions 2002-04-15 to report user-specified event durations
! Revisions 2003-03-31 to report annual absolute maxima in ecorisk files
! Revisions 2004-04-06 to optionally omit writing report.xms entries
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Statistical_Variables
Implicit None
! Local variables for this subroutine
real :: PCTSED, PCTWAT
real :: GNDOUT,HAFLS,HAFLT,HAFLW,PERCET,SOCBIO(2),SOCCHE,SOCDP,SOCHYD,SOCOUT,&
SOCOX,SOCPHO,SOCSOX, SOCVOL, SURWAT, TOTBIO, SOCRED, TOTFLX, TFIN
integer :: I, K, UE
! UE to count User Event numbers
character(len=2) :: KOUT
! KOUT reflects the number of the chemical in its output tables.
character(len=4), dimension(2) :: YRCH
! YRCH are character strings for entering simulation years
! (e.g., 0001, 1984, etc.) in table headers.
character(len=6),dimension(4) :: ITIME=(/' hours','  days','months',' years'/)
! ITIME is tag for time units (hour, ...).
logical :: MULTYR, ACTION
! MULTYR indicates multi-year (.T.) or single-year (.F.) data.
! ACTION is true when the chemical has a non-zero flux
real, dimension(4) :: TLOCAL = (/1.0,24.0,730.5,8766.0/)


Report_File: if (RPTFIL) then
! Convert simulation years to character strings for output
MULTYR = (LASTYR > FRSTYR)
! Load character string for transmitting year to table headers
write (YRCH(1),fmt='(I4)') FRSTYR
if (MULTYR) then
   write (YRCH(2),fmt='(I4)') LASTYR
   do K = 1, 2
      do I = 1, 4
         if (YRCH(K)(I:I) == ' ') YRCH(K)(I:I) = '0'
      end do
   end do
else
   do I = 1, 4
      if (YRCH(1)(I:I) == ' ') YRCH(1)(I:I) = '0'
   end do
endif
Chemicals: do K = 1, KCHEM
! Load character string for transmitting K to table headers
write (KOUT,fmt='(I2)') K
if (KOUT(1:1) == ' ') KOUT(1:1) = '0'
! Write page header
write (RPTLUN,5020) VERSN,MODEG,trim(ECONAM)
write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(K))
write (RPTLUN,5045) ! dashed line
if (MULTYR) then
   write (RPTLUN,fmt='(A)') ' Table 18.'//KOUT//&
      '.  Sensitivity analysis of chemical fate: '//YRCH(1)//'-'//YRCH(2)//'.'
else
   write (RPTLUN,fmt='(A)') ' Table 18.'//KOUT//&
      '.  Sensitivity analysis of chemical fate: '//YRCH(1)//'.'
end if
! Set up headers for mass flux table
write (RPTLUN,5045) ! dashed line
write (RPTLUN,fmt='(A)')&
   '    Mean Values by           Mass Flux    % of Total  Half-Life*'
! Analysis of average mass fluxes
! Calculate mass export rates (Factor of 1.0E-06 converts mg/hr to kg/hr)
SOCOUT = 1.E-06*YEXPO(K)/FLUXCT
GNDOUT = 1.E-06*YGWAT(K)/FLUXCT
SURWAT = SOCOUT-GNDOUT
! Compute volatilization and transformations of chemical,
! accumulate total mass fluxes for ecosystem--all as kg/hr
SOCVOL = 1.0E-06*YVOLK(K)/FLUXCT    ! kg/hr total volatilization
SOCHYD = 1.0E-06*YHYDR(K)/FLUXCT    ! Hydrolysis--kg/hr
SOCOX = 1.0E-06*YOXID(K)/FLUXCT     ! Oxidation--kg/hr
SOCDP = 1.0E-06*YPHOT(K)/FLUXCT     ! Direct photolysis--kg/hr
SOCSOX = 1.E-06*YS1O2(K)/FLUXCT     ! Singlet oxygen photooxidation--kg/hr
SOCRED = 1.0E-06*YRED(K)/FLUXCT     ! Reductive transformations
SOCBIO(1) = 1.0E-06*YBIOW(K)/FLUXCT ! Microbial transformation--Water column
SOCBIO(2) = 1.0E-06*YBIOS(K)/FLUXCT ! Bottom sediments
SOCCHE = SOCHYD+SOCOX+SOCDP+SOCSOX+SOCRED ! Total chemical transformations
TOTFLX = SOCOUT+SOCVOL+SOCBIO(1)+SOCBIO(2)+SOCCHE ! Compute total flux

! Estimate total system-level half-life in hours
if (TOTFLX .GreaterThan. 0.0) then        ! If the compound is active,
   HAFLT = 0.69315*(Z(5,K)+Z(6,K))/TOTFLX ! compute the actual halflife
   ACTION = .true.                        ! and activate the print stream
else                    ! Allow for entry of some compounds with zeros by
   HAFLT = 168.0        ! aliasing HAFLT to allow reporting units to be set,
   ACTION = .false.     ! signaling that TOTFLX should not be printed,
   TOTFLX = 1.0         ! and loading dummy value of TOTFLX for divides
end if

TFIN = 2.0*HAFLT
! Determine appropriate temporal unit for reporting results
if (TFIN  .LessThanOrEqual.  288.0) then
   KDTIME = 1   ! Time < 12 days, so report in hours
elseif ((TFIN .GreaterThan. 288.0) .and. (TFIN .LessThanOrEqual. 8766.0)) then
   KDTIME = 2   ! Time > 12 days but < 1 year, so report in days
elseif ((TFIN .GreaterThan. 8766.0).and.(TFIN.LessThanOrEqual.105192.0)) then
   KDTIME = 3   ! 1yr < time < 12 years, so report in months
else
   KDTIME = 4   ! More than 12 years, so report in years
end if

TFACTR = TLOCAL(KDTIME) ! Compute adjustment factor for report times
! Complete table heading based on time frame to be used
write (RPTLUN,fmt='(A)') '        Process              Kg/'//&
   ITIME(KDTIME)(1:5)//'        Flux      '//ITIME(KDTIME)
write (RPTLUN,fmt="(3X,16('-'),10X,10('-'),3X,10('-'),2X,10('-'))")
! Convert mass fluxes to kg/(appropriate time unit)
! If working in hours, simply go on
if (KDTIME > 1) then       ! Convert mass fluxes by time factor
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
   TOTFLX = TOTFLX*TFACTR
   SURWAT = SURWAT*TFACTR
end if
! Write out process mass fluxes

if (SOCHYD .GreaterThan. 0.0) then ! report hydrolysis
   PERCET = 100.0*SOCHYD/TOTFLX
   HAFLT = 0.69315*(Z(5,K)+Z(6,K))/SOCHYD
   write (RPTLUN,fmt='(A,17X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Hydrolysis',SOCHYD,PERCET,HAFLT
else
   write (RPTLUN,fmt='(A)') ' Hydrolysis'
endif

if (SOCRED .GreaterThan. 0.0) then ! report reductive transformation
   PERCET = 100.0*SOCRED/TOTFLX
   HAFLT = 0.69315*(Z(5,K)+Z(6,K))/SOCRED
   write (RPTLUN,fmt='(A,18X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Reduction',SOCRED,PERCET,HAFLT
else
   write (RPTLUN,fmt='(A)') ' Reduction'
endif

if (SOCOX .GreaterThan. 0.0) then ! report radical oxidation
   PERCET = 100.0*SOCOX/TOTFLX
   HAFLT = 0.69315*(Z(5,K)+Z(6,K))/SOCOX
   write (RPTLUN,fmt='(A,10X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Radical oxidation',SOCOX,PERCET,HAFLT
else
write (RPTLUN,fmt='(A)') ' Radical oxidation'
endif

SOCPHO = SOCDP ! Direct photolysis
! SOCPHO is also available for summing all photochemical processes
if (SOCPHO .GreaterThan. 0.0) then ! report direct photolysis
   PERCET = 100.0*SOCPHO/TOTFLX
   HAFLT = 0.69315*(Z(5,K)+Z(6,K))/SOCPHO
   write (RPTLUN,fmt='(A,10X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Direct photolysis',SOCPHO,PERCET,HAFLT
else
write (RPTLUN,fmt='(A)') ' Direct photolysis'
endif

if (SOCSOX .GreaterThan. 0.0) then  ! report singlet oxygen photooxidation
PERCET = 100.0*SOCSOX/TOTFLX
HAFLT = 0.69315*(Z(5,K)+Z(6,K))/SOCSOX
write (RPTLUN,fmt='(A,3X,1PG11.4,4X,0PF6.2,4X,1PG11.4)') &
      ' Singlet oxygen oxidation',SOCSOX,PERCET,HAFLT
else ! No singlet oxygen photooxidation
   write (RPTLUN,fmt='(A)') ' Singlet oxygen oxidation'
endif

CHEMPC(K) = 100.0*SOCCHE/TOTFLX ! Total chemical transformations
if (SOCCHE .GreaterThan. 0.0) then
   HAFLT = 0.69315*(Z(5,K)+Z(6,K))/SOCCHE
   write (RPTLUN,fmt='(A,3X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      '   All Chemical Processes',SOCCHE,CHEMPC(K),HAFLT
else
   write (RPTLUN,fmt='(A)') '   All Chemical Processes'
endif

if (SOCBIO(1) .GreaterThan. 0.0) then  ! report microbial transformations
   PERCET = 100.0*SOCBIO(1)/TOTFLX     ! in the water column
   HAFLW = 0.69315*(Z(5,K)+Z(6,K))/SOCBIO(1)
   write (RPTLUN,fmt='(A,11X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Bacterioplankton',SOCBIO(1),PERCET,HAFLW
else
   write (RPTLUN,fmt='(A)') ' Bacterioplankton'
endif

if (ACTION) then
   PERCET = 100.0*SOCBIO(2)/TOTFLX
else           ! Allow for entry of some compounds with zeros
   PERCET = 0.0
end if

if (SOCBIO(2) .GreaterThan. 0.0) then ! report biolysis in bottom sediments
   HAFLS = 0.69315*(Z(5,K)+Z(6,K))/SOCBIO(2)
   write (RPTLUN,fmt='(A,11X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Benthic Bacteria',SOCBIO(2),PERCET,HAFLS
else
   write (RPTLUN,fmt='(A)') ' Benthic Bacteria'
endif

! Under the first-order assumptions used in this report,
! the derivatives can be summed and related to total mass.
TOTBIO = SOCBIO(1)+SOCBIO(2)  ! Total microbial transformation
BIOPCT(K) = 100.0*TOTBIO/TOTFLX
if (TOTBIO .GreaterThan. 0.0) then
   HAFLT = 0.69315*(Z(5,K)+Z(6,K))/TOTBIO
   write (RPTLUN,fmt='(A,11X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      '   Total Biolysis',TOTBIO,BIOPCT(K),HAFLT
else              ! No biological transformations
   write (RPTLUN,fmt='(A)') '   Total Biolysis'
endif

EXPPCT(K) = 100.0*SOCOUT/TOTFLX  ! Water-borne export
if (SURWAT .GreaterThan. 0.0) then  ! Report surface water export flux
   PERCET = 100.0*SURWAT/TOTFLX
   HAFLT = 0.69315*(Z(5,K)+Z(6,K))/SURWAT
   write (RPTLUN,fmt='(A,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Surface Water-borne Export ',SURWAT,PERCET,HAFLT
else
   write (RPTLUN,fmt='(A)') ' Surface Water-borne Export'
endif

if (GNDOUT .GreaterThan. 0.0) then ! Report groundwater export
PERCET = 100.0*GNDOUT/TOTFLX
   HAFLT = 0.69315*(Z(5,K)+Z(6,K))/GNDOUT
   write (RPTLUN,fmt='(A,13X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Seepage export',GNDOUT,PERCET,HAFLT
else
   write (RPTLUN,fmt='(A)') ' Seepage export'
endif

VOLPCT(K) = 100.0*SOCVOL/TOTFLX  ! Volatilization
if (SOCVOL .GreaterThan. 0.0) then
   HAFLT = 0.69315*(Z(5,K)+Z(6,K))/SOCVOL
   write (RPTLUN,fmt='(A,13X,1PG11.4,4X,0PF6.2,4X,1PG11.4)')&
      ' Volatilization',SOCVOL,VOLPCT(K),HAFLT
else
   write (RPTLUN,fmt='(A)') ' Volatilization'
endif

if (ACTION) then   ! write loss by all processes combined
   write (RPTLUN,fmt="(29X,10('=')/A,11X,1PG11.4)")&
      ' Total mass flux:',TOTFLX
else
   write (RPTLUN,fmt="(29X,10('=')/A)") ' Total mass flux:'
endif
write (RPTLUN,5045) ! dashed line
write (RPTLUN,fmt='(A/A)')&
   ' * Pseudo-first-order estimates based on flux/resident mass;',&
   '   assumes transport delays will not throttle fluxes.'
! Completion of flux analysis; now report distribution in system
QTSAV(K) = Z(5,K)+Z(6,K) ! Compute mass distribution
QWSAV(K) = 0.0
QSSAV(K) = 0.0
PCTWAT = 0.0
PCTSED = 0.0
if (QTSAV(K) .GreaterThan. 0.0) then ! Compute and report summary mass distrib
   QWSAV(K) = Z(5,K)
   QSSAV(K) = Z(6,K)
   PCTWAT = 100.0*QWSAV(K)/QTSAV(K)
   PCTSED = 100.0*QSSAV(K)/QTSAV(K)
   write (RPTLUN,fmt='(A,1PG10.3,2(/A,0PF7.2,A))')&
      '        Average Resident Mass -- kg            ',QTSAV(K),&
      '           Water Column . . . . . . . . . . . .   ',PCTWAT,' %',&
      '           Benthic Sediments  . . . . . . . . .   ',PCTSED,' %'
else ! print empty entries
   write (RPTLUN,fmt='(/A/A/A)')&
      '        Average Resident Mass -- kg            ',&
      '           Water Column . . . . . . . . . . . .   ',&
      '           Benthic Sediments  . . . . . . . . .   '
end if

! The following sector writes a single-page summary of Mode 3
! post-simulation ecotoxicological analysis to Fortran LUN RPTLUN.
! In the report summaries:
! for the variables YMINaaa, YBARaaa, and PEAKaaa, the first index
! of the System variables (YMINSys et al.) hold the index of the
! system event duration (see Statvar.f90, module Statistical_Variables)
! For example, YMINSys(2,n,n) is the second system event, which is the
! 4-day (96-hour) event duration.
! xxxxLT is long-term--entire RUN period.
! elements  (n,1,K)  hold total concentration mg/L in water column
! elements  (n,2,K)  hold dissolved in water column
! elements  (n,3,K)  hold sediment-sorbed as mg/kg of dry solids
! elements  (n,4,K)  hold plankton-sorbed as ug/g of dry weight
! elements  (n,5,K)  hold pollutant mass in grams/square meter

! elements  (n,6,K)  hold total concentration mg/kg in benthic zone
! elements  (n,7,K)  hold dissolved in pore water
! elements  (n,8,K)  hold sediment-sorbed as mg/kg of dry solids
! elements  (n,9,K)  hold benthos-sorbed as mg/kg of dry weight biomass
! elements  (n,10,K) hold pollutant mass in grams/square meter


! Summarize results of run; write one page for each chemical
!*****************************************************************************
! System event report
write (RPTLUN,5020)VERSN,MODEG,trim(ECONAM)
write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(K))
!write (RPTLUN,5045) ! dashed line
if (MULTYR) then        ! Table title
   write (RPTLUN,fmt='(A)') ' Table 20.'//KOUT//&
    '.  Exposure analysis summary: Maximum Events of '//&
    YRCH(1)//'--'//YRCH(2)//'.'
   write (RPTLUN,5045) ! dashed line
   write (RPTLUN,fmt="(A/A)")& ! system event durations are hard-wired here
    ' Event Duration           96-hour    21-day     60-day'//&
    '     90-day    '//YRCH(1)//'-'//YRCH(2),&
    ' ==============----====  ---------  ---------  ---------'//&
    '  ---------  ---------'
else
   write (RPTLUN,fmt='(A)') ' Table 20.'//KOUT//&
    '.  Exposure analysis summary: Maximum Events of '//&
    YRCH(1)//'.'
   write (RPTLUN,5045) ! dashed line
   write (RPTLUN,fmt="(A/A)")&
    ' Event Duration           96-hour    21-day     60-day'//&
    '     90-day      '//YRCH(1),&
    ' ==============----====  ---------  ---------  ---------'//&
    '  ---------  ---------'
endif

write (RPTLUN,fmt='(9X,A)')&
   ' ***** Ecotoxicological Direct Exposure Concentrations ******'
! bioavailable (true dissolved) mg/L in water column
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Water Column      Min. ', (YMINSys(UE,2,K), UE=2,5), YMINLT(2,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  dissolved mg/L   Mean ', (YBARSys(UE,2,K), UE=2,5), YBARLT(2,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '                   Peak ', (PEAKSys(UE,2,K), UE=2,5), PEAKLT(2,K)
! bioavailable--dissolved mg/L of pore water in benthic zone
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Benthic Sediment  Min. ', (YMINSys(UE,7,K), UE=2,5), YMINLT(7,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  mg/L dissolved   Mean ', (YBARSys(UE,7,K), UE=2,5), YBARLT(7,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '    in pore water  Peak ', (PEAKSys(UE,7,K), UE=2,5), PEAKLT(7,K)
write (RPTLUN,fmt='(9X,A)')&
   ' ***** Ecotoxicological Trophic Exposure Concentrations *****'
! biosorbed on plankton
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Water Column      Min. ', (YMINSys(UE,4,K), UE=2,5), YMINLT(4,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  ug/g dry weight  Mean ', (YBARSys(UE,4,K), UE=2,5), YBARLT(4,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '    of plankton    Peak ', (PEAKSys(UE,4,K), UE=2,5), PEAKLT(4,K)
! benthos (ug/g dry)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Benthic Sediment  Min. ', (YMINSys(UE,9,K), UE=2,5), YMINLT(9,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  ug/g dry weight  Mean ', (YBARSys(UE,9,K), UE=2,5), YBARLT(9,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '    of benthos     Peak ', (PEAKSys(UE,9,K), UE=2,5), PEAKLT(9,K)
write (RPTLUN,fmt='(9X,A)')&
   ' ***** Total Media Concentrations ***************************'
! total medium concentration as mg/L in limnetic zone
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Water Column      Min. ', (YMINSys(UE,1,K), UE=2,5), YMINLT(1,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  total mg/L       Mean ', (YBARSys(UE,1,K), UE=2,5), YBARLT(1,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '                   Peak ', (PEAKSys(UE,1,K), UE=2,5), PEAKLT(1,K)
! total medium concentration as mg/kg (dry wt) in benthic zone
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Benthic Sediment  Min. ', (YMINSys(UE,6,K), UE=2,5), YMINLT(6,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  total mg/kg      Mean ', (YBARSys(UE,6,K), UE=2,5), YBARLT(6,K)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '    dry weight     Peak ', (PEAKSys(UE,6,K), UE=2,5), PEAKLT(6,K)
! End system event report
!*****************************************************************************

!*****************************************************************************
! Begin section for user-defined event durations
! The following sector writes the single-page summary of Mode 3
! post-simulation ecotoxicological analysis for user-specified
! event durations. If no user-specified events, the section is skipped
if (NumEvents == 0) cycle Chemicals
! Summarize results of run; write one page for each chemical
write (RPTLUN,5020)VERSN,MODEG,trim(ECONAM)
write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(K))
!write (RPTLUN,5045) ! dashed line
if (MULTYR) then        ! Table title
   write (RPTLUN,fmt='(A)') ' Table 20.'//KOUT//&
    '.  Exposure analysis summary: Maximum Events of '//&
    YRCH(1)//'--'//YRCH(2)//'.'
else
   write (RPTLUN,fmt='(A)') ' Table 20.'//KOUT//&
    '.  Exposure analysis summary: Maximum Events of '//&
    YRCH(1)//'.'
end if
   write (RPTLUN,5045) ! dashed line
   write (RPTLUN,fmt='(A,5(I3,A))')&
    ' Event Duration          ',(EventDL(UE),'-day    ', UE=NumEvents,1,-1)
   write (RPTLUN,fmt='(6A)')&   ! column lines
    ' ==============----====',('  ---------',UE=1,NumEvents)
write (RPTLUN,fmt='(9X,A)')&
   ' ***** Ecotoxicological Direct Exposure Concentrations ******'
! bioavailable (true dissolved) mg/L in water column
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Water Column      Min. ', (YMINUser(UE,2,K),UE=NumEvents,1,-1)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  dissolved mg/L   Mean ', (YBARUser(UE,2,K),UE=NumEvents,1,-1)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '                   Peak ', (PEAKUser(UE,2,K),UE=NumEvents,1,-1)

! bioavailable--dissolved mg/L of pore water in benthic zone
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Benthic Sediment  Min. ', (YMINUser(UE,7,K),UE=NumEvents,1,-1)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  mg/L dissolved   Mean ', (YBARUser(UE,7,K),UE=NumEvents,1,-1)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '    in pore water  Peak ', (PEAKUser(UE,7,K),UE=NumEvents,1,-1)

write (RPTLUN,fmt='(9X,A)')&
   ' ***** Ecotoxicological Trophic Exposure Concentrations *****'
! biosorbed on plankton
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Water Column      Min. ', (YMINUser(UE,4,K),UE=NumEvents,1,-1)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  ug/g dry weight  Mean ', (YBARUser(UE,4,K),UE=NumEvents,1,-1)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '    of plankton    Peak ', (PEAKUser(UE,4,K),UE=NumEvents,1,-1)

! benthos (ug/g dry)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Benthic Sediment  Min. ', (YMINUser(UE,9,K),UE=NumEvents,1,-1)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  ug/g dry weight  Mean ', (YBARUser(UE,9,K),UE=NumEvents,1,-1)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '    of benthos     Peak ', (PEAKUser(UE,9,K),UE=NumEvents,1,-1)

write (RPTLUN,fmt='(9X,A)')&
   ' ***** Total Media Concentrations ***************************'
! total medium concentration as mg/L in limnetic zone
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Water Column      Min. ', (YMINUser(UE,1,K),UE=NumEvents,1,-1)

write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  total mg/L       Mean ', (YBARUser(UE,1,K),UE=NumEvents,1,-1)

write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '                   Peak ', (PEAKUser(UE,1,K),UE=NumEvents,1,-1)

! total medium concentration as mg/kg (dry wt) in benthic zone
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   ' Benthic Sediment  Min. ', (YMINUser(UE,6,K),UE=NumEvents,1,-1)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '  total mg/kg      Mean ', (YBARUser(UE,6,K),UE=NumEvents,1,-1)
write (RPTLUN,fmt='(A,1PG10.3,4(1X,G10.3))')&
   '    dry weight     Peak ', (PEAKUser(UE,6,K),UE=NumEvents,1,-1)
!*****************************************************************************
! End of section for user-defined event durations
end do Chemicals
end if Report_File

! write annual maxima to scratch file for later ordering and output
if (RskFilC) then
   write (TmpLUN1,fmt='(32767(1X,ES9.2,1X,A10))') &
      (PEAKLT(2,K), PeakDetectDate(2,K), &
       PEAKLT(7,K), PeakDetectDate(7,K), &
       (YBARSys(UE,2,K), SysDetectDate(UE,2,K),&
        YBARSys(UE,7,K),  SysDetectDate(UE,7,K), UE=1,size(SysEventDur)),&
       (YBARUser(UE,2,K), UserDetectDate(UE,2,K),&
        YBARUser(UE,7,K), UserDetectDate(UE,7,K), UE=NumEvents,1,-1),&
      K=1,KCHEM)
end if
if (RskFilR) then
   write (TmpLUN2,fmt='(32767(1X,ES9.2,1X,A10))') &
      (PEAKLT(2,K), PeakDetectDate(2,K), &
       PEAKLT(7,K), PeakDetectDate(7,K), &
       (YBARSys(UE,2,K), SysDetectDate(UE,2,K),&
        YBARSys(UE,7,K),  SysDetectDate(UE,7,K), UE=1,size(SysEventDur)),&
      (YBARUser(UE,2,K), UserDetectDate(UE,2,K),&
        YBARUser(UE,7,K), UserDetectDate(UE,7,K), UE=NumEvents,1,-1),&
      K=1,KCHEM)
end if

YearCount=YearCount+1
return

5020 format ('1','Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode ',I0/' Ecosystem: ',A)
5045 format (1X,77('-')) ! dashed line
end subroutine M3FLUX
