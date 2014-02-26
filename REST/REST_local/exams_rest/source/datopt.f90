subroutine DATOPT(IDAT)
! Purpose: to determine the type of data concentrations to be plotted
! Subroutines required: INREC
! Revised 24-DEC-85 (LAB)
! Revised 10/19/88 (LAB) -- run-time formats for implementation-
! dependent cursor control
! Revised 10/26/88 to unify command abort style to "quit"
! Converted to Fortran90 2/20/96, 6/14/96
use Implementation_Control
use Input_Output
Implicit None
integer :: EOF, IDAT, IFIND
integer, parameter :: NDATA = 7, LENDAT = 43
integer, dimension(7) :: DATLEN = (/5,9,12,5,4,4,4/), &
                         MINDAT = (/1,1,1,1,1,1,1/)
character(len=1), dimension(43) :: DATNAM = &
(/'T','O','T','A','L',  'D','I','S','S','O','L','V','E','D', &
  'P','A','R','T','I','C','U','L','A','T','E','S',&
  'B','I','O','T','A',  'M','A','S','S',  'H','E','L','P',  'Q','U','I','T'/)
do ! Get the data option
   IDAT = IFIND(NDATA,LENDAT,DATLEN,DATNAM,MINDAT)
   select case (IDAT)
      case (0)
      write (stdout,fmt='(/A//A)',advance='NO')&
         ' Option not recognized; please try again.',&
         ' Option-> '
      case (7) ! QUIT requested, user confirmation written in PLOTX
         return
      case (-2,6) ! null input or Help was selected
         write (stdout,fmt='(/A//8(A/)/A)',advance='NO')&
           ' The following concentration options are available:',&
           '        Total       -  mg/L in Water Column',&
           '                    -  mg/kg in Benthic Sediments',&
           '        Dissolved   -  Dissolved (mg/L)',&
           '        Particulate -  Sediment-sorbed (mg/kg dry weight)',&
           '        Biota       -  Biosorbed (ug/g dry weight)',&
           '        Mass        -  Chemical mass as grams/square meter AREA',&
           '        Help        -  This message',&
           '        Quit        -  Return to the EXAMS prompt',&
           ' Option-> '
      case default
         return
   end select
   call INREC (EOF,stdin)
   IDAT = -1
   STOPIT = 0
   if (EOF == 1) return
end do
return
end subroutine DATOPT
