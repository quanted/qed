Module MultiScan
contains
subroutine SKAN(STRING,START,STOPIT,TYPE,DELIM)
! Purpose--this subroutine analyzes a character string for specified multiple
! delimiters and returns the index of the first delimiter encountered.
! Revised array dimensioning 11/1/88
! Rewritten to Fortran90 3/26/96; 05/12/99
Implicit None
character(*) :: STRING         ! the array of characters to be processed
character(len=1) :: DELIM(:)  ! array of delimiters tested
integer :: START, STOPIT, TYPE, Ndelim
! START - index of the first character to be analyzed
! STOPIT - index or location of delimiter
! TYPE   - type of delimiter
if (START < 1) START = 1
Ndelim=size(DELIM)
do STOPIT = START, len(STRING)
   do TYPE = 1, Ndelim      ! Search for delimiter, if found, return
      if (STRING(STOPIT:STOPIT) == DELIM(TYPE)) return
   end do
end do
TYPE = 100 ! null line--exited loop with no delimiter found
end subroutine SKAN
end Module MultiScan