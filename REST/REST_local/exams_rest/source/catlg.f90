subroutine CATLG
! Purpose: to catalog the current contents of the
! environmental, chemical, loads, or product chemistry database.
! Revised: 24-DEC-1985 (LAB); 10/21/88--run-time implementation of machine
! dependencies; Revised 11/17/88 to accommodate VAX multi-user environment
use Implementation_Control
use Initial_Sizes
Implicit None
real :: RESULT ! for DECOD1 interface
! Which: (1) - Chemicals,         (2) - Environmental descriptions, 
!        (3) - Chemical loadings, (4) - Product chemistry
integer :: II, I1, I2, ISET, MAXREC, IBUFF(VARIEC)
integer :: WHICH,CC,M,I,L,IO1,IO2,IO3,IO4,IO5,RECDAT(FILDAT),HRECS
integer, parameter :: FOUR = 4
! RECDAT carries the file information, HRECS is the number of
! header records required.
character(len=50) :: CBUFF
integer, dimension (5,4), parameter :: OFF = reshape(&
   (/ 9, 15, 16, 54, 17, 11, 21, 22, 55, 23,&
     45, 33, 34, 56, 35, 47, 39, 40, 57, 41/), (/5,4/))
logical :: Entry_printed
call DECOD1 (FOUR,WHICH,CC,RESULT) ! Call DECOD1 to find out which
if (CC /= 1) return                ! UDB is wanted, if error, bail out now
! Get file parameters (procedure is documented in DECOD1 and 2):
HRECS = FILDAT/VARIEC ! Read the header record for file control information
if (FILDAT-VARIEC*HRECS /= 0) HRECS = HRECS+1
M = 0
Read_loop: do I = 1, HRECS
   read (RANUNT,rec=I) IBUFF
   do L = 1, VARIEC
      M = M+1
      if (M > FILDAT) exit Read_loop
      RECDAT(M) = IBUFF(L)
   end do
end do Read_loop
IO1 = OFF(1,WHICH); IO2 = OFF(2,WHICH); IO3 = OFF(3,WHICH); IO4 = OFF(4,WHICH)
IO5 = OFF(5,WHICH); ISET = RECDAT(IO1); I2 = RECDAT(IO2)+RECDAT(IO3)
I1 = I2+RECDAT(IO4); MAXREC = RECDAT(IO5) ! File parameters complete
Entry_printed = .false. ! initialize detector of library entry
II = I2+ISET-I1 ! Compute loop-invariant part of character record offset
Tell_it: do I = 1, MAXREC
read (RANUNT,rec=(I*I1+II)) CBUFF
! If name field is blank, don't list this record; skip to next
if (len_trim(CBUFF) == 0) cycle Tell_it
First_entry: if (.not.Entry_printed) then ! print header
Entry_printed = .true.
select case (WHICH)
case(1);write (stdout,fmt='(/A)')' UDB #     Name of Chemistry Dataset'
case(2);write (stdout,fmt='(/A)')' UDB #     Name of Environmental Dataset'
case(3);write (stdout,fmt='(/A)')' UDB #     Name of Chemical Loadings Dataset'
case(4);write (stdout,fmt='(/A)')' UDB #     Name of Product Chemistry Dataset'
end select
write (stdout,fmt='(A)')& ! column header
   ' =====    =================================================='
end if First_entry
write (stdout,fmt='(1X,I4,5X,A)') I,trim(CBUFF) ! entry title
end do Tell_it
if (.not.Entry_printed) write (stdout,fmt='(/A)')&  ! i.e., loop ends
   ' No entries present in this library.'  ! without finding any entries
end subroutine CATLG
