subroutine CONTRL(Y,RUNOPT,IT)
! Developed 7 June 1982 by L.A. Burns
! Revisions 29-Nov-1985 (LAB) to accomodate IBM TSO file structures.
! Revisions 22-Oct-1988--run-time implementation of machine dependencies
! Revisions 30-Oct-1998--Fortran90 conversions; additional file controls
! Revisions April 2002 to support file production options
! Revisions 2004-04-06 to correct conditions for calling m3flux
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
Implicit None
real (kind (0D0)) :: Y(KOUNT,KCHEM)
integer :: File_error
integer, intent (in) :: RUNOPT, IT
integer :: Killer_LUN, IOerr
logical :: In_use, Found_It

! Entry for a "run" or "continue" command
! Open the report file Report.xms and the scratch file.
! RUNOPT is 0 when the "run" command or a batch run invokes the integrators.
! RUNOPT is 1 when entry is via a "continue" command.
! In a "RUN", all reports are replaced.
! For a CONTINUE, reported data are appended to the files.

Reporting: if (RPTFIL) then
   Run_Type: select case (RUNOPT)
   case (0) Run_Type ! Enter for "run" so replace existing files
     call Assign_LUN (RPTLUN)
     open (unit=RPTLUN,status='REPLACE',access='SEQUENTIAL',&
     form='FORMATTED',file='report.xms',iostat=File_error,position='REWIND')
     if (File_error /= 0) then
         write (stdout,fmt='(A)')&
            ' Error opening report file; command cancelled.'
         IFLAG = 8
         return
     end if
   case (1) Run_Type ! Set file for append mode when entering via continue
     call Assign_LUN (RPTLUN)
     open (unit=RPTLUN,status='OLD',access='SEQUENTIAL',&
     position='APPEND',form='FORMATTED',file='report.xms',iostat=File_error)
     if (File_error /= 0) then
         write (stdout,fmt='(A)')&
            ' Error opening report file; command cancelled.'
         IFLAG = 8
         call Release_LUN (RPTLUN)
         return
     end if
   case default Run_Type ! just in case...
     ! RUNOPT has a value of neither 0 nor 1...abort command and
     write (stdout,fmt='(/,A,I2,A/A)')&! report problem for analysis...
     ' System processing error in Subprogram "CONTRL"--"RUNOPT" =',&
     RUNOPT,'!',' Command cancelled; please report the problem to the author.'
     IFLAG = 8
     return
   end select Run_Type
else
   ! Delete old versions of the report file
   Inquire (File = 'report.xms', exist = Found_It, opened=In_use,&
            number=Killer_LUN) ! If the file is open, the LUN is noted
   if (Found_It) then
      if (.not.In_Use) then
         call Assign_LUN (Killer_LUN)
         open (unit=Killer_LUN, file='report.xms', action='read', &
            status='old', iostat=IOerr)
      end if
      ! In either case, now close and delete the file
      close (Killer_Lun, status = 'DELETE', iostat=IOerr)
      call Release_LUN (Killer_LUN)
   end if
end if Reporting

call Assign_LUN (WRKLUN)
open (WRKLUN,access='direct',form='unformatted',& ! Open scratch file
      status='scratch',recl=LENREC,iostat=File_error)
if (File_error /= 0) then
   write (stdout,fmt='(A)')&
      ' Error opening working files; command cancelled.'
   close (unit=RPTLUN,iostat=File_error); call Release_LUN (RPTLUN)
   call Release_LUN (WRKLUN)
   IFLAG = 8
   return
end if

call GHOST (Y,IT)
if (IFLAG >= 8) then ! Bail out: close files and return
   call Close_Files
   return
end if
! Calculate ecological parameter summary for mode 1 and 2 --
! at this stage these variables have been fixed for the duration
! of the simulation.
if (MODEG==1 .or. MODEG==2) then
   call Parameter_Summary (MONTHG)
   if (IFLAG == 8) then
      call Close_Files
      return ! run cannot be executed
   end if
end if

call DRIVER (Y,RUNOPT) ! Call integrator
! If error in integration is indicated, do not attempt analysis
! of time series (SUMUP does flux estimates and skips time series)
if (IFLAG > 2 .and. MODEG /= 1) then
  write (stderr,fmt='(A,I2)')&
      " Results cannot be analyzed; IFLAG = ", IFLAG
  ! close files and return
  call Close_Files; return
endif

select case (MODEG)       ! Call routines to analyze kinetics
  case (1)                !    and summarize results
      ! In mode 1, if integrator failed, the steady-state values
      ! can still be reported
      if (RPTFIL) call SUMUP
  case (2)
      if (RPTFIL .or. PLTFIL) call M2AVE (Y)
      if (IFLAG == 8) return
      if (RPTFIL) call M2FLUX (Y)
  case (3)
      if (RPTFIL .or. PLTFIL) call M3AVE
      if (IFLAG == 8) return
      if (RPTFIL .or. RskFilC .or. RskFilR) call M3FLUX
  case default
     write (stdout,fmt='(A,I2)')& ! MODEG corrupted
       ' Results cannot be analyzed: MODE = ', MODEG
  IFLAG = 8
end select

Call Close_Files

return

contains

Subroutine Close_Files
!  iostat is captured to prevent problems that arose
!  under NT with closing a file that wasn't actually created
   close (unit=WRKLUN,iostat=File_error)
   call Release_LUN (WRKLUN)
   if (RPTFIL) then
      endfile RPTLUN
      close (unit=RPTLUN,iostat=File_error)
      call Release_LUN (RPTLUN)
   end if
return
end Subroutine Close_Files


end subroutine CONTRL
