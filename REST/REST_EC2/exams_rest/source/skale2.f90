subroutine SKALE2(FMN,FMX,RN,VALMIN,STEP,VALMAX,IFAULT)
! This subroutine is a slight modification of the program given in:
! Nelder,J.A. 1976. Algorithm 96. A Simple Algorithm for Scaling Graphs.
! Applied Statistics 25:94-96.
! In particular, this version includes some documentation
! for the user that was not given in the original code.
! Revisions:   29-NOV-1984 -- F.G. Lether
!              21-FEB-1985 -- L.A. Burns
!              23-OCT-1998 -- L.A. Burns
! Given extreme values FMN, FMX, and a scale with N marks, this subroutine
! calculates: the value for the lowest tic mark VALMIN, the step length STEP,
! and the highest scale mark VALMAX. IFAULT is returned as 1 if improper input
! of N <= 1 or if FMX < FMN . Otherwise IFAULT is returned as 0 indicating
! satisfactory input data.
! A scale is constructed so that a scale mark at a value VAL is used for data
! values in the range (VAL - STEP/2,VAL + STEP/2). This means that the lowest
! scale mark VALMIN may be larger, or the largest scale mark VALMAX smaller,
! than one of the extreme data values, though VALMIN-STEP/2 or VALMAX+STEP/2
! will not be.
! The algorithm generates step lengths that are (apart from powers of ten) the
! numbers contained in the array UNIT initialized in the DATA statement below.
! This list of numbers can be altered if another set of steps is desired by
! changing the UNIT constructor statement below.
use Floating_Point_Comparisons ! Revision 09-Feb-1999
Implicit None
real :: FMAX,FMIN,FMN,FMX,RANGE,RJ,RN,S,STEP,VALMAX,VALMIN,X
real, parameter ::&
   Bias=1.0E-04, Half=0.5, One=1.0, Ten=10.0, Tol=5.0E-05, Zero=0.0
integer :: I, IFAULT, NUNIT=11
real, dimension(11) :: unit = (/1.0,1.2,1.6,2.0,2.5,3.0,4.0,5.0,6.0,8.0,10.0/)
FMAX = FMX
FMIN = FMN
IFAULT = 1
! Check for valid input parameters:
   if ((FMAX.LessThan.FMIN) .or. (RN.LessThanOrEqual.1.0)) return
IFAULT = 0
RN = aint(RN-1.0)
if (abs(FMAX) .GreaterThan. Zero) then
   X = abs(FMAX)
else
   X = One
end if
if (((FMAX-FMIN)/X) .LessThanOrEqual. Tol) then ! All values effectively equal
   if (FMAX .LessThan. Zero) then
      FMAX = Zero
   else if (FMAX .GreaterThan. Zero) then
      FMIN = Zero
   else ! FMAX = Zero
      FMAX = One
   end if
end if
STEP = (FMAX-FMIN)/RN
S = STEP
do ! Find power of 10
   if (S .GreaterThanOrEqual. One) exit
   S = Ten*S
end do
do 
   if (S .LessThan. Ten) exit
   S = S/Ten
end do
! Calculate step
X = S-Bias
do I = 1, NUNIT
   if (X .LessThanOrEqual. unit(I)) exit
end do
STEP = STEP*unit(I)/S
RANGE = STEP*RN
! Make first estimate of VALMIN
X = Half*(One+(FMIN+FMAX-RANGE)/STEP)
RJ = aint(X-Bias)
if (X .LessThan. Zero) RJ = RJ-1.0
VALMIN = STEP*RJ
! Test if VALMIN could be Zero
if ((FMIN.GreaterThanOrEqual.Zero).and.(RANGE.GreaterThanOrEqual.FMAX)) &
      VALMIN = Zero
VALMAX = VALMIN+RANGE
! Test if VALMAX could be Zero
if ((FMAX .GreaterThan. Zero) .or. (RANGE .LessThan. (-FMIN))) return
VALMAX = Zero
VALMIN = -RANGE
return
end Subroutine SKALE2
