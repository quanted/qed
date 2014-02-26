subroutine REDUCT(K2)   ! Computes reduction transformation kinetics
! First composed 15 June 1983 by L.A. Burns
! Revised 12 July 1983 (LAB) for mode 3 operations.
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
real :: KREDL, TKEL ! Local variables
integer :: I,II,J,K,KK
integer, intent (in) :: K2
Segments: do J = 1, KOUNT        ! Segment loop
   II = -3                       ! Initialize counter to map onto ALPHA matrix
   TKEL = TCELG(J,NDAT)+273.15   ! Compute Kelvin temperature
   Ions: do K = 1, 7             ! Ionic species loop
      II = II+1                  ! Increment ALPHA map
      if (SPFLGG(K,K2) == 0) cycle Ions
      Forms: do I = 1, 3         ! Loop on dissolved, sorbed, etc. forms
         KK = 3*K+II+I-1
         KREDL = KREDG(I,K,K2)   ! Load the input value of the rate constants
         if (EREDG(I,K,K2) .NotEqual. 0.0) &
            ! and adjust for environmental temperature
            KREDL = 10.**(KREDG(I,K,K2)-(EREDG(I,K,K2)/(R_Factor*TKEL)))
         ! Add current contribution to total rate constant:
         REDKL(J,K2) = REDKL(J,K2)+ALPHA(KK,J,K2)*KREDL*REDAGG(J,NDAT)
      end do Forms               ! End of forms loop
   end do Ions                   ! End of ionic species loop
end do Segments                  ! End of segment loop
end Subroutine REDUCT
