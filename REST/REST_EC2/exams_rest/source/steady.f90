Subroutine STEADY(Y)
! Revised 29 February 1984 (LAB) for scratch pad file handler.
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revisions 03-24-99--YSATL includes crystal energy term (see CKLOAD)
Use Implementation_Control
! STEADY computes the steady-state concentrations of chemicals in all system
! segments (via an iterative cascade), including internal transport effects
! and daughter product loadings. If solubility criteria are violated (as a
! result of drift loadings or product chemistry), the drift loads are reduced
! and the computations are repeated.
Use Floating_Point_Comparisons ! Revision 09-Feb-1999
Use Global_Variables
Use Local_Working_Space
Use Internal_Parameters
Use Rates_and_Sums
Use Process_Controls
Implicit None
Real (Kind (0D0)), Dimension(KOUNT,KCHEM) :: Y
! Local variables
Real (Kind (0D0)), Dimension(KOUNT,KCHEM) :: YSAV
! YSAV is used to store the values of Y between interations, for convergence
! testing of the linear cascade computation.
Real (Kind (0D0)) :: PRODLD, INTLDL, TEST, RELERR = 1.0D-09
! RELERR is relative error for convergence test
! PRODLD is autochthonous chemical loading. It is recomputed for each segment
! on each iteration of the steady-state computation.
Integer, Dimension(KOUNT) :: JJJ
! Counter for number of iterations executed while attempting to reduce drift
! loads and thus compute acceptable steady-state--if more than 5 are required
! the process is aborted.
Real :: CHECK, FACTR, SATST, TOTDRF
Integer :: I, II, J, JJ, K, KK, K2, LKOUNT
Logical :: Converged
! in case we encounter some primitive machinery, or some programmer
! gets carried away by delusions of infinite precision...
If (relerr .LessThan. Epsilon(relerr)) relerr = Epsilon(relerr)
! In this routine, only single values of the load matrices are needed
NDAT = MONTHG
JJJ = 0
Trials_loop: Do
   YSAV = 0.0D+00        ! Initialize values
      Y = 0.0D+00
   ! compute steady-state concentrations--allow for 10,000,000 trials
   Cascade: Do LKOUNT = 1, 10000000
      Converged = .True. ! Convergence criterion (all converged) indicator.
                         ! If NOT converged, this is set to .False. below.
      Chemical_cascade: Do K2 = 1, KCHEM
         Segment_cascade: Do J = 1, KOUNT
            ! Compute rate of generation (mg/L/hr) of current chemical due to
            ! transformation of other chemicals in this segment
            PRODLD = 0.0D+00
            Do I = 1, KCHEM
               PRODLD = PRODLD+YIELDL(K2,I,J)*Y(J,I)
            End Do
            ! Compute internal (i.e., between segments) transport loadings
            INTLDL = 0.0D+00
            Do I = 1, KOUNT
               INTLDL = INTLDL+INTINL(I,J,K2)*Y(I,K2)
            End Do
            ! Compute concentration
            Y(J,K2) = (CONLDL(J,K2)+INTLDL+PRODLD)/TOTKL(J,K2)
            ! Relative error tests to ensure that all compartments converged
            If (Y(J,K2) .NotEqual. 0.0) TEST = 1.0D+00 - YSAV(J,K2)/Y(J,K2)
            If (TEST .GreaterThan. RELERR) Converged = .False.
            YSAV(J,K2) = Y(J,K2)
         End Do Segment_cascade
      End Do Chemical_cascade
      ! If all segments and chemicals converged, exit loop
      If (Converged) Exit Cascade
   End Do Cascade
   
   If (.Not.Converged) Then ! Completion of the loop without convergence
      ! indicates a severe problem, e.g., persistent chemical in an ecosystem
      ! lacking carrier exports (e.g., a pond with evaporative water losses
      ! only). Therefore, EXAMS aborts the analysis and returns control to the
      ! user for evaluation.
      Write (stderr,fmt='(/A/A)')&
       ' Steady-state concentrations cannot be computed for this ecosystem.',&
       ' Try a system that includes an export flow.'
      IFLAG = 8
      Return
   End If
   ! Check final values; adjust drift loads if concentration limits exceeded
   ! Start from compartment 1 and proceed downstream,
   ! re-invoking the steady-state computation loop as required.
   Chemicals: Do K2 = 1, KCHEM
      Segments: Do J = 1, KOUNT
         II = -3   ! Load counter for locating distribution fractions (ALPHA)
         Species: Do I = 1, 7 ! There are 7 chemical species to be considered
            II = II+1  ! Increment counter for ALPHA address
            ! Increment the species loop if the current species doesn't occur
            If (SPFLGG(I,K2) == 0) Cycle Species
            ! Check for supersaturation (actually 50% of saturation to keep in
            ! range of linear isotherms)
            SATST = ALPHA(3*I+II,J,K2)*Y(J,K2)
            CHECK = 0.50*YSATL(I,J,K2) ! Includes crystal energy term (CKLOAD)
            If (SATST .LessThanOrEqual. CHECK) &
               Cycle Species ! this sp O.K., try the next
            ! Solubility limitations exceeded--reduce all drift loads
            ! and re-activate steady-state computations
            FACTR = 1.15*SATST/CHECK ! Factor for reducing loads
            ! 2. Report problem to user
            Write (stdout,fmt='(/A,I5,A)')&
            ' WARNING: Solubility criteria exceeded in system segment',J,'.'
            ! 3. Reduce drift loads if they are non-zero
            TOTDRF = Sum(DRFLDG(:,:,NDAT))
            ! If no drift loads are present, user will have to reduce other
            ! loads by hand--set flag to kill run and return to GHOST
            If (.Not. (TOTDRF.GreaterThan. 0.0)) Then
               IFLAG = 10
               Write (stdout,fmt='(/A/A)')&
                  '   Solubility criteria exceeded, cause not apparent.',&
                  '   Please reduce loads and try again.'
               Return
            End If
            ! Reduce drift loads and recalculate total loadings
            SYSLDL = 0.0
            DRFLDG = DRFLDG/FACTR
            Do KK = 1, KCHEM
               Do JJ = 1, KOUNT ! Re-evaluate total load
                  TOTLDL(JJ,KK) = SEELDG(JJ,KK,NDAT)+STRLDG(JJ,KK,NDAT)+&
                     NPSLDG(JJ,KK,NDAT)+PCPLDG(JJ,KK,NDAT)+DRFLDG(JJ,KK,NDAT)
                  CONLDL(JJ,KK) = 1.0D+06*TOTLDL(JJ,KK)/WATVOL(JJ)
                  SYSLDL(KK) = SYSLDL(KK)+TOTLDL(JJ,KK)
               End Do
            End Do
            Write (stdout,fmt='(/A,1PG11.4/)')&
               ' Drift loads have been reduced by a factor of ',FACTR
            JJJ(J) = JJJ(J)+1
            If (JJJ(J) <= 5) Then ! try again with reduced loads
               Cycle Trials_loop
            Else ! if all the other loads have been set up at saturation, this
                 ! could be a fruitless exercise, so if 5 trials didn't do it
               Write (stdout,fmt='(/A)')&
                  ' However, this does not seem to be working:'
               IFLAG = 10
               Write (stderr,fmt='(/A/A)')&
                  '   Solubility criteria exceeded, cause not apparent.',&
                  '   Reduce loads and try again.'
               Return
            End If
         End Do Species
      End Do Segments
   End Do Chemicals
   Exit Trials_loop ! if arrive at this point, problem is completed
End Do Trials_loop

! Acceptable steady-state values computed. Set external loads (CONLDL)
CONLDL = 0.0D+00    ! to zero for the integrators that evaluate persistence.
! Compute autochthonous chemical loadings resulting from transformation
! processes. (Needed in kg/hr for compatibility with allochthonous chemical
! loadings (SYSLDL), hence multiplication of result by 1.E-6 on exit from
! computation loop.)
TRANLD = 0.0
Do K = 1, KCHEM
   Do J = 1, KOUNT
      Do I = 1, KCHEM
         TRANLD(K) = TRANLD(K)+YIELDL(K,I,J)*Y(J,I)*WATVOL(J)
      End Do
   End Do
End Do
TRANLD = TRANLD*1.E-06
Return
End Subroutine STEADY
