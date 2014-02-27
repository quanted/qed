subroutine SINTRP(XOUT,YOUT,YPOUT,Y,PHI,NEQN)
! Subroutine SINTRP acts in conjunction with subroutine STEP to
! interpolate the solution to the nonmesh point XOUT. SINTRP
! should be called when the integration has proceeded to the first
! mesh point beyond XOUT.
!    The methods in subroutine STEP approximate the solution near
! X by a polynomial. SINTRP approximates the solution at
! XOUT by evaluating the polynomial there.
!
! The parameters in the argument list are:
!    XOUT --  the value of the independent variable for which
!             the solution is to be found
!    YOUT --  an array of dimension NEQN to hold the value of
!             the solution at XOUT.
!    YPOUT -- an array of dimension NEQN to hold the value of
!             the derivative at XOUT.
!    Y --     the array of dimension NEQN which contains the
!             solution returned at X by STEP
!    PHI --   the array of dimensions (NEQN,16) which holds the
!             modified divided differences returned at X by STEP
!    NEQN --  the number of equations
!
! The remaining parameters X, PSI(12), and KOLD which
! are needed for defining the polynomial, are passed from
! subroutine STEP through the module Step_data
use Step_data
Implicit None
integer :: NEQN,KI,KIP1,I,J,JM1,LIMIT1,L
real (kind (0D0)) :: XOUT,HI,TERM,PSIJM1,GAMMA,ETA,TEMP2,TEMP3
real (kind (0D0)) :: Y(NEQN),YOUT(NEQN),YPOUT(NEQN),PHI(NEQN,16)
real (kind (0D0)), dimension(13) :: G2, Work, RHO
G2(1)  = 1.0D+00
RHO(1) = 1.0D+00
HI     = XOUT-X
KI     = KOLD+1
KIP1   = KI+1
do I = 1, KI ! Initialize Work(*) for computing G2(*)
   Work(I) = 1.0D+00/dble(I)
end do
TERM = 0.0
do J = 2, KI ! Compute G2(*)
   JM1 = J-1
   PSIJM1 = PSI(JM1)
   GAMMA = (HI+TERM)/PSIJM1
   ETA = HI/PSIJM1
   LIMIT1 = KIP1-J
   do I = 1, LIMIT1
      Work(I) = GAMMA*Work(I)-ETA*Work(I+1)
   end do
   G2(J) = Work(1)
   RHO(J) = GAMMA*RHO(JM1)
   TERM = PSIJM1
end do
! Interpolate
YPOUT = 0.0
YOUT =  0.0
do J = 1, KI
   I = KIP1-J
   TEMP2 = G2(I)
   TEMP3 = RHO(I)
   do L = 1, NEQN
      YOUT(L) =  YOUT(L)+ TEMP2*PHI(L,I)
      YPOUT(L) = YPOUT(L)+TEMP3*PHI(L,I)
   end do
end do
do L = 1, NEQN
   YOUT(L) = Y(L)+HI*YOUT(L)
end do
return
end Subroutine SINTRP
