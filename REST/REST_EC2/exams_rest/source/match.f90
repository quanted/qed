integer function MATCH(NUMB,NUMNAM,LENS,NAME,MINS)
! This routine gets the next input 'token' (chemical name,
! command name, etc.) and returns the index of that list item.
! The procedure operates via loop processing that is cycled by the failure
! of a character to match. It tests the NAMEs one-by-one, and if no NAME
! survives the testing MATCH is set to zero. To survive the testing, a
! list entry must simply make it all the way through the loops without
! provoking a loop cycle triggered by a mismatch.
! Local variable identification area
! Name    Type         Dimension      Description
! K       Integer         01      temporary index variable
! LENS    Integer         *       vector of name lengths
! LSTART  Integer         01      temporary index variable
! MINS    Integer         *       vector of minimum command lengths
! NAME    Character       *       vector of names
! NUMB    Integer         01      number of entries in list
use Implementation_Control
use Input_Output
Implicit None
! Variable storage and definition section
integer :: K, NOCHAR, LSTART
integer, intent(in) :: NUMB, NUMNAM, LENS(NUMB), MINS(NUMB)
integer :: LENGTH, I, MNLEN, J, low
character(len=1) :: NAME(NUMNAM)
character(len=1) :: TEMP1, TEMP2
! Initialize the lower and upper case character constants
character (26), parameter :: Lower = "abcdefghijklmnopqrstuvwxyz",&
                             Upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

LENGTH = STOPIT-START ! Compute the input string length
K = 0
! Compare the input with the "NUMB" entries in the list "NAME"
Entry_loop : do I = 1, NUMB
   NOCHAR = LENS(I)              ! Get length of the i'th list entry
   if (I > 1) K = K+LENS(I-1)   ! Update pointer to the start of this item
   MNLEN = MINS(I)                        ! If the length of the input string
   if (LENGTH > NOCHAR .or. &             ! is incompatible with this item,
       LENGTH < MNLEN) cycle Entry_loop   ! try the next entry in the list.
   ! Compute the input string starting address minus one
   LSTART = START-1  ! LSTART will now count through the elements of INPUT
   ! Compare the input string with the list entry, character by character
   Character_loop: do J = 1, MNLEN
      LSTART = LSTART+1
      TEMP1 = INPUT(LSTART:LSTART)
      TEMP2 = NAME(J+K)
      if (TEMP1 == TEMP2) cycle Character_loop ! got a match, try the next
      ! Character did not match, but it may simply be lower case
      low = index(Lower,TEMP1) ! Is the input character lower case?
      if (low == 0) then  ! If not, then the entry is not this item;
         cycle Entry_loop ! try the next entry in the master list.
      else                ! The character is lower case, so 
         if (TEMP2 == Upper(low:low)) then  ! if the lower case input matches
            cycle Character_loop      ! this one, go on to the next character.
         else                         ! This character kills the trial, so
            cycle Entry_loop          ! try the next entry in the master list.
         end if
      end if
   End do Character_loop
                          ! This item matches out to the uniqueness point, BUT
  Longer: if (LENGTH > MNLEN) then    ! if the input is longer than uniqueness
    More_characters: do J = MNLEN+1, LENGTH        ! it must continue to match
      LSTART = LSTART+1         ! continue with LSTART to find input character
      TEMP1 = INPUT(LSTART:LSTART)
      TEMP2 = NAME(J+K)
      if (TEMP1 == TEMP2) cycle More_characters ! This one O.K., try the next
      ! Character did not match, but it may simply be lower case
      low = index(Lower,TEMP1) ! Is the input character lower case?
      if (low == 0) then  ! If not, then the input is not this item;
         cycle Entry_loop ! try the next entry in the master list.
      else                ! The character is lower case, so
         if (TEMP2 == Upper(low:low)) then  ! if the lower case input matches
            cycle More_characters     ! this one, go on to the next character.
         else                         ! This character kills the trial, so
            cycle Entry_loop          ! try the next entry in the master list.
         end if
      end if
    End do More_characters
  end if Longer
   MATCH = I    ! input identified--survived all tests
   return
End do Entry_loop
MATCH = 0    ! exhausted the Entry_loop with all candidates rejected
end function MATCH
