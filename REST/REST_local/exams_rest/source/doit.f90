subroutine DOIT
! Purpose--to provide support for executing EXAMS'
! commands stored in an external file. The procedure
! -- calls for the file specification information
! -- opens the file if initial testing indicates it's a valid file
! -- if successful, makes appropriate alterations to EXAMS
!    to handle input from the specified file.
! Subroutines required: Get_File_Name
! Revised 26-DEC-85 (LAB)
! Revised 10/26/88 to unify command abort style to "quit"
! File handling moved to subroutine Get_File_Name October 1998
use Implementation_Control
use Input_Output
Implicit None
!integer :: IT
integer :: Blowup ! for iostat problem detections
logical :: Found_It
!integer :: EOF, MINRES(2)=(/1,1/), NORESP(2)=(/4,4/), WHICH
!character(len=1) :: DELIM=' ', RESP(8)=(/'H','E','L','P',  'Q','U','I','T'/)
!integer :: One=1, Two=2, RSPSIZ=8
!logical :: period_found ! to test for presence of "." in file specification

call Get_File_Name ("DO", FILNAM(1), Found_It, "READ")

! Confirm the validity of the file name by opening it
if (.not.Found_It) then
   return
else ! further testing -- the file exists, but is it of the right sort?
   call Assign_LUN (DOLUN)
   open (unit=DOLUN,file=trim(FILNAM(1)),status='OLD',iostat=Blowup,&
      access='SEQUENTIAL',form='FORMATTED',action='READ')
   if (Blowup==0) then
     close (unit=DOLUN,iostat=Blowup)
     call Release_LUN (DOLUN)
     DOFLAG = 1
   else
      write (stderr,fmt='(//A/A)')&
         ' Error opening file '//trim(FILNAM(1)),&
         ' DO command cancelled.'
   end if
end if
end subroutine DOIT
