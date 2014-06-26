subroutine XVALUE(DIGIT,LENGTH,OUTCOM,NOTNUM)
! Purpose: this subroutine converts a character string to a numerical value
! The only acceptable characters are the digits 0,1,2,3,4,5,6,7,8,9 plus the
! delimiters -, +, ., E, D, e, and d.
! Revised 08-Feb-1999 to make floating point comparisons
use Floating_Point_Comparisons
Implicit None
real :: EXPON,Sum_total,TENTH
real, intent (out) :: OUTCOM
real, parameter :: TEN = 10.
real :: Real_KEY, Expo_KEY
integer :: START, I_dec, I_exp, I
logical :: Integer, Fraction, Exponent
logical, intent (out) :: NOTNUM ! added 1/22/96 to signal error in input
integer, intent (in) :: LENGTH ! number of characters in DIGIT
character(*), intent (in) :: DIGIT ! the input character string
character(len=10), parameter :: ANUMB= '0123456789'

NOTNUM = .false. ! Assume the input is a number until shown otherwise
TENTH = 0.1
Sum_total = 0.0
EXPON = 0.0
Real_KEY=1.0
Expo_KEY=1.0
Reality_Check: do I = 1, LENGTH
! The entry must contain only numbers, decimal point, exponent, or signs...
if (scan(DIGIT(I:I),'0123456789+-.eEdD') == 0) then ! if anything else
  NOTNUM = .true.                        ! is present, flag the result
end if
end do Reality_Check
if (LENGTH==1 .and. scan(DIGIT(1:1),ANUMB)==0) NOTNUM = .true. !
if (NOTNUM) return ! might as well quit now if failed either reality check

! Locate potential demarkation points, check for degenerate cases,
! and cue the rest of the code
I_dec = index(digit,'.') ! find the decimal point, if any
Point_check: if (I_dec > 0)  then
   Fraction = .true.
   Up_front: if (I_dec==1) then ! check for degeneracy--already tested singles
      if (scan(Digit(2:2),ANUMB) == 0) NOTNUM = .true. ! i.e., "." w/o number
   end if Up_front
   if (index(digit,'.',back=.true.)>I_dec) NOTNUM=.true.!i.e.,>1 decimal point
else Point_check
   Fraction = .false. ! i.e., no decimal point in input
   I_dec = LENGTH +1 ! alias I_dec for loop controls
endif Point_check; if (NOTNUM) return ! bail out here because of reset below
Integer = .true.     ! assume integer part exists,
if (I_dec == 1) then ! unless the entry leads off with decimal
Integer = .false.
end if
I_exp = scan(digit,'EeDd') ! find the exponent part, if any
Exponent_check: if (I_exp > 0) then
   Exponent = .true. ! but check for problems and degenerate cases
   if (I_exp==1) NOTNUM = .true. ! no number before exponent
   if (I_exp==LENGTH) then;NOTNUM=.true.;return;endif ! no exponent; bail out
   if (scan (Digit (I_exp+1:I_exp+1),'0123456789+-')==0) NOTNUM = .true.
   if (NOTNUM) return ! bail out here because the next test will
   NOTNUM = .true.    ! nullify results obtained already
   do i = 1, I_exp-1 ! There must be at least one numerical digit before E
      if (index(ANUMB,Digit(i:i))>0) NOTNUM = .false. ! note that 0 is o.k.
   end do ! if exits the loop without resetting NOTNUM, it's a bad case
   START = I_exp+1 ! now check what lies beyond the exponent (EeDd) sign
   call Check_Sign(Expo_KEY)! if it's + or -, start is bumped up one, so
   if (START>LENGTH) then;NOTNUM=.true.;return;endif ! out of room, bail out
   do i = START, LENGTH
   if (index(ANUMB,Digit(i:i))==0) NOTNUM = .true. ! i.e., non-numeric in field
   end do
   if (scan(digit,'EeDd',back=.true.)>I_exp) NOTNUM=.true. ! i.e., >1 exponent
else Exponent_check
   Exponent = .false.
   I_exp = LENGTH+1 ! alias I_exp if no exponent part
endif Exponent_check
if (NOTNUM) return ! Bail out now if problems detected

START = 1
call Check_Sign(Real_KEY)

if (Integer) then
   do I = Start, min(I_dec-1,I_exp-1,Length)
      Sum_total = Sum_total*TEN+float(index(ANUMB,DIGIT(I:I))-1)
   end do
end if

if (Fraction) then
   do I = I_dec+1,min(I_exp-1,Length)
      Sum_total = Sum_total + float(index(ANUMB,DIGIT(I:I))-1)*Tenth
      tenth = tenth/TEN
   end do
end if

if (.not. (Sum_total .GreaterThan. 0.0)) then
      OUTCOM=0.0; return; end if ! leave now if zero value
if (Exponent) then
   START = I_exp+1
   call Check_Sign(Expo_KEY) ! set sign of exponent...
   do I = start, length
      EXPON = EXPON*TEN + float(index(ANUMB,DIGIT(I:I))-1)
   end do
end if

OUTCOM = Sum_total*Real_KEY*TEN**(EXPON*Expo_KEY)
return

contains
Subroutine Check_Sign(KEY)
real :: KEY
select case (DIGIT(START:START)) ! Determine positive or negative value
case ('-') ! first digit is negative;
   KEY = -1. ! set multiplier,
   START = START+1 ! and start on next character
case ('+') ! first character is +; skip to next character
   KEY = 1.
   START = START+1
case default ! first character is neither + nor -
   KEY = 1. ! no lead sign, take as positive number
!  START = START ! commence with given character, don't change START
end select
end Subroutine Check_Sign
end Subroutine XVALUE
