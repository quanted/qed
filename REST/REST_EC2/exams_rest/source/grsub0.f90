subroutine GRSUB0(Y,SAVER,YP,WT,FOURU,NEQN)
! 7 June 1982 by L.A. Burns
! revised 29-AUG-1985 (LAB) for high precision version.
! converted to Fortran90 6/24/96
! revised 05-Feb-1999 for floating point comparisons
use Local_gear_data
use Gear_data
use Floating_Point_Comparisons
Use Define_f
Implicit None
real (kind (0D0)) :: ABSH, EPSMIN, YPNORM, YNORM, FOURU
integer :: NEQN, I, J
real (kind (0D0)) :: Y(NEQN,7), SAVER(NEQN,7), YP(NEQN), WT(NEQN)
! If stepsize is too small for machine precision, increase it to an acceptable
! value and return to calling program.
HMIN = FOURU*dabs(Time)
if (dabs(H) .LessThan. HMIN) then ! Boost the step slightly
   HMIN = HMIN*1.005     ! to facilitate passage through the problem zone
   H = dsign(HMIN,H)
   ICRASH = 1
   return
end if
! If the requested error tolerance is too small for the machine precision,
! increase it to an acceptable value and return to the calling program.
YNORM = 0.0
do I = 1, NEQN
   YNORM = dmax1(YNORM,dabs(Y(I,1)/WT(I)))
end do
EPSMIN = FOURU*YNORM
if (EPS .LessThan. EPSMIN) then
   EPS = EPSMIN*(1.0+FOURU)
   ICRASH = 2
   return
end if
! If this is the first step, choose a starting stepsize and initialize Y(*,2)
First_step: if (START) then
   START = .false.
   call FCT (Time,Y(1:neqn,1),YP)
   NFE = NFE+1
   YPNORM = 0.0
   do I = 1, NEQN
      YPNORM = dmax1(YPNORM,dabs(YP(I)/WT(I)))
   end do
   ABSH = dabs(H)
   if (EPS .LessThan. 16.0*YPNORM*H*H) ABSH = 0.25*dsqrt(EPS/YPNORM)
   H = dsign(dmax1(ABSH,HMIN),H)
   do I = 1, NEQN
      Y(I,2) = YP(I)*H
   end do
   HOLD = H; K = 1; KOLD = 0
end if First_step
! Initialize control variables for this step
! Save T and Y for use in case of step failure
ICRASH = 0; IFAIL = 0; KP1 = K+1; TOLD = Time
do J = 1, KP1
   do I = 1, NEQN
      SAVER(I,J) = Y(I,J)
   end do
end do
return
end Subroutine GRSUB0
