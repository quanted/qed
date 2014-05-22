subroutine AUDOPT ! purpose: AUDOPT determines the AUDIT option, ON or OFF
! subroutines required: IFIND, INREC
! Revised 23-DEC-1985 (LAB) to accomodate IBM file structures.
! Revised 10/24/88 (LAB) -- run-time formats for implementation-
! dependent cursor control
! Revised 10/26/88 to unify command abort style to "quit"
! Revised 10/15/91 to rename file "audout.xms"
use Implementation_Control
use Input_Output
use Local_Working_Space, only: RunDate
Implicit None
integer :: EOF,IA,IFIND,ioerror
integer, dimension(4) :: DATLEN = (/2,3,4,4/), MINDAT = (/2,2,1,1/)
integer :: LENAM = 13, NDATA = 4
character(len=1), dimension(13) :: DATNAM =&
   (/'O','N', 'O','F','F', 'H','E','L','P', 'Q','U','I','T'/)

Inquiry: do
   IA = IFIND(NDATA,LENAM,DATLEN,DATNAM,MINDAT)+3 ! Get the audit option
   select case (IA)
      case (1, 6) ! Help was selected
         write (stdout,fmt='(/A,/,4(/,8X,A))')&
               ' The following AUDIT options are available',&
               ' ON   -- begins a new Audit File,',&
               ' OFf  -- ends Audit recording of input commands,',&
               ' Help -- this message,',&
               ' Quit -- return to the EXAMS prompt.'
         write (stdout,fmt='(/A)', advance='No') " AUDIT-> "
         call INREC (EOF,stdin)
         if (EOF == 1) then; write (stdout,fmt='(/,A,/)')&
             ' End-of-file encountered.'; exit Inquiry
         end if
         STOPIT = 0; cycle Inquiry
      case (2); write (stdout,fmt='(/,A,/)') ' End-of-file encountered.'
         exit Inquiry
      case (3); write (stdout,fmt='(/,A,/)') ' Option not identified.'
         exit Inquiry
      case (4) ! request to turn audit ON
         if (AUDFLG == 1) then ! Audit is already on
            write (stdout, fmt='(/A/A)') ' Auditing is already in progress;',&
            ' the "AUDIT ON" command has been entered in the audit file.'
         else; AUDFLG = 1 ! Turn on command trace auditing
            write (stdout,fmt='(/,A,/,A,I2,A)')&
             ' All input will now be copied into file"AUDOUT.XMS".'
            call Assign_LUN (AUDLUN)   
            open (unit=AUDLUN,FILE='audout.xms',status='REPLACE',&
               access='SEQUENTIAL',form='FORMATTED',position='REWIND')
            write (AUDLUN,fmt='(A)')& ! First record is identifying marker line
               ' ! Audit trail of input sequence from EXAMS; created '//&
               &RunDate//'.'
            endfile AUDLUN;   close (unit=AUDLUN,iostat=ioerror)
                           call Release_LUN (AUDLUN)
         end if
         exit Inquiry
      case (5) ! request to turn auditing off
         if (AUDFLG == 1) then; write (stdout,fmt='(//A)')&
           ' The AUDIT option has been terminated.'
         else; write (stdout,fmt='(//A)')&
           ' Command sequence auditing is not currently turned on.'
         end if
         AUDFLG = 0; exit Inquiry
      case (7); exit Inquiry ! the QUIT option
   end select
end do Inquiry; return; end subroutine AUDOPT
