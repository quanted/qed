function IMBED(STRING,START)
! Locates next non-blank, non-tab character in input string
! Revised 27-DEC-85 (LAB), 11/10/88, 23-Feb-96, 21-Mar-96
Implicit None
integer :: IMBED
integer :: START ! starting point for search of "string"
integer :: i ! local counter
character (*) :: STRING
! Set IMBED to index of first non-blank character after START
Kill_tab: do ! Alter all horizontal tabs to blanks
  i = index(string,achar(09))
  if (i==0) exit
  string(i:i) = " "
end do Kill_tab
do i = START+1, len_trim(string)
  if (STRING(i:i) /= ' ') then
    IMBED = i
    return
   end if
end do
IMBED = -999 ! Set IMBED to -999 if no non-blank, non-tab character is present
end function IMBED
