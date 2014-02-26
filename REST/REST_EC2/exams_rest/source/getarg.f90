module getarg_mod

contains

subroutine GETARG(NARGS,ARGS,IT,ITM1)
! Purpose--to determine the number of subscripts for the model parameter.
! Subroutines required--SKAN, XVALUE
! Altered 1/22/96 for change in subroutine XVALUE interface
! Converted to Fortran90 6/5/96

use Implementation_Control
use Input_Output
use Model_Parameters
use MultiScan
Implicit None
real :: ARGS(:), ARG1
integer :: NARGS, IT, LENGTH, ITM1
logical :: NOTNUM
character(len=1), dimension(3) :: CLOLIM = (/' ',',',')'/)
NARGS = 0
Parse_argument: do
   START = STOPIT+1
   call SKAN(INPUT,START,STOPIT,TYPE,CLOLIM)
   if (TYPE == 1) then ! blank delimiter; insufficient input to process
      IT =2
      return
   end if
   LENGTH = STOPIT-START ! Compute length of the argument
   if (LENGTH == 0) then ! If length is zero, then the argument was null
      IT = 8
      return
   end if
   ARG1 = -1.0
   if (.not.(LENGTH==1 .and. INPUT(START:START)=='*')) then
      call XVALUE(INPUT(START:(START+LENGTH-1)),LENGTH,ARG1,NOTNUM)
      if (NOTNUM) then ! not valid numeric subscript
         IT = 5
         return
      end if
   end if
   NARGS = NARGS+1
   ARGS(NARGS) = ARG1
   ! If the delimiter was not a ")" search for more arguments;
   if (TYPE == 3) exit Parse_argument ! if it is a ")", exit the loop
end do Parse_argument
if (ITM1 /= NARGS) then ! NARGS is invalid for the variable's storage type
   IT = 4
else
   IT = 0 
end if
return
end subroutine GETARG

end module getarg_mod