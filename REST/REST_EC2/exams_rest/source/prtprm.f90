subroutine PRTPRM(IT)
! Purpose--To provide a means of reading the value of variables in the model.
! If the expression is not found on the current line, a prompt is presented.
! Revised 27-DEC-85 (LAB)
! Converted to Fortran90 6/6/96
! Error returns
! -3 * COMMON group not found
! -2 * invalid name
! -1 * E-O-F (end of file)
!  0 * O.K.
!  1 * null input
!  2 * imbedded blank, system error
!  3 * subscript out-of-range
!  4 * invalid number of arguments
!  5 * invalid subscript
!  6 * common name specified
!  7 * a scalar cannot have an argument
!  8 * null argument

use Implementation_Control
use Input_Output
use Alias_Transfer
use Global_Variables
use Model_Parameters
use MultiScan
use getarg_mod
Implicit None
real :: ARGS(10)
integer :: LOW1,LOW2,LOW3,UP1,UP2,UP3,SUBS(6),NARGS,ITDTD
integer :: LOWUP(6),IT,K,I,INDX,MATCH,N,N1,LENT,JJ,ITS,ITM1
character(len=1) :: NAME(6), TEMP
character(len=1), dimension(3) :: DELIM = (/' ','(','='/)
IT = 0
START = STOPIT+1
! Remove all imbedded blanks and tabs from the input line
K = START-1
do I = START, len(INPUT)
   TEMP = INPUT(I:I)
   if (TEMP == ' ' .or. TEMP == achar(9)) cycle
   K = K+1
   INPUT(K:K) = INPUT(I:I)
end do
! Blank remainder of line
if (K < len(INPUT)) then
   IT = 1
   if (K == START-1) return
   K = K+1
   INPUT(K:) = ' '
end if
! Now ready to decipher ... look for name of variable
call SKAN(INPUT,START,STOPIT,TYPE,DELIM)
! See if a valid name
INDX = MATCH(NOMOD,LNMODS,MODLEN,MODS,MODMIN)
IT = -2
if (INDX == 0) return
! See if the name of a Named Common Block was requested
IT = 6
if (TD(INDX) == 0) return
! Get starting location of name
N = 0
N1 = INDX-1
do I = 1, N1  ! F95 loop will not execute if N1=0
   N = N + MODLEN(I)
end do
LENT = MODLEN(INDX)
N1 = N+LENT
N = N+1
! If the last character in the name of the variable is "G",
! don't print it; it merely indicates that the variable
! is of Global extent (i.e., modifiable by the interactive
! user). Furthermore, the user's guide omits the last letter
! if it is a "G" so most users will not request this form.
if (MODS(N1) == 'G') then
   N1 = N1-1
   LENT = LENT-1
endif
JJ = N-1
do I = 1, LENT
   JJ = JJ+1
   NAME(I) = MODS(JJ)
end do
ITS = TS(INDX)
SUBS(6) = LENT
if (TYPE /= 1) then
   ! See if the variable is a scalar
   IT = 7
   if (ITS == 0) return
   ITM1 = TS(INDX)-1
   call GETARG (NARGS,ARGS,IT,ITM1)
   if (IT /= 0) return
end if
! Validate subscript ranges
call CHKSUB (ARGS,INDX,LOWUP,IT)
if (IT /= 0) return
LOW1 = LOWUP(1)
LOW2 = LOWUP(2)
LOW3 = LOWUP(3)
UP1 = LOWUP(4)
UP2 = LOWUP(5)
UP3 = LOWUP(6)
RDWR = 1
ITDTD = TD(INDX)
! Create output format
SUBS(4) = ITS
SUBS(5) = ITDTD
do ICL1 = LOW1, UP1
   SUBS(1) = ICL1
   do ICL2 = LOW2, UP2
      SUBS(2) = ICL2
      do ICL3 = LOW3, UP3
         SUBS(3) = ICL3
         call GETVAR
         call BLDOUT (SUBS,NAME)
      end do
   end do
end do
return
end subroutine PRTPRM
