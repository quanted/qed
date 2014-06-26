function IHELP(IT)
! Purpose: to determine if "HELP" or "QUIT" was input
! If IT = 0, then neither
! IT = 1, then "HELP"
! IT = 2, then "QUIT"
Implicit None
integer :: IHELP
integer, parameter :: TWO = 2
integer :: IT
integer :: MATCH, HELSIZ=8
integer, dimension(2) :: HQUIT=(/4,4/), HELMIN=(/1,1/)
character(len=1), dimension(8) :: HELNAM= (/'H','E','L','P','Q','U','I','T'/)
IT = MATCH(TWO,HELSIZ,HQUIT,HELNAM,HELMIN)
IHELP = IT
end function IHELP
