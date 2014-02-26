subroutine FLOWS
! FLOWS computes the advective and dispersive transport field that moves
! chemicals through the ecosystem segments. After conversion of the input
! hydrologic data to a form suitable for further computations, FLOWS calls
! three subsidiary routines: WATADV, SEDADV, and DISPER.
! Revised 11 July 1983 (LAB) for mode 3 operations.
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 05-Feb-1999 to use floating point comparisons
! Revised 03-Mar-2000 to augment base flow when required for mass balance
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Input_Output
use Internal_Parameters
use Rates_and_Sums
use Floating_Point_Comparisons
Implicit None
! Local variables
real :: EVAPL(KOUNT), WATINL(KOUNT), TOTIN, TOTOUT
! NumDAYS are days in each month -- average values support modes 1 & 2
real, dimension(13) :: NumDAYS = &
   (/31.,28.25,31.,30.,31.,30.,31.,31.,30.,31.,30.,31.,30.4375/)
integer :: J
logical :: test
logical, dimension(KOUNT) :: ICPTES
! EVAPL is evaporative water losses converted to internal units (L/hr)
! WATINL is total water flow (L/hr) to segments
! TOTIN is passed to WATADV for error checking - -
if (ModeG==3) then ! test for leap year
   NumDAYS(2) = real (NDAYS(2))
   if (NDAYS(2)==29) NumDAYS(13) = 30.5
else
   NumDays(2) = 28.25; NumDays(13) = 30.4375
end if
! Convert global input variables to internal variables used in the program
RAINFL = 0.0  ! Pre-zero to eliminate left-overs from previous run
EVAPL  = 0.0
SEEPSL = 0.0
NPSFL  = 0.0
STRMFL = 0.0
STSCOL = 0.0
NPSCOL = 0.0
ICPTES = .false.
! Set up check on definition of advective flow field - load test vector with
! 1s for segments that include an active flow pathway leaving the segment
do J = 1, size(JFRADG)
   if (JFRADG(J)<=0 .or. JFRADG(J)>KOUNT) cycle
   ICPTES(JFRADG(J)) = .true.
end do
Segments: do J = 1, KOUNT
   ! Test for segments with an air/water interface for loading precipitation
   ! inputs and evaporative removals: Rain falls on segment 1 (by definition),
   ! but not on benthic or hypolimnion segments, and it falls on others (L
   ! and E) only when the preceding segment is "B":

   If (j==1) then   !2013
      test=.true.
   else
      test = (TYPEG(J)/='B' .and. TYPEG(J)/='H' .and. TYPEG(J-1)=='B')
   end if
   Air_water: if (test) then
!   Air_water: if (J==1 .or. &
!    (J>1 .and. TYPEG(J)/='B' .and. TYPEG(J)/='H' .and. TYPEG(J-1)=='B')) then
      Ice: if (TCELG(J,NDAT) .LessThanOrEqual. 0.0) then
                                 ! there is ice cover, so cut off
         RAINFL(J) = 0.0         ! precipitation additions and
         EVAPL(J) = 0.0          ! evaporative losses of water in the segment
      else Ice ! Liquid water, so
         ! convert input rainfall and evaporation (mm/mon=L/m2/mon) to L/hr:
         RAINFL(J) = RAING(NDAT)*AREAG(J)/(24.0*NumDAYS(NDAT))
         EVAPL(J) = EVAPG(J,NDAT)*AREAG(J)/(24.0*NumDAYS(NDAT))
      end if Ice
   end if Air_water
   STRMFL(J) = STFLOG(J,NDAT)*1000.
   if (STRMFL(J) .GreaterThan. 0.0) STSCOL(J) = STSEDG(J,NDAT)/STRMFL(J)
   SEEPSL(J) = SEEPSG(J,NDAT)*1000. ! 1000 Liters per cubic meter
   NPSFL(J) = NPSFLG(J,NDAT)*1000.
   if (NPSFL(J) .GreaterThan. 0.0) NPSCOL(J) = NPSEDG(J,NDAT)/NPSFL(J)
   ! Net advective flow available to segment:
   WATINL(J) = STRMFL(J)+SEEPSL(J)+NPSFL(J)+RAINFL(J)-EVAPL(J)
   ! Check for proper definition of advective flow field: any segment
   ! with a net advective flow must include a pathway for the flow.
   Unreal: if ( (WATINL(J) .GreaterThan. 0.0) .and. &
               .not.ICPTES(J)) then! Improper definition:
      ! net advective flow, no outlet - notify user and abort simulation
      write (stderr,fmt='(/A,I4,A,2(/A))')&
         ' Hydrologic definition of segment ',J,' is improper.',&
         ' There is a net advected flow leaving this segment,',&
         ' but the flow pathway has not been specified. Simulation aborted.'
      IFLAG = 8 ! Set flag when simulation cannot be run
      return
   end if Unreal
end do Segments
TOTIN = sum(WATINL)
! check for improper hydrology
if (TOTIN .LessThan. 0.0) then
   ! write (*,*) ' Deficit (L/hr) = ', -TOTIN
   if (ICPTES(1)) then ! increase base flow to compensate (110% of need)
      ! Save the original values of streamflow and stream sediment
      ! for restoration at the end of the Run or Continue
      STFLOG_saved(1,NDAT)=STFLOG(1,NDAT)
      STSEDG_saved(1,NDAT)=STSEDG(1,NDAT)
      ! If base flow currently enters the system, the sediment
      ! concentration will be maintained. If not, a nominal
      ! sediment concentration of 20 mg/L will be established
      if (.not.(STFLOG(1,NDAT).GreaterThan. 0.0)) STSCOL(1) = 0.000020
      STSEDG(1,NDAT) = STSEDG(1,NDAT) + 1.10 * abs(TOTIN) * STSCOL(1)             
      STRMFL(1) = STRMFL(1) + 1.10 * abs(TOTIN)
      STFLOG(1,NDAT) = STFLOG(1,NDAT) + 1.10 * abs(TOTIN)/1000.0
      ! Recalculate WATINL(1)
      WATINL(1) = STRMFL(1)+SEEPSL(1)+NPSFL(1)+RAINFL(1)-EVAPL(1)
      ! Recalculate TOTIN
      TOTIN = sum(WATINL)
   else ! there is no possibility of a positive water balance, so
      write (stderr,fmt='(A/A)') &
         ' Hydrologic definition is improper; the water body',&
         ' has a negative water balance. Simulation aborted.'
      IFLAG = 8 ! Set flag when simulation cannot be run
      return
   end if
end if

! Recheck hydrology
if (TOTIN .LessThan. 0.0) then
   write (stderr,fmt='(A/A/A)') &
      ' Hydrologic definition is improper; the water body has a ',&
      ' negative water balance and base flow augmentation did not',&
      ' solve the problem. Simulation aborted.'
   IFLAG = 8 ! Set flag when simulation cannot be run
   return
end if

call WATADV (TOTIN,WATINL) ! subroutine to evaluate advective flows
if (IFLAG == 8) return
call SEDADV ! subroutine to compute advective sediment transport
call DISPER ! subroutine to compute dispersive transport of water & sediment
! Check for elements that are disconnected from the rest of the system.
! Abort if necessary as this will generate zero divides later in the program.
! Test: row total + column total should be non-zero
Disconnect: if (KOUNT > 1) then; Check_segments: do J = 1, KOUNT
   TOTOUT = sum(WATFL(:,J))+sum(WATFL(J,:))
   if (TOTOUT .GreaterThan. 0.0) cycle Check_segments
   ! if connected, check the next one, if not, error message and kill process
   write (stderr,fmt='(A,I4/A)')&
      ' System definition error: segment ',J,&
      ' is not connected to other system elements. Simulation aborted.'
   IFLAG = 8 ! Set flag when simulation cannot be run
   exit Check_segments
end do Check_segments; end if Disconnect; end Subroutine FLOWS
