function DSPLY(AVAR,N,DX,CVAR,TTYOUT)
Implicit None
integer :: N, I, NX, TTYOUT
real (kind (0D0)) :: AVAR(20), CVAR(N), DX
real (kind (0D0)) :: DSPLY
Problem: if (N < 1 .or. N > 100) then
   write (TTYOUT,fmt='(A)') ' ERROR IN SUBPROGRAM DSPLY'
   DSPLY = 0.0D+00; return
end if Problem
DSPLY = AVAR(N+1)
do I = 1, N
   NX = N-I+1
   DSPLY = DSPLY*(DX-CVAR(NX))+AVAR(NX)
end do
end Function DSPLY
