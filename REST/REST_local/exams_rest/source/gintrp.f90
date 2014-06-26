subroutine GINTRP(TOUT,YOUT,YPOUT,Y,NEQN)
! Revised 26 September 1983 (LAB) for high precision operations.
! Subroutine GINTRP may be used in conjunction with subroutine GEAR to
! interpolate the solution to the nonmesh point TOUT. GINTRP should be called
! when the integration has proceeded to the first mesh point beyond TOUT.
!
! Subroutine GEAR approximates the solution for X near T by a K degree
! polynomial P(X). The coefficient of the S**L term of P(X) is stored in
! Y(*,L+1), L=0,1,...,K, where S = (X-T)/HOLD
!
! Subroutine GINTRP approximates the solution and its derivative at TOUT by
! YOUT(*)=P(TOUT) and YPOUT(*)=P'(TOUT), respectively.
!
! The parameters in the argument list are:
!   TOUT  -- the value of the independent variable for which
!            the solution is to be found.
!   YOUT  -- an array of dimension NEQN to hold the value of
!            the solution at TOUT
!   YPOUT -- an array of dimension NEQN to hold the value of
!            the derivative at TOUT.
!   Y     -- the array of dimensions (NEQN,7) returned at Time by
!            subroutine GEAR.
!
! The values of Time, HOLD, NEQN, and K are passed from subroutine
! GEAR through the module Gear_data
use Gear_data, only: Time, HOLD, K
Implicit None
integer :: NEQN,KP1,KP2,J,I,JBACK
! computational variables
real (kind (0D0)) :: YOUT(NEQN),YPOUT(NEQN),Y(NEQN,7),FACT(7),&
   TOUT,S,TEMP1,TEMP2
S = (TOUT-Time)/HOLD
KP1 = K+1
KP2 = K+2
do J = 2, KP1
   FACT(J) = float(J-1)/HOLD
end do
do I = 1, NEQN
   TEMP1 = 0.0
   TEMP2 = 0.0
   do JBACK = 1, K
      J = KP2-JBACK
      TEMP1 = TEMP1*S+Y(I,J)
      TEMP2 = TEMP2*S+Y(I,J)*FACT(J)
   end do
   YOUT(I) = TEMP1*S+Y(I,1)
   YPOUT(I) = TEMP2
end do
return
end Subroutine GINTRP
