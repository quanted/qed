subroutine EndRskR
! Created 2002-06-04
! Sorts annual maxima and moves data to EcoRisk file.
use Global_Variables
use Implementation_Control
use Statistical_Variables
use Local_Working_Space
implicit none
real, allocatable :: Maxima(:,:)
integer:: Space, Year, I, IOErr
real :: WPP, WPP_Denominator ! Weibull plotting position
character (len=10), allocatable :: Dates(:,:)
character (len=24) :: Read_Format = ' '
character (len=30) :: Write_Format = ' '
! read scratch file containing annual maxima, re-order for Weibull plot
rewind TmpLUN2
! allocate space for annual maxima and their dates
Space = KCHEM*(7+NumEvents)*2
allocate (Maxima(Space,YearCount-1), Dates(Space,YearCount-1))
! create run-time formats for file processing
write (Read_Format,"('(',I5,'(1X,ES9.2,1X,A10))')") Space
write (Write_Format,"('(F6.2,',I5,'(1X,ES9.2,1X,A10))')") Space
do year=1,YearCount-1
! read annual maxima from scratch file for ordering and output
!   read (TmpLUN2,fmt='(32767(1X,ES9.2,1X,A10))') &
   read (TmpLUN2,Read_Format) &
      (Maxima(I,Year),Dates(I,Year),I=1,Space)
end do
! The file is closed and deleted when Exams terminates
! Sort the events
do I=1,Space
   call RankSort(YearCount-1,Maxima(I,:),Dates(I,:))
end do

call Assign_LUN (RSKRLUN)
open (unit=RSKRLUN, status='old', access='sequential',&
      position='append',form='formatted', file='EcoRiskR.xms',&
      action='readwrite', iostat=IOerr)
! notate the beginning of the data stream
write (RskRLUN,fmt='(A)') '!!! Start of numerical data'
! write the events to the EcoRisk file in sorted order
WPP_Denominator=YearCount ! number of years + 1
do Year=1,YearCount-1
   WPP=100.0*float(Year)/WPP_Denominator
!   write (RskRLUN,fmt='(F6.2,32767(1X,ES9.2,1X,A10))')&
   write (RskRLUN,Write_Format)&
!      (100*Year/YearCount, (Maxima(I,Year),Dates(I,Year),I=1,Space),Year=1,YearCount-1)
      WPP, (Maxima(I,Year),Dates(I,Year),I=1,Space)
!      100*Year/YearCount, ((Maxima(I,Year),Dates(I,Year), Dates(I,Year)),I=1,Space)
end do
deallocate (Maxima, Dates)
close (TmpLUN2, status='DELETE') ! close and delete working storage
end subroutine EndRskR
