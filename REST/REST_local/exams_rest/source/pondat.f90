subroutine PONDAT(EOF,NOTE,NOTEE,Y1,IVAL,IDAT)
! Purpose: to retrieve specific records from the plot file.
! The data to be selected are statistical information about the simulation
! and are available in two forms: water column, and bottom sediments. Each
! form has three parts--average, maximum and minimum.
! Latest revision 24-DEC-1985 (LAB)
use Implementation_Control
Implicit None
real :: Y(5,6),Y1(2)
integer :: EOF,IVAL,IDAT,NT(5,4),NOTE(2),I,K1,K2,J,IO_stat
character(len=1) :: DUM1(5,4), NOTEE(2)
logical :: Problem
! NOTE is used to acquire the number of the segment
! NOTEE is used to acquire the type of the segment (L, E, etc.)
! Y1 is used to acquire the value of the concentration
! NT is used to read the segment numbers from the file
! DUM1 is used to read the segment types from the file
! Y is used to read the values from the file
EOF = 0
Problem = .false.
do I = 1, 2
   K1 = (I-1)*3
   K2 = (I-1)*2
   ! Get the average data (initial read of J is a dummy read)
   read (PLTLUN,iostat=IO_stat) J,(Y(J,K1+1),J=1,5)
      if (IO_stat /= 0) Problem = .true.
   read (PLTLUN,iostat=IO_stat)&
   ! Get the maximum data (initial read of J is a dummy read)
      J,(NT(J,K2+1),J=1,5),(DUM1(J,K2+1),J=1,5),(Y(J,K1+2),J=1,5)
      if (IO_stat /= 0) Problem = .true.
   ! Get the minimum data (initial read of J is a dummy read)
   read (PLTLUN,iostat=IO_stat)&
      J,(NT(J,K2+2),J=1,5),(DUM1(J,K2+2),J=1,5),(Y(J,K1+3),J=1,5)
      if (IO_stat /= 0) Problem = .true.
   if (Problem) then
      write (stdout,fmt='(/A/)')&
         ' Problems reading plot file. Command cancelled.'
      EOF = 1
      return
   end if
end do
Y1(1) = Y(IDAT,IVAL)
Y1(2) = Y(IDAT,IVAL+3)
if (IVAL == 1) then ! average data was selected; special attention is required
   NOTE(1) = 0
   NOTE(2) = 0
   NOTEE(1) = 'A'
   NOTEE(2) = 'A'
else
   NOTE(1) = NT(IDAT,IVAL-1)
   NOTE(2) = NT(IDAT,IVAL+1)
   NOTEE(1) = DUM1(IDAT,IVAL-1)
   NOTEE(2) = DUM1(IDAT,IVAL+1)
end if
return
end subroutine PONDAT
