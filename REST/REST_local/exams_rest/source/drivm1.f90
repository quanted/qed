subroutine DRIVM1()
! File drivm1.f90
! The "driver" for EXAMS' mode 1 integration subroutines
! Revised 27-DEC-1985 (L.A. Burns)
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revisions 08-Feb-1999 to use floating point comparisons
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
! TFIX has number of hours in an hour, day, month, and year
! (TFIX is used only in modes 1 and 2.)
integer :: K
character(len=5), dimension(4) :: PIECE = & ! Time trace header
   (/'Hours','Days ','Month','Years'/)

Return_code: select case (IBACK)

case (1) Return_code ! initial entry
   ! STIFEQ is used to force an immediate branch to the stiff equation
   ! integrator for CONTINUations of problems already shown to be
   ! stiff. The need for this was was demonstrated by study of
   ! extremely stiff photo-chemical problems; these caused the RKF
   ! and ADAM routines to fail on second calls. STIFEQ is
   ! initialized as .false. in module Local_Working_Space.
   ABEXIT = .false. ! Reset indicator of ABnormal EXIT
   Reporting: if (RPTFIL) then
   ! Set up page header for report on temporal simulation
   write (RPTLUN,fmt='(A,A,A,I2/A)')&
      '1Exposure Analysis Modeling System -- EXAMS Version ',&
      VERSN,', Mode',MODEG,' Ecosystem: '//trim(ECONAM)
   do K = 1, KCHEM
      write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(K))
   end do
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt='(A/A)')&
      ' Table 19.  Summary time-trace of dissipation of steady-state',&
      '   chemical mass following termination of allochthonous loadings.'
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt='(A,4(/A))')& ! Column headers
      '   Time     Average Chemical Concentrations    Total Chemical Mass',&
      '   -----    -------------------------------    -------------------',&
      '   '//PIECE(KDTIME)//&
              '  Water Column      Benthic Sediments   Water Col  Benthic',&
      '      -------------------- -------------------  --------- --------',&
      '      Free-mg/L Sorb-mg/kg Pore-mg/L Sed-mg/kg  Total kg  Total kg'
   write (RPTLUN,5020) ! dashed line
   end if Reporting

   ! Load upper bytes of TINIT with zero
   ! T set to zero in FLXOUT in steady-state mode (MODEG=1).
   TINIT = T*1.0D+00
   if (STIFEQ) then
      ! call GEAR integrator
      IBACK = 3
      ISOO = 2
   else
      ! Call ADAM integrator
      IBACK = 2
      ISOO = 1
   end if
   return

case (2) Return_code ! return from ADAM-PECE integrator
   ! Normal return - integration from TINIT to TENDL complete,
   ! IFLAG=2: (if for some reason (user revisions) the mesh points
   ! do not include TENDL, both TENDL and TENDG are updated).
   if (T .GreaterThan. TENDL) TENDL = T
   TENDG = TENDL
   if (IFLAG == 2) then
      TENDG = TENDG/TFIX(TCODEG) ! Convert TENDG from hours to input units
      ISOO = 0 ! Set flag to show integrator finished
      return
   end if
   ! Abnormal termination of integration
   if (IFLAG >= 8) then             ! 1. Fatal error on integrator
      call Integrator_failure       ! write message and return 
      return
   end if
   if (IFLAG == 6) then ! 2. Return due to stiff equations
      TINIT = T         ! Set new time frame
      IBACK = 3         ! Call STIFF integrator to continue integration
      ISOO = 2
      return
   end if
   ! 3. Abnormal return from non-stiff equations: determine if
   ! partial data is available. If so, write advisory message to
   ! user and return. If not, set IFLAG to cancel persistence
   ! computations in "SUMUP" and return.
   ! Test for partial data -- TPRINT is the next output point
   TITEST = TPRINT-TINCRL
   if (TITEST .GreaterThan. 0.0) then  ! Partial data available
      write (stderr,fmt='(/A/A)')&
         ' The kinetic equations are causing difficulties;',&
         ' the decay simulation has been abbreviated.'
      if (TITEST .LessThan. TENDL) TENDL = TITEST
      TENDG = TENDL
      IFLAG = 2
      TENDG = TENDG/TFIX(TCODEG) ! Convert TENDG from hours to input units
      ISOO = 0 ! Set flag to show integrator finished
      return
   else ! Integrator failed to reach first mesh point
      call Integrator_failure
      return
   end if

case (3) Return_code ! Return from Gear's method stiff equation integrator
   if (T .GreaterThan. TENDL) TENDL = T
   TENDG = TENDL
   if (IFLAG == 2) then          ! Normal return
      TENDG = TENDG/TFIX(TCODEG) ! Convert TENDG from hours to input units
      ISOO = 0                   ! Set flag to show integrator finished
      return
   end if
   ! Analyze abnormal returns:
   if (IFLAG >= 8) then             ! 1. Fatal error on integrator
      call Integrator_failure       ! write message and return
      return
   end if
   ! 2. Integrator timed out, but partial data may be available
   TITEST = TPRINT-TINCRL              ! Test for partial data
   if (TITEST .GreaterThan. 0.0) then  ! Partial data available
      write (stderr,fmt='(/A/A)')&
         ' The kinetic equations are causing difficulties;',&
         ' the decay simulation has been abbreviated.'
      if (TITEST .LessThan. TENDL) TENDL = TITEST
      TENDG = TENDL
      IFLAG = 2
      TENDG = TENDG/TFIX(TCODEG) ! Convert TENDG from hours to input units
      ISOO = 0                   ! Set flag to show integrator finished
      return
   else
      call Integrator_failure
      return
   end if
end select Return_code
5020  format (1X,77('-')) ! dashed line

contains
Subroutine Integrator_failure
   IFLAG = 9 ! Analysis of kinetics (in "SUMUP" skipped if IFLAG >= 8
   write (stderr,fmt='(/A)')&
     ' Integrator failed--persistence information not computed.'
   IUNITG = 1 ! Turn on integrator diagnostics
   write (stderr,fmt='(/A)')&
      ' Integrator diagnostics now switched on (IUNIT=1).'
   TENDG = TENDG/TFIX(TCODEG) ! Convert TENDG from hours back to input units
   ISOO = 0 ! Set flag to show integrator finished
end Subroutine Integrator_failure

end Subroutine DRIVM1
