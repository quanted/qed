real (kind (0D0)) function DINTPT(N,X,Y)
! DINTPT calculates an approximation for an integral on the basis of points
! supplied by using cubic interpolation and Gaussian quadrature.
! Input parameters:
! N = Number of points input (must have N>2 and N<12)
! X = Single precision array of abscissas
! Y = Single precision array of ordinates
! Revisions 10/22/88--run-time implementation of machine dependencies
use Implementation_Control
Implicit None
real (kind (0D0)) :: DX(11),DY(11)
real (kind (0D0)) :: DALF,DBET,DGC,DSUM,DXX,DINTRP
integer :: I,N,NIP
real :: X(N),Y(N)
integer :: NGPTS=7 ! NGPTS is number of gaussian points to be used
! DC = Gaussian points, DW = Gaussian weights
real (kind (0D0)), dimension(7) :: DC = (/-0.949107912342759D+00,&
-0.741531185599394D+00, -0.405845151377397D+00,0.0D+00,0.405845151377397D+00,&
0.741531185599394D+00, 0.949107912342759D+00/)
real (kind (0D0)), dimension(7) :: DW = (/0.129484966168870D+00,&
0.279705391489277D+00, 0.381830050505119D+00, 0.417959183673469D+00,&
0.381830050505119D+00, 0.279705391489277D+00, 0.129484966168870D+00/)

if (N < 3 .or. N > 11) then ! problem
   write (stdout,fmt='(A,I5)') ' Invalid input in DINTPT: N = ',N
   dintpt = 0.0D+00; return
end if

do I = 1, N
   DX(I) = dble(X(I))
   DY(I) = dble(Y(I))
end do

NIP = 4
if (N == 3) NIP = 3
DALF = 0.5D+00*(DX(1)+DX(N))
DBET = 0.5D+00*(DX(N)-DX(1))

DSUM = 0.0D+00
do I = 1, NGPTS
   DXX = DBET*DC(I)+DALF
   DGC = DBET*DINTRP(N,DX,DY,DXX,NIP)
   DSUM = DSUM+DW(I)*DGC
end do
DINTPT = DSUM
return
end function DINTPT
