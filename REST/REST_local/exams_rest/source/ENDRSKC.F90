subroutine EndRskC
! Created 2002-06-04
! Sorts annual maxima and moves data to EcoRisk file.
use Global_Variables
use Implementation_Control
use Statistical_Variables
use Local_Working_Space
implicit none
real, allocatable :: Maxima(:,:)
character (len=10), allocatable :: Dates(:,:)
integer:: Space, Year, I, IOErr
real :: WPP, WPP_Denominator ! Weibull plotting position
! read scratch file containing annual maxima, re-order for Weibull plot
rewind TmpLUN1
! allocate space for annual maxima and their dates
Space = KCHEM*(7+NumEvents)*2
allocate (Maxima(Space,YearCount-1), Dates(Space,YearCount-1))

do Year=1,YearCount-1
! read annual maxima from scratch file for ordering and output
   read (TmpLUN1,fmt='(32767(1X,ES9.2,1X,A10))') &
      (Maxima(I,Year),Dates(I,Year),I=1,Space)
end do
! The file is closed and deleted when Exams terminates
! Sort the events
do I=1,Space
   call RankSort(YearCount-1,Maxima(I,:),Dates(I,:))
end do

call Assign_LUN (RSKCLUN)
open (unit=RSKCLUN, status='old', access='sequential',&
      position='append',form='formatted', file='EcoRiskC.xms',&
      action='readwrite', iostat=IOerr)
! notate the beginning of the data stream
write (RskCLUN,fmt='(A)') '!!! Start of numerical data'
! write the events to the EcoRisk file in sorted order
WPP_Denominator=YearCount ! number of years + 1
do Year=1,YearCount-1
   WPP=100.0*float(Year)/WPP_Denominator
   write (RskCLUN,fmt='(F6.2,32767(1X,ES9.2,1X,A10))')&
      WPP, (Maxima(I,Year),Dates(I,Year),I=1,Space)
end do
deallocate (Maxima, Dates)
close (TmpLUN1, status='DELETE') ! close and delete working storage
end subroutine EndRskC
