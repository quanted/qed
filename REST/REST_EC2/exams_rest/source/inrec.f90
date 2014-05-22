subroutine INREC(EOF,INUNIT)
! This routine reads a single record from logical unit "INUNIT". The
! results are transmitted to the calling program by the variable "String".
! End-of-file is indicated by "EOF," which is 0 if no eof encountered, 1
! otherwise. An error in reading the command line is signalled by
! setting "INPERR" to 1.
! Revised May 2, 1988 (LAB)
! Revisions 10/21/88 to convert machine dependencies to run-time solutions
use Implementation_Control, String => INPUT
use Input_Output
Implicit None
integer :: I, INUNIT, ios ! ios captures IOSTAT during read operations
integer, intent (out) :: EOF
INPERR = 0; EOF = 0; ios = 0
if (DOFLAG > 0 .and. INUNIT /= RPTLUN) then ! process command file
   call Assign_LUN (DOLUN)
   open (unit=DOLUN,file=trim(FILNAM(1)),status='OLD',access='SEQUENTIAL',&
      form='FORMATTED', position='REWIND', action='READ')
   do I = 1, DOFLAG
      read (DOLUN,fmt='(A)',iostat=ios) String
      if (ios > 0) then       ! error reading record
         write (stderr, fmt='(A)') ' Error reading command file.'
         INPerr = 1
      elseif (ios < 0) then    ! end of file
         EOF = 1
      end if
      if (ios /= 0) then      ! e-o-f or error; terminate file processing
         DOFLAG = 0                    ! reset DO flag
         close (unit=DOLUN,iostat=ios) ! close file
         call Release_LUN (DOLUN)
         String = ' '                  ! blank out the input line
         return
      endif
   end do         ! the last read is the command to be executed on this call
   call No_tabs   ! convert horizontal tabs to space on command to be executed
   DOFLAG = DOFLAG+1
   close (unit=DOLUN,iostat=ios)
   call Release_LUN (DOLUN)
   if (echo) write (stdout,fmt='(A)') ' EXAMS/DO-> '//trim(String)
else ! process keyboard input, batch input, or report file
   read (INUNIT,fmt='(A)',iostat=ios) String
      if (ios > 0) then                ! error reading record
         INPERR = 1                    ! signal problem and
         return                        ! return to calling procedure
      elseif (ios < 0 ) then           ! end of file or end of record
         String = ' '                  ! blank out the input line
         EOF=1                         ! signal end-of-file
         return                        ! return to calling procedure
      endif
   call No_tabs ! to convert horizontal tabs to space
endif

! When a "do" file was on the command line when Exams started, echo it
! in the log file, unless user has turned the echo off
if (BatchRun .and. echo) write (stdout,fmt='(A)') String

Audit:& ! When auditing, append input text to audit file
   if (AUDFLG == 1 .and. DOFLAG == 0 .and. INUNIT == stdin) then
      call Assign_LUN (AUDLUN)
      open (unit=AUDLUN,file='audout.xms',status='UNknown',&
      access='SEQUENTIAL',form='FORMATTED', position='APPEND')
      write (AUDLUN,fmt='(A)') ' '//trim(String)
      endfile AUDLUN; close (unit=AUDLUN,iostat=ios);call Release_LUN (AUDLUN)
   endif Audit

return

contains

Subroutine No_tabs
integer :: i ! local counter
Kill_tab: do ! Alter all horizontal tabs to blanks
  i = index(string,achar(09))
  if (i==0) exit
  string(i:i) = " "
end do Kill_tab
end Subroutine No_tabs

end subroutine INREC
