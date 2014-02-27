Subroutine GETNUM(ERROR,RESULT) ! Routine to search a record and return the
         ! numerical equivalent of the characters found on the line
! Subroutines required: SKAN, XVALUE
! Altered 1/22/96 for new interface to XVALUE
use Implementation_Control
use Input_Output
use MultiScan
Implicit None
real :: RESULT
integer :: ERROR, LENGTH, IMBED
! ERROR - 0 if no errors detected
! ERROR - 1 if no characters encountered
! ERROR - 2 if the converted characters are not a valid number
logical :: NOTNUM
character(len=1), dimension(1), parameter :: BLANK = ' '
ERROR = 0 ! Initialize ERROR, i.e., set for no error
! Search for the beginning of a number after skipping lead blanks
START = IMBED(INPUT,STOPIT) ! delimiter: skip preceding blanks
if (START == -999) then ! no non-blank characters found
   ERROR = 1; return
endif
! Start of input found by IMBED at START, now skan for blank as the end mark
call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
if (TYPE == 100) STOPIT = len(INPUT)+1 ! if no blank, process the whole line
LENGTH = STOPIT-START
call XVALUE(INPUT(START:(START+LENGTH-1)),LENGTH,RESULT,NOTNUM)
if (NOTNUM) ERROR = 2
return
end subroutine GETNUM
