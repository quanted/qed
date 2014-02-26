subroutine XBAR(X,HGT,WIDTH,MAXY,AREA,NOTE,NOTE1)
! Revised 24-DEC-85 (LAB)
use Implementation_Control
Implicit None
integer :: X,HGT,WIDTH,MAXY,X2,Y2,Y1,FLAG,NOTE
integer :: MAXW=15,IW,I,J,IOFF,K
! CHARACTER*1 STAR
! DATA STAR /'|'/
character(len=1) :: NOTE1, TEMP1
character(len=1), dimension(15) :: TOP, NONE = &
   (/'N','o','n','e',' ','N','o','n','e',' ','N','o','n','e',' '/)
character(len=3) :: TEMP3
character(len=61), dimension(21) :: AREA
IW = WIDTH
if (IW > MAXW) then
   write (stdout,fmt='(//A/A,I5,A,I5)')&
      ' Dimension of "TOP" in "XBAR" has been exceeded.',&
      ' Value is: ',IW,'; maximum is: ',MAXW
   IW = MAXW
endif
! Compute the right-hand side of the bar coordinates
X2 = X+IW-1
if (NOTE1 /= 'A' .and. NOTE == 0) then ! No data for this box
   J = 0
   do I = X, X2
      J = J+1
      AREA(Y2)(I:I) = NONE(J)
   end do
   return
end if
! Inscribe the box
Y1 = MAXY
if (HGT > 0) then
   do I = 1, HGT
      Y1 = MAXY-I+1
      ! Inscribe the margins of the box
      AREA(Y1)(X:X) = NOTE1
      AREA(Y1)(X2:X2) = NOTE1
      do J = X+1, X2-1
         AREA(Y1)(J:J) = '|' ! Inscribe the interior of the box
      end do
   end do
end if
! Fill in the top and bottom: This option requires that NOTE
! be printed at the top of the bar.
do I = 1, IW
   TOP(I) = NOTE1
end do
! If the parameters, NOTE and NOTE1, imply that "AVERAGE"
! values are being plotted, don't load the number stored
! in "NOTE" into the character string.
if (NOTE1 == 'A' .and. NOTE == 0) then
   FLAG = 1
else
   FLAG = 0
   IOFF = (IW-3)/2
   write (TEMP3,fmt='(I3)') NOTE
   do I = 1, 3
      if (TEMP3(I:I) == ' ') TEMP3(I:I) = '0'
      IOFF = IOFF+1
      TOP(IOFF) = TEMP3(I:I)
   end do
end if
Y2 = MAXY
K = 0
do I = X, X2
   if (FLAG == 1) then
      TEMP1 = NOTE1
   else
      K = K+1
      TEMP1 = TOP(K)
   endif
   AREA(Y1)(I:I) = NOTE1      ! Y1 = f(HGT), the top line
   AREA(Y2)(I:I) = TEMP1      ! Y2 = 21, the bottom line
end do
return
end Subroutine XBAR
