subroutine PRTMSG(IS) ! PURPOSE: To process the condition codes from routines
! used to display the current contents of activity databases.
! Subroutines required: None
! Revisions 10/21/88 to convert machine dependencies to run-time solutions
! Revisions April 2002 to support ECHO command and separate errors from info
use Implementation_Control
use Input_Output, only: ECHO
Implicit None
integer, intent (in) :: IS
select case (IS)
case (-3)
   write (stderr,fmt='(/A)')&
      ' COMMON group not found. See the MAINTAINER.'
case (-2)
   write (stderr,fmt='(/A)') ' Option not identified.'
case (-1) ! EOF on line
   if (echo) write (stdout,fmt='(/A)')&
      ' End-of-File encountered. Command terminated.'
case (0) ! success
   if (echo) write (stdout,fmt='(/A)')&
   &' Command processing complete; ready for input.'
case (1)
   write (stderr,fmt='(/A)')&
      ' Error in definition of subscript. Try again.'
case (2)
   write (stderr,fmt='(/A)')&
      ' Insufficient information to decode input.'
case (3)
   write (stderr,fmt='(/A)') ' Subscript out-of-range.'
case (4)
   write (stderr,fmt='(/A)') ' Invalid number of subscripts.'
case (5)
   write (stderr,fmt='(/A)') ' Invalid numeric expression.'
case (6) ! not a valid option
   write (stderr,fmt='(/A)') ' COMMON name specified.'
case (7)
   write (stderr,fmt='(/A)') ' SCALAR followed by a (.'
case (8)
   write (stderr,fmt='(/A)') ' Input not understood (null argument).'
case (9)
   write (stderr,fmt='(/A)') ' "TO" or "=" not specified.'
case (10)
write (stderr,fmt='(/A)')&
   ' Invalid numeric quantity after "TO" or "=" -- please try again.'
end select
return
end Subroutine PRTMSG
