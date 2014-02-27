subroutine SEDADV
! SEDADV uses the outcome of WATADV to compute the entrained
! transport of suspended sediments, sediment exports, and bedloads
! Revised 11 July 1983 (LAB) for mode 3 operations.
! Conversion to F90 10/1998
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
Implicit None
! Local variables
integer :: I, J, K
! Compute sediment exports and entrained intrasystem flows
Segments: do J = 1, KOUNT
   Aqueous: if (TYPEG(J) /= 'B') then ! Source is a water column segment
      SEDOUL(J) = WATOUL(J)*SEDCOL(J)    ! Exports (kg/hr)
      do I = 1, KOUNT ! Advective interchange among segments
         ! If the destination of the flow is a bottom sediment, only water
         ! is moving; otherwise sediment is entrained in proportion to its
         ! concentration in the source segment:
         do K = 1, KCHEM
            if (TYPEG(I) /= 'B') SEDFL(I,J,K) = WATFL(I,J)*SEDCOL(J)
         end do
      end do
      cycle Segments ! Increment loop to next segment
   end if Aqueous

! Bottom sediment segments. If this is segment one, the user has not followed
! the assumptions needed for these computations - abort -
Bad_start: if (J==1) then
   write (stdout,fmt='()')&
   ' The system elements have not been properly numbered:',&
   ' segment 1 has been designated a benthic sediment. Simulation aborted.'
   IFLAG = 8
   return
end if Bad_start
! If the previous (overlying) segment is NOT another sediment, the current
! segment is surficial (bbl), and export is taken to be a bed load.
if (TYPEG(J-1) /= 'B') SEDOUL(J) = WATOUL(J)*SEDCOL(J)
! If the previous segment IS another sediment, an export of water along this
! flow path represents a vertical ground-water recharge carrying
! a water flow only.
do I = 1, KOUNT ! Compute intra-system sediment transport
! Advective sediment transport from a sediment segment to another system
! element is permitted only when the destination segment is another sediment,
! and the segment number for the other sediment indicates that the segments
! are NOT vertically adjacent. Given the numbering scheme outlined in the user
! manual, this constraint allows one to enter bedloads that move along the
! advective flowpath(s), but limits vertical hydraulic advection 
! to water flow (interflow, ground-water recharge) only.
   do K = 1, KCHEM
      if (TYPEG(I)=='B' .and. iabs(J-I)>1) SEDFL(I,J,K) = WATFL(I,J)*SEDCOL(J)
   end do
end do
end do Segments
end Subroutine SEDADV
