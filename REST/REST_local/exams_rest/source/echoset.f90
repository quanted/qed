subroutine EchoSet ! purpose: ECHO turns command echoing on and off
! subroutines required: IFIND, INREC
! Created April 2002 to suppress command and informational echo
use Implementation_Control
use Input_Output
Implicit None
integer :: EOF,IA,IFIND,ioerror
integer, dimension(4) :: DATLEN = (/2,3,4,4/), MINDAT = (/2,2,1,1/)
integer :: LENAM = 13, NDATA = 4
character(len=1), dimension(13) :: DATNAM =&
   (/'O','N', 'O','F','F', 'H','E','L','P', 'Q','U','I','T'/)

Inquiry: do
   IA = IFIND(NDATA,LENAM,DATLEN,DATNAM,MINDAT)+3 ! Get the Echo option
   select case (IA)
      case (1, 6) ! Help was selected
         write (stdout,fmt='(/A,/,4(/,8X,A))')&
               ' The following Echo options are available',&
               ' ON   -- begins command echo,',&
               ' OFf  -- turns off echo of input commands,',&
               ' Help -- this message,',&
               ' Quit -- return to the EXAMS prompt.'
         write (stdout,fmt='(/A)', advance='No') " ECHO-> "
         call INREC (EOF,stdin)
         if (EOF == 1) then; write (stdout,fmt='(/,A,/)')&
             ' End-of-file encountered.'; exit Inquiry
         end if
         STOPIT = 0; cycle Inquiry
      case (2); write (stdout,fmt='(/,A,/)') ' End-of-file encountered.'
                 exit Inquiry
      case (3); write (stdout,fmt='(/,A,/)') ' Option not identified.'
                 exit Inquiry
      case (4) ! request to turn echo ON
         if (ECHO) then ! Echo is already on
            write (stdout, fmt='(/A)') ' ECHO ON: Confirmed'
         else; ECHO = .true. ! Turn on command line echo
            write (stdout,fmt='(/A)')&
             ' ECHO is now ON.'
         end if; exit Inquiry
      case (5) ! request to turn echo off
         if (ECHO) then; write (stdout,fmt='(//A)')&
           ' ECHO is now OFF.'
             ECHO = .false.
         else; write (stdout,fmt='(//A)')&
           ' ECHO OFF: Confirmed.' 
         end if; exit Inquiry
      case (7);  exit Inquiry ! the QUIT option
   end select
end do Inquiry; return; end subroutine EchoSet
