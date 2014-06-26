subroutine KINLIS(KOUNT,SELECT,NSEL,TABLE,OUTPUT,TYPEG,CHEMNA,ECONAM,MCHEMG)
! Purpose: KINLIS lists selected kinetic outputs on the terminal
! Subroutines required: KINHED, KINRED
! Revised 24-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
use Implementation_Control
Implicit None
real :: OUTPUT(7), TABLE(132), TFACTR
integer :: IERR, KOUNT, ICODE, MCHEMG, IHIT, I, NSEL
integer, dimension(7) :: SELECT
character(len=1), dimension(KOUNT) :: TYPEG
character(len=50) :: CHEMNA, ECONAM
real, dimension(4) :: TN = (/1.0, 24.0, 730.5, 8766.0/)
rewind PLTLUN
call KINHED (IERR,CHEMNA,ECONAM,KOUNT,TYPEG,ICODE,MCHEMG)
if (IERR == 1) return
TFACTR = 1.0
if (SELECT(1) == 1) TFACTR = TN(ICODE)
do
   call KINRED (IERR,KOUNT,TABLE,IHIT,MCHEMG)
   if (IERR == 2) exit
   if (IHIT == 0) cycle
   do I = 1, NSEL
      OUTPUT(I) = TABLE(SELECT(I))
   end do
   OUTPUT(1) = OUTPUT(1)/TFACTR
   write (stdout,fmt='(1X,1PG11.4,6(G11.4))') (OUTPUT(I),I=1,NSEL)
end do
return
end Subroutine KINLIS
