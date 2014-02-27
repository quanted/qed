subroutine SETPSW
! Written 20-MAY-1985 to implement EXAMS UDB passwords.
! Revised 27-DEC-85, 22-APR-87 (LAB)
! Revised 10/20/88 (LAB) run-time formats for implementation-
! dependent cursor control.
! Revised 11/17/88 to accommodate VAX multi-user environment
! Converted to Fortran90 2/20/96, 4/23/96
! N.B. this procedure is INTENTIONALLY unforgiving--any slip results in
! cancellation of the command, so as to impede password cracking
use Implementation_Control
use Input_Output
use Initial_Sizes
use MultiScan
Implicit None
real :: RESULT
integer :: CC, EOF, RWOPT, WHICH
integer :: IMBED,MATCH,IREC,II,NUSED,J
character(len=1), dimension(VARCEC) :: CBUFF(VARCEC)
character(len=1), dimension(1), parameter :: BLANK = ' '
character(len=1), parameter, dimension(23) :: PASOPT = &
   (/'R','E','C','A','L','L',  'S','T','O','R','E',&
     'B','O','T','H',  'H','E','L','P',  'Q','U','I','T'/)
integer, parameter, dimension(5) :: NOPASS=(/6,5,4,4,4/), MINPAS=(/1,1,1,1,1/)
integer, parameter :: Five = 5, LENPAS = 23
! See if there is more information on the input record
START = IMBED(INPUT,STOPIT)
Inquiry: do
   Need_more: if (START == -999) then ! ask for more input
      write (stdout,fmt='(6(/A))',advance='NO')&
         ' Enter the type of password protection desired:',&
         '   Recall -- to prevent unauthorized access to the dataset',&
         '   Store  -- to prevent unauthorized changes or erasure',&
         '   Both   -- to use the same password for both Store and Recall',&
         ' Help     -- for further information',&
         ' Quit     -- cancel command and return to EXAMS prompt-> '
      call INREC (EOF,stdin)
      if (EOF == 1) then
         write (stdout,fmt='(/A)') ' PASSWORD command cancelled.'
         call Kill_Passwords
         return
      endif
      START = IMBED(INPUT,0)
      if (START == -999) cycle Inquiry
   end if Need_more
   ! Locate the next blank in the input stream
   call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
   if (TYPE == 100) STOPIT = Key_Buffer+1  ! no blanks in input
   WHICH = MATCH(Five,LENPAS,NOPASS,PASOPT,MINPAS)
   ! WHICH:  0 = no match, 1 = Read, 2 = Write, 3 = Both, 4 = Help, 5 = Quit.
   Decode_input: select case (WHICH)
   case (0) Decode_input
      write (stdout,fmt='(/A)')&
         ' Response not understood; please try again.'
      INPUT = ' '
      START = -999
      cycle Inquiry
   case (5) Decode_input ! Quit request
      call Kill_passwords
      write (stdout,fmt='(/A)') ' PASSWORD command cancelled.'
      return
   case (4) Decode_input ! Help requested
      write (stdout,fmt='(7(/A))')&
         ' Use the PASSWORD command to restrict access to',&
         ' datasets in any of EXAMS'' four User DataBases.',&
         ' You can prevent unauthorized retrieval of the data (with',&
         ' a Recall password), and/or unauthorized erasure or revision',&
         ' of the dataset (with a Store password). You can use a',&
         ' different character string for each password, or you',&
         ' can set both passwords to the same value with "Both."'
      INPUT = ' '
      START = -999
      cycle Inquiry
   case (1,2,3) Decode_input
      RWOPT = WHICH ! Save WHICH for later
      call DECOD1 (Five,WHICH,CC,RESULT) ! here Five denotes PASSWORD command
      if (CC > 1) then
         call Kill_Passwords
         write (stdout,fmt='(/A)') ' PASSWORD command cancelled.'
         return
      end if
      IREC = int(RESULT)
      call DECOD2 (IREC,CC,WHICH,II,CBUFF)
      if (CC == 3 .or. CC == 2) then
         if (CC == 2) write (stdout,fmt='(A)')&
            ' This dataset is empty...passwords prohibited.'
         call Kill_Passwords
         write (stdout,fmt='(/A)') ' PASSWORD command cancelled.'
         return
      endif
      read (RANUNT,rec=II) CBUFF  ! read passwords
      NUSED = 50    ! Skip over name of entry
      do J = 1, 6   ! Read current passwords for this record
         RPASS(WHICH)(J:J) = CBUFF(NUSED+1)
         WPASS(WHICH)(J:J) = CBUFF(NUSED+2)
         NUSED = NUSED+2
      end do
      if (WPASS(WHICH) == 'GLOBAL') exit Inquiry
      ! Entry is write-protected, solicit password
      write (stdout,fmt='(A/A)',advance='NO')&
         ' This entry is protected from unauthorized changes.',&
         ' Please enter the Store Access Password-> '
      call INREC (EOF,stdin)
      if (EOF == 1) then
         write (stdout,fmt='(/A)') ' PASSWORD command cancelled.'
         call Kill_Passwords
         return
      endif
      START = IMBED(INPUT,0)
      if (START == -999) then   ! all blank input when password requested
         write (stdout,fmt='(/A)') ' PASSWORD command cancelled.'
         call Kill_Passwords
         return
      endif
      if (INPUT(START:START+5) == WPASS(WHICH) &
            .or. INPUT(START:START+5) == SYSPAS) then
         INPUT = ' '
         STOPIT = 0
         exit Inquiry
      else
         write (stdout,fmt='(/A/A)')&
            ' This password does not match the current protection.',&
            ' The PASSWORD command has been cancelled.'
         call Kill_Passwords
         return
      endif
   end select Decode_input
end do Inquiry

! Change the password(s)...the new password may be in the input already
START = IMBED(INPUT,STOPIT)
Need_password: if (START == -999) then
   write (stdout,fmt='(A)',advance='NO')& ! Prompt for new password
      ' Enter new Password (up to six characters)-> '
   ! Load the next six characters into the password
   call INREC (EOF,stdin)
   if (EOF == 1) then
      write (stdout,fmt='(/A)') ' PASSWORD command cancelled.'
      call Kill_Passwords
      return
   endif
   START = IMBED(INPUT,0)
   if (START == -999) then ! blank input...remove password protection
      write (stdout,fmt='(/A)') ' PASSWORD protection removed.'
      START = 1
      INPUT(START:START+5) = 'GLOBAL'
   endif
end if Need_password
if (RWOPT == 1) then
      RPASS(WHICH) = INPUT(START:START+5)
   elseif (RWOPT == 2) then
      WPASS(WHICH) = INPUT(START:START+5)
   elseif (RWOPT == 3) then
      RPASS(WHICH) = INPUT(START:START+5)
      WPASS(WHICH) = INPUT(START:START+5)
   else ! failure in code...report problem
      write (stdout,fmt='(/A)')&
         ' PASSWORD procedure failed. Password protection not installed.'
      INPUT = ' '
      call Kill_Passwords
      return ! bail out here so as not to write back to the UDB record
endif
NUSED = 50
do J = 1, 6                            ! write the new (and any unchanged)
   CBUFF(NUSED+1) = RPASS(WHICH)(J:J)  ! password into the character buffer
   CBUFF(NUSED+2) = WPASS(WHICH)(J:J)
   NUSED = NUSED+2
end do                                 ! and now write the character buffer
write (RANUNT,rec=II) CBUFF    ! back to the database record, and
call Kill_Passwords                    ! reset password fields
return
contains
Subroutine Kill_Passwords
! reset password fields
WPASS = 'GLOBAL'
RPASS = 'GLOBAL'
end Subroutine Kill_Passwords
end subroutine SETPSW
