subroutine STIFF(Y,YP,IPS,YY,W,WORK,FOURU,NEQN)
! rewritten 22-Jul-1982 by L.A. Burns
! revised  30-AUG-1985 for high precision operations.
! revised  05-Feb-1999 for floating point comparisons.
!
! Subroutine STIFF uses subroutine GEAR to integrate a system of NEQN first-
! order ordinary differential equations:
!       DY/DT = F(T,Y) ,  Y = (Y(1),Y(2),...,Y(NEQN))
! from T to TOUT. For reasons of efficiency, STIFF integrates beyond TOUT
! internally, though never beyond T + 10.*(TOUT-T), and calls subroutine
! GINTRP to interpolate the solution at TOUT. An option is provided to stop
! the integration at TOUT, but it should be used only if the characteristics
! of the problem make it impossible to continue the integration beyond TOUT.
!
! Stiff is intended for solving stiff problems. It is not an efficient means
! for solving nonstiff problems.
!
! The parameters in the argument list are
!
!  Y  -- an array of dimension NEQN, which contains the value of the solution.
!  YP -- an array of dimension NEQN, which contains the value of the
!        derivative DY/DT.
!  IPS, YY, W -- an integer array of dimension NEQN, and arrays of dimensions
!        (NEQN,7) and (NEQN,NEQN), respectively. Their values are needed for
!        continuing integration on subsequent calls.
!  WORK -- an array of dimensions (NEQN,9) which is used for working storage
!        by GEAR. WORK is composed of CVEC(NEQN), ERROR(NEQN), and
!        SAVER(NEQN,7)
!
!  FCT -- is the user-supplied subroutine F(T,Y,YP), which evaluates the
!        derivatives YP(I)=DY(I)/DT, I=1,2,...,NEQN.
!  FDER --is the user-supplied subroutine which evaluates the Jacobian matrix
!        as described in the comments to GEAR.
!
! The parameters in the module STIFF_DATA are
!   T --    the independent variable
!   TOUT -- the value of T at which output is desired
!   RELERR, ABSERR -- relative and absolute error tolerances for the local
!        error test. Each stepsize is chosen so that
!        ABS(LOCAL ERROR(I)) <= RELERR*ABS(Y(I))+ABSERR for each component of
!        the solution.
!   NEQN -- the number of equations
!   IFLAG -- indicator of the status of integration
!   DTSGN, IOLD, INIT, KOP -- those quantities used for internal bookkeeping
!        by STIFF which are needed for continuing integration, but which are
!        normally of no interest to the user. See the program documentation
!        for a description of their functioning.
!
! To use STIFF, the calling program must allocate space for the arrays
! Y(NEQN), YP(NEQN), IPS(NEQN), YY(NEQN,7), W(NEQN,NEQN), and WORK(NEQN,9).
! (Y and YP must be arrays even if NEQN=1.)
!
! First call to STIFF
! -------------------
! To begin integration, the calling program must
!
!   1. Initialize the following variables in the module Stiff_data
!        T -- the starting value of the independent variable
!        TOUT -- the value of the independent variable at which output is
!           desired. (TOUT=T is permitted on the first call only, in which
!           case stiff evaluates the derivatives YP and returns with IFLAG=2.)
!        RELERR -- the desired relative error tolerance
!        ABSERR -- the desired absolute error tolerance
!        IFLAG -- normally +1. If the integration cannot proceed beyond TOUT,
!           set IFLAG = -1.
!
!   2. Initialize Y(*) to contain the starting value of the solution.
!
! Upon successful return (IFLAG=2), T=TOUT, Y contains the solution at TOUT,
! and YP contains the derivatives at TOUT.
!
! Otherwise, Time is the last value of the independent variable successfully
! reached during the integration, Y contains the solution at T, YP contains
! the derivatives at T, and IFLAG indicates the status of the integration as
! described below.
!
! Subsequent calls to STIFF
! -------------------------
! STIFF normally returns with all information needed to continue integration.
! If the integration reached TOUT (IFLAG=2), the user need only define a new
! TOUT and call STIFF again. If the integration cannot continue internally
! beyond the new TOUT, the user must also set IFLAG=-2. If the new TOUT
! represents a reversal of the direction of integration, it is necessary
! that Y not have been altered.
!
! If the integration was interrupted with ABS(IFLAG) = 3, 4, 5, 6, or 7,
! integration may be continued simply by calling STIFF again.  However, such a
! return indicates that the integration is not proceeding so smoothly as might
! be expected, so the user should exercise some caution.
!
! If the integration was interrupted with IFLAG = 8, the user must give ABSERR
! a nonzero positive value and set IFLAG = 2 (or IFLAG=-2 if it is necessary
! to stop at TOUT) in order to continue.
!
! If STIFF returned with IFLAG = 9, the user must correct the invalid input
! and set IFLAG = 2 or -2 (or IFLAG = 1 or -1, if integration has not yet
! started) in order to continue.
!
! Upon return, the value of IFLAG indicates the status of the integration:
! IFLAG = 2 -- T=TOUT, so that integration was successful to the output point.
! IFLAG = 3 -- integration was interrupted because the requested error
!              tolerances were too small for the machine precision. They have
!              been increased to minimum acceptable values.
! IFLAG = 4 -- integration was interrupted because the requested error
!              tolerances could not be attained at the smallest allowable
!              stepsize. The tolerances have been increased to values which
!              should allow successful continuation.
! IFLAG = 5 -- integration was interrupted after the counter of calls to F
!              exceeded MAXNFE.  The counter has been reduced by MAXNFE.
! IFLAG = 6 -- integration was interrupted because the error tolerances were
!              too small to permit the iteration in GEAR to converge for the
!              smallest allowable stepsize. The tolerances have been increased
!              to values which will allow convergence.
! IFLAG = 7 -- integration was not continued because the spacing of output
!              points has been so small as to restrict the stepsize for 50
!              calls to GEAR, indicating that the code is being used in a way
!              which greatly impairs its efficiency. The monitor of this
!              effect was reset to allow continuation if desired.
! IFLAG = 8 -- integration was interrupted when a component of the solution
!              vanished while a pure relative error test was specified. The
!              user must supply a nonzero ABSERR to continue integration.
! IFLAG = 9 -- invalid input was passed to STIFF.  The user must locate and
!              correct the error in order to continue integration.
! IFLAG =-3, -4, -5, -6, or -7
!           -- same as IFLAG = 3, 4, 5, 6, or 7, respectively, except that
!              STIFF was called with IFLAG negative.

use Stiff_data
use Gear_data
use Floating_Point_Comparisons
Use Define_f
Implicit None
real (kind (0D0)) :: ABSDT, ABSEPS, DT, RELEPS, TEND, FOURU
integer :: NEQN,MFLAG,L,IPS(NEQN)
! Computational variables
real (kind (0D0)) :: Y(NEQN),YP(NEQN),YY(NEQN,7),W(NEQN,NEQN),WORK(NEQN,9)
! The expense is controlled by restricting the number
! of function evaluations to be approximately MAXNFE.
integer :: MAXNFE = 4000 ! As set, this corresponds to about 1500 steps.
logical :: Go_home
MFLAG = iabs(IFLAG)  ! Tests for improper parameters
EPS = dmax1(RELERR,ABSERR)
Go_home = .false.
if (MFLAG>7 .or. MFLAG==0 .or. NEQN<1 .or. (RELERR .LessThan. 0.0) .or. &
   (ABSERR .LessThan. 0.0).or.(EPS .LessThanOrEqual. 0.0)) then! invalid input
   IFLAG = 9
   return
end if
DT = TOUT-T
ABSDT = dabs(DT)
TEND = T + 10.0*DT
if (IFLAG < 0) TEND = TOUT
RELEPS = RELERR/EPS
ABSEPS = ABSERR/EPS

Setup: if (MFLAG == 1) then ! this is the first call; initialize
   NFE = 0
   call Initialize (Y,YY,YP)
   if (Go_home) return
elseif (.not. (abs(abs(T)-abs(TOUT)) .GreaterThan. tiny(T))) then
   ! As this is not the first call, T=TOUT is not valid input.
   IFLAG = 9
   return
elseif (INIT == 0) then
   ! If initialization was not completed on the first call, do it now.
   INIT = 1
   DTSGN = DT
   H = dsign(dmax1(dabs(TOUT-Time),FOURU*dabs(Time)),TOUT-Time)
elseif (IOLD<0 .or. (DTSGN*DT .LessThan. 0.0)) then
   ! If the last step was made with IFLAG negative, or if the
   ! direction of integration is changed, restart the integration.
   call Initialize (Y,YY,YP)
   if (Go_home) return
end if Setup

Integrate: do
   if (dabs(Time-T).GreaterThanOrEqual.ABSDT) then! already past output point,
      call GINTRP (TOUT,Y,YP,YY,NEQN)    ! so interpolate and return
      IOLD = IFLAG
      IFLAG = 2
      T = TOUT
      return
   end if
   if (IFLAG<0 &  ! If cannot go past output point,
                  ! test whether too close to integrate with GEAR.
      .and. (dabs(TOUT-Time) .LessThan. FOURU*dabs(Time))) then
      ! Cannot pass TOUT, but too close to call GEAR.
      ! Extrapolate by Euler method and return.
      H = TOUT-Time
      call FCT (Time,YY(1:neqn,1),YP)
      NFE = NFE+1
      do L = 1, NEQN
         Y(L) = YY(L,1)+H*YP(L)
      end do
      IFLAG = 2
      T = TOUT
      call FCT (T,Y,YP)
      NFE = NFE+1
      IOLD = -1
      return
   end if
   ! Test for too much work.
   if (NFE > MAXNFE) then    ! Number of function calls exceeded MAXNFE.
      IFLAG = isign(5,IFLAG)
      NFE = NFE-MAXNFE       ! Reset counter NFE.
      call Error_return (Y,YP,YY)
      exit Integrate
   end if
   ! Limit stepsize, set weight vector, and take a step.
   if (dabs(H) .GreaterThanOrEqual. dabs(TEND-Time)) then
      KOP = KOP+1
      if (KOP > 50) then   ! The output interval has been too small
         KOP = 0           ! to allow efficient operation of STIFF
         IFLAG = isign(7,IFLAG)
         call Error_return (Y,YP,YY)
         exit Integrate
      end if
      H = TEND-Time
   end if
   ! The weight vector is placed in Y(*).
   do L = 1, NEQN
      Y(L) = RELEPS*dabs(YY(L,1))+ABSEPS
      if (Y(L) .Equals. 0.0) then ! A component of the solution vanished when
                                  ! a pure relative error test was specified.
                                  ! User must set ABSERR positive to proceed.
         IFLAG = 8
         call Error_return (Y,YP,YY)
         exit Integrate
      end if
   end do
   call GEAR (YY,W,IPS,Y,YP,WORK(1,1),WORK(1,2),WORK(1,3),FOURU,NEQN)
   ! Test whether step was successful.
   if (ICRASH == 0) then  ! Step succeeded; continue integration
      cycle Integrate
   else ! Error tolerances were too small to permit a successful step
      IFLAG = isign(4,IFLAG)     ! set IFLAG to indicate the cause
      if (ICRASH == 2) IFLAG = isign(3,IFLAG)
      if (ICRASH == 3) IFLAG = isign(6,IFLAG)
      if (ICRASH == 1) then      ! and increase error tolerances
         RELERR = RELERR*3.0
         ABSERR = ABSERR*3.0
      else
         RELERR = EPS*RELEPS
         ABSERR = EPS*ABSEPS
      end if
      call Error_return (Y,YP,YY)
      exit Integrate
   end if
end do Integrate
return
contains
Subroutine Error_return (Y,YP,YY)
   real (kind (0D0)), dimension(:) :: Y,YP
   real (kind (0D0)), dimension(:,:) :: YY
   ! For error return, set T, Y(*), and YP(*) to the most recent
   ! values reached in the integration.
   T = Time
   ! Treatment of error returns depends on whether
   ! HOLD is zero (LAB revision 22/7/1982)
   do L = 1, NEQN
      Y(L) = YY(L,1)
   end do
   if (HOLD .NotEqual. 0.0) then
      do L = 1, NEQN
         YP(L) = YY(L,2)/HOLD
      end do
      IOLD = 1
   else ! HOLD is zero
        ! In the case of error returns provoked by faulty input data,
        ! there may not have been an opportunity to compute "HOLD." Thus,
        ! the YP transfer loop is replaced with a call to FCT at initial T.
      call FCT (T,Y,YP)
         ! IF HOLD is Zero, the next call to STIFF can result in division by
         ! zero in GINTRP. Therefore, the integration must be restarted:
      IOLD = -1
   end if
end Subroutine Error_return
Subroutine Initialize (Y,YY,YP)
   ! Initialization section--on start and restart, set work variables Time and
   ! YY, store the direction of integration, and initialize the stepsize.
   real (kind (0D0)), dimension(:) :: Y,YP
   real (kind (0D0)), dimension(:,:) :: YY
   START = .true.
   INIT = 0
   KOP = 0
   Time = T
   do L = 1, NEQN
     YY(L,1) = Y(L)
   end do
   if (.not. (abs(abs(T)-abs(TOUT)) .GreaterThan. tiny(T))) then  ! T=TOUT on
      call FCT (TOUT,YY(1:neqn,1),YP)   !  first call, so evaluate derivatives
      NFE = NFE+1
      IFLAG = 2
      Go_home = .true.
      return                  ! and return
   end if
   ! Set stepsize to begin integration.
   INIT = 1
   DTSGN = DT
   H = dsign(dmax1(dabs(TOUT-Time),FOURU*dabs(Time)),TOUT-Time)
end Subroutine Initialize
end subroutine STIFF
