subroutine STEP(Y,YP,WT,PHI,FOURU,NEQN)
! Revised 7 June 1982 by L.A. Burns
! Revised 30-AUG-1985 (LAB)
! Revised 05-Feb-1999 to use floating point comparisons
! Revised 2004-04-09 to remove "P" from caling sequence (also in ADAM)
! Subroutine STEP uses a modified divided difference form of an Adams PECE
! method (of Order <= 12) to perform one step in the integration of a system
! of NEQN first order ordinary differential equations:
!  DY/DX = F(X,Y) ,  Y = (Y(1),Y(2),...,Y(NEQN))
! Local extrapolation is used to improve stability and accuracy.
!
! To specify the differential equations to be solved, the user must supply a
! subroutine, denoted here by F, to calculate the NEQN derivatives DY(I)/DX.
! F must be of the form F(X,Y,YP), where Y and YP are arrays each of
! dimension NEQN. F must calculate the values of the derivatives DY(I)/DX at
! (X,Y) and place them in YP. X and Y must not be altered by F.
!
! Information is exchanged with STEP both through the argument
! list and through the module Step_data
!
! The parameters in the argument list are
!   F -- the name of the user-supplied subroutine to calculate the derivative
!   Y -- an array of dimension NEQN which contains the solution. Its value
!     must not be altered between calls to STEP.
!   YP -- an array of dimension NEQN which contains the derivative of the
!     solution after a successful step. Its value need not be preserved
!     between steps.
!   WT -- an array of dimension NEQN used in specifying the error test.
!   PHI -- an array of dimensions (NEQN,16) which contains the modified
!      divided differences. PHI(*,15) and PHI(*,16) are used for propagated
!      roundoff control. PHI must not be changed between calls.
!   P -- an array of dimension NEQN used for working storage. Its value is not
!      needed for subsequent calls.
!
! The parameters in the module Step_data are:
!  X -- the independent variable
!  H -- the stepsize to be used in attempting the next step
!  HOLD -- the stepsize used for the last successful step
!  EPS -- the desired tolerance for the error test
!  NEQN -- the number of equations being integrated
!  KOLD -- the order of the method used for the last successful step
!  ICRASH -- an indicator of error conditions upon return
!  K -- the order of the method to be used for the next step
!  NFE -- a counter which is incremented by 1 after each call to F
!  START -- a logical which must be set .TRUE. on the first call to step
!  ALPHA(12), BETA(12), G(13), SIG(13), V(12), W(12), PSI(12), NS, NORND,
!     PHASE1 -- quantities used for internal bookkeeping by STEP whose values
!     are needed for continuing integration. Their values are normally of no
!     interest to the user. NORND and PHASE1 are logical variables.
!
! Except for H, EPS, and NFE, the values in the module must not be altered
! between calls to STEP.
!
! The counter NFE is provided so that the user can monitor the amount of work
! being done. Its value has no meaning to STEP.
!
! STEP automatically adjusts the stepsize and the order of the method so that
! the max norm of the vector with components local ERROR(I)/WT(I) is less than
! EPS for each step. The array WT allows the user to specify an error test
! which is appropriate for the problem.
!
! For example,
!  WT(I) = 1.0  specifies absolute error
!  WT(I) = DABS(Y(I)) specifies error relative to the most recent value of the
!    I-th component of the solution
!  WT(I) = DMAX1(WT(I),DABS(Y(I))) specifies error relative to the largest
!     magnitude yet achieved by the I-th component of the solution
!  WT(I) = DABS(Y(I))*RELERR/EPS+ABSERR/EPS, where EPS = DMAX1(RELERR,ABSERR),
!     specifies a mixed error test where RELERR is relative error and ABSERR
!     is absolute error
!  All components of WT must be nonzero.
!
!  Upon return, the value of ICRASH indicates the action which was taken.
!  ICRASH = 0 -- a step of length HOLD was successfully taken to the value now
!     in X. The solution at X is in Y, and YP contains the derivatives. The
!     derivatives are also in PHI(*,1).
!  ICRASH = 1 -- no step was taken because H was smaller than permitted by
!     the machine precision. H was increased to an acceptable value.
!  ICRASH = 2 -- no step was taken because EPS was too small for the machine
!     precision. EPS was increased to an acceptable value.
!  ICRASH = 3 -- no step was taken because the error test could not be
!     satisfied at the smallest allowed stepsize. EPS is increased to a value
!     which is achievable.
!
!  First call to STEP
!  ------------------
!  To begin the solution, the calling program must
!   1. Provide storage for the arrays Y(NEQN), YP(NEQN),
!       WT(NEQN), PHI(NEQN,16), and P(NEQN).
!   2. Place the initial values of the solution in Y.
!   3. Set WT(1), ..., WT(NEQN) to nonzero values to provide
!      the error test desired.
!   4. Initialize the following variables in the module Step_data
!      X -- the starting value of the independent variable
!      H -- a nominal stepsize for the first step, indicating the direction
!           of integration and the maximum stepsize. H will be reduced as
!           necessary to meet the error criterion.
!      EPS -- the desired error tolerance
!      NEQN -- the number of equations
!      NFE -- set to 0 to begin a count of function calls
!      START -- set .TRUE.
!
! Subsequent calls to STEP
! ------------------------
! STEP returns with all information needed to continue the integration. To
! maintain relative error tests as described above, WT(*) must be updated
! after each step. Calling STEP again then advances the solution another step.
! To continue integration using the revised stepsize or tolerance provided
! with an error return (ICRASH /= 0), it is only necessary to call STEP again.
!
! Normally, the integration is continued to the first step beyond the desired
! output point, and the solution is interpolated to the output point using the
! subroutine SINTRP. If it is impossible to integrate beyond the output point,
! H may be reduced to hit the output point. Otherwise, H should not be
! altered, since changing H impairs the efficiency of the code. H must never
! be increased. EPS may be changed between calls, but large decreases should
! be avoided, since this will invalidate the step selection mechanism and lead
! to step failures.
!
use Step_data
use Floating_Point_Comparisons
Use Define_f
Implicit None
real (kind (0D0)) :: ABSH,ERK,ERKM1,ERKM2,ERKP1,err,HNEW,R,REALNS,RHO,&
   ROUND,Sum_total,TAU,TEMP1,TEMP2,TEMP3,TEMP4,TEMP5,TEMP6,XOLD,FOURU
integer :: NEQN,L,IFAIL,KP1,KP2,KM1,KM2,NSP1,I,IM1,IQ,NSM2,J,LIMIT1,&
   NSP2,LIMIT2,IP1,KNEW
real (kind (0D0)) :: Y(NEQN),WT(NEQN),PHI(NEQN,16),P(NEQN),YP(NEQN)
real (kind (0D0)), dimension (12) :: TWO = &
  (/8.0,16.0,32.0,64.0,128.0,256.0,512.0,1024.0,2048.0,4096.0,8192.0,16384.0/)
!real (kind (0D0)), dimension (13) :: GSTR = &
!  (/0.5,0.0833,0.0417,0.0264,0.0188,0.0143,0.0114,0.00936,0.00789,0.00697,&
!    0.00592,0.00524,0.00468/)
real (kind (0D0)), dimension (13), parameter :: GSTR = (/ 0.500D+00,&
1.0D+00/12.0D+00, 1.0D+00/24.0D+00, 19.0D+00/720.0D+00, 3.0D+00/160.0D+00,&
863.0D+00/60480.0D+00, 275.0D+00/24192.0D+00, 33953.0D+00/3628800.0D+00,&
8183.0D+00/1036800.0D+00, 3250433.0D+00/479001600.0D+00, &
4671.0D+00/788480.0D+00, 13695779093.0D+00/2615348736000.0D+00,&
2224234463.0D+00/475517952000.0D+00 /)
!****************************************************************
!  BEGIN BLOCK 0  ******
!***********************
! See if stepsize or error tolerance is too small for machine precision.
! If first step, initialize PHI array and estimate a starting stepsize.
! If stepsize is too small, determine an acceptable one.
if (dabs(H) .LessThan. FOURU*dabs(X)) then
   H = dsign(FOURU*dabs(X),H)
   ICRASH = 1
   return
end if
! If error tolerance is too small, increase it to an acceptable value
ROUND = 0.0
do L = 1, NEQN
   ROUND = dmax1(ROUND,dabs(Y(L)/WT(L)))
end do
ROUND = FOURU*ROUND
if (EPS .LessThan. ROUND) then
   EPS = ROUND*(1.0+FOURU)
   ICRASH = 2
   return
endif
ICRASH = 0
IFAIL =  0
G(1)   = 1.0
G(2)   = 0.5
SIG(1) = 1.0
Not_initialized: if (START) then ! Initialize--Compute stepsize for first step
   call FCT (X,Y,YP)
   NFE = NFE+1
   Sum_total = 0.0
   do L = 1, NEQN
      PHI(L,1) = YP(L)
      PHI(L,2) = 0.0
      Sum_total = dmax1(Sum_total,dabs(YP(L)/WT(L)))
   end do
   ABSH = dabs(H)
   if (EPS .LessThan. 16.0*Sum_total*H*H) ABSH = 0.25*dsqrt(EPS/Sum_total)
   H = dsign(dmax1(ABSH,FOURU*dabs(X)),H)
   HOLD = 0.0
   K = 1
   KOLD = 0
   START = .false.
   PHASE1 = .true.
   NORND = .true.
   if (EPS .LessThanOrEqual. 200.0*ROUND) then
      NORND = .false.
      do L = 1, NEQN
         PHI(L,15) = 0.0
      end do
   endif
End if Not_initialized
!***********************
!  END BLOCK 0    ******
!****************************************************************
!  BEGIN BLOCK 1  ******
!***********************
! Compute coefficients of formulas for this step. Avoid computing those
! quantities not changed when stepsize is not changed.
Take_a_step: do
   KP1 = K+1
   KP2 = K+2
   KM1 = K-1
   KM2 = K-2
   ! NS is the number of steps taken with size H, including the
   ! current one. When K < NS, no coefficients change.
   if (abs(H-HOLD) .GreaterThan. 0.0) NS = 0
   NS = min0(NS+1,KOLD+1)
   NSP1 = NS+1
   changed: if (K >= NS) then ! Compute those components of ALPHA(*), BETA(*),
      BETA(NS) = 1.0          ! PSI(*), and SIG(*) which are changed.
      REALNS = NS
      ALPHA(NS) = 1.0/REALNS
      TEMP1 = H*REALNS
      SIG(NSP1) = 1.0
      do I = NSP1, K
         IM1 = I-1
         TEMP2 = PSI(IM1)
         PSI(IM1) = TEMP1
         BETA(I) = BETA(IM1)*PSI(IM1)/TEMP2
         TEMP1 = TEMP2+H
         ALPHA(I) = H/TEMP1
         SIG(I+1) = float(I)*ALPHA(I)*SIG(I)
      end do
      PSI(K) = TEMP1
      ! Compute coefficients G(*)
      ! Initialize V(*) and set W(*).
      if (NS <= 1) then
         do IQ = 1, K
            TEMP3 = IQ*(IQ+1)
            V(IQ) = 1.0D+00/TEMP3
            W(IQ) = V(IQ)
         end do
      else ! If order was raised, update diagonal part of V(*).
         if (K > KOLD) then
            TEMP4 = K*KP1
            V(K) = 1.0/TEMP4
            NSM2 = NS-2
            do J = 1, NSM2
               I = K-J
               V(I) = V(I)-ALPHA(J+1)*V(I+1)
            end do
         end if
         ! Update V(*) and set W(*).
         LIMIT1 = KP1-NS
         TEMP5 = ALPHA(NS)
         do IQ = 1, LIMIT1
            V(IQ) = V(IQ)-TEMP5*V(IQ+1)
            W(IQ) = V(IQ)
         end do
         G(NSP1) = W(1)
      end if
      ! Compute the G(*) in the work vector W(*).
      NSP2 = NS+2
      do I = NSP2, KP1
         LIMIT2 = KP2-I
         TEMP6 = ALPHA(I-1)
         do IQ = 1, LIMIT2
            W(IQ) = W(IQ)-TEMP6*W(IQ+1)
         end do
         G(I) = W(1)
      end do
   end if Changed
   !***********************
   !  END BLOCK 1    ******
   !****************************************************************
   !  BEGIN BLOCK 2  ******
   !***********************
   ! Predict a solution P(*), evaluate derivatives using predicted solution,
   ! and estimate local error at order K and errors at orders K, K-1, K-2 as
   ! if constant stepsize were used.
   ! Change PHI to PHI STAR.
   do I = NSP1, K
      TEMP1 = BETA(I)
      do L = 1, NEQN
         PHI(L,I) = TEMP1*PHI(L,I)
      end do
   end do
   ! Predict solution and differences.
   do L = 1, NEQN
      PHI(L,KP2) = PHI(L,KP1)
      PHI(L,KP1) = 0.0
      P(L) = 0.0
   end do
   do J = 1, K
      I = KP1-J
      IP1 = I+1
      TEMP2 = G(I)
      do L = 1, NEQN
         P(L) = P(L)+TEMP2*PHI(L,I)
         PHI(L,I) = PHI(L,I)+PHI(L,IP1)
      end do
   end do
   if (NORND) then
      do L = 1, NEQN
         P(L) = Y(L)+H*P(L)
      end do
   else
      do L = 1, NEQN
         TAU = H*P(L)-PHI(L,15)
         P(L) = Y(L)+TAU
         PHI(L,16) = (P(L)-Y(L))-TAU
      end do
   end if
   XOLD = X
   X = X+H
   ABSH = dabs(H)
   call FCT (X,P,YP)
   NFE = NFE+1
   ! Estimate errors at orders K, K-1, K-2.
   ERKM2 = 0.0
   ERKM1 = 0.0
   ERK = 0.0
   do L = 1, NEQN
      TEMP3 = 1.0/WT(L)
      TEMP4 = YP(L)-PHI(L,1)
      if (KM2 >= 0) then
         if (KM2 > 0) ERKM2 = dmax1(ERKM2,dabs((PHI(L,KM1)+TEMP4)*TEMP3))
         ERKM1 = dmax1(ERKM1,dabs((PHI(L,K)+TEMP4)*TEMP3))
         ERK = dmax1(ERK,dabs(TEMP4*TEMP3))
      end if
   end do
   if (KM2 >= 0) then
      if (KM2 > 0) ERKM2 = ABSH*SIG(KM1)*GSTR(KM2)*ERKM2
      ERKM1 = ABSH*SIG(K)*GSTR(KM1)*ERKM1
   end if
   TEMP5 = ABSH*ERK
   err = TEMP5*(G(K)-G(KP1))
   ERK = TEMP5*SIG(KP1)*GSTR(K)
   if ((KM2==0 .and. (ERKM1 .LessThanOrEqual. 0.5*ERK)) .or. &
       (KM2 > 0  .and. (dmax1(ERKM1,ERKM2) .LessThanOrEqual. ERK)))then
      KNEW = KM1
   else
      KNEW = K
   end if
   !***********************
   !  END BLOCK 2    ******
   !****************************************************************
   !  BEGIN BLOCK 3  ******
   !***********************
   if (err .GreaterThan. EPS) then ! The step is unsuccessful.
      ! Restore X, PHI(*,*), PSI(*). If third consecutive failure set order to
      ! one. If step fails more than three times, consider an optimal
      ! stepsize. Double error tolerance and return if estimated stepsize is
      ! too small for machine precision.
      PHASE1 = .false.
      X = XOLD          ! Restore X, PHI(*,*), and PSI(*)
      do I = 1, K
         TEMP1 = 1.0/BETA(I)
         IP1 = I+1
         do L = 1, NEQN
            PHI(L,I) = TEMP1*(PHI(L,I)-PHI(L,IP1))
         end do
      end do
      if (K >= 2) then
         do I = 2, K
            PSI(I-1) = PSI(I)-H
         end do
      end if
      ! On third failure, set order to one. Thereafter, use optimal stepsize.
      IFAIL = IFAIL+1
      TEMP2 = 0.5
      if (IFAIL >= 3) then
         if (IFAIL>3 .and. (EPS.LessThan.0.5*ERK)) TEMP2 = dsqrt(0.5*EPS/ERK)
         KNEW =1
      end if
      H = TEMP2*H
      K = KNEW
      if (dabs(H) .GreaterThanOrEqual. FOURU*dabs(X)) cycle Take_a_step
      ICRASH = 3
      H = dsign(FOURU*dabs(X),H)
      EPS = EPS+EPS
      return
      !***********************
      !  END BLOCK 3    ******
      !****************************************************************
      !  BEGIN BLOCK 4  ******
      !***********************
   else ! The step is successful (err <= EPS).
        ! Correct the predicted solution, evaluate the derivatives
        ! using the corrected solution, and update the differences.
        ! Determine best order and stepsize for the next step.
      KOLD = K
      HOLD = H
      !  Correct and evaluate.
      TEMP1 = H*G(KP1)
      if (NORND) then
         do L = 1, NEQN
            Y(L) = P(L)+TEMP1*(YP(L)-PHI(L,1))
         end do
      else
         do L = 1, NEQN
            RHO = TEMP1*(YP(L)-PHI(L,1))-PHI(L,16)
            Y(L) = P(L)+RHO
            PHI(L,15) = (Y(L)-P(L))-RHO
         end do
      end if
      
      call FCT (X,Y,YP)
      NFE = NFE+1
      ! Update differences for next step
      do L = 1, NEQN
         PHI(L,KP1) = YP(L)-PHI(L,1)
         PHI(L,KP2) = PHI(L,KP1)-PHI(L,KP2)
      end do
      do I = 1, K
         do L = 1, NEQN
            PHI(L,I) = PHI(L,I)+PHI(L,KP1)
         end do
      end do
      ! Estimate error at order K+1 unless, in starting phase when order is
      ! always raised, already decided in block 2 to lower order, stepsize
      ! is not constant so estimate would be unreliable.
      ERKP1 = 0.0
      if (KNEW==KM1 .or. K==12) PHASE1 = .false.
      if (PHASE1) then
         K = KP1
         ERK = ERKP1
         HNEW = H + H
         H = HNEW
         return
      end if
      if (KNEW == KM1) then
         K = KM1
         ERK = ERKM1
      elseif (KP1 <= NS) then
         do L = 1, NEQN
            ERKP1 = dmax1(ERKP1,dabs(PHI(L,KP2)/WT(L)))
         end do
         ERKP1 = ABSH*GSTR(KP1)*ERKP1
         ! Using estimated error at order K+1,
         ! determine appropriate order for next step
         if (K > 1) then
            if (ERKM1 .LessThanOrEqual. dmin1(ERK,ERKP1)) then ! lower order
               K = KM1
               ERK = ERKM1
            elseif ((ERKP1 .LessThan. ERK) .and. K/=12) then
               ! Here ERKP1 < ERK < dmax1(ERKM1,ERKM2), else order would
               ! have been lowered in block 2. Thus, order is raised.
               K = KP1
               ERK = ERKP1
            endif
         elseif (ERKP1 .LessThan. (0.5*ERK)) then ! raise order
            K = KP1
            ERK = ERKP1
         endif
      end if
      ! With new order determine appropriate stepsize for next step.
      HNEW = H+H
      if (EPS .LessThan. (ERK*TWO(K))) then
         HNEW = H
         if (EPS .LessThan. (2.0D+00*ERK)) then
            R = (0.5*EPS/ERK)**(1.0/float(K+1))
            if (R .GreaterThan. 0.9) R = 0.9
            if (R .LessThan.    0.5) R = 0.5
            HNEW = dsign(dmax1(ABSH*R,FOURU*dabs(X)),H)
         end if
      end if
      H = HNEW
      return
      !***********************
      !  END BLOCK 4    ******
      !****************************************************************
   end if
end do Take_a_step
return
end Subroutine STEP
