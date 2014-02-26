subroutine SHOVAR
! Revised 27-DEC-1985 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
use Implementation_Control
use Model_Parameters
Implicit None
! Local variables
integer :: I,index,ITAB,J,K,L,N
character(len=1) :: OUTPUT(64), LAST
OUTPUT = ' ' ! Blank the output line
ITAB = 0
K = 0
write (stdout,fmt='()')
I_loop: do I = 1, NOMOD
   ITAB = ITAB+1
   index = (ITAB-1)*7+1
   N = MODLEN(I)
   if (ITAB > 9) then
      write (stdout,fmt='(64A1)') (OUTPUT(L),L=1,index)
      OUTPUT = ' '
      ITAB = 1
   end if
   index = (ITAB-1)*7+1
   J_loop: do J = 1, N
      K = K+1
      LAST = MODS(K)
      if (J == N .and. LAST == 'G') exit J_loop ! i.e., skip a terminal "G"
      index = index+1
      OUTPUT(index) = LAST
   end do J_loop
end do I_loop
if (index > 1) write (stdout,fmt='(64A1)') (OUTPUT(L),L=1,index)
return
end Subroutine SHOVAR
