subroutine HYDLYS(K2) ! Computes hydrolytic transformation kinetics
! Revised 12 July 1983 (LAB) for mode 3 operations.
! Revised 2004-06-30 (LAB) for more efficient Arrhenius calculation
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
real :: KAHL, KNHL, KBHL ! KAH, KNH, KBH are hydrolysis rate constants
real :: HPLUS, HYDRX, TKEL
! HPLUS is hydronium ion, HYDRX is hydroxide ion, TKEL temperature in Kelvins
integer :: I, II, J, K, KK ! loop counters
integer, intent (in) :: K2
Segments: do J = 1, KOUNT      ! Loop on segments
  II = -3 ! Initialize counter to map onto ALPHA matrix
  HPLUS = 10.**(-PHG(J,NDAT))  ! Compute acid/base concentrations
  HYDRX = 10.**(-POHG(J,NDAT))
  TKEL = TCELG(J,NDAT)+273.15  ! Compute Kelvin temperature
  Ions: do K = 1, 7            ! Loop on ionic species
    II = II+1 ! Increment ALPHA map
    if (SPFLGG(K,K2) == 0) cycle Ions
    Forms: do I = 1, 3         ! Loop on dissolved, sediment-sorbed, and
      KK = 3*K+II+I-1          ! DOC-complexed forms
      ! ********************************************
      ! Specific acid, base, and neutral hydrolyses:
      ! ********************************************
      ! Load the global (input) value of the rate constants
      ! Acid hydrolysis
      if (EAHG(I,K,K2) .NotEqual. 0.0) then ! adjust for temperature
         KAHL = 10.**(KAHG(I,K,K2)-(EAHG(I,K,K2)/(R_Factor*TKEL)))
      else
         KAHL = KAHG(I,K,K2)  
      end if
      ! Neutral hydrolysis
      if (ENHG(I,K,K2) .NotEqual. 0.0) then ! adjust for temperature
         KNHL = 10.**(KNHG(I,K,K2)-(ENHG(I,K,K2)/(R_Factor*TKEL)))
      else
         KNHL = KNHG(I,K,K2) 
      end if
      ! Alkaline hydrolysis
      if (EBHG(I,K,K2) .NotEqual. 0.0) then ! adjust for temperature
         KBHL = 10.**(KBHG(I,K,K2)-(EBHG(I,K,K2)/(R_Factor*TKEL)))
      else
         KBHL = KBHG(I,K,K2) 
      end if

      ! Add current contribution to total rate constant:
      HYDRKL(J,K2) = HYDRKL(J,K2)+ALPHA(KK,J,K2)*(KAHL*HPLUS+KNHL+KBHL*HYDRX)
    end do Forms
  end do Ions
end do Segments
end Subroutine HYDLYS
