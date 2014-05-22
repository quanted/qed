subroutine KINOPT(KIN)
! Purpose: KINOPT determines the KINETIC option (LIST or PLOT)
! Subroutines required: IFIND, INREC
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
! dependent cursor control.
! Revised 10/26/88 to unify command abort style to "quit"
! Converted to Fortran90 2/20/96; 6/14/96
use Implementation_Control
use Input_Output
Implicit None
integer EOF, KIN, IFIND
integer :: NDATA = 4, LENDAT = 16
integer, dimension(4) :: DATLEN = (/4,4,4,4/), MINDAT = (/1,1,1,1/)
character(len=1), dimension(16) :: DATNAM = &
   (/'L','I','S','T',  'P','L','O','T',  'H','E','L','P',  'Q','U','I','T'/)
do ! Get the kinetic option
   KIN = IFIND(NDATA,LENDAT,DATLEN,DATNAM,MINDAT)
   select case (KIN)
      case (0)
         write (stdout,fmt='(/A//A)',advance='NO')&
            ' Option not recognized, please try again.',&
            ' Option-> '
      case (-2,3)! null input or HELP was selected
         write (stdout,fmt='(/A//4(A/)/A)',advance='NO')&
            ' The following KINETIC options are available:',&
            '        List - lists selected KINETIC output parameters',&
            '        Plot - plots selected KINETIC output parameters',&
            '        Help - this message',&
            '        Quit - return to the EXAMS prompt',&
            ' Option-> '
      case (4) ! QUIT requested, user confirmation written in PLOTX
         return
      case default
         return
   end select
   call INREC (EOF,stdin)
   KIN = -1
   STOPIT = 0
   if (EOF == 1) return
end do
return
end subroutine KINOPT
