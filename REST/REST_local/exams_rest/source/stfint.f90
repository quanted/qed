subroutine STFINT(NEQN,Y,W,IW,TINIT,TFINAL,TINCR,&
   RELER,ABSER,IUNIT,TT,IIFLAG,TPRINT,TTYOUT,FOURU,Stiff_Start)
! Revised 27-FEB-1985 (LAB) to send "working" message.
! Revised: 30-AUG-1985 (LAB) -- FOURU added to call
! Conversion to Fortran90 6/24/96
! Revised 05-Feb-1999 to use floating point comparisons
! Revised 05-Jan-2001 -- new method to capture partial results
! Subroutine STFINT uses STIFF to integrate a system of NEQN first order
! ordinary differential equations:
!   DY/DT = F(T,Y) ,  Y = (Y(1),Y(2),...,Y(NEQN))
! from TINIT to TFINAL, with output of the solution at intervals of TINCR by
! means of calls to subroutine OUTP. STIFF is intended for solving stiff
! problems, and is not an efficient means of solving nonstiff problems.
!
! The quantities in the argument list represent
!   NEQN -- the number of equations
!   Y -- an array of dimension NEQN, which contains the value of the solution
!   W -- an array of dimension NEQN**2+17*NEQN, which is used for working
!        storage.
!   IW -- an integer array of dimension NEQN, which is used for working
!         storage.
!   TINIT --  the starting value of the independent variable
!   TFINAL -- the value of the independent variable at which integration is to
!             be terminated
!   TINCR --  the desired spacing, in the independent variable, of the output
!             points
!   RELER  -- the desired relative error tolerance
!   ABSER  -- the desired absolute error tolerance
!   IUNIT --  the logical unit number of the data set to be used for writing
!             diagnostic messages. If IUNIT is less than or equal to zero,
!             no messages are written
!
!   FCT --  is the user-supplied subroutine FCT(T,Y,YP) which evaluates
!           the derivatives  YP(I)=DY(I)/DT, I=1,2,...,NEQN
!   FDER -- is the user-supplied subroutine which evaluates the Jacobian
!           matrix as described in the comments to GEAR.
!   OUTP -- is the user-supplied subroutine OUTP(T,Y,YP,JFLAG) used
!           to handle output. (IFLAG added to call 02/11/99 to detect
!           violations of Exams' assumption of linear sorption isotherms.)
!
! To use STFINT, the calling program must
!
!   1. Allocate space for the arrays Y(*), IW(*), and W(*) in a dimension
!      statement.  (Note that Y must be an array, even if NEQN=1.)
!   2. Set Y(1),Y(2), ... , Y(NEQN) to the initial values to be used for
!      the solution.
!   3. Provide appropriate values for NEQN, TINIT, TFINAL, TINCR, RELER,
!      ABSER, and IUNIT. (As these quantities are not altered by STFINT,
!      they may, if desired, be written as constants in the call list.)
!
! At each call to OUTP(T,Y,DY,JFLAG), the current values of the derivatives
! DY(I)/DT are in W(1),W(2),...,W(NEQN). The first call to OUTP is made at
! TINIT. JFLAG is 1 on initial value calls to OUTP.
!
! It is not necessary that the integration interval be evenly divisible by the
! output mesh size TINCR. However, if it is not, integration will proceed to
! the first mesh point beyond TFINAL, rather than terminating at TFINAL.
use Stiff_data
use Gear_data
use Floating_Point_Comparisons
Implicit None
integer :: TTYOUT,NEQN,IUNIT,K1,K2,K3,JFLAG,IER,IIFLAG
integer :: MAXERR=20 ! maximum number of error returns allowed
! Computational variables: (The actual dimension of W, as defined by the
! calling program, must be at least NEQN**2 + 17*NEQN.)
real (kind (0D0)) :: ABSER, DT, EPSDT, RELER, TFINAL, TPRINT, TINCR, TINIT,&
   TMAXIN, TT, FOURU, Y(NEQN), W(NEQN**2+17*NEQN)
integer :: IW(NEQN)
logical :: Stiff_Start
! Write starting data into message file
if (IUNIT > 0) call STMESS (TTYOUT,10,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T)
! Compute indices for splitting the work array
K1 = NEQN+1
K2 = K1+9*NEQN
K3 = K2+7*NEQN
! Initialize variables to start integration with STIFF, i.e., transfer
! parameters from call list to internal module
RELERR = RELER
ABSERR = ABSER
IFLAG = 1
JFLAG = 1
T = TINIT
! TOUT set to TPRINT (rather than TINIT) to suppress printing of pseudo
! initial condition when the STIFF integrator was not used to initiate the
! problem solutions.
if (Stiff_Start) then
   TOUT = TINIT
else ! transfer from ADMINT
   TOUT = TPRINT
   JFLAG = 2  ! to deal with cases when ADMINT evaluated the I.C and started
              ! but had not made it to the first output point
end if
! store information needed to locate end of integration.
TMAXIN = dabs(TFINAL-TINIT)
EPSDT = 0.001*dabs(TINCR)
! Set sign of output interval to proceed from TINIT to TFINAL.
DT = dsign(TINCR,TFINAL-TINIT)
IER = 0        ! Initialize counter of error returns.
Integrate: do  ! Call STIFF to integrate to the next output point
   call STIFF (Y,W(1),IW,W(K2),W(K3),W(K1),FOURU,NEQN)
   if (IFLAG == 2) then ! Successful integration to output point
      call OUTP (T,Y,W,JFLAG,IFLAG)
! 2005-03-16: warn user and recommend Freundlich isotherm; do not kill run
!      if (IFLAG == 10) exit Integrate ! violation of isotherm linearity
      JFLAG = IFLAG
      ! Check whether TFINAL has been reached or passed
      if (dabs(T-TINIT) .GreaterThanOrEqual. TMAXIN) then
         ! The integration has been completed
         if (IUNIT>0) call STMESS &
            (TTYOUT,95,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
         exit Integrate
      else ! Integration is not yet complete, so the next output
           ! point is set. If the new point differs from TFINAL
           ! by an amount attributable to roundoff error, it is
           ! reset to TFINAL exactly. Integration is then continued.
         TOUT = T+DT
         if (dabs(TFINAL-TOUT) .LessThan. EPSDT) TOUT = TFINAL
         cycle Integrate
      end if
   else  ! Integration was interrupted before reaching the output point.
         ! Increment the error counter and select the appropriate diagnostic
         ! message. Integration will continue if the error is not too severe.
      IER = IER+1
      select case (IFLAG)
      case (3) ! IFLAG = 3 -- the requested error tolerances were too small
               ! for the machine precision and have been increased to
               ! minimum permissible values.
         if (IUNIT > 0) call STMESS &
            (TTYOUT,30,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
         if (IER > MAXERR) then
            ! The program is halted because there have been
            ! MAXERR error returns from STIFF, indicating serious
            ! problems which require intervention by the user.
            if (IUNIT > 0) call STMESS &
               (TTYOUT,92,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
            exit Integrate
         else
            cycle Integrate
         end if
      case (4) ! IFLAG = 4 -- the requested error tolerances were too
               ! stringent for this problem and have been increased to values
               ! which should be acceptable.
         if (IUNIT > 0) call STMESS &
            (TTYOUT,40,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
         if (IER > MAXERR) then
            ! The program is halted because there have been
            ! MAXERR error returns from STIFF, indicating serious
            ! problems which require intervention by the user.
            if (IUNIT > 0) call STMESS &
               (TTYOUT,92,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
            exit Integrate
         else
            cycle Integrate
         end if
      case (5) ! IFLAG = 5 -- the counter of calls to FCT was reset after
               ! exceeding the limit imposed in STIFF.
               ! Relax error tolerances to reduce amount of work required
         RELERR = RELERR*10.0
         ABSERR = ABSERR*10.0
         if (IUNIT > 0) call STMESS &
            (TTYOUT,50,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
         if (IUNIT == 0) write (TTYOUT,fmt='(/A)')&
            '     Simulation RUN/CONTINUE in progress...'
         if (IER > MAXERR) then
            ! The program is halted because there have been
            ! MAXERR error returns from STIFF, indicating serious
            ! problems which require intervention by the user.
            if (IUNIT > 0) call STMESS &
               (TTYOUT,92,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
            exit Integrate
         else
            cycle Integrate
         end if
      case (6) ! IFLAG = 6 -- the convergence test in GEAR could not be met
               ! using the smallest allowable stepsize. The error tolerances
               ! have been increased to values which will allow the
               ! convergence test to be passed.
         if (IUNIT > 0) call STMESS &
            (TTYOUT,60,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
         if (IER > MAXERR) then
            ! The program is halted because there have been
            ! MAXERR error returns from STIFF, indicating serious
            ! problems which require intervention by the user.
            if (IUNIT > 0) call STMESS &
               (TTYOUT,92,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
            exit Integrate
         else
            cycle Integrate
         end if
      case (7) ! IFLAG = 7 -- the monitor of output frequency was reset after
               ! indicating that the output interval is too small to allow
               ! efficient operation of STIFF.
         if (IUNIT > 0) call STMESS &
            (TTYOUT,70,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
         if (IER > MAXERR) then
            ! The program is halted because there have been
            ! MAXERR error returns from STIFF, indicating serious
            ! problems which require intervention by the user.
            if (IUNIT > 0) call STMESS &
               (TTYOUT,92,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
            exit Integrate
         else
            cycle Integrate
         end if
      case (8) ! IFLAG = 8 -- fatal error -- a component of the solution
               ! vanished, making a pure relative error test impossible. The
               ! user must supply an appropriate nonzero value of ABSERR for
               ! successful integration.
         if (IUNIT > 0) call STMESS &
            (TTYOUT,80,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
         exit Integrate
      case (9) ! IFLAG = 9 -- fatal error -- an illegal parameter value was
               ! passed to STIFF. The user must locate and correct the error.
         if (IUNIT > 0) call STMESS &
            (TTYOUT,90,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
         exit Integrate
      case default ! IFLAG has an illegal value, so a precise definition of
              ! the error is not possible, and execution must be terminated.
         if (IUNIT > 0) call STMESS &
            (TTYOUT,20,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T)
         IFLAG = 9   ! Set IFLAG to 9 and return
         exit Integrate
      end select
   end if
end do Integrate
TT = T   ! Revision: retrieve T, IFLAG, TOUT
IIFLAG = IFLAG
TPRINT = TOUT
return
end subroutine STFINT
