subroutine PHOX(K2,LIGHTL)
! Computes photochemical oxidation other than singlet oxygen
! Revised 12 July 1983 (LAB) for mode 3 operations.
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
real, dimension(KOUNT) :: LIGHTL
real :: KOXL, TKEL
integer :: I, II, J, K, K2, KK
Segment_loop: do J = 1, KOUNT
  if (TYPEG(J) == 'B') cycle Segment_loop ! i.e., no photochemical oxidation
  OXRADL(J)= OXRADG(NDAT)*LIGHTL(J)! Compute segment value of oxidant radicals
  II = -3  ! Initialize counter to map onto ALPHA matrix
  TKEL = TCELG(J,NDAT)+273.15  ! Compute Kelvin temperature
  Ionic_species_loop: do K = 1, 7
    II = II+1 ! Increment ALPHA map
    if (SPFLGG(K,K2) == 0) cycle Ionic_species_loop
    Forms_loop: do I = 1, 3  ! Loop on dissolved, sorbed, etc. forms
      KK = 3*K+II+I-1
      KOXL = KOXG(I,K,K2)  ! Photochemical oxidation
      if (EOXG(I,K,K2) .NotEqual. 0.0)&
          KOXL = 10.**(KOXG(I,K,K2)-(EOXG(I,K,K2)/(R_Factor*TKEL)))
      ! Add current contribution to total rate constant:
      OXIDKL(J,K2) = OXIDKL(J,K2)+ALPHA(KK,J,K2)*KOXL*OXRADL(J)
    end do Forms_loop
  end do Ionic_species_loop
end do Segment_loop
return
end Subroutine PHOX
