function IFIND(NUMB,NAMLEN,LENS,NAME,MINS)
! Purpose--to test whether an input string is contained in the set of strings,
! NAME. There are NUMB entries, each entry(I) has a length of LENS(I)
! and requires a minimum length of MINS(I) to be unique.
! Subroutines required--IMBED, MATCH, SKAN
use Implementation_Control
use Input_Output
use MultiScan
Implicit None
integer :: IFIND
integer :: NUMB, NAMLEN, LENS(NUMB), MINS(NUMB)
integer :: IMBED, MATCH ! external functions
character(len=1), dimension(1), parameter :: BLANK = ' '
character :: NAME(NAMLEN)

! Update the string pointer, start search for the first non-blank character
START = IMBED(INPUT,STOPIT)
if (START == -999) then ! null input
   IFIND = -2
   return
endif

! Start of a string encountered, determine its length by searching out the
! next blank
call SKAN (INPUT,START,STOPIT,TYPE,BLANK)

! If no blank is found, then presumably we have signifant input all the way
! to the end of INPUT, so the location AFTER the end of the input is len+1
if (TYPE == 100) STOPIT = len(INPUT) + 1

IFIND = MATCH(NUMB,NAMLEN,LENS,NAME,MINS)
! IFIND could be set to -1 to indicate end-of-file...
return
end function IFIND
