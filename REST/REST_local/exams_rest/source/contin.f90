subroutine CONTIN(CCODE)
! Purpose: To process EXAMS' CONTINUE command. Condition code
!   (CCODE) of 0 indicates that the run should be continued.
! Revised 25-Dec-1985
! Revised 24-Oct-1988 to include run-time formats for cursor control
! Revised 26-Oct-1988 to unify command abort style to "quit"
! Revised 08-Feb-1999 to use floating point comparisons
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
use Floating_Point_Comparisons
use MultiScan
Implicit None
real :: RESULT
integer :: EOF,ERROR,IMBED,IT,ITEMP,IHELP
integer, intent(out) :: CCODE
integer, parameter :: Zero = 0
character(len=6), dimension(4) :: TUNIT=&
            (/'Hours ','Days  ','Months','Years '/)
character(len=1), dimension(1), parameter :: BLANK=' '
CCODE = 1 ! initialize return code to show error

Operation_mode: select case (MODEG)

case (2) Operation_mode ! Initial value problems
 Get_time: do ! endless loop--break out on user command (or e-o-f)
 if (echo) write (stdout,fmt='(/A,I6,A,/A)',advance='NO')&
   ' Initial time for integration will be ',&
     int(TENDG),' '//trim(TUNIT(TCODEG)),&
   ' Enter ending time of integration, Help, or Quit-> '
 call INREC (EOF,stdin)
 if (EOF==1) return ! allow for end-of-file cancellation
 ! See if HELP or QUIT was requested
 START = IMBED(INPUT,Zero) ! look for next non-blank character
 if (START == -999) cycle Get_time ! all blanks, try again
 call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
      ! look for blank after number
 if (TYPE == 100) then
   write(stderr,fmt='(/A)') ' Unrecognized response; no action taken.'
   return
 endif
 IT = IHELP(IT)
 Parse_it: select case (IT)

  case (0) Parse_it ! Neither Help nor Quit, find the requested time
   STOPIT = 0
   START = 1
   call GETNUM (ERROR,RESULT)

   Numbers: select case (ERROR)
    case (0) Numbers
      if (RESULT .GreaterThan. TENDG) then 
         exit Get_time ! leave loop to set times
      else
         write (stderr,fmt='(/A)')&
            ' Ending time must be greater than initial time.'
         cycle Get_time
      end if
    case (1) Numbers ! blank number field
      cycle Get_time
    case default Numbers ! If error = 2, it's not a number. In any case:
      write(stderr,fmt='(/A)') ' Unrecognized response; no action taken.'
      return
   end select Numbers

  case (1) Parse_it ! User requested help
   write (stderr,fmt='(/A/A)')&
      ' To continue the simulation, you must supply the time',&
      ' at which you next want to see output.'
   cycle Get_time

  case (2) Parse_it
   return ! user asked to Quit

  case default Parse_it ! fail-safe...keep looking for input
   cycle Get_time
 end select Parse_it

 end do Get_time

 TINITG = TENDG ! transfer old ending time to new initial time
 TENDG = dble(RESULT) ! load new ending time
 ! if the ending time is not on a mesh point...
 if (dmod((TENDG-TINITG),CINTG) .GreaterThan. 0.0d+00) then ! fix it
   TENDG = TENDG + CINTG - dmod((TENDG-TINITG),CINTG)
   if (echo) write (stdout,fmt='(/A/A,I6,A)')&
      ' The reporting interval (CINT) extends beyond the ending time.',&
      ' TEND has been extended to ', int(TENDG), ' to give complete results.'
 end if
 CCODE = 0

case (3) Operation_mode ! Seasonal dynamics
 CCODE = 0
 if (NYEARG < 1) NYEARG = 1
 ITEMP = LASTYR+NYEARG
 if (echo) write (stdout,fmt='(A,I6,A)')&
   ' CONTinuing integration through 31 December ',ITEMP,'.'

end select Operation_mode

return
end Subroutine CONTIN
