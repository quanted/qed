subroutine GRSUB4(Y,ERROR,WT,D,FOURU,NEQN)
! Rewritten 1-APR-1982 by L.A. Burns
! Revised 15-APR-87 (LAB)
! Revised 05-Feb-1999 for floating point comparisons
use local_gear_data
use Gear_data
use Floating_Point_Comparisons
Implicit None
real (kind (0D0)) :: D, D1, FOURU, R, RDWN, RUP
integer NEQN, J, I, KD
real (kind (0D0)) :: Y(NEQN,7), ERROR(NEQN), WT(NEQN)
real (kind (0D0)) :: ERUP(5)  = (/3.0,6.0,9.167,12.5,15.98/),&
                     ERDWN(6) = (/1.0,1.0,0.5,0.1667,0.04133,0.008267/)
HOLD = H
if (KP1 > 2) then
   do J = 3, KP1
      do I = 1, NEQN
         Y(I,J) = Y(I,J)+A(J)*ERROR(I)
      end do
   end do
end if
ITST = ITST-1
! Revision of order and stepsize is considered only if ITST = 0.
if (ITST /= 0) then
   if (ITST==1 .and. K/=6) then ! save ERROR(*) in Y(*,7).
   ! (If next step succeeds,
   !  it will be used in deciding whether to raise order.)
      do I = 1, NEQN
         Y(I,7) = ERROR(I)
      end do
   end if
   return
end if
! Determine appropriate order and stepsize for next step.
KD = 0 ! assume no change
R = 1.2*(2.0*D)**(1.0/float(KP1))
! If K=1, cannot lower order.
if (K > 1) then ! Check whether order K-1 allows larger stepsize.
   D1 = 0.0
   do I = 1, NEQN
      D1 = dmax1(D1,dabs(Y(I,KP1)/WT(I)))
   end do
   RDWN = 1.3*(2.0*D1/(ERDWN(K)*EPS))**(1.0/float(K))
   if (RDWN .LessThanOrEqual. R) then  ! Order K-1 is better than order K.
      R = RDWN
      KD = -1
   end if   
end if
! If K=6, cannot raise order. Otherwise, check whether order K+1 allows
! larger stepsize.
if (K < 6) then
   D1 = 0.0
   do I = 1, NEQN
      D1 = dmax1(D1,dabs((ERROR(I)-Y(I,7))/WT(I)))
   end do
   RUP = 1.4*(2.0*D1/(ERUP(K)*EPS))**(1.0/float(K+2))
   if (RUP .LessThanOrEqual. R) then 
      ! Order will be raised, so append a new column to Y.
      KD = 1
      R = RUP
      D1 = A(KP1)/float(KP1)
      do I = 1, NEQN
         Y(I,KP1+1) = ERROR(I)*D1
      end do
   end if
end if
! If order is unchanged and the stepsize change would be less than 12%
! increase, or less than 1% decrease, no change is made. Otherwise, the
! new order and stepsize are set. Another test will be made after K+1 steps.
! Step increase is limited to a factor of 2.
ITST = KP1
if (KD==0 .and. (dabs(R-0.95) .LessThan. 0.06D+00)) return
K = K+KD
if (R .LessThan. 0.5) R = 0.5
H = dsign(dmax1(dabs(H/R),FOURU*dabs(Time)),H)
return
end subroutine GRSUB4
