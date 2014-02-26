module Environmental_Data_Space
! file Envsiz.f90
Use Initial_Sizes
Implicit None
save
! Establish amount of mass storage required for data in the direct
! access file (exams.daf) describing the Exams aquatic environments.
! The number of reals NREALS = (MAXDAT+3)*NCON + MAXDAT*(NPX*26+6) + 6*NPX + 3
! The number of integers NINTS  = 4*NCON + 1
! The number of characters NCHARS = 50 + 12 + NPX + MAXDAT
!   i.e., 50 character name plus 2 passwords of 6 characters each
!   plus NPX compartment types and MAXDAT air mass types
integer, parameter :: IOSIZ = (MAXDAT+3)*NCON+MAXDAT*(NPX*26+6)+6*NPX+3
integer, parameter :: IOISIZ=4*NCON+1, IOCSIZ=62+NPX+MAXDAT
real,    allocatable  ::  IO(:) ! IO(IOSIZ)    upon allocation
integer, allocatable  ::  IOI(:) ! IOI(IOISIZ) upon allocation
integer, private ::  I
character(len=1), dimension(IOCSIZ) :: IOC=&
    (/(' ',i=1,50),'G','G','L','L','O','O','B','B','A','A','L','L',&
    (' ',i=1,(NPX+MAXDAT))/)
end module Environmental_Data_Space