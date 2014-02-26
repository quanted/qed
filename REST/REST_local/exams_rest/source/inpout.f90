module Input_Output ! connections and controls for files and commands
! file inpout.f90
Implicit None
public
save
integer :: START, STOPIT, TYPE, IRUN, INPERR
! IRUN signals that RUN command can be executed.
!    IRUN=0 means not ready to run; IRUN=1 means ready to run.
! INPERR is a flag to signal errors when INREC is executing a Read statement.
!    INPERR=0 signals no error, INPERR is set to 1 when an error occurs.

character(len=6), dimension(4) :: RPASS = 'GLOBAL'
character(len=6), dimension(4) :: WPASS = 'GLOBAL'
!  Passwords for UDBs
!          1: Chemical             RPASS: Read privilege
!          2: Environments         WPASS: Write privelege
!          3: Loads                The "GLOBAL" setting gives RW access
!          4: Products             without password checking by EXAMS.

character(len=6) :: SYSPAS = 'SeSaMe'
! SYSPAS is system manager "trap door" password.
! Revision for Exams3: if you know it, you can reset it...
! If security is an issue you should do this, but DON'T FERGIT IT!!

! AUDFLG signals auditing file to be written (if >0, i.e., 0 = no audit)
! If AUDFLG is set = 1 by default, Exams opens the audit file during
! startup. This file is then appended to during each session.
! (See treatment in INREC: this behavior is necessitated by the continual
! getLUN/openFile/write/closeFile/releaseLUN behavior of the Audit process.)
! DOFLAG signals command file processing is underway (if >0, i.e., 0 = no DO)
! and tracks the processing of the file line-by-line
! ECHO turns command line and command file echoing on and off
integer :: AUDFLG = 0, DOFLAG = 0
logical :: ECHO = .true.
! Append_Lines signals the Print command to continue to add data to the
! output file
logical :: Append_Lines

logical :: BatchRun = .false.
! BatchRun is logical for detecting invocation with command file specified

end module Input_Output
