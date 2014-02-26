subroutine SHOPLO(FIXFIL,JUMP,I1,I2,I3,IERR,PLTLUN,TTYOUT)
! Subroutines required: none
! Revisions 10/21/88--run-time implementation of machine dependencies
! Convert to Fortran90 3/21/96; LUNs added to call list
Implicit None
integer :: FIXFIL,I1,I2,I3,IERR
integer, intent(in) :: PLTLUN,TTYOUT,JUMP
integer :: I ! local counter
character(len=50) :: NAMECO, NAMEEC ! names of compounds, ecosystem
rewind PLTLUN
IERR = 0
if (FIXFIL == 0) then ! If no results are available, return at once
   IERR = 1
   return
endif
read (PLTLUN,end=120,err=110) I1,I2,I3
if (JUMP == 0) write (TTYOUT,fmt='(/,3(/,A,I0),/)')&
   ' Number of chemicals: ',I1,&
   ' Simulation Mode:     ',I2,&
   ' Number of segments:  ',I3
do I = 1, I1  ! Read name of chemical
   read (PLTLUN,end=120,err=110) NAMECO
   if (JUMP /= 0) cycle ! i.e., skip the write, or, jump over chemical name
   write (TTYOUT,fmt='(A,I2,A)') ' Chemical: ',I,') '//trim(NAMECO)
end do
read (PLTLUN,end=120,err=110) NAMEEC ! Read name of ecosystem
if (JUMP == 0) write (TTYOUT,fmt='(A)') ' Environment:  '//trim(NAMEEC)
return

110 write (TTYOUT,fmt='(//A)') ' Error reading the plot file.'
   IERR = 3; return

120 write (TTYOUT,fmt='(//A)')&
   ' End-of-file enountered while reading the plot file.'
   IERR = 2; return

end Subroutine SHOPLO
