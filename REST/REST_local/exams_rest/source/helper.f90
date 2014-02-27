module Help_Text_Space
! file helper.f90
! defines size of storage areas for EXAMS help text
! COMCHR is maximum number of characters in EXAMS commands
! MAXHLP is maximum number of entries in the help text
! MAXINI is maximum number of help characters permitted
Implicit None
Save
integer, parameter :: COMCHR = 6, MAXHLP = 75
integer, parameter :: MAXINI = COMCHR*MAXHLP
end module Help_Text_Space
