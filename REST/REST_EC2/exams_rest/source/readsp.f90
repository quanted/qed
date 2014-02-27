subroutine READSP
! Purpose--to input the system parameter information
! Subroutines required--UNPREC
! Revised 24-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
! Revised 11/17/88 to accommodate VAX multi-user environment
use Implementation_Control
use Initial_Sizes
use Model_Parameters
Implicit None
integer :: HRECS,IBUFF(VARIEC),RECDAT(FILDAT),M,I,L,IN,NMODS
! RECDAT carries the file information; HRECS is the number of
! header records required.
character(len=1) :: BUFFER(VARCEC)
character(len=4) :: TEMP
! Retrieve the system parameter information from disk
! Read the header record for file control information
HRECS = FILDAT/VARIEC
if (FILDAT-VARIEC*HRECS /= 0) HRECS = HRECS+1
M = 0
Loop: do I = 1, HRECS
   read (RANUNT,rec=I) IBUFF
   do L = 1, VARIEC
      M = M+1
      if (M > FILDAT) exit Loop
      RECDAT(M) = IBUFF(L)
   end do
end do Loop

IN = RECDAT(5)-1
call UNPREC (IN,MODLEN,NOMOD,PARCNT)
call UNPREC (IN,MODMIN,NOMOD,PARCNT)
call UNPREC (IN,TS,NOMOD,PARCNT)
call UNPREC (IN,TD,NOMOD,PARCNT)
call UNPREC (IN,TCL1,NOMOD,PARCNT)
call UNPREC (IN,TCL2,NOMOD,PARCNT)
call UNPREC (IN,TCL3,NOMOD,PARCNT)
call UNPREC (IN,COMVAR,NOCOM,COMCNT)
! Unload character record
IN = IN+1
read (RANUNT,rec=IN) BUFFER
do I = 1, 4
   TEMP(I:I) = BUFFER(I)
end do
read (TEMP,fmt='(I4)') NMODS
L = 4
M = 0
do I = 1, NMODS
   L = L+1
   if (L>VARCEC) then
      IN = IN+1
      read (RANUNT,rec=IN) BUFFER
      L = 1
   endif
   M = M+1
   MODS(M) = BUFFER(L)
end do
return
end subroutine READSP
