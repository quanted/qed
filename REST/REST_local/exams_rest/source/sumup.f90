subroutine SUMUP
! SUMUP writes a single-page summary of Mode 1 (steady-state) analysis to
! FORTRAN LUN RPTLUN, along with an estimate of the time required for
! significant reduction in chemical contamination of the ecosystem. The latter
! is derived from analysis of the kinetic decay data computed by integration.
! Revised: 21-AUG-1985 (LAB)
! Revisions 10/22/88--run-time implementation of machine dependencies

! Notes 2002-09-11:
! Another useful statistic is the deviation from linear first-order behavior.
! This could perhaps be calculated as the ratio of the mass remaining at a
! given time as given by the dynamic simulation, 
! as a ratio to that expected under first-order conditions.
! This would be a measure of the "tailing" of contaminant
! mass due to non-first-order behavior.
! Because I use a composite end time for the simulation (2 half-lives, but
! weighted according to the dymanics of the several chemicals being simulated)
! it is not entirely obvious how to produce a useful measure of tailing.

use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Implementation_Control
use Global_Variables
use Local_Working_Space
Implicit None
! Local variables for this subroutine
real :: DECTIM, HAFLS, HAFLW, PCTSED, PCTTOT, PCTWAT, TIMEPR, TOTLOD
integer :: ITIME, K2
character(len=78) :: OUTLIN
character(len=2)  :: KOUT !  character representation of number of chemical
character(len=7), dimension(4) :: PRTIME =&
   (/' hours.','  days.','months.',' years.'/)
logical :: Print_it
! Summarize results of run:
Chemicals: do K2 = 1, KCHEM ! Write one page for each chemical
   ! Load character string for transmitting K to table headers:
   write (KOUT,fmt='(I2)') K2
   if (KOUT(1:1) == ' ') KOUT(1:1) = '0'
   write (RPTLUN,5010) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(K2))
   write (RPTLUN,5030) ! dashed line
   ! Table title:
   write (RPTLUN,fmt='(A)')&
      ' Table 20.'//KOUT//'.  Exposure analysis summary.'
   write (RPTLUN,5030) ! dashed line
   ! Compute initial mass distribution:
   ! Allow for entry of some compounds with zeros
   if (QTSAV(K2) .GreaterThan. 0.0) then
      PCTWAT = 100.0*QWSAV(K2)/QTSAV(K2)
      PCTSED = 100.0*QSSAV(K2)/QTSAV(K2)
   else
      PCTWAT = 0.0
      PCTSED = 0.0
   endif
   ! Report summary:
   write (RPTLUN,fmt='(A/A,1PG10.3,A,G10.3,A,2(/A,G10.3,A))')&
   ' Exposure (maximum steady-state concentrations):',&
   '  Water column:',DOMAX(2,K2),' mg/L dissolved; total =',DOMAX(1,K2),' mg/L',&
   '  Benthic sediments:',DOMAX(7,K2),' mg/L dissolved in pore water;',&
   '    maximum total concentration =',DOMAX(6,K2),' mg/kg (dry weight).'
   
   write (OUTLIN,fmt='(A,1PG9.2,A,G9.2)')&
   '  Biota (ug/g dry weight): Plankton:',DOMAX(4,K2),' Benthos:',DOMAX(9,K2)
   if (DOMAX(4,K2) .Equals. 0.0) OUTLIN(37:45) = '         '
   if (DOMAX(9,K2) .Equals. 0.0) OUTLIN(55:63) = '         '
   write (RPTLUN,fmt='(A)') trim(OUTLIN)
   write (RPTLUN,fmt='(/A/A,1PG10.3,A,0PF7.2,A/A,F6.2,A)') &
      ' Fate:',&
      '  Total steady-state accumulation:',QTSAV(K2),' kg, with',PCTWAT,'%',&
      '    in the water column and ',PCTSED,'% in the benthic sediments.'
   TOTLOD = SYSLDL(K2)+TRANLD(K2)
   write (RPTLUN,fmt='(A,1PG9.2,A,0PF7.2,A)')&
      '  Total chemical load:',TOTLOD,' kg/'//PRTIME(KDTIME)(1:5)//&
      '.  Disposition:',CHEMPC(K2),'%'
   write (RPTLUN,fmt='(A,F7.2,A,F7.2,A/A,F7.2,A)')&
'    chemically transformed,',BIOPCT(K2),'% biotransformed,',VOLPCT(K2),'%',&
'    volatilized, and',EXPPCT(K2),'% exported via other pathways.'
   ! Estimate persistence from results of decay simulation...however,
   if (abs(IFLAG) >= 8) return ! skip this if the integrator failed
   HAFLW = 0.0
   HAFLS = 0.0
   ! If simulation badly overruns true halflives, final masses
   ! may underflow to zero or even be slightly negative. Hence:
   if (Z(5,K2) .LessThanOrEqual. 0.0) then
      Z(5,K2) = tiny(Z(5,K2))
      Print_it = .false.
   elseif (Z(6,K2) .LessThanOrEqual. 0.0)then
      Z(6,K2) = tiny(Z(6,K2))
      Print_it = .false.
   else
      Print_it = .true.
   end if
   ! Daughter products may not show a reduction in concentration because
   ! the time frame is based on the parant compound. If this is the case,
   ! skip computation of "half-life" and printing of outcome
   if (Z(5,K2) .GreaterThanOrEqual. QWSAV(K2)) then
      Z(5,K2) = QWSAV(K2)
      Print_it = .false.
   elseif (Z(6,K2) .GreaterThanOrEqual. QSSAV(K2)) then
      Z(6,K2) = QSSAV(K2)
      Print_it = .false.
   else ! compute halflifes from system simulation results
      HAFLW = 0.69315/(TFACTR*(-alog(Z(5,K2)/QWSAV(K2)))/TENDL)
      HAFLS = 0.69315/(TFACTR*(-alog(Z(6,K2)/QSSAV(K2)))/TENDL)
   end if

   ! Convert endpoint on decay simulation to report units
   TIMEPR = TENDL/TFACTR
   write (RPTLUN,fmt='(/A/A,1PG10.3,A)')&
      '  Persistence:',&
      '   After',TIMEPR,' '//PRTIME(KDTIME)(1:6)//&
      ' of recovery time, the water column had'
   ! Time to remove ca. 95% of steady-state resident chemical:
   ! estimated as weighted average of first-order approximations of
   ! overall water column and bottom sediment half-lives.
   DECTIM = 5.0*((PCTWAT/100.0)*HAFLW+(PCTSED/100.0)*HAFLS)
   ! Allow for some compounds with zeros
   ! and for run of single water compartment:
   PCTWAT = 0.0
   PCTSED = 0.0
   PCTTOT = 0.0
   ! Compute percent lost by end of decay simulation
   if (QWSAV(K2).NotEqual.0.0) PCTWAT=100.*(1.-(Z(5,K2)/QWSAV(K2)))
   if (QSSAV(K2).NotEqual.0.0) PCTSED=100.*(1.-(Z(6,K2)/QSSAV(K2)))
   if (QTSAV(K2).NotEqual.0.0) PCTTOT=100.*(1.-((Z(5,K2)+Z(6,K2))/QTSAV(K2)))
   write (RPTLUN,fmt='(A,F7.2,A/A,F7.2,A,F6.1,A)')&
    '   lost',PCTWAT,'% of its initial chemical burden; the benthic zone',&
    '   had lost',PCTSED,'%; system-wide total loss of chemical =',PCTTOT,'%.'
   Printing: if (Print_it) then
      ITIME = KDTIME ! Adjust report units for easier reading
      ! For times up to 96 hours,  report in  hours
      ! For times up to 90 days,   report in  days
      ! For times up to 96 months, report in  months
      ! For times longer than 96 months, report in years
      Output_format: select case (ITIME)
         case (1) Output_format       ! currently operating in hours
            select case (int(DECTIM)) ! alter output format only if >96 hours
               case (97:2160)             ! <= 90 days, so
                  DECTIM=DECTIM / 24.0    ! convert from hours to days
                  ITIME = 2               ! now operate in days
               case (2161:70128)          ! <= 96 months, so
                  DECTIM = DECTIM / 730.5 ! convert from hours to months
                  ITIME = 3               ! now operate in months
               case (70129:)                ! > 96 months, so
                  DECTIM = DECTIM / 8766.0  ! convert from hours to years
                  ITIME = 4                 ! now operate in years
            end select
         case (2) Output_format        ! currently operating in days
            select case (int(DECTIM))  ! alter output format only if > 90 days
               case (91:2922)                ! <= 96 months, so
                  DECTIM = DECTIM / 30.4375  ! convert from days to months
                  ITIME = 3                  ! now operate in months
               case (2923:)                  ! > 96 months, so
                  DECTIM = DECTIM / 365.25   ! convert from days to years
                  ITIME = 4                  ! now operate in years
            end select
         case (3) Output_format       ! currently operating in months
            select case (int(DECTIM)) ! alter output format only if >96 months
               case (97:)                 ! > 96 months, so
                  DECTIM = DECTIM / 12.0  ! convert from months to years
                  ITIME = 4               ! now operate in years
            end select
         case (4) Output_format ! already operating in years
      end select Output_format
      write (RPTLUN,fmt='(A,F7.0,A)')&
         '   Five half-lives (>95% cleanup) thus require ca.',&
         DECTIM,' '//PRTIME(ITIME)
   end if Printing
end do Chemicals
return
5010 format ('1','Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2,/,' Ecosystem: ',A)
5030 format (1X,77('-')) ! dashed line
end Subroutine SUMUP
