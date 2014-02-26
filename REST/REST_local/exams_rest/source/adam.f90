subroutine ADAM(Y,YP,WT,YY,PHI,FOURU,NEQN)
! Revised 29-AUG-1985 (LAB) for higher (0D0) precision operations
! Revised 02-Feb-1999 to use floating point comparisons
! Revised 2004-04-09 to improve data management
! Notes from March 1999: To make test for stiffness more stringent,
!   the problem can be defined as stiff if a sequence of, say, 25 (rather than
!   50) steps are taken with order <= 5 (rather than 4), with MAXNFE = 250.
!   This entails modifying maxnfe, the kle4 test, and the Kold test.
! Notes from February 2000: Failures during HWIR testing suggested the
!     following revisions:
!     (1) Made the RMS threshold 4.0 rather than 5.0 -- this caught at
!         least one numerical instability before it happens.
!     (2) Revised the test for stiffness, as indicated by a run of steps
!         at low order, to declare the problem stiff if 25 sequential steps
!         are taken of order 4 or less, and immediately remand the problem
!         to Gear. If Maxnfe steps are taken, and the last 10 are of
!         order < 5, declare the problem stiff. In addition (June 2000),
!         results obtained during transition to stiffness are not preserved
!         for Gear; instead Gear is passed the state of the system at the
!         last output point prior to failure.
!
! Subroutine ADAM uses subroutine STEP to integrate a system of NEQN first
! order ordinary differential equations:
!   DY/DT = F(T,Y) ,  Y = (Y(1),Y(2),...,Y(NEQN))
! from T to TOUT. For reasons of efficiency, ADAM integrates beyond TOUT
! internally, though never beyond T + 10.*(TOUT-T), and calls subroutine
! SINTRP to interpolate the solution at TOUT. An option is provided to stop
! the integration at TOUT, but it should be used only if the characteristics
! of the problem make it impossible to continue the integration beyond TOUT.
! The parameters in the argument list are:
!  F -- the name of the user-supplied subroutine F(T,Y,YP), which evaluates
!     the derivatives YP(I)=DY(I)/DT, I=1,2,...,NEQN.
!  Y -- an array of dimension NEQN, which contains the value of the solution.
!  YP -- an array of dimension NEQN, which contains the value of the
!     derivative DY/DT.
!  WT,YY,PHI -- arrays of dimensions NEQN, NEQN, and 16*NEQN, respectively,
!     which are used for working storage by ADAM and STEP. The values stored
!     in YY and PHI are needed for continuing integration on subsequent calls.
! The parameters in the module Adam_data are
!   T -- the independent variable
!   TOUT -- the value of t at which output is desired
!   RELER, ABSER -- relative and absolute error tolerances for the local
!      error test. Each stepsize is chosen so that
!         DABS(LOCAL ERROR(I)) <= RELER*DABS(Y(I))+ABSER
!      for each component of the solution.
!   NEQN -- the number of equations
!   IFLAG -- indicator of the status of integration
!   DTSGN, IOLD, KLE4, INIT, KOP -- those quantities used for internal
!      bookkeeping by ADAM which are needed for continuing integration, but
!      which are normally of no interest to the user. They are placed in the
!      module to avoid local retention by ADAM between calls. See the
!      program documentation for a description of their functioning.
! To use ADAM, the calling program must allocate space for the arrays
!    Y(NEQN), YP(NEQN), WT(NEQN), YY(NEQN), and PHI(NEQN,16)
!   (Y, YP, WT, and YY must be arrays even if NEQN=1).
!
! First call to ADAM
! ------------------
! To begin integration, the calling program must
!   1. Initialize the following variables in the module Adam_data
!      T -- the starting value of the independent variable
!      TOUT -- the value of the independent variable at which output is
!         desired. (TOUT = T is permitted on the first call only, in which
!         case ADAM evaluates the derivatives YP and returns with IFLAG = 2.)
!      RELER -- the desired relative error tolerance
!      ABSER -- the desired absolute error tolerance
!      IFLAG -- normally +1.  If the integration cannot proceed beyond TOUT,
!         set IFLAG = -1.
!   2. Initialize Y(*) to contain the starting value of the solution.
! Upon successful return (IFLAG=2), T=TOUT, Y contains the solution at TOUT,
! and YP contains the derivatives at TOUT.
!
! Otherwise, T is the last value of the independent variable successfully
! reached during the integration, Y contains the solution at T, YP contains
! the derivatives at T, and IFLAG indicates the status of the integration as
! described below.
!
! Subsequent calls to ADAM
! ------------------------
! ADAM normally returns with all information needed to continue integration.
! If the integration reached TOUT (IFLAG=2), the user need only define a new
! TOUT and call ADAM again.  If the integration cannot continue internally
! beyond the new TOUT, the user must also set IFLAG=-2. If the new TOUT
! represents a reversal of the direction of integration, it is necessary that
! Y not have been altered.
!
! If the integration was interrupted with IABS(IFLAG) = 3, 4, 5, 6, or 7,
! integration may be continued simply by calling ADAM again. However, such a
! return indicates that the integration is not proceeding so smoothly as might
! be expected, so the user should exercise some caution.
! If the integration was interrupted with IFLAG = 8, the user must give ABSER
! a nonzero positive value and set IFLAG = 2 (or IFLAG = -2 if it is necessary
! to stop at TOUT) in order to continue.
! If ADAM returned with IFLAG = 9, the user must correct the invalid input and
! set IFLAG = 2 or -2 (or IFLAG = 1 or -1, if integration has not yet started)
! in order to continue.
!----------------------------------------------------------------
! Upon return, the value of IFLAG indicates the status of the
! integration as follows,
! IFLAG = 2: T = TOUT, so that integration was successful to the output point.
! IFLAG = 3: integration was interrupted because the requested error
!    tolerances were too small for the machine precision. They have been
!    increased to minimum acceptable values.
! IFLAG = 4: integration was interrupted because the requested error
!    tolerances could not be attained at the smallest allowable stepsize. The
!    tolerances have been increased to values which should allow successful
!    continuation.
! IFLAG = 5: integration was interrupted after the counter of calls to F
!    exceeded MAXNFE. The counter has been reduced by MAXNFE.
! IFLAG = 6: same as IFLAG=5, except that the problem has been additionally
!    diagnosed as stiff.
! IFLAG = 7: integration was not continued because the spacing of output
!    points has been so small as to restrict the stepsize for 50 calls to
!    STEP, indicating that the code is being used in a way which greatly
!    impairs its efficiency. The monitor of this effect was reset to allow
!    continuation if desired.
! IFLAG = 8: integration was interrupted when a component of the solution
!    vanished while a pure relative error test was specified. The user must
!    supply a nonzero ABSER to continue integration.
! IFLAG = 9: invalid input was passed to ADAM. The user must locate and
!    correct the error in order to continue integration.
! IFLAG = -3, -4, -5, -6, or -7; same as IFLAG = 3, 4, 5, 6, or 7,
!    respectively, except that ADAM was called with IFLAG negative.
use Global_variables, only: Stiff_threshold
use Adam_data
use Step_data
use Floating_Point_Comparisons
Use Global_Variables, Only: IUNITG
Use Implementation_Control, Only: StdOut
Use Define_f
Implicit None
integer :: NEQN
real (kind (0D0)) :: Y(NEQN),YP(NEQN),YY(NEQN),WT(NEQN),PHI(NEQN,16)
! Local variables
real (kind (0D0)) :: ABSDT, ABSEPS, DT, RELEPS, TEND, FOURU, &
      Local_stiff_function
integer :: L, MFLAG
! The expense is controlled by restricting the number of function evaluations
! to be approximately MAXNFE. As set, this corresponds to about 1500 steps.
integer, parameter :: MAXNFE=3000
logical :: Go_home = .false.
MFLAG = iabs(IFLAG) ! Tests for improper parameters
EPS = dmax1(RELER,ABSER)
if ((MFLAG>7) .or. (MFLAG==0) .or. (NEQN<1) .or. (RELER.LessThan.0.0) .or. &
   (ABSER.LessThan.0.0) .or. (EPS.LessThanOrEqual.0.0)) then
      ! Invalid input--set marker and return
   IFLAG = 9
   return
end if
DT = TOUT-T
ABSDT = dabs(DT)
TEND = T+10.0*DT
if (IFLAG < 0) TEND = TOUT
RELEPS = RELER/EPS
ABSEPS = ABSER/EPS
Go_home = .false.
! If this is the first call, initialize
if (MFLAG == 1) then
   NFE = 0
   call Initialize (Y,YP,YY,NEQN)
   if (Go_home) return
elseif (.not. (abs(abs(T)-abs(TOUT)) .GreaterThan. tiny(T))) then
   IFLAG = 9   ! T=TOUT is not valid input,
   return      ! as this is not the first call,
! If initialization was not completed on the first call, do it now.
elseif (INIT == 0) then
   INIT = 1
   DTSGN = DT
   H = dsign(dmax1(dabs(TOUT-X),FOURU*dabs(X)),TOUT-X)
! If the last step was made with IFLAG negative, if the
! direction of integration has changed, or if returning from
! an error detection, restart the integration.
elseif (IOLD<0 .or. (DTSGN*DT.LessThan.0.0)) then
   call Initialize (Y,YP,YY,NEQN)
   if (Go_home) return
end if

Integrate: do
   if (dabs(X-T).GreaterThanOrEqual.ABSDT) then ! already past output point;
      call SINTRP (TOUT,Y,YP,YY,PHI,NEQN)       ! interpolate and return.
      IOLD = IFLAG
      IFLAG = 2
      T = TOUT
      return
   end if
   ! If cannot go past output point, test whether too close to
   ! integrate with STEP
   if ((IFLAG<0) .and. ((dabs(TOUT-X).LessThan.FOURU*dabs(X)))) then
      ! Cannot pass TOUT, but too close to call STEP.
      ! Extrapolate by Euler method and return.
      H = TOUT-X; call FCT (X,YY,YP); NFE = NFE+1
      do L = 1, NEQN
         Y(L) = YY(L)+H*YP(L)
      end do
      IFLAG = 2
      T = TOUT
      call FCT (T,Y,YP)
      NFE = NFE+1
      IOLD = -1
      return
   end if
   !  Test for too much work.
   if (NFE > MAXNFE) then
      ! Number of function calls exceeded MAXNFE. Set IFLAG to indicate
      ! whether this resulted from stiffness, and reset counter NFE.
      ! The test is somewhat more stringent here (10 as opposed to 25
      ! sequential calls in the more immediate test of KLE4 below) because
      ! it is presumed that exceeding MAXNFE calls can happen if the problem
      ! is marginally stiff with some oscillation between orders < 5 and
      ! occasional steps with 5th or 6th order, which reset KLE4 to 0.
      IFLAG = isign(5,IFLAG)
      if (KLE4 >= 10) IFLAG = isign(6,IFLAG)
      NFE = NFE-MAXNFE
      KLE4 = 0
      exit Integrate
   end if
   ! Limit stepsize, set weight vector, and take a step
   if (dabs(H) .GreaterThanOrEqual. dabs(TEND-X)) then
      KOP = KOP+1
      if (KOP > 50) then ! The output interval has been too small
         KOP = 0 ! to allow efficient operation of ADAM
         IFLAG = isign(7,IFLAG)
         exit Integrate
      end if
      H = TEND-X
   end if
   do L = 1, NEQN
      WT(L) = RELEPS*dabs(YY(L))+ABSEPS
      if (WT(L) .Equals. 0.0) then
         ! A component of the solution vanished
         ! when a pure relative error test was specified.
         ! User must set ABSER positive in order to proceed.
         IFLAG = 8
         exit Integrate
      end if
   end do

   ! This RMS test for stiffness was drawn from Bader, M. 1998. A new
   ! technique for the early detection of stiffness in coupled differential
   ! equations and application to standard Runge-Kutta algorithms. Theoretical
   ! Chemistry Accounts 99:215-219. (H_standard set in Admint.)

   ! Table 3. Empirical Interpretation of LSF (Local Stiff Function)
   ! LSF Range     Interpretation
   ! ---------     --------------
   !   0 - 1       Problem not stiff
   !   1 - 5       Slightly stiff, results still acceptable
   !     > 5       Results may be unreliable
   ! For use with Adam's methods, the empirical interpretation of LSF perhaps
   ! must needs be more rigorous. As of 02/19/2000, using 4.0 as threshold.
   ! The test uses the values of the derivatives returned from the latest
   ! call to FCT. When a step has failed, the last prior call has advanced
   ! slightly beyond the state of the current solution. This is an advantage
   ! in detecting the development of stiffness, so there is no need nor
   ! any value to obtaining a current value by calling FCT here.

   Local_stiff_function = H * sqrt(sum(yp(1:neqn)**2))/H_standard
   if (Local_stiff_function .GreaterThan. Stiff_threshold) then
      If (Iunitg > 0) then
         Write (StdOut,fmt='(a)') &
              ' ADAM Warning: RMS test indicates stiffness.'
         Write (StdOut,fmt='(A,1pg12.5,A,g9.2)') &
              ' Local_stiff_function = ', &
              Local_stiff_function,' exceeds ', Stiff_threshold
      End If
      Iflag = isign(6,iflag)
      exit Integrate
   Else
      If (Iunitg == 2) then
         Write (StdOut,fmt='(a,1pg12.5)')&
            ' Local_stiff_function = ', Local_stiff_function
      Endif
   Endif
   call STEP (YY,YP,WT,PHI,FOURU,NEQN)
   ! Test whether step was successful.
   if (ICRASH /= 0) then ! Error tolerances were too small to permit
                         ! a successful step. Increase RELER and ABSER.
      IFLAG = isign(4,IFLAG)
      if (ICRASH == 2) IFLAG = isign(3,IFLAG)
      RELER = EPS*RELEPS
      ABSER = EPS*ABSEPS
      exit Integrate
   end if
   ! Step was successful. Test for stiffness.
   if (KLE4 >= 25) then
      IFLAG = isign(6,IFLAG)
      exit Integrate
   end if
   KLE4 = KLE4+1
   ! write (*,*) ' Order of method is: ', KOLD
   if (KOLD > 4) KLE4 = 0
end do Integrate


! Setting IOLD to +1 (the original version of the integrator) does
! not work--apparently the integrator should be restarted after
! any error return. Hence (LAB, 7 June 82):
IOLD = -1

! For error return, set T, Y(*), and YP(*) to the most recent
! values reached in the integration, except when stiffness will
! result in transfer of the solution to Gear: tests in June 2000
! demonstrated that an error return can result during extension
! of the solution beyond the output point into an unstable region,
! leading to catastrophic contamination of the solution and transfer
! of gibberish to Gear.
if (iabs(iflag)/=6) then
   T=X
   Y = YY
   do L = 1, NEQN
     YP(L) = PHI(L,1)
   end do
end if
return
contains

subroutine Initialize (Y,YP,YY,NEQN)
   ! On start and restart, set work variables X and YY(*), store
   ! the direction of integration, and initialize the stepsize.
   integer :: NEQN
   real (kind (0D0)), dimension(NEQN) :: Y, YP, YY
   START = .true.
   KLE4 = 0
   INIT = 0
   KOP = 0
   X = T
   do L = 1, NEQN
     YY(L) = Y(L)
   end do
   ! If T=TOUT on first call, evaluate derivatives and return
   if (.not. (abs(abs(T)-abs(TOUT)) .GreaterThan. tiny(T))) then
      call FCT (X,YY,YP)
      NFE = NFE+1
      IFLAG = 2
      Go_home = .true.
      return
   end if
   ! Set stepsize to begin integration.
   INIT = 1
   DTSGN = DT
   H = dsign(dmax1(dabs(TOUT-X),FOURU*dabs(X)),TOUT-X)
end subroutine Initialize

end Subroutine ADAM
