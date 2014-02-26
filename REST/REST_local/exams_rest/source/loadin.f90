subroutine LoadIn (LogUnit, Problem, SegCount, ChemCount)
! Subroutine to read an external file of allochthonous chemical loadings.
! Only loadings that are in the current problem set are valid, and
! the expected ordering must be observed if a hand-built file is used.
! The output files contain documentation to assist in manual revision.
! MAXMAS is the maximum number of allochthonous chemical pulses.

use Implementation_Control
use Global_Variables
Implicit None
real, dimension(13) :: buffer ! for safely reading the file
integer, intent (in) :: LogUnit, SegCount, ChemCount
integer :: NPULSE, I, J, ChemCheck, SegmentCheck
! LogUnit is the Logical Unit Number of the target file
! SegCount is the number of active segments, SegmentCheck checks the file
! ChemCount is the number of active chemicals, ChemCheck checks the file
logical, intent (out) :: Problem ! to report failure of routine
Problem = .false.
! Process pulse loads-read the number of loads and bring them in

! Check the number of chemicals and segments represented
read (LogUnit,fmt='(/12x,I5,11x,I5)') ChemCheck, SegmentCheck
if (ChemCheck/=ChemCount .or. SegmentCheck/=SegCount) then
   Problem=.true.
   write (stderr, fmt='(A/A,I0,A,I0,A/A,I0,A,I0,A)')&
      ' The load file is not consistent with the problem setup:',&
      ' The problem has ',KOUNT,' segments; the file has ',SegmentCheck,'.',&
      ' The problem has ',KCHEM,' chemicals; the file has ',ChemCheck,'.'
   return
end if

read (LogUnit, fmt='(1x,I9/)') NPULSE
! Check the number of pulses against the current capacity of the storage
if (NPULSE > size(ISEGG)) then
   Problem = .true.
   write (stderr,fmt='(A/A)') &
      ' The load file contains more data than can be accommodated',&
      ' by this version of Exams. Ask the author to increase "MAXMAS".'
   return
end if

ReadPulses: do I = 1,NPULSE
   read (LogUnit,err=5000,fmt='(1x,I5,1x,I5,1x,I5,1x,I5,4x,ES9.3)') &
      ISEGG(I),ICHEMG(I),IMONG(I),IDAYG(I),IMASSG(I)
end do ReadPulses

ReadLoads: do I=1,ChemCount
   call Read_Chem_Line
   if (Problem) return
   do J=1,SegCount
      read (LogUnit,err=5010,fmt='(9x,I5,13(1x,ES8.2))') SegmentCheck, buffer
      if (SegmentCheck==J) then
         STRLDG(J,I,:) = buffer
      else
         Problem = .true.
         write (stderr,fmt='(A/A,I0,A,I0,A)')&
            ' The stream loadings cannot be read;',' segment number ',&
            SegmentCheck,' was found where ',J,' was expected.'
         return
      end if
   end do

   call Read_Chem_Line
   if (Problem) return
   do J=1,SegCount
      read (LogUnit,err=5010,fmt='(9x,I5,13(1x,ES8.2))') SegmentCheck, buffer
      if (SegmentCheck==J) then
         NPSLDG(J,I,:) = buffer
      else
         Problem = .true.
         write (stderr,fmt='(A/A,I0,A,I0,A)')&
            ' The non-point-source loadings cannot be read;',&
            ' segment number ',&
            SegmentCheck,' was found where ',J,' was expected.'
         return
      end if
   end do

   call Read_Chem_Line
   if (Problem) return
   do J=1,SegCount
      read (LogUnit,err=5010,fmt='(9x,I5,13(1x,ES8.2))') SegmentCheck, buffer
      if (SegmentCheck==J) then
         PCPLDG(J,I,:) = buffer
      else
         Problem = .true.
         write (stderr,fmt='(A/A,I0,A,I0,A)')&
            ' The precipitation loadings cannot be read;',' segment number ',&
            SegmentCheck,' was found where ',J,' was expected.'
         return
      end if
   end do

   call Read_Chem_Line
   if (Problem) return
   do J=1,SegCount
      read (LogUnit,err=5010,fmt='(9x,I5,13(1x,ES8.2))') SegmentCheck, buffer
      if (SegmentCheck==J) then
         DRFLDG(J,I,:) = buffer
      else
         Problem = .true.
         write (stderr,fmt='(A/A,I0,A,I0,A)')&
            ' The monthly drift loadings cannot be read;',' segment number ',&
            SegmentCheck,' was found where ',J,' was expected.'
         return
      end if
   end do

   call Read_Chem_Line
   if (Problem) return
   do J=1,SegCount
      read (LogUnit,err=5010,fmt='(9x,I5,13(1x,ES8.2))') SegmentCheck, buffer
      if (SegmentCheck==J) then
         SEELDG(J,I,:) = buffer
      else
         Problem = .true.
         write (stderr,fmt='(A/A,I0,A,I0,A)')&
            ' The seepage loadings cannot be read;',' segment number ',&
            SegmentCheck,' was found where ',J,' was expected.'
         return
      end if
   end do
end do ReadLoads
return
5000 continue ! error reading pulse loads
Problem = .true.
write (stderr, fmt='(A)') ' Error reading load file. Pulse loads deleted.'
return
5010 continue ! error reading monthly loads
Problem = .true.
write (stderr, fmt='(A)') ' Error reading load file. All loads deleted.'
return

contains
subroutine Read_Chem_Line
! procedure to read the information lines between the sets of monthly loads
   read (LogUnit, err=6000, fmt='(35X,I5)') ChemCheck
   if (ChemCheck/=I) then
      Problem = .true.
      write (stderr, fmt='(A/A,I0,A,I0,A)') ' The load file cannot be read;',&
         ' chemical number ',ChemCheck,' was found where ',I,' was expected.'
      return
   else
      return
   end if
   6000 continue ! error reading monthly data
   Problem=.true.
   write (stderr, fmt='(A)') ' Error reading loadings file.'
   return
end subroutine Read_Chem_Line

end subroutine LoadIn
