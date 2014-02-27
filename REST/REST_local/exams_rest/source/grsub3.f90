subroutine GRSUB3(IQ,Y,SAVER,YP,D,WT,FOURU,NEQN)
! Revised 30 August 1982 by L.A. Burns
! Revised 29-AUG-1985 for high precision operations.
! Revised 05-Feb-1999 for floating point comparisons
use local_gear_data
use Gear_data
use Floating_Point_Comparisons
Use Define_f
Implicit None
real (kind (0D0)) :: D, D1, GFACT, R, RDWN, FOURU
integer :: NEQN, I, IQ, J
real(kind(0D0)),parameter :: ERDWN(6)=(/1.0,1.0,0.5,0.1667,0.04133,0.008267/)
real (kind (0D0)) :: Y(NEQN,7),SAVER(NEQN,7),YP(NEQN),WT(NEQN)
! The step was not successful. The stepsize is reduced for the next step.
! If K >= 2, reduction of the order is also considered.
Time = TOLD ! restore T and Y(*,1)
do I = 1, NEQN
  Y(I,1) = SAVER(I,1)
end do
IFAIL = IFAIL+1 ! check possibilities for continuation
if (IFAIL > 3) then
   ! IFAIL > 3 and K=1--choose optimum stepsize for next attempt
   H = H/dsqrt(2.0*D)
   if (dabs(H) .LessThan. HMIN) then
      call Increase_tolerance (Y,SAVER)
   else
      IQ = 2
   end if
elseif (IFAIL<3 .and. K>1) then ! First or second failure and K >= 2.
   ! Test whether order should be lowered; choose stepsize for next attempt
   R = 1.2*(2.0*D)**(1.0/float(KP1))
   D1 = 0.0
   do I = 1, NEQN
     D1 = dmax1(D1,dabs(Y(I,KP1)/WT(I)))
   end do
   RDWN = 1.3*(2.0*D1/(ERDWN(K)*EPS))**(1.0/float(K))
   if (RDWN .GreaterThanOrEqual. R) then
                        ! The order is not changed. The step decrease
                        ! is limited to a factor of 1/10.0
      if (R .GreaterThan. 10.0) R = 10.0
      H = H/R
      if (dabs(H) .LessThan. HMIN) then
         call Increase_tolerance (Y,SAVER)
      else
         IQ = 2
      end if
   else  ! The order is lowered. The step is decreased by at least 9 percent,
         ! but the decrease is limited to a factor of 1/10.
      K = K-1
      if (RDWN .LessThan.     1.1) RDWN =  1.1
      if (RDWN .GreaterThan. 10.0) RDWN = 10.0
      H = H/R
      if (dabs(H) .GreaterThanOrEqual. HMIN) then
         IQ = 1
      else
         KP1 = K+1
         call Increase_tolerance (Y,SAVER)
      end if
   end if
else ! This is the third failure, or else K=1 on the first or second failure.
     ! H is halved, Y(*,2) is evaluated, and the order is set to 1 for the
     ! next attempt.
   IFAIL = 3
   H = 0.5*H
   if (dabs(H) .LessThan. HMIN) H = dsign(HMIN,H)
   call FCT (Time,Y(1:neqn,1),YP)
   NFE = NFE+1
   do I = 1, NEQN
     SAVER(I,2) = YP(I)*H
     Y(I,2) = SAVER(I,2)
   end do
   HOLD = H
   K = 1
   KP1 = 2
   A(1) = -1.0
   KOLD = 1
   ITST = 2
   IWEVAL = 1
   ! set address on return
   IQ = 3
end if
return
contains
Subroutine Increase_tolerance (Y,SAVER)
real (kind (0D0)), dimension (:,:) :: Y, SAVER
! Error tolerance cannot be met at smallest allowed stepsize.
! Increase tolerance, restore Y, and return to calling program.
GFACT = max((HMIN/dabs(H))**KP1,2.0D+00)
EPS = EPS*GFACT*(1.0D+00+FOURU)
H = dsign(HMIN,H)
do J = 2, KP1
   do I = 1, NEQN
      Y(I,J) = SAVER(I,J)
   end do
end do
ICRASH = 4
return
end Subroutine Increase_tolerance
end Subroutine GRSUB3
