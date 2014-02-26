subroutine WHTCMD(CMD)
! This routine prompts for a primary Exams command, loads and decodes the user
! entry string, and returns the index number of the command to be executed
! to the calling program in the "CMD" argument.
! Revised 10/19/88 (LAB) -- run-time formats for implementation-
! dependent cursor control.
! Debug change 11/22/88, maintenance 09/06/89.
! Addition of ECHO command April 2002
use Implementation_Control
use Input_Output
use MultiScan
! Subroutines required--IMBED, INREC, MATCH, SKAN
Implicit None
! Variable definition section
! Name    Type      Dimension         Description
! ======  ========  =========   ===============================
! CMD     Integer      01       index of command to be executed
! EOF     Integer      01       End-of-file signal from INREC
! DELIM   Character    06       string delimiters
! Variable storage
integer :: CMD,EOF,IMBED,MATCH
integer, parameter :: NCMDS=28  ! number of commands
integer, parameter :: NPRIC=146 ! number of chatracters in command names
integer, parameter, dimension(28) :: CMDLEN =&
   (/8,4,4,3,4,4,5,4,6,4,11,8,5,6,5,5,4,8,3,2,7,4,7,4,5,8,4,4/)
integer, parameter, dimension(28) :: MINCMD=&
   (/3,2,1,2,2,1,3,2,3,2,02,2,2,3,2,1,1,2,2,2,3,2,2,3,1,2,1,2/)
character(len=1), parameter, dimension(146) :: PRICMD=&
(/'C','H','E','M','I','C','A','L',   'S','H','O','W',&
'Q','U','I','T',   'R','U','N',   'E','X','I','T',   'H','E','L','P',&
'P','R','I','N','T',   'L','I','S','T',   'C','H','A','N','G','E',&
'P','L','O','T',   'E','N','V','I','R','O','N','M','E','N','T',&
'D','E','S','C','R','I','B','E',   'S','T','O','R','E',&
'R','E','C','A','L','L',   'E','R','A','S','E',   'A','U','D','I','T',&
'Z','E','R','O',   'C','O','N','T','I','N','U','E',   'S','E','T',&
'D','O',   'P','R','O','D','U','C','T',   'L','O','A','D',&
'C','A','T','A','L','O','G',   'R','E','A','D',   'W','R','I','T','E',&
'P','A','S','S','W','O','R','D',   'N','A','M','E',  'E','C','H','O'/)
character(len=1), parameter, dimension(6) :: DELIM=(/' ','=','@','?','*','!'/)

Get_command: do ! Main routine loop
! Prompt for input. If a command file is being processed
!    don't print the "EXAMS->" prompt.
if (DOFLAG==0 .and. .not.BatchRun)&
   write (stdout,fmt='(/A)', Advance='NO') " EXAMS-> "
call INREC (EOF,stdin) ! get the user input
if (EOF == 1) then ! End of file in command string or end of DO file
   if (ECHO) write (stdout,fmt='(/A/)')&
      ' End-of-file mark; ready for command now.'
   INPUT = ' '
   if (BatchRun) then ! processing an externally supplied list of commands
                      ! so an end-of-file indicates that the 'do' file
                      ! does not have an 'exit' or 'quit' as its terminus
                      ! and thus needs special action
      CMD=0
      exit Get_command
   end if
   cycle Get_command
elseif (INPERR == 1) then ! error in reading command string
   write (stderr,fmt='(/A/)')&
      ' Error reading command; no action taken.'
   INPUT = ' '
   cycle Get_command
endif
! What has the user specified?

! Find the first command character after any leading blanks or horizontal tabs
START = IMBED(INPUT,0)
if (START == -999) cycle Get_command ! If null input, ignore it

call SKAN (INPUT,START,STOPIT,TYPE,DELIM) ! Search for a delimiter
Delimiter: select case (TYPE)
case (100) Delimiter ! fail-safe provision to protect against clever user
   write (stdout,fmt='(/A,/A)')&
      ' Command not recognized. Type "HELP" for general information,',&
      ' or "HELP USE" for a table of available commands.'
   cycle Get_command
case (3)   Delimiter   ! "@" Encountered, treat it like "DO"
   CMD = 20
   exit Get_command
case (4) Delimiter     ! "?" Encountered, treat it like "SHOW"
   CMD = 2
   exit Get_command
case (5, 6) Delimiter  ! Skip comment lines (! or *); return for more input
   cycle Get_command
case default Delimiter ! try for a match on a primary Exams command
   CMD = MATCH(NCMDS,NPRIC,CMDLEN,PRICMD,MINCMD)
   if (CMD /= 0) then
      exit Get_command
   else
      write (stderr,fmt='(/A,/A)')& ! no match on primary commands
         ' Command not recognized. Type "HELP" for general information,',&
         ' or "HELP USE" for a table of available commands.'
      cycle Get_command
   end if
end select Delimiter
end do Get_command
return
end subroutine WHTCMD
