subroutine ZONOPT(IZON)
! Purpose: to determine which zone is to be plotted, water or sediments
! Subroutines required: INREC
! Revised 24-DEC-85 (LAB)
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
! dependent cursor control. Converted to Fortran90 3/13/96
use Implementation_Control
use Input_Output
Implicit None
integer :: EOF, IZON, IFIND
integer :: NZONE = 4, LENZON = 21
integer, dimension(4) :: ZONLEN = (/5,8,4,4/), MINZON = (/1,1,1,1/)
character(len=1), dimension(21) :: ZONNAM = (/'W','A','T','E','R',&
   'S','E','D','I','M','E','N','T',  'H','E','L','P',  'Q','U','I','T'/)
Get_option: do
   IZON = IFIND(NZONE,LENZON,ZONLEN,ZONNAM,MINZON)
   select case (IZON)
      case (0)    ! no MATCH on available options
         write (stdout,fmt='(/A/)')&
            ' Option not recognized, please try again.'
      case (-2,3) ! null input, or help was selected
         write (stdout,fmt='(/A,/,/,4(15X,A,/))')&
            ' The following options are available:',&
            ' Water     - Water Column concentrations',&
            ' Sediments - Benthic Sediment concentrations',&
            ' Help      - This message',&
            ' Quit      - Return to the EXAMS prompt'
         write (stdout,fmt='(A)',advance='NO') ' Option-> '
         call INREC (EOF,stdin)
         if (EOF == 1) then
            IZON = -1
            exit Get_option
         else
            STOPIT = 0
         end if
      case (1,2,4)
         exit Get_option
   end select
end do Get_option
end subroutine ZONOPT
