subroutine WATADV(TOTIN,WATINL)
! WATADV uses gaussian elimination to calculate the total advection of water
! among system segments and the magnitude of net advective exports.
! Revised 30 July 1982 by L.A. Burns
! Revised 11 July 1983 (LAB) for mode 3 operations.
! Revisions 10/22/88--run-time implementation of machine dependencies
use Implementation_Control; use Global_Variables; use Local_Working_Space
use Internal_Parameters; use Rates_and_Sums
use Floating_Point_Comparisons ! revision 08-Feb-1999
Implicit None
! Local variables
real (kind (0D0)), allocatable, dimension (:,:) ::  AMAT 
real (kind (0D0)) :: SAVER
integer :: I, J, K, KK, KEXCH, KOUNT1, LL, M, N
real :: COLTOT
real, intent (in) :: TOTIN, WATINL(KOUNT)
logical :: NotEnoughFlow, NoOutlet
! Dimension matrix for gaussian processor of advective flow field--
! KOUNT segments in this environmental model
allocate (AMAT(KOUNT,KOUNT+1)) ! get storage for computational matrix
AMAT = 0.0
! Generate advective flow field from input data
! Uses vectors JFRADG and ITOADG to load matrix "WATFL" with the values
! of ADVPRG, and identifies ADVPRG for segments that advect water
! across system boundaries (exports).
! Prezero the matrix and vector
WATOUL = 0.0
SEDOUL = 0.0
WATFL  = 0.0
SEDFL  = 0.0
!write (*,*) ' The water input vector is ', watinl
! Load the matrix
Pairs: do K = 1, size(JFRADG)
! Simplify code by loading values from the vector to indices
J = JFRADG(K)
I = ITOADG(K)
! Check pairs
if (J < 0 .or. I < 0) then
   write (stderr,fmt='(/A/A)')&
      ' A negative segment number was entered for advective flow.',&
      ' Simulation aborted.'
   IFLAG = 8
   deallocate (AMAT)
   return
end if
if (J == 0 .and. I /= 0) then
   write (stderr,fmt='(/A/A/A,I4,A)')&
      ' Inputs to the system must be via stream flows,',&
      ' non-point-source flows, etc. Simulation aborted.',&
      ' Remove the (0,',I,') advective pair.'
   IFLAG = 8
   deallocate (AMAT)
   return
end if
if (J==0 .and. I==0) cycle Pairs ! Skip (0,0) pairs
if (J > KOUNT .or. I > KOUNT) then ! segment not in the system
   write (stderr,fmt='(A,I0,A,I0/A,I0,A)')&
      ' Advection from element ',J,' to element ',I,&
      ' is not possible--only ',KOUNT,' are available. Simulation aborted.'
   IFLAG = 8
   deallocate (AMAT)
   return
end if
if (I == 0) then                    ! Check for export list
   WATOUL(J) = WATOUL(J)+ADVPRG(K)
else                                ! Load WATFL
   WATFL(I,J) = ADVPRG(K)
end if
! Issue warning if diagonal element loaded
if (J == I) write (stdout,fmt='(A/A,I0,A)')&
   ' The specifications for advective flows include an internal',&
   ' recycle in segment ',J,'. This may generate a system error.'
! Check for proper throughput of advected water masses
if (I == 0) cycle Pairs       ! If current pair is an export, go on...
! Process the source term list (JFRADG) to make sure the current
! (Ith) receptor segment has a pathway for transporting the flow
do KK = 1, size(JFRADG)
   ! Move on to the next pair when the removal pathway is found
   if (JFRADG(KK) == I) cycle Pairs
end do
! Exit from this loop indicates that the flow into segment I does not then
! leave the segment; the mass of water is not conserved. If no removal pathway
! has been specified, report the problem and abort the run
write (stderr,fmt='(A/A,I4,A,I4,A/A,I4/A)')&
   ' System definition error-',&
   ' segment ',I,' receives an advected flow from segment ',J,',',&
   ' but the route of release of this flow from segment',I,&
   ' has not been specified. Simulation aborted.'
   IFLAG = 8
   deallocate (AMAT)
   return
end do Pairs

do J = 1, KOUNT
   WATFL(J,J) = 0.0 ! Zero the matrix diagonal just in case
end do

Test_loop: do J = 1, KOUNT
COLTOT = sum(WATFL(:,J)) + WATOUL(J)
!write (*,*) ' COLTOT for Segment ',J,' is ', COLTOT
! Columns must sum to either 1 or 0 (the latter for purely dispersive
! exchange segments, e.g., hypolimnion or bottom sediments in many cases).
! NotEoughFlow tests for this with some allowance for base conversion slop.
NotEnoughFlow = ((COLTOT .GreaterThan. 0.0) .and. &
        (abs(COLTOT-1.0) .GreaterThan. epsilon(COLTOT)))
! NoOutlet tests for external inflow with incomplete outlet flows (COLTOT<1).
! Note that COLTOT<1.0 fails if COLTOT is still in a register. If you first
! write COLTOT (which is 1), then COLTOT<1.0 does not fail.
NoOutlet = ((WATINL(J) .GreaterThan. 0.0) .and.  &
           (abs(COLTOT-1.0) .GreaterThan. epsilon(COLTOT)))
if (NotEnoughFlow .or. NoOutlet) then
!write (*,*) ' In segment ',J,' NotEnoughFlow = ', NotEnoughFlow
!write (*,*) ' In segment ', J,' NoOutlet = ', NoOutlet
   write (stderr,fmt='(A,I0/A)')&
      ' System definition error--advective transport in segment ',J,&
      ' does not conserve mass. Simulation aborted.'
   if (NotEnoughFlow) write (stderr,fmt='(A)') ' (Flow paths are incomplete.)'
   if (NoOutlet) write (stderr,fmt='(A)')&
      ' (Inflows cannot flow out of the segment.)'
   IFLAG = 8
   deallocate (AMAT)
   return
end if
end do Test_loop
! Check for evaporative system (e.g., pond with only evaporative water losses)
! TOTIN is total inputs to segment less evaporative losses, i.e., the net flow
! available to advective processes. If this is non-zero, the system definition
! is improper, but some error margin could be retained for the user defining
! an evaporative system through the change command--as in
!if (.not.(sum(WATOUL)>0.0) .and. TOTIN>1.E-04) then
if (.not.(sum(WATOUL).GreaterThan.0.0) .and. (TOTIN.GreaterThan.0.0)) then
   write (stderr,fmt='(/A/A)')&
      ' System definition error--no outlet flows provided; evaporation',&
      ' does not balance the water budget. Simulation aborted.'
   IFLAG = 8
   deallocate (AMAT)
   return
end if

! Solve system for total segment flows by gaussian elimination.
! Copy waterflow matrix to gaussian processor, load 1's on diagonal, and
! normalized inflows on last column
do J = 1, KOUNT
   do I = 1, KOUNT
      AMAT(I,J) = -WATFL(I,J)
   end do
   AMAT(J,J) = 1.0
end do

KOUNT1 = KOUNT+1
do J = 1, KOUNT
   AMAT(J,KOUNT1) = 0.00  ! Load total exogenous inputs on last column
   if (TOTIN .GreaterThan. 0.0) AMAT(J,KOUNT1) = WATINL(J)/TOTIN
end do

Gauss_elimination: do I = 1, KOUNT
   KEXCH = 1
   M = I+1
   Diagonal: do ! Test of current diagonal element
      if (dabs(AMAT(I,I)) .GreaterThan. 1.E-05) exit Diagonal
      ! Interchange of equations
      LL = I+KEXCH
      ! Test for existence of LL-th equation
      if (LL>KOUNT) then
         write (stderr,fmt='(/A,/A)')& ! System failure
            ' System failure--advective transport field',&
            ' cannot be defined. Simulation aborted.'
         IFLAG = 8
         deallocate (AMAT)
         return
      end if
      do N = I, KOUNT1
         SAVER = AMAT(I,N)
         AMAT(I,N) = AMAT(LL,N)
         AMAT(LL,N) = SAVER
      end do
      KEXCH = KEXCH+1
   end do Diagonal
   
   ! Reduction of Ith equation
   do J = M, KOUNT1
      AMAT(I,J) = AMAT(I,J)/AMAT(I,I)
   end do
   
   ! Elimination in other equations
   Elimination: do J = 1, KOUNT
   if (J==I) cycle Elimination
      do K = M, KOUNT1
         AMAT(J,K) = AMAT(J,K)-AMAT(J,I)*AMAT(I,K)
      end do
   end do Elimination
end do Gauss_elimination

! Advective flow field completed
do J = 1, KOUNT        ! Calculate export flows from segment
   WATOUL(J) = WATOUL(J)*TOTIN*AMAT(J,KOUNT1)
   do I = 1, KOUNT     ! Calculate intra-system transports
      WATFL(I,J) = WATFL(I,J)*TOTIN*AMAT(J,KOUNT1)
   end do
end do
do j=1,kount
!   write (*,*) ' The exogenous net input to',j,' is ', WATINL(J)
!   write (*,*) ' WATFLows entering segment',j,' = ', WATFL(j,:)
   if ((WATINL(J)+sum(WATFL(J,:))) .LessThan. 0.0) then
     ! hydrology bad -- segment has negative water balance after
     ! accounting for internal flow field...
     write (stderr,fmt='(A,I4/A)')' Hydrology of system is faulty; segment ',&
     J,' has a negative flow balance. Simulation aborted.'
     IFLAG = 8
     deallocate (AMAT)
     return
   end if
end do
deallocate (AMAT) ! release computational matrix
end subroutine WATADV
