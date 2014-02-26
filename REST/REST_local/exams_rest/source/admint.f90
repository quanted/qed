subroutine ADMINT(NEQN,Y,W,TINIT,TFINAL,TINCR,RELERR,ABSERR,IUNIT,TT,IIFLAG,&
   TPRINT,TTYOUT,FOURU)
! Revised 21-Jul-82, 11-Sep-85, 14-May-87 (LAB)
! Revised 02-Feb-1999 -- floating point comparisons
! Revised 05-Jan-2001 -- new method to capture partial results
! Subroutine ADMINT uses ADAM to integrate a system of NEQN
! first order ordinary differential equations
! DY/DT = F(T,Y) ,  Y = (Y(1),Y(2),...,Y(NEQN))
! from TINIT to TFINAL, with output of the solution
! at intervals of TINCR by means of calls to the user-
! supplied subroutine OUTP.
! The quantities in the argument list represent
!    NEQN -- the number of equations
!    Y -- an array of dimension NEQN, which contains the
!         value of the solution
!    W -- an array of dimension 19*NEQN, which is used for
!         working storage.
!     TINIT -- the starting value of the independent variable
!     TFINAL -- the value of the independent variable at which
!         integration is to stop
!     TINCR -- the desired spacing, in the independent variable,
!         of the output points
!     RELERR -- the desired relative error tolerance
!     ABSERR -- the desired absolute error tolerance
!     IUNIT -- the logical unit number of the data set to be
!         used for writing diagnostic messages. If IUNIT
!         is less than or equal to zero, no messages are
!         written.
!     FCT -- is the user-supplied subroutine
!     FCT(T,Y,YP) which evaluates the derivatives
!         YP(I)=DY(I)/DT, I=1,2,...,NEQN
!     OUTP -- is the user-supplied subroutine
!         OUTP(T,Y,W,JFLAG) used to handle output.
!         (IFLAG added to call 02/11/99 to detect violations
!         of Exams' assumption of linear sorption isotherms.)
!         JFLAG is 1 on initial value calls to OUTP.
! To use ADMINT, the calling program must
! 1. Allocate space for the arrays Y(*) and W(*) in a DIMENSION statement.
!     (Note that Y must be an array, even if NEQN=1.)
! 2. Set Y(1),Y(2),...,Y(NEQN) to the initial values to be
!     used for the solution.
!   3. Provide appropriate values for NEQN, TINIT, TFINAL, TINCR, RELERR,
!     ABSERR, and IUNIT. (As these quantities are not altered by ADMINT,
!     they may, if desired, be written as constants in the call list.)
! At each call to OUTP(T,Y,W,JFLAG), the current values of the
! derivatives DY(I)/DT are in W(1),W(2),...,W(NEQN).  The
! first call to OUTP is made at TINIT.
! It is not necessary that the integration interval be evenly
! divisible by the output mesh size TINCR. However, if it is not,
! integration will proceed to the first mesh point
! beyond TFINAL, rather than stopping at TFINAL.
use Adam_data
use Floating_Point_Comparisons
use Step_data, only: h_standard
use define_f
Implicit None
real (kind (0D0)) :: DT,EPSDT,TMAXIN
real (kind (0D0)), intent(in) :: TINIT,TFINAL,TINCR,RELERR,ABSERR
integer :: IER,K1,K2,K3,JFLAG,IIFLAG
integer, intent(in) :: NEQN, IUNIT
real (kind (0D0)) :: Y(NEQN),W(19*NEQN)
! The actual dimension of W, as defined by the calling program,
! must be at least 19*NEQN.
real (kind (0D0)) :: TT, TPRINT, FOURU
integer :: TTYOUT, MAXERR=20
! MAXERR is maximum number of error returns permitted
IFLAG = IIFLAG
! Initialize counter of error returns
IER = 0
! Write starting data into message file
if (IUNIT>0) &
   call ADMESS(TTYOUT,10,NEQN,TINIT,TFINAL,TINCR,RELERR,ABSERR,T,IFLAG)
! Compute indices for splitting the work array W(*).
K1 = NEQN+1
K2 = K1+NEQN
K3 = K2+NEQN
! Initialize variables to start integration with ADAM.
RELER = RELERR
ABSER = ABSERR
IFLAG = 1
JFLAG = 1
T = TINIT
TOUT = TINIT
! Save information needed to locate end of integration.
TMAXIN = dabs(TFINAL-TINIT)
EPSDT = 0.001*dabs(TINCR)
! Set sign of output interval to proceed from TINIT to TFINAL.
DT = dsign(TINCR,TFINAL-TINIT)

! Local RMS test for stiffness was drawn from Bader, M. 1998. A new
! technique for the early detection of stiffness in coupled differential
! equations and application to standard Runge-Kutta algorithms. Theoretical
! Chemistry Accounts 99:215-219. (Test conducted in Adam.)
call fct(t,y,w(1:neqn))
h_standard = abs(DT)*sqrt(sum(w(1:neqn)**2))
if (h_standard .equals. 0.0d+00) h_standard = 1.0d+00

Integrate: do ! Call ADAM to integrate to the next output point
   call ADAM (Y,W(1),W(K1),W(K2),W(K3),FOURU,NEQN)
   if (IFLAG == 2) then ! Successful integration to output point.
      call OUTP (T,Y,W,JFLAG,IFLAG)
! 2005-03-16: no longer fatal, instead OUTP recommends using Freundlich isotherm
!      if (IFLAG == 10) exit Integrate ! violation of isotherm linearity
      JFLAG = IFLAG
      ! Check whether TFINAL has been reached or passed.
      if (dabs(T-TINIT) .GreaterThanOrEqual. TMAXIN) then
         ! The integration has been completed
         if (IUNIT > 0) &
            call ADMESS(TTYOUT,20,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
         exit Integrate
      else ! Integration is not yet complete, so the next output point is set.
         ! If the new point differs from TFINAL by an amount attributable to
         ! roundoff error, it is reset to TFINAL exactly.
         TOUT = T+DT
         if (dabs(TFINAL-TOUT) .LessThan. EPSDT) TOUT = TFINAL
         cycle Integrate      ! Integration is then continued
      end if
   else  ! Integration was interrupted before reaching the output point.
         ! Increment the error counter and branch for writing the appropriate
         ! diagnostic message. Integration will then be continued if the error
         ! is not too severe.
      IER = IER+1
      select case (IFLAG)
      case (3) ! IFLAG = 3 -- The requested error tolerances were too small
               ! for the machine precision and have been increased to minimum
               ! permissible values.
         if (IUNIT > 0) &
            call ADMESS(TTYOUT,30,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
         if (IER > MAXERR) then
            if (IUNIT > 0) call &
               ADMESS(TTYOUT,92,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
            exit Integrate
         else
            cycle Integrate
         end if
      case (4) ! IFLAG = 4 -- The requested error tolerances were too
               ! stringent for this problem and have been increased to
               ! values which should be acceptable.
         if (IUNIT > 0) call &
            ADMESS(TTYOUT,40,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
         if (IER > MAXERR) then
            if (IUNIT > 0) call &
               ADMESS(TTYOUT,92,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
            exit Integrate
         else
            cycle Integrate
         end if
      case (5) ! IFLAG = 5 -- The counter of calls to FCT was reset after
               ! exceeding the limit imposed in ADAM.
         if (IUNIT > 0) then
            call ADMESS(TTYOUT,50,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
! this is too chatty all too often...
!         else
!            write (TTYOUT,fmt='(/A)') &
!               '     Simulation RUN/CONTINUE in progress...'
         end if
         if (IER > MAXERR) then
            if (IUNIT > 0) call &
               ADMESS(TTYOUT,92,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
            exit Integrate
         else
            cycle Integrate
         end if
      case (6) ! IFLAG = 6 -- The counter of calls to FCT was reset after
               ! stiffness caused it to exceed the limit imposed in ADAM.
               ! Return to DRIVER and invoke stiff integrator
         if (IUNIT > 0) then
            call ADMESS(TTYOUT,60,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
! this is too chatty for most users, and when we want to see what's going
! on, set iunit=1
!         else ! inform user that integration is continuing
!            write (TTYOUT,fmt='(/A)') &
!               '     Simulation RUN/CONTINUE in progress...'
         end if
         exit Integrate
      case (7) ! IFLAG = 7 -- the monitor of output frequency was reset
               ! after indicating that the output interval is too small
               ! to allow efficient operation of ADAM.
         if (IUNIT > 0) &
            call ADMESS(TTYOUT,70,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
         if (IER > MAXERR) then
            if (IUNIT > 0) call &
               ADMESS(TTYOUT,92,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
            exit Integrate
         else
            cycle Integrate
         end if
      case (8) ! IFLAG = 8 -- fatal error -- a component of the solution
               ! vanished, making a pure relative error test impossible.
               ! The user must supply an appropriate nonzero value of
               ! ABSERR for successful integration.
         if (IUNIT > 0) &
            call ADMESS(TTYOUT,80,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
         exit Integrate
      case (9) ! IFLAG = 9 --fatal error--an illegal parameter value was
               ! passed to ADAM. The user must locate and correct the error.
         if (IUNIT > 0) &
            call ADMESS(TTYOUT,90,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
         exit Integrate
      case default
               ! IFLAG has an illegal value, so that a precise definition of
               ! the error is not possible, and execution must be terminated.
         if (IUNIT > 0) &
            call ADMESS(TTYOUT,25,NEQN,TINIT,TFINAL,TINCR,RELER,ABSER,T,IFLAG)
         IFLAG = 9
         exit Integrate
      end select
   end if
end do Integrate
TT = T
IIFLAG = IFLAG
TPRINT = TOUT
return
end subroutine ADMINT
