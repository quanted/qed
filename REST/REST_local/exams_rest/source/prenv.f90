subroutine PRENV ()
! PRENV places the canonical characterization of the ecosystem (input data)
! in the report file.
! Created August 1979 by L.A. Burns.
! Revised 14.I.1985 (LAB) -- adding to COMMON "TABLES"
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revisions 09-Feb-1999 to use floating point comparisons module
! Revisions April 2002 to support optional creation of report.xms
use Floating_Point_Comparisons
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
use Table_Variables

Implicit None

call TYPECK ! check compartment designations
if (IFLAG==8) return

! Set up (initial) table headings according to case
if (PRSWG == 0 .or. &    ! Single table of average values
   (PRSWG == 1 .and. MODEG<3 .and. MONTHG == 13)) then
   NFIRST = 13
   NLAST = 13
   if (PRSWG == 0) then
      MEAN = .true.
   else
      MEAN = .false.
   endif
   TAG = '**'
   NMON = NAMONG(13)
elseif (PRSWG == 1 .and. MODEG < 3 .and. MONTHG < 13) then ! Single table
   NFIRST = MONTHG                         ! of values from specific time
   NLAST = MONTHG
   MEAN = .false.
   TAG = '  '
   NMON = NAMONG(MONTHG)
elseif (PRSWG == 1 .and. MODEG == 3) then ! Multiple tables
   NFIRST = 1
   NLAST = 13
   MEAN = .false. ! Computation of mean values postponed
   TAG = '  '     ! till Jan-Dec data printed
else              ! Case failure--notify user and abort
   IFLAG = 8
   write (stderr,fmt='(A/3(A,I3),A/A)')&
      ' Code failure in procedure PRENV due to:',' PRSW = ',PRSWG,&
      ',  MODE = ',MODEG,',  and MONTH = ',MONTHG,'.',' Simulation aborted.'
   return
endif

! Call routines to assemble output tables
! TABA - table of flows - postponed until after FLOWS determines
! whether base flow augmentation is needed for hyrologic balance
call TABB
call TABC
call TABD
return

contains
subroutine TYPECK
! to test that compartment type designations are proper
! split from "geock" 8/26/1998
Implicit None
integer :: J ! to count through segment loop
! Set up index vectors and count number of active water column
! and bottom sediment segments:
KOUNTW = 0.0
KOUNTS = 0.0
do J = 1, KOUNT ! Count the segments by benthic vs. water column types
   if (TYPEG(J) == 'B') then
      KOUNTS = KOUNTS+1.0
   elseif (TYPEG(J)=='L' .or. TYPEG(J)=='E'.or. TYPEG(J)=='H') then
      KOUNTW = KOUNTW+1.0
   else  ! Segment type is improper; write message and quit
      write (stderr,fmt='(/A)')&
         ' Segment TYPE "'//TYPEG(J)//'" unknown. Please use the',&
         ' following nomenclature for segment TYPEs:',&
         '            "L" for Littoral,',&
         '            "E" for Epilimnion,',&
         '            "H" for Hypolimnion, and',&
         '            "B" for Benthic sediment.',&
         ' (Simulation was aborted.)'
      IFLAG = 8
      return
   endif
end do
! Allow for possibility of runs with all water column or benthic types, i.e.,
! eliminate need to test for zero divides when calculating segment averages.
if (KOUNTS .LessThanOrEqual. 0.0) KOUNTS = 1.0
if (KOUNTW .LessThanOrEqual. 0.0) KOUNTW = 1.0
end subroutine TYPECK
end Subroutine PRENV
