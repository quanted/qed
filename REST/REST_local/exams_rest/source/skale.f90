subroutine SKALE(ARRAY,AXLEN,NPTS,INC,ARYSIZ)
! Revisions:  02-DEC-1984: F.G. Lether
! 21-FEB-1985: L.A. Burns
! Revisions 10/21/88--run-time implementation of machine dependencies
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Implementation_Control
Implicit None
! Subroutines required: SKALE2
integer :: ARYSIZ
real :: ARRAY(ARYSIZ),AXLEN
real :: DIST,DUMMY,RN,Z,ZMAX,ZMIN,ZMINP
integer :: I,INC,NPTS,IFAULT
! ARRAY--Input array of values to be scaled.
! AXLEN--Length, in inches, that the values are to be scaled.
! AXLEN should be a positive integer >= 2.
! INC  --Not used, but required for compatibility.
! NPTS --Number of points to be plotted. NPTS must be .GE. 2.
! ARYSIZ--size of ARRAY as allocated in calling program unit
! Find maximum and minimum:
ZMIN = ARRAY(1)
ZMAX = ARRAY(1)
do I = 2, NPTS, INC
   Z = ARRAY(I)
   if (Z .GreaterThan. ZMAX) ZMAX = Z
   if (Z .LessThan.    ZMIN) ZMIN = Z
end do
RN = aint(AXLEN)
if (.not.(abs(ZMIN-ZMAX) .GreaterThan. 0.0)) then
   ! special case--MAX and MIN are equal
   ZMIN = ZMIN-0.1*ZMIN
   ZMAX = ZMIN+0.1*ZMIN
endif
if (RN .LessThanOrEqual. 1.0) RN = 2.0
call SKALE2 (ZMIN,ZMAX,RN,ZMINP,DIST,DUMMY,IFAULT)
if (IFAULT > 0) then
   write (stdout,fmt='(A)') ' Improper input to Subroutine SKALE2.'
   return
end if
! Uncomment the next statement if XMIN must be <= ZMINP, i.e,.
! the left scale mark not be greater than the least data point.
! Otherwise SKALE2 will possibly have ZMINP near XMIN, but
! not <= XMIN. See documentation in Subroutine SKALE2 for further
! explanation on this point.
! IF (ZMIN .LT. ZMINP) ZMINP = ZMINP - DIST
ARRAY(NPTS+1) = ZMINP
ARRAY(NPTS+2) = DIST
return
end Subroutine SKALE
