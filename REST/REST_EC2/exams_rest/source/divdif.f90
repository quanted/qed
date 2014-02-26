subroutine DIVDIF(DC,DY,NP,DVD)
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 08-Feb-1999 to use floating point comparisons
use Implementation_Control
use Floating_Point_Comparisons
Implicit None
integer :: J,N,NP,KP,KYCL
real (kind (0D0)) :: DC(NP), DY(NP), DVD(20), DIVS !WHY 20?
if (NP < 2 .or. NP > 60) then ! error--BUT S.B. 20???
  write (stdout,FMT='(1X,I4,A)') NP, " POINTS INV IN DIVDIF"
  return
end if
do J = 1, NP
  DVD(J) = DY(J)
end do
N = NP-1
kycl_loop: do KYCL = 1, N
  KP = KYCL+1
  Div_loop: do J = KP, NP
    DIVS = DC(J)-DC(KYCL)
    if (dabs(DIVS) .LessThan. 1.0D-14) then ! WHY THIS NUMBER (1.0D-14)???
      write (stdout,FMT='(A)') " TWO ARGS EQUAL"
      return
    end if
    DVD(J) = (DVD(J)-DVD(KYCL))/DIVS
  end do Div_loop
end do kycl_loop
return
end Subroutine DIVDIF
