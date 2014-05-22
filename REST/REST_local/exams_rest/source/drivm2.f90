subroutine DRIVM2()
! File drivm2.f90
! The "driver" for EXAMS' mode 2 integration subroutines.
! Created 12.XII.1983 (L.A. Burns) by disaggregation of DRIVER.
! Revised 27-DEC-1985 (LAB)
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revisions 02/05/99 -- floating point comparisons
! Revised 05-Jan-2001 -- new method to capture partial results
use Implementation_Control
use Integrator_Working_Storage
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Floating_Point_Comparisons
Implicit None
real (kind (0D0)) :: TITEST
real, dimension(4) :: TFIX = (/1.0, 24.0, 730.5, 8766.0/)
! TFIX is factor for keeping track of temporal units;
! TFIX has number of hours in an hour, day, month, and year.
! (TFIX is used only in modes 1 and 2.)
integer :: I, K
! I and K are general counters.
! Variable FORMAT for time trace header:
character(len=7), dimension(4) :: PIECE = &
   (/'hours. ','days.  ','months.','years. '/)

! On each entry to DRIVM2, a block of time steps are to be computed.
! The non-state-variable output variables for FGETS, BASS, and HWIR
! are calculated here and then reported via output sequences in OUTP.

Return_code: select case (IBACK)

case (1) Return_code ! Initial call
   ! STIFEQ is used to cause an immediate branch to the stiff equation
   ! integrator for CONTINUations of problems already shown to be
   ! stiff. The need for this was was demonstrated by study of
   ! extremely stiff photochemical problems; these caused the RKF and
   ! ADAM routines to fail on second calls.  STIFEQ is initialized as
   ! .false. in module Local_Working_Space.
   ! When reentering from integrator abort, skip page headers
   if (.not.ABEXIT) then ! Set up page header for temporal simulation
      Reporting: if (RPTFIL) then
      write (RPTLUN,fmt='(A,A,A,I2/A)')&
         '1Exposure Analysis Modeling System -- EXAMS Version ',&
         VERSN,', Mode',MODEG,&
         ' Ecosystem: '//trim(ECONAM)
      do K = 1, KCHEM
         write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(K))
      end do
      write (RPTLUN,5020) ! dashed line
      I = TINITG

      K = TENDG
      write (RPTLUN,fmt='(A/A,I0,A,I0,A)')&
      ' Table 19.  Summary time-trace of chemical concentrations during',&
      '   the period from ',I,' through ',K,' '//PIECE(KDTIME)
      write (RPTLUN,5020) ! dashed line
      write (RPTLUN,fmt='(A/A/A,A5,A/A/A)') & ! Column headers
         '   Time     Average Chemical Concentrations    Total Chemical Mass',&
         '   -----    -------------------------------    -------------------',&
   
         '   ',PIECE(KDTIME),&
               '   Water Column      Benthic Sediments  Water Col  Benthic',&
         '       -------------------- ------------------- --------- --------',&
         '       Free-mg/L Sorb-mg/kg Pore-mg/L Sed-mg/kg  Total kg Total kg'
      write (RPTLUN,5020) ! dashed line
      end if Reporting
   end if
   ABEXIT = .false. ! Reset indicator of ABnormal EXIT
   ! T set to proper number of hours in CKICM2 in mode 2.
   TINIT = T
   ! If the problem has been diagnosed as stiff,
   ! invoke the stiff integrator at once
   if (STIFEQ) then
      TINIT = T      ! Set time frame
      IBACK = 3      ! Call STIFF integrator
      ISOO = 2
   else ! Call ADAM integrator
      IBACK = 2
      ISOO = 1
   end if
   return

case (2) Return_code ! Return from ADAM_PECE integration
   ! Normal return - integration from TINIT to TENDL complete, IFLAG=2
   ! If for some reason (programmer oversight or batch entry) the mesh points
   ! do not include TENDL, do a (fail-safe) update on TENDL and TENDG.
   if (T .GreaterThan. TENDL) TENDL = T
   TENDG = TENDL
   if (IFLAG == 2) then
      TENDG = TENDG/TFIX(TCODEG) ! Convert TENDG from hours to input units
      ISOO = 0 ! Set flag to show integration completed
      return
   end if
   ! Abnormal termination of integration

!   if (IFLAG == 10) return   ! OUTP detected violation of isotherm linearity
!   2005-03-16: recommends Freundlich isotherm and continues

   if (IFLAG >= 8) then      ! Fatal error on integrator
     call Integrator_Failed  ! write message and return
     return
   end if
   ! 2. Return due to stiff equations: transfer to stiff integrator -
   if (IFLAG == 6) then ! Stiff equations
      STIFEQ = .true. ! Set flag to show that problem is stiff
      TINIT = T       ! Set new time frame
      IBACK = 3       ! Call STIFF integrator
      ISOO = 2
      return
   end if
   ! 3. Abnormal return from non-stiff equations: determine if
   ! partial data are available, write message, and return
   TITEST = TPRINT-TINCRL                  ! Test for partial data
   if (TITEST .GreaterThan. 0.0) then      ! Partial data available
      write (stderr,fmt='(/A/A,I2,A/A)')&
         ' The kinetic equations are causing difficulties',&
         ' (The integrator returned IFLAG as',IFLAG,'.)',&
         ' The decay simulation has been abbreviated.'
      if (TITEST .LessThan. TENDL) TENDL = TITEST
      TENDG = TENDL
      IFLAG = 2
      TENDG = TENDG/TFIX(TCODEG) ! Convert TENDG from hours to input units
      ISOO = 0 ! Set flag to show integration completed
   else ! Integrator failed to reach first mesh point
      call Integrator_Failed
    end if
   return

case (3) Return_code ! from Gear's method stiff equation solver
   if (T .GreaterThan. TENDL) TENDL = T
   TENDG = TENDL
   if (IFLAG == 2) then          ! Normal return
      TENDG = TENDG/TFIX(TCODEG) ! Reconvert TENDG from hours to input units
      ISOO = 0                   ! Set flag to show integration completed
      return
   end if
   ! Analyze abnormal returns
   if (IFLAG >= 8) then            ! Fatal error on integrator
     call Integrator_Failed        ! write message and return
     return
   end if
   ! 2. Integrator timed out, but partial data may be available
   TITEST = TPRINT-TINCRL                ! Test for partial data
   if (TITEST .GreaterThan. 0.0) then    ! Partial data available
      write (stderr,fmt='(/A/A)')&
         ' The kinetic equations are causing difficulties;',&
         ' the decay simulation has been abbreviated.'
      if (TITEST .LessThan. TENDL) TENDL = TITEST
      TENDG = TENDL
      IFLAG = 2
      TENDG = TENDG/TFIX(TCODEG) ! Reconvert TENDG from hours to input units
      ISOO = 0                   ! Set flag to show integration completed
      return
   else                            ! total integrator failure;
     call Integrator_Failed        ! write message and return
     return
   end if
end select Return_code
return
5020  format (1X,77('-')) ! dashed line

contains
subroutine Integrator_Failed
   ! If total integrator failure, write message and return
!   IFLAG = 8
!   IFLAG = 2 ! Reset error flag for CONTINUE command
   TITEST = TPRINT-TINCRL
   if (TITEST .LessThan. TENDG) TENDG = TITEST
   write (stderr,fmt='(/A)')&
      ' Integrator failed to reach the requested output point.'
   write (stdout,fmt='(/A)') &
      ' Integrator diagnostics now switched on (IUNIT=1).'
   IUNITG = 1
   TENDG = TENDG/TFIX(TCODEG) ! Convert TENDG from hours back to input units
   ISOO = 0                   ! Set flag to show integrator finished
end subroutine Integrator_failed

end Subroutine DRIVM2
