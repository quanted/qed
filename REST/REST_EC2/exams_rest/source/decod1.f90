subroutine DECOD1(OPTION,WHICH,CC,RESULT)
! For Catalog and Name (April 1996), determines WHICH UDB is desired.
! For Erase, Recall, Store, and Password, also determines the UDB
! and the target number in the UDB catalog.
! Subroutines required--GETNUM, IMBED, INREC, MATCH, SKAN
! Subroutines calling DECOD1--CATLG, ERASE, RECALL, SETPSW, STORE, NEWNAM
! Revised 3-Jan-86 (LAB)
! Revised 10/19/88 (LAB) -- run-time formats for implementation-
! dependent cursor control
! Revised 10/27/88 to unify command abort style to "quit"
use Implementation_Control
use Input_Output
use MultiScan
Implicit None
real :: RESULT
integer :: IMBED, MATCH ! functions
integer :: CC,EOF,ERROR,WHICH,IT
integer, intent(in) :: OPTION
integer, parameter :: Zero = 0 
! CC is the condition code reporting on the outcome of the call to DECOD1.
! When CC=1, all is well
!      CC=2, an end-of-file condition arose
!      CC=4, user requested a QUIT from the command
! Input parameter OPTION indicates the command being processed
! -- 1 = Store
! -- 2 = Recall
! -- 3 = Erase
! -- 4 = Catalog
! -- 5 = Password
! -- 6 = Name
! WHICH indicates the UDB target of the command--
! -- 1 = Chemical
! -- 2 = Environment
! -- 3 = Load
! -- 4 = Product
! OPT holds the character data for printing command-dependent help.
character(len=8), dimension(6), parameter :: OPT = (/ 'Store   ','Recall  ',&
    'Erase   ','Catalog ','Password','Name    '/) ! command helps
character(len=20 ), dimension(4), parameter :: UDB_type = &! UDB help text
  (/'chemical            ',  'environment         ',  'allocthonous loading',&
    'product chemistry   '/)
character(len=1), dimension(1), parameter :: BLANK = ' '
! RESP is character data for decoding WHICH UDB, Help, or Quit
character(len=1), dimension(38) :: RESP =(/'C','H','E','M','I','C','A','L',&
'E','N','V','I','R','O','N','M','E','N','T',  'L','O','A','D',&
'P','R','O','D','U','C','T',  'H','E','L','P',  'Q','U','I','T'/)
integer, parameter ,dimension(6) :: NORESP= (/8,11,4,7,4,4/)
integer, parameter ,dimension(6) :: MNRESP=(/1,1,1,1,1,1/)
! HELNAM holds strings for HELP and QUIT
character(len=1), dimension(8) :: HELNAM =(/'H','E','L','P', 'Q','U','I','T'/)
integer, parameter, dimension(2) :: HQUIT=(/4,4/), HELMIN=(/1,1/)
integer, parameter :: SIX=6, TWO=2, RSPSIZ=38, HELSIZ=8
CC = 1 ! presume that all will go well. (CC is reset if problems arise)
! More information in input record? (IMBED locates the next non-blank, non-tab
! character beyond STOPIT in the string INPUT and loads its location in that
! string into START. If only blanks and tabs found, it returns the value -999.
START = IMBED(INPUT,STOPIT)
Prompt_for_UDB: do
if (START==-999) then !If no further input on the line, prompt for it
   write (stdout,fmt='(/A,/A)',advance='no')&
      ' Enter Environment, Chemical, Load, Product,', ' Help, or Quit-> '
   ! Inrec reads a single record from LUN stdin, and loads it into
   ! the string INPUT. If INREC hits an end-of-file, EOF is set to 1
   call INREC (EOF,stdin); if (EOF==1) then
      write (stdout,fmt='(/A)') ' End-of-File encountered on input.'
      CC=2; return; end if
   ! Locate the first non-blank/non-tab character
   START = IMBED(INPUT,Zero) ! and put its location into START
   if (START == -999) cycle Prompt_for_UDB
end if
! With non-blank input in hand, SKAN now searches the string INPUT for the
! next blank beyond the current START point and puts its location in STOPIT.
! If no blanks are found, TYPE is set to 100
call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
if (TYPE == 100) STOPIT = len(input)+1 ! in case the whole input field is used
! MATCH now examines the 6 possible valid responses (including "Help" and
! "Quit") and loads the number corresponding to the character string found on
! INPUT between START and STOPIT. If no match can be made, a value of zero is
! returned.
WHICH = MATCH(SIX,RSPSIZ,NORESP,RESP,MNRESP)
Analysis: select case (WHICH)
case (1:4) Analysis ! User chose chemical, environment, load, or product
   ! For the Catalog and Name commands, processing is complete
   if (OPTION==4 .or. OPTION==6) exit Prompt_for_UDB
   Prompt_for_Catalog_number:do  ! Determine the UDB catalog number for the
                                 ! Store, Recall, Erase, or Password command
      call GETNUM (ERROR,RESULT) ! GETNUM searches INPUT for a number
                                 ! and places it in RESULT--start here because
                                 ! the number may already be in INPUT
      ! For the error returns, ERROR=0 means no error, ERROR=1 means no
      ! characters were on the line (so prompt for it with the loop)
      ! ERROR=2 means the characters could not be converted to a number.
      Test_it: select case (ERROR)
      case (0) Test_it            ! no problem, return the number
         exit Prompt_for_UDB      ! to the calling procedure via RESULT arg
      case (1) Test_it
         write (stdout,fmt='(/A)')& ! Nothing there, prompt for input
            ' Enter '//trim(UDB_type(WHICH))//' UDB catalog number,'
         write (stdout,fmt='(A)',advance='NO') ' Help, or Quit-> '
         call INREC (EOF,stdin)
               if (EOF == 1) then
                  write (stdout,fmt='(/A)')&
                     ' End-of-File encountered on input.'
                  CC=2
                  exit Prompt_for_UDB
               end if
         STOPIT = 0 ! set STOPIT to zero so GETNUM will know where to look
         cycle Prompt_for_Catalog_number ! Reprocess the entry
      case default Test_it ! The entry was not a valid catalog number, but it
                           ! may have been either a request for Help or a Quit.
         ! IT takes on values of 1 for help, 2 for quit, or 0 for neither.
         IT = MATCH(TWO,HELSIZ,HQUIT,HELNAM,HELMIN)
         Check: select case (IT)
         case (1) Check ! request for Help when Exams asked for entry number
            write (stdout,fmt='(/A,A,/A,/A)')&
               ' Enter the User Database Catalog Number',&
               ' of the dataset to be processed.',&
               ' (If you need more information, quit to the EXAMS->',&
               '  prompt and then type "HELP UDB".)'
            cycle Prompt_for_Catalog_number
         case default Check ! IT was not 1, so cancel command--Quit or bad num
            if (IT/=2 ) write (stdout,fmt='(/A)')& ! due to bad number
               ' Entries must be numbers. Command cancelled.'
            CC = 4 ! set condition code for Quit or error abort
            exit Prompt_for_UDB
         end select Check
      end select Test_it
   end do Prompt_for_Catalog_number
case (5) Analysis ! Help requested for specification of UDB target type--
   write (stdout,fmt='(/,A,6(/,10X,A),/)')&
     ' The '//trim(OPT(OPTION))//' command requires that you specify either',&
     ' 1. Environment,',' 2. Chemical,',' 3. Load,',' 4. Product,',&
     ' 5. Help (this option), or',' 6. Quit.'
   START = -999 ! to signal that more input should be requested
   cycle Prompt_for_UDB
case (6) analysis
   CC = 4 ! set condition code for QUIT; cancel command...
   exit Prompt_for_UDB
case default Analysis ! (all other cases, i.e., .not. (0 < WHICH < 7))
   write (stdout,fmt='(A)')&
      ' Response not recognized. Please try again.'
   START = -999 ! to flag that entry should be requested
   cycle Prompt_for_UDB
end select Analysis
end do Prompt_for_UDB
end subroutine DECOD1
