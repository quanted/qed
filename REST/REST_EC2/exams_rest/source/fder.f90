subroutine FDER(W)
! Subroutine to load (constant) EXAMS Jacobian for stiff integration routine.
! Revised 23 September 1983 (LAB) for high precision.
! Simplified call structure 22 January 2001
use Global_Variables
use Local_Working_Space
use Internal_Parameters
Implicit None
! Local variables:
integer :: I, IPAR, ISEG1, IST, J, JW, K, KK
real (kind (0D0)), dimension(KEQN,KEQN), intent(out) :: W

W = 0.0  ! Zero Jacobian
IST = 0
Chemicals: do K = 1, KCHEM
   do J = 1, KOUNT
      do I = 1, KOUNT
         W(I+IST,J+IST) = INTINL(J,I,K)
      end do
      JW = J+IST
      W(JW,JW) = -TOTKL(J,K)
   end do
   if (IST /= 0) then
      J = 1
      KK = K-1
      do IPAR = 1, KK
         I = IST+1
         do ISEG1 = 1, KOUNT
            W(I,J) = YIELDL(K,IPAR,ISEG1)
            W(J,I) = YIELDL(IPAR,K,ISEG1)
            I = I+1
            J = J+1
         end do
      end do
   end if
   IST = IST+KOUNT
end do Chemicals
return
end Subroutine FDER
