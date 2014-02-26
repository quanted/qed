subroutine GEAR(Y,W,IPS,WT,YP,C,ERROR,SAVER,FOURU,NEQN)
! Revised 30 August 1982 by L.A. Burns
! Last revised: 29-AUG-1985 (LAB) for real (kind (0D0)) version.
! Last revised: 05-Feb-99 for floating point comparisons.
! Subroutine GEAR uses a backward differentiation method (of order .LE. 6)
! to perform one step in the integration of a system of NEQN first order
! ordinary differential equations:
!   DY/DT = F(T,Y) ,  Y = (Y(1),Y(2),...,Y(NEQN))
! To specify the differential equations to be solved, two subroutines must be
! supplied. The first, denoted here by FCT, calculates the NEQN derivatives
! DY(I)/DT. The second, denoted here by FDER, calculates the NEQN**2 elements
! of the Jacobian matrix of F(T,Y).
!
!   FCT must be of the form FCT(T,Y,YP), where Y and YP are arrays each of
!   dimension NEQN. FCT must calculate the values of the derivatives DY(I)/DT
!   at (T,Y) and place them in YP. T and Y must not be altered by FCT.
!
!   FDER must be of the form FDER(T,Y,W,YP), where Y and YP are arrays each of
!   dimension NEQN, and W is an array of dimensions (NEQN,NEQN). FDER must
!   calculate the values of all the partial derivatives of F at (T,Y). The
!   partial derivative of the M-th component of F with respect to Y(N) is to
!   be placed in W(M,N). When FDER is called, YP contains the values of DY/DT
!   at (T,Y). For some problems, these values may be useful in simplifying the
!   evaluation of the Jacobian. T, Y, and YP must not be altered by FDER.
!
!   For FDER, the user may use the default subroutine QJACOB, which uses FCT
!   to compute the Jacobian by numerical differencing. Since this procedure
!   involves NEQN calls to FCT, its use is not recommended unless the Jacobian
!   is difficult to compute directly.
!
! Subroutine GEAR is intended specifically for the solution of stiff problems.
! For nonstiff problems, GEAR will be less efficient than a code based on
! Adams methods.
!
! Information is exchanged with GEAR both through the argument list and
! through the module Gear_data.
!
! The parameters in the argument list are:
!
!   Y -- an array of dimensions (NEQN,7) whose value must not be altered
!      between calls to GEAR. The first NEQN locations, Y(1,1), Y(2,1), ... ,
!      Y(NEQN,1) contain the solution values
!   W, IPS -- respectively, an array of dimensions (NEQN,NEQN) and an integer
!      array of dimension NEQN, whose values must not be altered between calls
!      to GEAR
!   WT -- an array of dimension NEQN used in specifying the error test.
!   YP, C, ERROR, SAVER--respectively, arrays of dimensions NEQN, NEQN, NEQN,
!      and (NEQN,7), which are used for working storage by GEAR. It is not
!      necessary to preserve their values between steps.
!
! The parameters in the module Gear_data area:
!
!   Time -- the independent variable
!   HOLD -- the stepsize used for the last successful step
!   H -- the stepsize to be used in attempting the next step
!   EPS -- the desired tolerance for the error test
!   NEQN -- the number of equations being integrated
!   K -- the order of the method to be used for the next step
!   ICRASH -- an indicator of error conditions upon return
!   NFE -- a counter which is incremented by 1 after each call to FCT
!   START -- a logical variable which must be set .TRUE. on
!      the first call to GEAR
!   AHINV, A(7), KOLD, ITST, IWEVAL -- variables used for internal bookkeeping
!      by GEAR whose values are needed for continuing integration. Their
!      values are normally of no interest to the user, and they are placed in
!      the COMMON block only to avoid local retention between calls.
!
! Except for H, EPS, and NFE, the values in the module must not be altered
! between calls to GEAR.
!
! The counter NFE is provided so that the user can monitor the amount of work
! being done. Its value has no meaning to GEAR.
!
! GEAR automatically adjusts the stepsize and the order of the method so that
! the max norm of the vector with components local ERROR(I)/WT(I) is less than
! EPS for each step. The array WT allows one to specify an error test which
! is appropriate for the problem at hand.
!
! For example,
!   WT(I) = 1.0  specifies absolute error
!   WT(I) = DABS(Y(I,1)) specifies error relative to the most recent value of
!                the I-th component of the solution
!   WT(I) = DMAX1(WT(I),DABS(Y(I,1))) specifies error relative to the largest
!                magnitude yet achieved by the I-th component of the solution
!   WT(I) = DABS(Y(I,1))*RELERR/EPS+ABSERR/EPS, where EPS =
!                DMAX1(RELERR,ABSERR), specifies a mixed error test where
!                RELERR is relative error and ABSERR is absolute error
!
! All components of WT must be nonzero.
!
! Upon return, the value of ICRASH indicates the action which was taken.
!
!   ICRASH = 0 -- a step of length HOLD was successfully taken to the value
!      now in T.  The solution at T is in Y(*,1), and Y(*,2) contains the
!      derivatives multiplied by HOLD.
!   ICRASH = 1 -- no step was taken because H was smaller than permitted by
!      the machine precision. H was increased to an acceptable value.
!   ICRASH = 2 -- no step was taken because EPS was too small for the machine
!      precision. EPS was increased to an acceptable value.
!   ICRASH = 3 -- no step was taken because corrector convergence could not be
!      achieved at the smallest allowed stepsize. EPS is increased to a value
!      which allows the convergence test to be passed.
!   ICRASH = 4 -- no step was taken because the error test could not be
!      satisfied at the smallest allowed stepsize. EPS is increased to a
!      value which is achievable.
!
! First call to GEAR
! ------------------
! To begin the solution, the calling program must
!   1. Provide storage for the arrays Y(NEQN,7), W(NEQN,NEQN),
!      IPS(NEQN), WT(NEQN), YP(NEQN), C(NEQN), ERROR(NEQN), and SAVER(NEQN,7).
!   2. Place the initial values of the solution in
!      Y(1,1), Y(2,1), ..., Y(NEQN,1).
!   3. Set WT(1), ..., WT(NEQN) to nonzero values to provide
!      the error test desired.
!   4. Initialize the following variables in the COMMON block GEDATA
!         Time -- the starting value of the independent variable
!         H -- a nominal stepsize for the first step, indicating the
!            direction of integration and the maximum stepsize. H will be
!            reduced as necessary to meet the error criterion.
!         EPS -- the desired error tolerance
!         NEQN -- the number of equations
!         NFE -- set to 0 to begin a count of function calls
!         START -- set .TRUE.
! Subsequent calls to GEAR
! ------------------------
! GEAR returns with all information needed to continue the integration. To
! maintain relative error tests as described above, WT(*) must be updated
! after each step. Calling GEAR again then advances the solution another step.
! To continue integration using the revised stepsize or tolerance provided
! with an error return (ICRASH.NE.0), it is only necessary to call GEAR again.
!
! Normally, the integration is continued to the first step beyond the desired
! output point, and the solution is interpolated to the output point using the
! subroutine GINTRP. If it is impossible to integrate beyond the output point,
! H may be reduced to hit the output point. Otherwise, H should not be altered
! since changing H impairs the efficiency of the code. H must never be
! increased. EPS may be changed between calls, but large decreases should be
! avoided, since this will invalidate the step selection mechanism and lead
! to step failures.
use Gear_data
use Local_gear_data
use Floating_Point_Comparisons
Implicit None
integer :: NEQN,index,J,J1,I,IQ
! computational variables
real (kind (0D0)):: Y(NEQN,7),SAVER(NEQN,7),YP(NEQN),WT(NEQN),&
      ERROR(NEQN),C(NEQN),W(NEQN,NEQN), D, FOURU, RATIO, R1
integer :: IPS (NEQN)
real (kind (0D0)) :: ERTST(6) = (/2.0,4.5,7.333,10.42,13.7,17.15/)
! Note that the 10th entry of ANUM should be 25, not 24 (see p.217, Table 11.2
! in Gear, C.W. 1971. Numerical Initial Value Problems in Ordinary
! Differential Equations. Prentice-Hall, Englewood Cliffs, N.J.
real (kind (0D0)) :: ANUM(27) = (/1.0,1.0,2.0,3.0,1.0,6.0,11.0,6.0,1.0,25.0,&
   50.0,35.0,10.0,1.0,120.0,274.0,225.0,85.0,15.0,1.0,720.0,1764.0,1624.0,&
   735.0,175.0,21.0,1.0/)
real (kind (0D0)) :: ADEN(6) = (/-1.0,-3.0,-11.0,-50.0,-274.0,-1764.0/)
! BEGIN BLOCK 0  ******
call GRSUB0 (Y,SAVER,YP,WT,FOURU,NEQN)
if (ICRASH == 1 .or. ICRASH == 2) return
! BEGIN BLOCK 1  ******
Order: do ! If order has been changed, recompute coefficients A(*)
   if (K /= KOLD) then
     KP1 = K+1; index = (K*KP1)/2-1
     do J = 1, KP1
       J1 = index+J; A(J) = ANUM(J1)/ADEN(K)
     end do
     ITST = KP1; IWEVAL = 1; KOLD = K
   end if
   stepsize: do ! If the stepsize has been changed, revise Y
                ! to conform to the new stepsize.
      if (abs(abs(H)-abs(HOLD)) .GreaterThan. tiny(H)) then ! i.e., if H/=HOLD
        RATIO = H/HOLD; R1 = 1.0
        do J = 2, KP1
        R1 = R1*RATIO
          do I = 1, NEQN
            Y(I,J) = SAVER(I,J)*R1
          end do
        end do
        ITST = KP1; IWEVAL = 1
      end if
      BND = EPS/float(2*NEQN*(K+2)) ! Set limit for test of convergence
      ! BEGIN BLOCK 2  ******
      Newton: do  ! Solve for Y at Time+H by using Newton iteration
         call GRSUB2 (Y,W,IPS,WT,YP,C,ERROR,SAVER,FOURU,NEQN)
         if (ICRASH == 3) return
         if (.not. CONVRG) cycle Stepsize
         ! Convergence achieved. Test whether solution meets error tolerance.
         IWEVAL = 0; D = 0.0
         do I = 1, NEQN
           D = dmax1(D,dabs(ERROR(I)/WT(I)))
         end do
         D = D/(ERTST(K)*EPS)
         if (D .LessThanOrEqual. 1.0) then ! The step was successful.
               ! Store the stepsize used and correct the remaining
               ! components of Y.
            call GRSUB4 (Y,ERROR,WT,D,FOURU,NEQN)
            return
         end if
         ! BEGIN BLOCK 3  ******
         ! The step was not successful. The stepsize is reduced for the
         ! next step. If K >= 2, reduction of the order is also considered.
         call GRSUB3 (IQ,Y,SAVER,YP,D,WT,FOURU,NEQN)
         if (ICRASH == 4) return
         select case (IQ)
            case (1); cycle Order
            case (2); cycle Stepsize
            case (3); cycle Newton
         end select
      end do Newton
   end do Stepsize
end do Order
end Subroutine GEAR
