subroutine NEWNAM(IT) ! Purpose of this routine is to get a user defined name.
! It may be on the input record. If not, prompt for it and read records until
! a name is found. IT classifies the request:
! IT   Request
! --   ----------------------
!  0   chemical
!  1   environment
!  2   load
!  3   product chemistry
!  4   entry via NAME command
! Revised 25-DEC-85 (LAB)
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
!    dependent cursor control.
! Revised 10/26/88 to unify command abort style to "quit"
use Implementation_Control
use Input_Output
!use Initial_Sizes
use Global_Variables
Implicit None
integer :: LEN1(3)=(/4,4,4/), LEN2(3)=(/2,4,4/), LEN3(2)=(/4,4/)
integer :: NAMLN1=12, NAMLN2=10, NAMLN3=08
integer :: MINNO1(3)=(/1,1,1/), MINNO2(3)=(/1,1,1/), MINNO3(2)=(/1,1/)
integer :: EOF,WHICH,IFIND,ISAVE,IT,CC
integer :: NUMB1 = 3, NUMB2 = 3, NUMB3 = 2
integer, parameter :: Six = 6
real :: RESULT ! not used here, needed only for DECOD1 call list
character(len=1), parameter, dimension(12) :: NAME1 =&
   (/'N','A','M','E',  'H','E','L','P',  'Q','U','I','T'/)
character(len=1), parameter, dimension(10) :: NAME2 =&
   (/'I','S',  'H','E','L','P',  'Q','U','I','T'/)
character(len=1), parameter, dimension(08) :: NAME3 =&
   (/'H','E','L','P',  'Q','U','I','T'/)
character(len=17), dimension(4) :: Text = (/'chemical         ',&
   'environment      ', 'load scenario    ', 'product chemistry'/)
if (IT == 4) then ! entry via NAME command; see WHICH UDB is desired
  call decod1(Six,WHICH,CC,RESULT)
  select case (CC)
  case (1)           ! all is well, reload IT with UDB requested
    IT = WHICH - 1
  case default       ! CC/=1, so End-of-file, or Quit requested, or error...
     return          ! any of these merit instant bail-out
  end select
end if
ISAVE = STOPIT
! Search for the phrase NAME IS and advance the STOPIT locator
WHICH = IFIND(NUMB1,NAMLN1,LEN1,NAME1,MINNO1)! Search for the phrase NAME IS
if (WHICH == 1) then ! found NAME, check for IS
    ISAVE = STOPIT
    WHICH =  IFIND (NUMB2,NAMLN2,LEN2,NAME2,MINNO2)
    if (WHICH /= 1) STOPIT = ISAVE
else
  STOPIT = ISAVE ! to allow restart of IFIND
end if
Find_name: do
WHICH = IFIND(NUMB3,NAMLN3,LEN3,NAME3,MINNO3)
Analysis: select case (WHICH)
case (-2, 1) Analysis ! null input or HELP requested
write (stdout,fmt='(//A/6(/10X,A))')&
' Options available are ',&
' Help                 - this message.',&
' Quit                 - return to EXAMS command mode.',&
' <carriage return>    = Help',&
' <any other response> - accepted as the new '//trim(text(IT+1))//' name.',&
' For more information, quit to the EXAMS prompt',&
' and then type "HELP NAME".'
write (stdout,fmt='(A)',advance='NO') ' Enter new name-> '
call INREC (EOF,stdin)
if (EOF == 1) then
   write (stdout,fmt='(A)')&
      ' Name of '//trim(text(IT+1))//' dataset not altered'
   return
end if
STOPIT = 0
cycle Find_name
case (2) Analysis ! Quit requested
   write (stdout,fmt='(A)')&
      ' Name of '//trim(text(IT+1))//' dataset not altered'
   exit Find_name
case (0) Analysis ! no match on HELP or QUIT; start of name found
select case (IT)
   case (0); CHEMNA(MCHEMG) = INPUT(start:)
   case (1); ECONAM = INPUT(start:)
   case (2); LOADNM = INPUT(start:)
   case (3); PRODNM = INPUT(start:)
end select
if (len_trim(INPUT)-START > 49) write (stdout,fmt='(A//5X,A)')&
   ' Names cannot exceed 50 characters. The name has been truncated to',&
   ' "'//INPUT(START:START+49)//'"'
exit Find_name
end select Analysis
end do Find_name
end subroutine NEWNAM
