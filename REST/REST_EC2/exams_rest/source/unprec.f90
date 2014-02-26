subroutine UNPREC (RECNUM,OUTPUT,LENGTH,OUTSIZ)
! Revised 22-APR-87 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
! Revised 11/17/88 to accommodate VAX multi-user environment
use Implementation_Control
Implicit None
integer :: BUFFER(VARIEC),LENGTH,OUTSIZ,OUTPUT(OUTSIZ),RECNUM,L,M,I
RECNUM = RECNUM+1
read (RANUNT,rec=RECNUM) BUFFER
LENGTH = BUFFER(1)
L = 1
M = 0
do I = 1, LENGTH
   L = L+1
   if (L > VARIEC) then
      RECNUM = RECNUM+1
      read (RANUNT,rec=RECNUM) BUFFER
      L = 1
   endif
   M = M+1
   OUTPUT(M) = BUFFER(L)
end do
return
end subroutine UNPREC
