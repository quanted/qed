subroutine CKLOAD
! Subroutine CKLOAD accumulates the total loadings to system elements, checks
! to ensure that none of the loadings (via rainfall, interflow, point (stream)
! or non-point sources) give aqueous concentrations (after accounting for
! partitioning in the input flows) greater than (1) full solubility in
! rainfall and groundwater (interflow), or, (2) for stream and NPS flow, >50%
! of the aqueous solubility of the neutral moiety. For materials that are
! solids at the ambient temperature, a crytal energy correction term is
! introduced (March 1999). The temperature and pH of the system element
! loaded by the flow are used for these calculations. This prevents violation
! of the assumption of linear sorption isotherms and prevents loadings
! of solid chemical particles.
use Implementation_Control
! Created August 1979 by L.A. Burns
! Revised 03-MAY-1985 (LAB) -- Fortran77 character processing
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revisions 01/21/99--better advice to user
! Revisions Feb-08-1999 -- full use of floating point comparisons
! Revisions Mar-1999 -- crystal energy correction term
! Revised 2005-03-16 to suggest Freundlich isotherm if linear is problematic
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Floating_Point_Comparisons
Implicit None
! Local variables
real :: BETA(7), CHECK(7), DISFUN(14), SATTST, SUMFUN, TESTLD,&
   TKEL, TMPLOD, TOTCON, HPLUS, HPLSQ, HPLCUB, HYDRX, HYDSQ, HYDCUB, &
   LiquidCrystalEnergy
integer :: I, IPRFLG, J, K2, NLOAD
character(len=4) :: NMON
! NMON is the 4-character abbreviation of a month (from NAMONG)
! BETA are fractions of total concentration present in the 7 dissolved species
! DISFUN are elements of the distribution functions
! CHECK is for checking that loads do not exceed solubility limits
! Flag to suppress multiple printings of ion solubility warning
IPRFLG = 0
! Set control on the chemical load sector to be evaluated
NLOAD = NDAT
if (PRSWG == 0 .and. MODEG < 3) NLOAD = 13
NMON = NAMONG(NLOAD) ! Set name of month
Segments_solubility: do J = 1, KOUNT   ! Compute solubilities
   TKEL = 273.15+TCELG(J,NDAT)
   Chemicals_solubility: do K2 = 1, KCHEM ! Compute for KCHEM active compounds
      ! Compute solubility of the 7 species in this compartment
      Species_solubility: do I = 1, 7
         YSATL(I,J,K2) = 0.0
         ! Increment loop if species I does not occur:
         if (SPFLGG(I,K2) == 0) cycle Species_solubility
         YSATL(I,J,K2) = SOLG(I,K2) ! Acquire solubility
         ! Check for temperature function
         Temperature_function: if (ESOLG(I,K2) .GreaterThan. 0.0) then
            ! Solubility data loaded as temperature function -- Check for
            ! inconsistent input data: temperature function lacking MWTG -
            Data_check: if (MWTG(K2) .LessThanOrEqual. 0.0) then
               ! Improper input data
               IFLAG = 8
               write (stderr,fmt='(5(/A))')&
               ' The chemical input data contains an inconsistency that',&
               ' must be remedied before a RUN can be completed:',&
               ' The molar solubility of '//trim(CHEMNA(K2)),&
               ' is given as a function of temperature, but its molecular',&
               ' weight is not specified in the chemical data base.'
               return
            end if Data_check
            YSATL(I,J,K2) = (10.**(SOLG(I,K2)- &! Adjust for local temperature
               (ESOLG(I,K2)/(R_Factor*TKEL))))*MWTG(K2)*1000.
            ! Temperature function yields molar solubility, YSATL multiplied
            ! by gram molecular weight and 1000 mg/g to convert to mg/liter.
         end if Temperature_function

         ! Estimate ion solubility as 5000.* neutral species solubility if
         ! user neglected to load a value
         if (I == 1 .or. &
            (YSATL(I,J,K2).GreaterThan.0.0)) cycle Species_solubility
         YSATL(I,J,K2) = 5000.*YSATL(1,J,K2) ! user neglected to load a value
         if (IPRFLG == 0) then
            write (stdout,fmt='(/A/A)')&
               ' Solubility of ionic species estimated from the neutral',&
               ' molecule as ion solubility is not given in the input data.'
            IPRFLG = 1
         end if
      end do Species_solubility
   end do Chemicals_solubility
end do Segments_solubility

! Evaluate validity of loads and estimate maximum values for those that
! exceed isotherm linearity limits - the procedure uses the temperature
! and pH of the target compartment.
Chemicals: do K2 = 1, KCHEM
Segments: do J = 1, KOUNT
! Increment loop if this segment receives no loadings on this day:
TOTLDL(J,K2) = STRLDG(J,K2,NLOAD)+NPSLDG(J,K2,NLOAD)+PCPLDG(J,K2,NLOAD)+ &
   DRFLDG(J,K2,NLOAD)+SEELDG(J,K2,NLOAD)
if (.not. (TOTLDL(J,K2) .GreaterThan. 0.0)) cycle Segments
do I = 1, 7
   CHECK(I) = YSATL(I,J,K2) ! Compute test values for solubility checks
end do
HPLUS = 10.**(-PHG(J,NDAT)) ! Compute H+ and OH- for partitioning computations
HYDRX = 10.**(-POHG(J,NDAT))
HPLSQ = HPLUS*HPLUS
HYDSQ = HYDRX*HYDRX
HPLCUB = HPLUS*HPLSQ
HYDCUB = HYDRX*HYDSQ

DISFUN(1) = 1.0               ! Compute first 7 distribution factors
DISFUN(2) = KB1L(J,K2)/HYDRX
DISFUN(3) = KB1L(J,K2)*KB2L(J,K2)/HYDSQ
DISFUN(4) = KB1L(J,K2)*KB2L(J,K2)*KB3L(J,K2)/HYDCUB
DISFUN(5) = KA1L(J,K2)/HPLUS
DISFUN(6) = KA1L(J,K2)*KA2L(J,K2)/HPLSQ
DISFUN(7) = KA1L(J,K2)*KA2L(J,K2)*KA3L(J,K2)/HPLCUB
!
! Take loading types one by one: first, rainfall or interflow
Rain_or_Seeps: if ( (SEELDG(J,K2,NLOAD) .GreaterThan. 0.0) .or. &
                    (PCPLDG(J,K2,NLOAD) .GreaterThan. 0.0)) then
! Calculate distribution coefficients for interflow and rainfall
SUMFUN = sum(DISFUN(1:7))
BETA(1:7) = DISFUN(1:7)/SUMFUN
! 1. Interflow load: water flow only.
Seepage_load: if (SEELDG(J,K2,NLOAD) .GreaterThan. 0.0) then
                                       ! there is a proposed load
   Seepage: if (SEEPSL(J) .GreaterThan. 0.0) then
      ! there is interflow to carry the load, so
      ! Compute total concentration (mg/L) in interflow:
      TOTCON = 1.0E+06*SEELDG(J,K2,NLOAD)/SEEPSL(J)
      do I = 1, 7 ! Take chemical species in order
         ! Increment species loop if species does not occur:
         if (SPFLGG(I,K2) == 0) cycle
         ! Compute actual concentration of species:
         SATTST = BETA(I)*TOTCON
         if (SATTST .LessThanOrEqual. CHECK(I)) cycle
         ! Solubility limit exceeded - calculate maximum load and notify user
         TMPLOD = 1.0E-06*CHECK(I)*SEEPSL(J)/BETA(I)
         write (stderr,fmt='(A/A,I4,A)')&
         ' '//NMON//' interflow loading of '//trim(CHEMNA(K2)),&
         ' at segment',J,' exceeds its solubility.'//&
         ' The Exams run was cancelled.'
         if (SEELDG(J,K2,NLOAD) .GreaterThan. TMPLOD) then
             SEELDG(J,K2,NLOAD) = TMPLOD
            write (stderr,fmt='(A,es8.1,A)')&
            ' This load cannot exceed',TMPLOD,' kg/hr.'
         end if
         call TheMessage(1)
         IFLAG=10
         return
      end do
   else Seepage ! No groundwater flow enters this compartment
      SEELDG(J,K2,NLOAD) = 0.0
      write (stderr,fmt='(A,I4,A/A)')&
      ' '//NMON//' interflow load entered for segment',J,', which does not',&
      ' receive interflow. The load was removed and the simulation cancelled.'
      IFLAG=8
      return
   end if Seepage
end if Seepage_load

! 2. Rainfall loadings: water flow only
Rain_load: if (PCPLDG(J,K2,NLOAD) .GreaterThan. 0.0) then ! a load is proposed
   Rain: if (RAINFL(J) .GreaterThan. 0.0) then ! it is raining
      ! Compute total concentration in rainfall:
      TOTCON = 1.0E+06*PCPLDG(J,K2,NLOAD)/RAINFL(J)
      do I = 1, 7
         if (SPFLGG(I,K2) == 0) cycle
         ! Actual concentration
         SATTST = BETA(I)*TOTCON
         if (SATTST .LessThanOrEqual. CHECK(I)) cycle
         ! Solubility limit exceeded - calculate maximum load and notify user
         TMPLOD = CHECK(I)*RAINFL(J)/(1.0E+06*BETA(I))
         write (stderr,fmt='(A/A,I4,A)')&
         ' '//NMON//' rainfall loading of '//trim(CHEMNA(K2)),&
         ' at segment',J,' exceeds its solubility.'//&
         ' The Exams run was cancelled.'
         if (PCPLDG(J,K2,NLOAD) .GreaterThan. TMPLOD) then
             PCPLDG(J,K2,NLOAD) = TMPLOD
            write (stderr,fmt='(A,es8.1,A)')&
            ' This load cannot exceed',TMPLOD,' kg/hr.'
         end if
         call TheMessage(1)
         IFLAG=10
         return
      end do
   else Rain ! No rainfall:
      PCPLDG(J,K2,NLOAD) = 0.0
      write (stderr,fmt='(A,I4,A/A)')&
      ' '//NMON//' rainfall loading entered for segment',J,', which gets no',&
      ' rain. The load was removed and the simulation cancelled.'
      IFLAG=8
      return
   end if Rain
end if Rain_load
end if Rain_or_Seeps

! Stream and NPS loadings
Land_flows: if ( (STRLDG(J,K2,NLOAD) .GreaterThan. 0.0) .or. &
                 (NPSLDG(J,K2,NLOAD) .GreaterThan. 0.0)      &
               )  then
do I = 1, 7
   CHECK(I) = 0.50*YSATL(I,J,K2) ! Compute test values for isotherm tests
end do
! Add crystal energy correction for neutral molecule
! for chemicals that are solids at the ambient temperature.
! See: Karickhoff, S.W. 1984. Organic pollutant sorption in aquatic
! systems. Journal of Hydraulic Engineering 110:707-735; eq. 12 on p. 712.
! The factor of 6.5 was arrived at from the range of solute entropy of fusions
! of some 12-15 eu, divided by the gas constant R (1.98 cal/deg mol).
if (MPG(K2) .GreaterThan. TCELG(J,NDAT)) then
   LiquidCrystalEnergy = 6.5*(MPG(K2)-TCELG(J,NDAT))/(TCELG(J,NDAT)+273.15)
   CHECK(1)=0.50*YSATL(1,J,K2)*exp(LiquidCrystalEnergy)
end if

! 3. Stream loads
Stream_loads: if (STRLDG(J,K2,NLOAD) .GreaterThan. 0.0) then
   Stream_flow: if (STRMFL(J) .GreaterThan. 0.0) then ! if the stream flows
      TOTCON = 1.0E+06*STRLDG(J,K2,NLOAD)/STRMFL(J) ! Total concentration
      ! Compute distribution factors for stream
      DISFUN(8) =  KPSL(1,J,K2)*STSCOL(J)
      DISFUN(9) =  DISFUN(2)*KPSL(2,J,K2)*STSCOL(J)
      DISFUN(10) = DISFUN(3)*KPSL(3,J,K2)*STSCOL(J)
      DISFUN(11) = DISFUN(4)*KPSL(4,J,K2)*STSCOL(J)
      DISFUN(12) = DISFUN(5)*KPSL(5,J,K2)*STSCOL(J)
      DISFUN(13) = DISFUN(6)*KPSL(6,J,K2)*STSCOL(J)
      DISFUN(14) = DISFUN(7)*KPSL(7,J,K2)*STSCOL(J)
      ! Calculate distribution coefficients
      SUMFUN = sum(DISFUN)
      BETA(1:7) = DISFUN(1:7)/SUMFUN
      do I = 1, 7
         if (Freundlich(K2)) exit
         if (SPFLGG(I,K2)==0) cycle
         SATTST = BETA(I)*TOTCON
         if (SATTST .LessThanOrEqual. CHECK(I)) cycle
         TMPLOD = CHECK(I)*STRMFL(J)/(1.0E+06*BETA(I))
         write (stderr,fmt='(A/A,I4,A)')&
         ' '//NMON//' stream loading of '//trim(CHEMNA(K2)),&
         ' at segment',J,' violates isotherm linearity.'//&
         ' Consider using a Freundlich isotherm.'
         if (STRLDG(J,K2,NLOAD) .GreaterThan. TMPLOD) then
            write (WarnLun,fmt='(A,es8.1,A)')&
            ' This load should not exceed',TMPLOD,' kg/hr.'
         end if
         call TheMessage(2)
      end do
   else Stream_flow ! no flow in the stream
      STRLDG(J,K2,NLOAD) = 0.0
      write (stderr,fmt='(A,I4,A/A)')&
      ' '//NMON//' streamflow loading entered for segment',J,', which',&
      ' receives no stream flow. The load was removed'//&
      ' and the simulation cancelled.'
      IFLAG=8
      return
   end if Stream_flow
end if Stream_loads

! 4. Non-point-source loads
NPS_load: if (NPSLDG(J,K2,NLOAD) .GreaterThan. 0.0) then
   NPS_flow: if (NPSFL(J) .GreaterThan. 0.0) then
      TOTCON = 1.0E+06*NPSLDG(J,K2,NLOAD)/NPSFL(J)
      ! Calculate distribution coefficients:
      DISFUN(8) = KPSL(1,J,K2)*NPSCOL(J)
      DISFUN(9) = DISFUN(2)*KPSL(2,J,K2)*NPSCOL(J)
      DISFUN(10) = DISFUN(3)*KPSL(3,J,K2)*NPSCOL(J)
      DISFUN(11) = DISFUN(4)*KPSL(4,J,K2)*NPSCOL(J)
      DISFUN(12) = DISFUN(5)*KPSL(5,J,K2)*NPSCOL(J)
      DISFUN(13) = DISFUN(6)*KPSL(6,J,K2)*NPSCOL(J)
      DISFUN(14) = DISFUN(7)*KPSL(7,J,K2)*NPSCOL(J)
      SUMFUN = sum(DISFUN)
      BETA(1:7) = DISFUN(1:7)/SUMFUN
      do I = 1, 7
         if (Freundlich(K2)) exit
         if (SPFLGG(I,K2) == 0) cycle
         SATTST = BETA(I)*TOTCON
         if (SATTST .LessThanOrEqual. CHECK(I)) cycle
         TMPLOD = CHECK(I)*NPSFL(J)/(1.0E+06*BETA(I))
         write (WarnLun,fmt='(A/A,I0,A)')&
         ' '//NMON//' non-point-source loading of '//trim(CHEMNA(K2)),&
         ' at segment ',J,' violates isotherm linearity.'//&
         ' Consider using a Freundlich isotherm.'
         if (NPSLDG(J,K2,NLOAD) .GreaterThan. TMPLOD) then
            write (WarnLun,fmt='(A,es8.1,A)')&
            ' This load should not exceed',TMPLOD,' kg/hr.'
         end if
         call TheMessage(2)
      end do
   else NPS_flow ! NPS load, but no flow to carry it
      NPSLDG(J,K2,NLOAD) = 0.0
      write (stderr, fmt='(A,I3/A)')&
      ' '//NMON//' non-point-source loading entered for segment ',J,&
      ' with no non-point-source flow. Load removed and simulation aborted.'
      IFLAG=8
      return
   end if NPS_flow
end if NPS_load
end if Land_flows
end do Segments
end do Chemicals

! Compute total validated segment loads, total allochthonous chemical
! loads on the ecosystem, and update YSATL for crystal energy terms
TESTLD = 0.0
SYSLDL = 0.0
do K2 = 1, KCHEM
   do J = 1, KOUNT
      TOTLDL(J,K2) = SEELDG(J,K2,NLOAD)+STRLDG(J,K2,NLOAD)+ &
         NPSLDG(J,K2,NLOAD)+PCPLDG(J,K2,NLOAD)+DRFLDG(J,K2,NLOAD)
      SYSLDL(K2) = SYSLDL(K2)+TOTLDL(J,K2)
      ! Add crystal energy correction for neutral molecule
      ! for chemicals that are solids at the ambient temperature.
      ! See: Karickhoff, S.W. 1984. Organic pollutant sorption in aquatic
      ! systems. Journal of Hydraulic Engineering 110:707-735.
      if (MPG(K2) .GreaterThan. TCELG(J,NDAT)) then
         LiquidCrystalEnergy = 6.5 *(MPG(K2)-TCELG(J,NDAT)) &
               / (TCELG(J,NDAT)+273.15)
         YSATL(1,J,K2)=YSATL(1,J,K2)*exp(LiquidCrystalEnergy)
      end if
   end do
   TESTLD = TESTLD+SYSLDL(K2)
end do
! If, at this stage, no non-zero allochthonous loads remain,
! there is no point in computing steady-state concentrations:
if (.not.(TESTLD .GreaterThan. 0.0) .and. MODEG==1) then
   IFLAG=8
   write (stderr, fmt='(/A/A)')&
      ' No allochthonous chemical loadings.',&
      ' Steady-state computations cancelled.'
end if
return

Contains

Subroutine TheMessage(Item)
integer, intent(in) :: Item
! Item selects the correct error message
select case (Item)

case (1)
! Unless assume that supersaturated solution or colloidal suspension is O.K.
!  (and subject to transformation processes)
write (stderr,fmt='(2(A/))')&
' Exams contains no provision for loadings that exceed aqueous solubility.',&
' Evaluate the chemical loadings before re-starting the simulation.'

case (2)
write (WarnLun,fmt='(4(A/))')&
' Exams uses linear isotherms for its sorption and partitioning algorithms.',&
' These are valid up to 50% of aqueous solubility in the residual aqueous',&
' phase of any constituent. Exposures may be somewhat underestimated;',&
' consider using a Freundlich isotherm in this analysis.'
end select
end Subroutine TheMessage
end Subroutine CKLOAD
