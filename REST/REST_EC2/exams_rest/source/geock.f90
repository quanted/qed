subroutine GEOCK
! GEOCK computes segment volume, area, and depth when these are
! specified via reach width, length, and cross-section.
! Revised FORMAT 6-AUG-1985 (LAB)
! Revisions 10/22/88--run-time implementation of machine dependencies
! Converted to Fortran90 5/30/96
use Floating_Point_Comparisons ! Revisions 09-Feb-1999
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
Implicit None
! Local variables for this subroutine
integer :: J ! J counts through segment loop
Segment_loop: do J = 1, KOUNT
   ! If volume, area, and depth are already available, do next segment
   if ( (VOLG(J)  .GreaterThan. 0.0) .and. &
        (AREAG(J) .GreaterThan. 0.0) .and. &
        (DEPTHG(J).GreaterThan. 0.0)       &
      )  cycle
   Zero_area: if (.not. (AREAG(J) .GreaterThan. 0.0)) then ! Area is zero
      AREAG(J) = LENGG(J)*WIDTHG(J)
      if (.not. (AREAG(J) .GreaterThan. 0.0)) then
         if (VOLG(J) .Equals. 0.0)  VOLG(J)  = LENGG(J)*XSAG(J)
         if (DEPTHG(J) .GreaterThan. 0.0) AREAG(J) = VOLG(J)/DEPTHG(J)
         if (.not. (AREAG(J) .GreaterThan. 0.0)) then
            IFLAG = 8
            write (stdout,fmt='(A,I4,A/A)')&
               ' Area of segment ',J,' cannot be determined.',&
               ' Simulation aborted.'
            exit
         end if
      end if
   end if Zero_area
   Zero_depth: if (.not. (DEPTHG(J) .GreaterThan. 0.0)) then ! Depth is zero
      DEPTHG(J) = VOLG(J)/AREAG(J) ! can't get here if AREAG(J) is zero
      if (DEPTHG(J) .GreaterThan. 0.0) cycle Segment_loop
      if (WIDTHG(J) .GreaterThan. 0.0) DEPTHG(J) = XSAG(J)/WIDTHG(J)
      if ((.not.(DEPTHG(J).GreaterThan.0.0)) .and. &
         (TYPEG(J)/='B')) then ! (depth of benthics not used in calculation)
         write (stdout,fmt='(A,I4,A/A)') &  
            ' Depth of water column segment ',J,' cannot be determined.',&
            ' Simulation aborted.'
         IFLAG = 8
         exit Segment_loop
      end if
   end if Zero_depth
   Zero_volume: if (.not. (VOLG(J) .GreaterThan. 0.0)) then ! Volume is zero
      VOLG(J) = AREAG(J)*DEPTHG(J)
      if (VOLG(J) .GreaterThan. 0.0) cycle Segment_loop
      VOLG(J) = XSAG(J)*LENGG(J)
      if (VOLG(J) .GreaterThan. 0.0) cycle Segment_loop
      IFLAG = 8
      write (stdout,fmt='(A,I4,A/A)')&
         ' Volume of segment ',J,' cannot be determined.',&
         ' Simulation aborted.'
      exit Segment_loop
   end if Zero_volume
end do Segment_loop
return
end Subroutine GEOCK
