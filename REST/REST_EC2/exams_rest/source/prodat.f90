subroutine PRODAT(EOF,Y1,Y2,N1,N2,NOTE11,NOTE12,NOTE21,NOTE22,IDAT)
! Revised 24-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
use Implementation_Control
Implicit None
real :: Y1(1), Y2(1), X(7)
integer :: EOF,N1,N2,IDAT,NOTE11(1),NOTE21(1),ID,J
character(len=1) :: NOTE12(1), NOTE22(1), DUMMY
! NOTE11 and NOTE21 are used to acquire segment numbers.
! NOTE12 and NOTE22 are used to acquire segment types.
! X is used to aquire values for transfer to Y.
EOF = 0
! Compute the proper subscript
ID = IDAT+3
if (ID > 7) ID = 1
! Get water column data
N1 = 0
N2 = 0
do
   read (PLTLUN,err=150,end=140) J,J,DUMMY,X ! 1st J is dummy read
   if (DUMMY == '*') exit
   N1 = N1+1
   NOTE11(N1) = J
   NOTE12(N1) = DUMMY
   Y1(N1) = X(ID)
end do

! Collect the sediment data
do
   read (PLTLUN,err=150,end=140) J,J,DUMMY,X ! 1st J is dummy read
   if (DUMMY == '*') exit
   N2 = N2+1
   NOTE21(N2) = J
   NOTE22(N2) = DUMMY
   Y2(N2) = X(ID)
end do
return

140   continue
EOF = 1
return
150   continue
write (stdout,fmt='(/A/)')&
   ' Error while reading plot file. Task aborted.'
EOF = 1
return
end Subroutine PRODAT
