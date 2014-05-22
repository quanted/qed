subroutine TYPOPT(IOPT)
! Purpose: to determine type of plot desired: point, profile or kinetic
! Subroutines required: INREC
! Revised 24-DEC-85 (LAB)
! Revised 10/20/88--run-time formats for cursor control.
! Revision of message text 10/25/88
! Revised 10/26/88 to unify command abort style to "quit"
! Converted to Fortran90 2/20/96; 6/14/96
use Implementation_Control
use Input_Output
Implicit None
integer :: IFIND, EOF, IOPT
integer :: NTYPE = 5,  LENTYP=27
integer, dimension(5) :: TYPLEN = (/5,7,4,4,7/),&
                         MINTYP = (/2,2,1,1,1/)
character(len=1), dimension(27) :: TYPNAM = &
(/'P','O','I','N','T',  'P','R','O','F','I','L','E',&
  'H','E','L','P',  'Q','U','I','T',  'K','I','N','E','T','I','C'/)
do ! Find the type option
   IOPT = IFIND(NTYPE,LENTYP,TYPLEN,TYPNAM,MINTYP)
   select case (IOPT)
      case (0)
         write (stdout,fmt='(/A//A)',advance='NO')&
            ' Option not recognized; please try again.',&
            ' Option-> '
      case (-2,3) ! Null input or Help was selected
         write (stdout,fmt='(/A//5(A/)/A)',advance='NO')&
            ' The following options are available:',&
            '         POint   - Vertical concentration profile',&
            '         PRofile - Longitudinal concentration profile',&
            '         Kinetic - List or plot kinetic outputs',&
            '         Help    - This message',&
            '         Quit    - Return to the EXAMS program prompt',&
            ' Option-> '
      case (4) ! QUIT requested, user confirmation written in PLOTX
         return
      case default ! legit option or default bailout (2)
         return
   end select
   call INREC (EOF,stdin)
   IOPT = -1
   STOPIT = 0
   if (EOF == 1) return ! cancellation message written from calling procedure
end do
end subroutine TYPOPT
