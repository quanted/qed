subroutine KINRED(EOF,KOUNT,RECURD,HIT,MCHEMG)
! Purpose: to retrieve one logical record from the kinetic output file
! Revised 06-April-1987 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
use Implementation_Control
Implicit None
real :: RECURD(132), AVE(6), NEXT(5),TTEMP
integer :: EOF,HIT,K,MCHEMG,I,KOUNT,JDUMMY,IOFF, Status_check
HIT = 0
read (PLTLUN,iostat=Status_check) K,TTEMP,AVE
if (Status_check == IOeof) then ! end of file
   EOF = 2
   return
end if
if (K == MCHEMG) then
   HIT = 1
   RECURD(1) = TTEMP
   do I = 1, 6
      RECURD(I+1) = AVE(I)
   end do
end if

do I = 1, KOUNT
   read (PLTLUN,iostat=Status_check) K,TTEMP,JDUMMY,NEXT
   if (Status_check == IOeof) then ! end of file
      EOF =2
      return
   end if
   if (K /= MCHEMG) cycle
   IOFF = (I-1)*5+7
   do K = 1, 5
      RECURD(K+IOFF) = NEXT(K)
   end do
end do
return
end Subroutine KINRED
