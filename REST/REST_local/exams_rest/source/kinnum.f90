subroutine KINNUM(CC,RESULT)
! KINNUM gets input from stdin and determines if the response contains a
! number or one of the strings "HELP" or "QUIT". CC is set to reflect the
! success of the operation.
! Subroutines required: INREC, IFIND, GETNUM
! Revised 24-DEC-85 (LAB)
use Implementation_Control
use Input_Output
Implicit None
real :: RESULT
integer :: CC,EOF,IFIND,IERR,Two=2,HELSIZ=8
integer, dimension(2) :: HQUIT = (/4,4/), HELMIN=(/1,1/)
character(len=1), dimension(8) :: HELNAM=(/'H','E','L','P',  'Q','U','I','T'/)
call INREC(EOF,stdin)
CC = 2
if (EOF == 1) return
STOPIT = 0
CC = IFIND(Two,HELSIZ,HQUIT,HELNAM,HELMIN)+3
if (CC /= 3) return
STOPIT = 0
call GETNUM (IERR,RESULT)
select case (IERR)
   case (0)    ! no error
      CC = 6
   case (1)    ! no character on the line,
      CC = 1   ! treat as request for help
   case (2)    ! not a number, set CC
      CC = 3   ! to emit "unrecognized" message
end select
return
end subroutine KINNUM
