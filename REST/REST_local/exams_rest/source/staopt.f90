subroutine STAOPT(IVAL)
! Purpose: to determine the statistical option
! Subroutines required: INREC
! Revised 24-DEC-85 (LAB)
! Revised 10/24/88 (LAB) -- run-time formats for implementation-
! dependent cursor control.
! Revised message text 10/25/88
! Converted to Fortran90 2/20/96; 6/14/96
use Implementation_Control
use Input_Output
Implicit None
integer :: EOF, IVAL, IFIND
integer, dimension(5) :: VALLEN = (/7,7,7,4,4/), &
                         MINVAL = (/1,2,2,1,1/)
integer :: NVAL = 5, LENVAL = 29
character(len=1), dimension(29) :: VALNAM = &
(/'A','V','E','R','A','G','E',  'M','A','X','I','M','U','M', &
  'M','I','N','I','M','U','M',  'H','E','L','P',  'Q','U','I','T'/)
do ! Get the value parameter
   IVAL = IFIND(NVAL,LENVAL,VALLEN,VALNAM,MINVAL)
   select case (IVAL)
      case (0)
         write (stdout,fmt='(/A//A)',advance='NO')&
            ' Option not recognized; please try again.',&
            ' Option-> '
      case (-2,4) ! null input or Help was selected
         write (stdout,fmt='(/A//5(A/)/A)',advance='NO')&
         ' The following statistical options are available:',&
         '        MAXimum    - Maximum concentration',&
         '        MINimum    - Minimum concentration',&
         '        Average    - Average concentration',&
         '        Help       - This message',&
         '        Quit       - Return to the EXAMS prompt',&
         ' Option-> '
      case (5) ! QUIT requested, user confirmation written in PLOTX
         return
      case default
         return
   end select
   call INREC (EOF,stdin)
   IVAL = -1
   STOPIT = 0
   if (EOF == 1) return
end do
return
end subroutine STAOPT
