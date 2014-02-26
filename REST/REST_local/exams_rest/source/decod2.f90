subroutine DECOD2(IREC,CC,WHICH,II,CBUFF)
! Revised 24-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
! Revised 11/17/88 to accommodate VAX multi-user environment
use Implementation_Control
use Initial_Sizes
Implicit None
integer :: CC,IBUFF(VARIEC),HRECS,RECDAT(FILDAT)
integer, intent (in) :: IREC, WHICH
! RECDAT carries the file information
! HRECS is the number of header records required.
integer :: M,I,L,IO1,IO2,IO3,IO4,IO5,ISET,I1,I2,MAXREC,II,J
character(len=1) :: CBUFF(VARCEC)
character(len=11), dimension(4), parameter:: UDB_string = &
   (/'Chemical   ','Environment','Load       ','Product    '/)
! Define table that relates databases and pointers in Record 1
! of file EXAMDAF. The entries in the table refer to Integer
! locations in the file information vector (RECDAT(9), etc.).
!
!          1      2      3      4
!      +------+------+------+------+
!  A   :  09  :  11  :  45  :  47  :
!  B   :  15  :  21  :  33  :  39  :
!  C   :  16  :  22  :  34  :  40  :
!  D   :  54  :  55  :  56  :  57  :
!  E   :  17  :  23  :  35  :  41  :
!      +------:------:------:------+
integer, dimension (5,4), parameter :: OFF = reshape(&
   (/ 9, 15, 16, 54, 17, 11, 21, 22, 55, 23,&
     45, 33, 34, 56, 35, 47, 39, 40, 57, 41/), (/5,4/))
! Where  A - beginning record number of database - 1
!        B - number of real records
!        C - number of integer records
!        D - number of character records
!        E - maximum number of logical records, i.e.,
!            the total number of entries in the catalog.
! Databases
!        1 - Chemical
!        2 - Environment
!        3 - Load
!        4 - Product

CC = 1 ! set signal that all is well, it will be reset if a problem is found

bad_record: if (IREC < 1) then ! set signal, report, and get out
   CC=3
   write (stdout,fmt='(A,I11)')&
      ' '//trim(UDB_string(WHICH))//' record number is out-of-range: ',IREC
   return
end if bad_record

HRECS = FILDAT/VARIEC ! Get file parameters from the disk file
if (FILDAT-VARIEC*HRECS /= 0) HRECS = HRECS+1
M = 0
records: do I = 1, HRECS ! Read the header record for file control information
read (RANUNT,rec=I) IBUFF
   data: do L = 1, VARIEC
      M = M+1
      if (M > FILDAT) exit records
      RECDAT(M) = IBUFF(L)
   end do data
end do records

IO1 = OFF(1,WHICH) ! Starting number of database
IO2 = OFF(2,WHICH) ! Number of real records per entry in this database
IO3 = OFF(3,WHICH) ! Number of Integer records per entry in this database
IO4 = OFF(4,WHICH) ! Number of Character records per entry in this database
IO5 = OFF(5,WHICH) ! Total number of catalog entries in this database

ISET = RECDAT(IO1) ! First record in this UDB dataset (chemical, etc.)
I2 = RECDAT(IO2)+RECDAT(IO3)  ! Offset from first record needed to reach first
  ! Character record, which contains the name field in its first 50 characters
I1 = I2+RECDAT(IO4) ! Total number of records in each entry
MAXREC = RECDAT(IO5)
Too_big: if (IREC > MAXREC) then ! Check that record number is in range...
   CC=3                          ! if not, signal error, report, and get out
   write (stdout,fmt='(A,I11)')&
      ' '//trim(UDB_string(WHICH))//' record number is out-of-range: ',IREC
   return
end if Too_big

II = ISET+(IREC-1)*I1+I2 ! Calculate the record to be read as
!    ISET, (first record in this database) PLUS
! (IREC (the catalog number) - 1) * I1 (the total number of records per entry)
! PLUS I2 (the (real+integer) records that precede the first character record,
!                            the which contains the name of the catalog entry)
read (RANUNT,rec=II) CBUFF ! Next: is the requested record defined?
Title_test: do J = 1, 50     ! Test for an actual entry, i.e., that title for
   if (CBUFF(J) /= ' ') return      !  this slot has some non-blank character
end do Title_test      !****** note device of terminating routine if O.K.
CC = 2 ! i.e., if loop terminates with no non-blanks, set error report and end
end subroutine DECOD2
