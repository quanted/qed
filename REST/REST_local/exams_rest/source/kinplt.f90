subroutine KINPLT(KOUNT,SELECT,NSEL,TABLE,OUTPUT,TYPEG,&
                  CHEMNA,ECONAM,PMAX,PMIN,MCHEMG)
! Purpose: KINPLT plots selected kinetic outputs on the user's terminal
! Subroutines required: KINHED, KINRED
! Revised 27-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
use Floating_Point_Comparisons ! Revisions 09-Feb-1999
use Implementation_Control
use Input_Output
Implicit None
real :: TABLE(132),OUTPUT(7),PMAX(7),PMIN(7),TFACTR
real :: X,XROW,XCOL,XMIN,XRANGE,Y,YMIN,YMAX,YRANGE
real :: YINC,XK,XINC
integer :: IX,IY,ROW=16,COL=51,YANNOT=4,XANNOT=11
integer :: IERR,KOUNT,ICODE,MCHEMG,INDEP,J,I,NSEL,IT,IHIT
integer, dimension(7) :: SELECT
! Plotting area is 51 columns by 16 rows
character(len=51), dimension(16) :: AREA
character(len=1), dimension (KOUNT) :: TYPEG
character(len=50) :: CHEMNA, ECONAM, NAMEC, NAMES
character(len=1), dimension(10) :: CCHAR = & 
   (/'A','*','+','#','>','X','J','K','L','M'/)
character(len=1) :: BAR ='I'
character(len=6),dimension(4) :: TUNIT=(/'Hours ','Days  ','Months','Years '/)
real, dimension(4) :: TN = (/1.0, 24.0, 730.5, 8766.0/)
rewind PLTLUN
call KINHED (IERR,NAMEC,NAMES,KOUNT,TYPEG,ICODE,MCHEMG)
if (IERR == 1) return
TFACTR = 1.0
if (SELECT(1) == 1) TFACTR = TN(ICODE)
INDEP = 1
! Initialize the plotting area
AREA = ' '
! Compute the plotting factors
XROW = real(ROW-1)
XCOL = real(COL-1)
YMIN =  1.0E+30
YMAX = -1.0E+30
do I = 1, NSEL
   if (I == INDEP) then
      XRANGE = PMAX(I)-PMIN(I)
      if (XRANGE .Equals. 0.0) XRANGE = 1.0
      XMIN = PMIN(I)
      IT = SELECT(INDEP)
   else
      if (PMAX(I) .GreaterThan. YMAX) YMAX = PMAX(I)
      if (PMIN(I) .LessThan.    YMIN) YMIN = PMIN(I)
   end if
end do

! Force YMIN to 0.0
YMIN = 0.0
YRANGE = YMAX-YMIN
if (YRANGE .Equals. 0.0) YRANGE = 1.0
! Compute plotting locations
rewind PLTLUN
call KINHED (IERR,CHEMNA,ECONAM,KOUNT,TYPEG,ICODE,MCHEMG)
if (IERR /= 1) then
   do
      call KINRED (IERR,KOUNT,TABLE,IHIT,MCHEMG)
      if (IERR == 2) exit
      if (IHIT == 0) cycle
      X = TABLE(IT)
      IX = int((X-XMIN)/XRANGE*XCOL+1.5)
      do I = 1, NSEL
         J = SELECT(I)
         if (J == INDEP) cycle
         Y = TABLE(J)
         IY = int((Y-YMIN)/YRANGE*XROW+1.5)
         IY = ROW-IY+1
         if (IY<1 .or. IY>ROW .or. IX<1 .or. IX>COL)&
            write (stdout,fmt='(//A/2(A,I5/),2(A,G14.7/),A,2I5)')&
               ' Plotting symbol out-of-range.',&
               ' Independent variable: ',IT,&
               ' Dependent variable  : ',J,&
               ' Independent value   : ',TABLE(IT),&
               ' Dependent value     : ',TABLE(J),&
               ' IX,  IY             : ',IX,IY
         AREA(IY)(IX:IX) = CCHAR(I)
      end do
   end do
end if
write (stdout,fmt='(//A/A)')&
   ' System:   '//NAMES,&
   ' Chemical: '//NAMEC
YINC = YMAX/real(YANNOT-1)
XK = 0.0
do I = 1, ROW
   if (mod(I,5) /= 1) then
      write (stdout,fmt='(12X,1A1,A)') BAR,AREA(I)(1:COL)
   else
      Y = YMAX-XK*YINC
      if (I == ROW) Y = 0.0   ! Force the label to 0.0 for aesthetics
      XK = XK+1.0
      write (stdout,fmt='(1X,1PG10.3,1X,1A1,A)') Y,BAR,AREA(I)(1:COL)
   end if
end do
write (stdout,fmt='(13X,10("+----"),"+")')
XINC = XRANGE/real(XANNOT-1)
do I = 1, XANNOT
   TABLE(I) = XMIN+real(I-1)*XINC
   TABLE(I) = TABLE(I)/TFACTR
end do
write (stdout,fmt='(10X,1PG10.3,10(1PG10.3))') (TABLE(I),I=1,XANNOT,2)
write (stdout,fmt='(15X,1PG10.3,10(1PG10.3))') (TABLE(I),I=2,XANNOT,2)
write (stdout,fmt='(32X,A)') 'Time, '//TUNIT(ICODE)
TABLE = 0.0 ! reset for next plot
return
end Subroutine KINPLT
