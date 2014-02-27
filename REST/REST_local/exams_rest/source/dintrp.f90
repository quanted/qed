function DINTRP(NN,DX,DY,DXX,MMM)
! Revised 08-Feb-1999 -- floating point comparisons
use Implementation_Control
use Floating_Point_Comparisons
Implicit None
integer :: L,M,MM,N
integer, intent (in) :: NN, MMM
real (kind (0D0)) :: DINTRP
real (kind (0D0)) :: DX(NN),DY(NN),DVD(20)
real (kind (0D0)) :: DXX
real (kind (0D0)) :: DSPLY ! function
real (kind (0D0)), parameter :: DEPS=1.0D-12
! Check for valid parameters, return with DINTRP set to zero if problem
DINTRP = 0.0D+00
if (DXX .LessThan. (DX(1)-DEPS)) then
   write (stdout,fmt='(/A)') " DXX outside table."
   return
end if
if (MMM < 3 .or. MMM > 20 .or. NN < 2 .or. NN > 14) then
   write (stdout,fmt='(/A)') " Invalid argument in DINTRP."
   return
end if
L = 1
M = MMM
N = NN
Unequal: if (NN > M) then
   do L = 1,N
      if (dabs(DXX-DX(L)) .LessThan. DEPS) then
         DINTRP = DY(L) ! direct hit
         return
      end if
      if (DXX < DX(L)) exit
      if (L == N) then ! loop ending without results
         write (stdout,fmt='(/A)') " DXX outside table."
         return
      end if
   end do
   L = L-1
   ! Calculate beginning point for input to DIVDIF
   L = L-M/2+1
   if (L <= 0) L = 1
   if (L > (N-M+1)) L = N-M+1
else Unequal
   M = NN
end if Unequal
MM = M-1
call DIVDIF (DX(L),DY(L),M,DVD)
DINTRP = DSPLY(DVD,MM,DXX,DX(L),stdout)
end Function DINTRP
