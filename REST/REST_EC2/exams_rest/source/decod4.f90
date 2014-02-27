subroutine DECOD4(OPTION,IREC,KT,KCHEM,CC)
! OPTION - 1: STORE
!        - 2: RECALL
! CC     - 1: OK
!        - 2: EOF
!        - 3: QUIT
! Subroutines required: GETNUM, IMBED, INREC, SKAN
! Revised 25-DEC-85 (LAB)
! Revised 10/19/88 (LAB) -- run-time formats for implementation-
! dependent cursor control
use Implementation_Control
use Input_Output
use MultiScan
Implicit None
real :: RESULT
integer :: IMBED,MATCH,IHELP
integer, intent (inout) :: KT, IREC
integer, intent (in) :: OPTION, KCHEM
integer :: WHICH, IT, ERROR, CC, EOF
integer, parameter :: Three = 3, NUMAS = 10, NUMIN = 10
integer, parameter, dimension(3) :: ASLEN = (/2,4,4/), MINAS = (/1,1,1/),&
   INLEN = (/2,4,4/), MININ = (/1,1,1/)
character(len=1), dimension(1), parameter :: BLANK = ' '
character(len=1), parameter, dimension(10) ::  AS = &
      (/'A','S',   'H','E','L','P',   'Q','U','I','T'/)
character(len=1), parameter, dimension(10) ::  IN = &
      (/'I','N',   'H','E','L','P',   'Q','U','I','T'/)
character(len=10), parameter, dimension(2) ::  TEXT1= &
      (/'stored.   ','retrieved.'/)
character(len=23), parameter, dimension(2) :: HelpText = &
      (/'chemical catalog (UDB) ','activity database (ADB)'/)
CC = 1
START = IMBED(INPUT,STOPIT) ! look for additional specifications on line

More_input: if (START /= -999) then

call SKAN (INPUT,START,STOPIT,TYPE,BLANK)! if no blank, the line may
if (TYPE == 100) STOPIT = len(input) + 1         ! be chock full of entry data
if (OPTION == 1) WHICH = MATCH(Three,NUMIN,INLEN,IN,MININ)
if (OPTION == 2) WHICH = MATCH(Three,NUMAS,ASLEN,AS,MINAS)

Analysis: select case (WHICH)
case (0) Analysis
   write (stdout,fmt='(A)') ' Command not understood.'
   CC = 3
case (3) Analysis ! Quit requested
   CC=3
case (1,2) Analysis ! as/in or help entered
if (WHICH==2) then ! help requested...
   call Print_Help ! give help and then request a number
   call INREC (EOF,stdin); if(EOF==1)then;CC=2;return;endif
   STOPIT = 0
end if
Prompt_for_target_number: do
call GETNUM (ERROR,RESULT) ! Get target chemical number
Test_it: select case (ERROR)
case (0) Test_it ! select outcome based on the command OPTION
   if (OPTION == 2) then ! recall command
      KT = RESULT
   else                  ! store command
      KT = IREC
      IREC = RESULT
   endif
   exit Prompt_for_target_number
case (1) Test_it                  ! need more data...response was blank
   call Print_help                ! give some help
   call INREC (EOF,stdin); if(EOF==1)then;CC=2;return;endif
   STOPIT = 0
   cycle Prompt_for_target_number ! and try again for number
case default Test_it ! Not a number, see if help or quit was specified
   IT = IHELP(IT)
   more_test: select case (IT)
   case (1) more_test ! Help requested
      call Print_help
      call INREC (EOF,stdin); if(EOF==1)then;CC=2;return;endif
      STOPIT = 0
      cycle Prompt_for_target_number
   case (2) more_test ! Quit requested
      CC=3
      return
   case default more_test                ! not a number nor quit nor help...
      write (stdout,fmt='(2(/A))')& ! write message and treat as quit
         ' Chemical ADB and UDB accessions must be numbers.',&
         ' Nothing '//trim(TEXT1(OPTION))
      CC=3
      return
   end select more_test
end select Test_it
end do Prompt_for_target_number
end select Analysis
end if More_input

! If problem with request, notify user and set error flag to "Quit" setting.
! KT should never be greater than KCHEM; this is a fail-safe check
! should the SET command checks be by-passed.
if (KT > KCHEM) then
   write (stdout,fmt='(/A,I4,A/A,I4,A/A)')&
 ' You cannot currently put data into an ADB entry beyond number',KCHEM,'.',&
 ' Before re-issuing this command, you may wish to "Set KCHEM =',KT,'."',&
      ' Nothing '//trim(TEXT1(OPTION))
   CC = 3 !  Set error flag to "Quit" setting
end if
return
contains
Subroutine Print_Help
if (OPTION == 1) write (stdout,fmt='(/A)')&
   ' Enter the UDB chemical entry number where you wish to store the data.'
if (OPTION == 2) write (stdout,fmt='(/A,I3,A,3(/A))')&
   ' Enter a number between 1 and ',KCHEM,'.',&
   ' The database from the chemical UDB will be transferred to',&
   ' that sector of active chemical memory (i.e., the ADB),',&
   ' and will then be available for simulation.'
   write (stdout,fmt='(/A)',Advance='NO')&
      ' Enter '//trim(HelpText(OPTION))//' number, Help, or Quit-> '
end Subroutine Print_Help
end subroutine DECOD4
