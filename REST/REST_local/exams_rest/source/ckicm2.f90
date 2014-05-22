subroutine CKICM2(Y)
! Mode 2 initial condition checker -- 9 September 1983 (L.A. Burns)
! This subroutine checks initial conditions to ensure that EXAMS' assumptions
! are not violated. Specifically, the aqueous concentrations should not be
! larger than one-half the solubility of the chemical in the neutral species,
! unless a Freundlich isotherm is in play.
! The operation of the routine is predicated on pre-processing of the input
! stream to remove bad values of ISEGG, ICHEMG, and IMASSG.
! Revised 27 April 1984 (LAB) -- debug.
! Revisions 10/22/88--run-time implementation of machine dependencies
use Implementation_Control
! Revised 02-Feb-1999 for floating point comparisons
! Revised 24-Mar-1999 to use Liquid Crystal Energy corrector.
! Revised 2005-03-16 for Freundlich isotherms
use Floating_Point_Comparisons
use Global_Variables
use Local_Working_Space
use Internal_Parameters
Implicit None
! Y is chemical concentration referred to aqueous phase of system.
real (kind (0D0)) :: Y(KOUNT,KCHEM), DTEMP
real, dimension(4) :: TLOCAL = (/ 1.0, 24.0, 730.5, 8766.0/)
! TLOCAL is number of hours in an hour, day, month, and year.
! Local variables:
real :: CHECK, TEMP, YMAX, YOLD, SATST, TIME1, TIME2, TOTALT
integer :: I, J, K, II, ITST, IPULS1
! Run-time word for error message
character(len=6),dimension(4) :: FIXUP=(/'hours ','days  ','months','years '/)
IFLAG = 1   ! Reset error checking flag
! Skip to timer section if no pulses
if (NPULSE > 0) then ! Check for initial conditions that are too high
do IPULS1 = 1, MAXMAS
   ! End loop when all values processed:
   if (ICHEMG(IPULS1) == 0) exit
   ! (CKPULS has already ordered the values and entered zeros at the
   ! endpoint). Transfer pointers to local values:
   K = ICHEMG(IPULS1)
   J = ISEGG(IPULS1)
   II = -3        ! Load counter for locating distribution fractions (ALPHA)
   ITST = 0       ! Reset flag to suppress multiple error message printing
   YOLD = Y(J,K)  ! Store current value of state variable
   Species_loop: do I = 1, 7 ! Take chemical species in order
      II = II+1 ! Increment counter for ALPHA address
      ! Increment the species loop if the species does not exist:
      if (SPFLGG(I,K) == 0) cycle Species_loop
      ! Compute size of pulse or explicit initial condition
      ! (This computation is inside the chemical species loop so that each
      ! adjusted value is incorporated as the correction is made...)
        TEMP = 1.0E+06       * IMASSG(IPULS1) / WATVOL(J)
      ! mg/L = 1.0E+06 mg/kg *  kg            / liters
      SATST = ALPHA(3*I+II,J,K)*YOLD
      ! Impose super-cooled liquid solubility limitation on maximum
      ! concentration of residual neutral molecule in order to keep
      ! within linear range of sorption isotherms. The check is 50%
      ! of the aqueous solubility, with a crystal energy term (see CKLOAD)
      ! added for chemicals that are solids at the ambient temperature.
      ! See: Karickhoff, S.W. 1984. Organic pollutant sorption in aquatic
      ! systems. Journal of Hydraulic Engineering 110:707-735.
      CHECK = 0.50*YSATL(I,J,K)
      if ((SATST .GreaterThan. CHECK) .and. (.not.Freundlich(K))) then
                      ! Solubility limits exceeded during RUN; warn user
         write (WarnLun,fmt='(A/A,I0,A/A)')& 
            " Concentration of "//trim(CHEMNA(K))," in segment ",J,&
            " reached a level at which EXAMS' isotherm linearity assumptions",&
            " are violated. Consider using a Freundlich isotherm."
      end if
      ! Solubility not exceeded at end of run; add in pulse and
      SATST = ALPHA(3*I+II,J,K)*(YOLD+TEMP) ! retest concentration
      if ((SATST .LessThanOrEqual. CHECK) .or. (Freundlich(K))) cycle Species_loop
      ! Solubility limits exceeded -- warn user
      if (ITST == 0) write (stderr,fmt='(/A,I0,A,I0,A/A/A)') &
      " Pulse number ",IPULS1," in segment ",J," results in concentrations",&
      " that violate Exams' assumption of isotherm linearity.",&
      " Consider using a Freundlich isotherm."
      ITST = 1
      YMAX = CHECK/ALPHA(3*I+II,J,K)
      write (WarnLun,fmt='(A,1pG11.4)')&
         ' The maximum value this pulse should assume is ',&
           (YMAX-YOLD)*WATVOL(J)*1.0E-06
!     Uncomment the next statement to reset this pulse to its maximum value.
!     IMASSG(IPULS1) = (YMAX-YOLD)*WATVOL(J)*1.0E-06
   end do Species_loop
   ! Add on final adjusted value of IMASS:
   DTEMP = 1.0D+06*IMASSG(IPULS1)/WATVOL(J)
   Y(J,K) = Y(J,K)+DTEMP
end do; end if
! Evaluate time-frame requested by user
! Step 1: check validity of time frame:
if (TCODEG < 1 .or. TCODEG > 4) then ! Improper time frame
   write (stdout,fmt='(/A,I3/A)')&
      ' Faulty timer data: TCODE is ',TCODEG,&
      '     RUN cancelled.'
   IFLAG = 8
   return
end if
! Step 2: check for negative values on timer controls
if ( (TENDG  .LessThan. 0.0) .or. &
     (TINITG .LessThan. 0.0) .or. &
     (CINTG  .LessThan. 0.0)      &
   ) then                     ! Negative or
write (stdout,fmt='(A/A/A)')& ! inappropriate zero on timer controls
   ' Timer controls include a bad value:',&
   ' make sure neither TINIT nor CINT is negative,',&
   ' and that TEND is greater than zero. RUN cancelled.'
   IFLAG = 8
   return
end if
TFACTR = TLOCAL(TCODEG) ! Convert timer data to hours for integrator
KDTIME = TCODEG ! Transfer input to integrator control variable
! Multiply by 1.00D+00 to load upper bytes of timer data with zeros
! Compute initial time (T) and final time (TENDL) in hours
T = TINITG*TFACTR*1.0D+00
TENDL = TENDG*TFACTR*1.0D+00
TINCRL = CINTG*TFACTR*1.0D+00 ! Convert CINTG to hours
TOTALT = TENDL-T ! Compute length of simulation (TOTAL T) in hours
if (TOTALT .LessThanOrEqual. 0.0) then
   ! Negative or zero simulation times are improper,
   ! although strictly speaking the integrators can be operated in this way.
   TOTALT = TOTALT/TFACTR  ! Still, why allow the user to feel foolish...
   write (stdout,fmt='(A,1PG11.4,A/A)')&
      ' A simulation period of ',TOTALT,FIXUP(TCODEG),&
      ' is inappropriate. RUN cancelled.'
   IFLAG = 8
   return
end if
! At least one hour between output points is required:
if ((TINCRL.GreaterThan.0.0).and.(TINCRL.LessThan.1.0D+00)) TINCRL = 1.0D+00
if (.not. (TINCRL .GreaterThanOrEqual. 1.0D+00)) then
   ! TINCR set to zero indicates that EXAMS is
   ! to adjust to give 12 equal-increment output points.
   ! Re-evaluate user inputs, reset if necessary:
   ! 1. Time less than 12 days: report in hours --
   if (TOTALT .LessThanOrEqual. 288.0) then; KDTIME = 1
   ! 2. Time more than 12 days but less than 1 yr -- report in days
   elseif (TOTALT .LessThanOrEqual. 8766.0) then; KDTIME = 2
   ! 3. Time more than one year but < 12 years -- report in months
   elseif (TOTALT .LessThanOrEqual. 105192.0) then; KDTIME = 3
   ! 4. More than 12 years: report in years
   else; KDTIME = 4
   end if
   ! Recompute adjustment factor for report times:
   TFACTR = TLOCAL(KDTIME)
   ! Convert time frame to appropriate integers
   TIME1 = TOTALT/12.0/TFACTR
   TIME2 = float(int(TIME1))
   if ((TIME1-TIME2) .GreaterThanOrEqual. 0.5) TIME2 = TIME2+1.0
   TINCRL = TFACTR*TIME2*1.00D+00
   if (TINCRL .LessThan. 1.0) TINCRL = 1.0D+00
     ! TINCR restricted to at least one hour
   ! Place TINIT (initial time) on next smaller integer valued time
   DTEMP = TFACTR*1.00D+00
   T = DTEMP*float(int(T/DTEMP))
   TENDL = T+TINCRL*12.0D+00
   CINTG = TINCRL/TFACTR ! set CINTG for next iteration
end if
return
end Subroutine CKICM2
