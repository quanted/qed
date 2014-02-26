subroutine CKICM3(Y,NYR,PFIRST,PLAST)
! This subroutine checks initial conditions to ensure that EXAMS' assumptions
! are not violated. Specifically, the aqueous concentrations should not be
! larger than one-half the solubility of the chemical or 1.E-5 M in the
! neutral species, whichever is less. The routine assumes prior processing of
! the input stream by CKPULS.
! Revised 23/09/83 (LAB) for high precision integrator.
! Revised 03-MAY-1985 (LAB) -- F'77 conversion
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 08-Feb-1999 to make floating point comparisons
! Revised 2005-03-16 to suggest Freundlich isotherm if linear isotherm problem
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Floating_Point_Comparisons
Implicit None
! Y is chemical concentration referred to aqueous phase of system.
real (kind (0D0)) :: Y(KOUNT,KCHEM)
real :: SATST, CHECK, TEMP, YMAX, YOLD
integer :: I, J, K, II, ITST, IPULS1, NYR, PFIRST, PLAST
! NYR is the (mode 3) year being processed in a simulation via DRIVER
! PFIRST is the first pulse to be evaluated for a given date
! PLAST is the last pulse for that date.
! Check for initial conditions that are too high, adjust to
! largest legitimate value:
Pulse_loop: do IPULS1 = PFIRST, PLAST
   K = ICHEMG(IPULS1)
   J = ISEGG(IPULS1)
   II = -3  ! Load counter for locating distribution fractions (ALPHA)
   ITST = 0 ! Reset flag to suppress multiple error message printing
   YOLD = Y(J,K)  ! Store current value of state variable
   Species_loop: do I = 1, 7
      II = II+1 ! Increment counter for ALPHA address
      ! Increment the species loop if the species does not exist:
      if (SPFLGG(I,K) == 0) cycle Species_loop
      ! Compute size of pulse or explicit initial condition
      ! (This computation is inside the chemical species loop so that each
      ! adjusted value is incorporated as the correction is made ...)
        TEMP = 1.0E+06       * IMASSG(IPULS1) / WATVOL(J)
      ! mg/L = 1.0E+06 mg/kg *  kg            / liters
      ! Check for supersaturation (actually 50% of saturation to keep in
      ! range of linear isotherms):
      SATST = ALPHA(3*I+II,J,K)*YOLD
      CHECK = 0.50*YSATL(I,J,K) ! includes crystal energy correction (CKLOAD)
      if ((SATST .GreaterThan. CHECK) .and. (.not.Freundlich(K))) then
      ! Solubility limits exceeded during RUN;
      ! notify user and suggest using Freundlich isotherm
         write (WarnLun,fmt='(A,I4,A/A)')&
            ' During '//NAMONG(NDAT)//' of year ',NYR,&
            ' the concentration of',' '//trim(CHEMNA(K))
         write (WarnLun,fmt='(A,I0/A/A)') " in segment ",J,&
            " reached a level at which EXAMS' underlying assumptions are",&
            " violated. Consider using a Freundlich isotherm."
      end if
      ! Solubility not exceeded; now add in pulse and retest concentration
      SATST = ALPHA(3*I+II,J,K)*(YOLD+TEMP)
      if ((SATST .LessThanOrEqual. CHECK) .or. (Freundlich(K))) cycle Species_loop
      ! Solubility limits exceeded -- notify user and suggest Freundlich.
      if (ITST == 0) write (WarnLun,fmt='(/A,I0,A,I0,A/A/A)') &
      " Pulse number ",IPULS1," in segment ",J," results in concentrations",&
      " that violate Exams' assumption of isotherm linearity.",&
      " Consider using a Freundlich isotherm."
      ITST = 1
      YMAX = CHECK/ALPHA(3*I+II,J,K)
      write (WarnLun,fmt='(A,1pG11.4)')&
         ' The maximum value this pulse should assume is ',&
           (YMAX-YOLD)*WATVOL(J)*1.0E-06
!     to set the pulse to its maximum value, uncomment the next statement
!     IMASSG(IPULS1) = (YMAX-YOLD)*WATVOL(J)*1.0E-06
   end do Species_loop
   Y(J,K) = Y(J,K)+1.0D+06*IMASSG(IPULS1)/WATVOL(J) ! Add final value of IMASS
end do Pulse_loop
return
end Subroutine CKICM3
