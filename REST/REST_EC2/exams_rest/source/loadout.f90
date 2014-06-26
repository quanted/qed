subroutine LoadOut (LogUnit, Problem, SegCount, ChemCount)
! Subroutine to write an external file of allochthonous chemical loadings.
! Only loadings that are in the current problem set are written, i.e.,
! loads referring to segments>SegCount or chemicals>Chemcount are ignored.
! The output file contains documentation to assist in manual revision.
use Implementation_Control
use Global_Variables
use Floating_Point_Comparisons
Implicit None
integer, intent (in) :: LogUnit, SegCount, ChemCount
integer :: NPULSE, I, J
real :: TEST
! LogUnit is the Logical Unit Number of the target file
! SegCount is the number of active segments
! ChemCount is the number of active chemicals
logical, intent (out) :: Problem ! to report failure of routine
Problem = .false.
! Process pulse loads
NPULSE = 0
CountPulses: do I = 1, MAXMAS
   TEST = float(ISEGG(I)+ICHEMG(I)+IMONG(I)+IDAYG(I))+IMASSG(I)
   if (TEST .Equals. 0.0) then 
      cycle CountPulses ! Skip unused locations
   else
      NPULSE = NPULSE + 1
   end if
end do CountPulses
! If, however, in Mode 1, any data contained in the structure are irrelevant:
if (MODEG==1) NPULSE=0
! Document the output file
write (LogUnit, fmt='(A)') ' Loading pattern for Exams.'
write (LogUnit,fmt='(A12,I5,A11,I5)')&
 ' Chemicals: ',ChemCount,' Segments: ',SegCount
write (LogUnit, fmt='(1x,I9,1x,A/A)') NPULSE,&
   ' pulse loads with elements','   ISEG, ICHEM, IMON, IDAY, IMASS'
WritePulses: do I = 1,NPULSE
   TEST = float(ISEGG(I)+ICHEMG(I)+IMONG(I)+IDAYG(I))+IMASSG(I)
   if (TEST .Equals. 0.0) then 
      cycle WritePulses ! Skip unused locations
   else
      write (LogUnit,fmt='(1x,I5,1x,I5,1x,I5,1x,I5,4x,ES9.3)') &
         ISEGG(I),ICHEMG(I),IMONG(I),IDAYG(I),IMASSG(I)
   end if
end do WritePulses

WriteLoads: do I=1,ChemCount
   write (LogUnit, fmt='(A,I5,A)') ' Stream Loads (STRLD) for Chemical ',&
      I,'. Order is Jan, Feb,...,Dec, Average'
   do J=1,SegCount
      write (LogUnit,fmt='(A,I5,13(1x,ES8.2))') ' Segment ', J, STRLDG(J,I,:)
   end do

   write (LogUnit, fmt='(A,I5,A)') ' Non-Point Loads (NPSLD), Chemical ',&
      I,'. Order is Jan, Feb,...,Dec, Average'
   do J=1,SegCount
      write (LogUnit,fmt='(A,I5,13(1x,ES8.2))') ' Segment ', J, NPSLDG(J,I,:)
   end do

   write (LogUnit, fmt='(A,I5,A)') ' Precip Loads (PCPLD) for Chemical ',&
      I,'. Order is Jan, Feb,...,Dec, Average'
   do J=1,SegCount
      write (LogUnit,fmt='(A,I5,13(1x,ES8.2))') ' Segment ', J, PCPLDG(J,I,:)
   end do

   write (LogUnit, fmt='(A,I5,A)') ' Drift Loads (DRFLD) for Chemical  ',&
      I,'. Order is Jan, Feb,...,Dec, Average'
   do J=1,SegCount
      write (LogUnit,fmt='(A,I5,13(1x,ES8.2))') ' Segment ', J, DRFLDG(J,I,:)
   end do

   write (LogUnit, fmt='(A,I5,A)') ' Seepage Load (SEELD) for Chemical ',&
      I,'. Order is Jan, Feb,...,Dec, Average'
   do J=1,SegCount
      write (LogUnit,fmt='(A,I5,13(1x,ES8.2))') ' Segment ', J, SEELDG(J,I,:)
   end do

end do WriteLoads

return
end subroutine LoadOut
