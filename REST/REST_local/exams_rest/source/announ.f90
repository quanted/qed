subroutine ANNOUN ()
! Purpose: prints introductory and implementation-specific information
! Subroutines required: none
use Solar_Data ! to set limits on computation of light extinction (02-09-99)
use Implementation_Control
use Initial_Sizes
use Local_Working_Space
Implicit None

! Revision 2002-04-03 to list maintenance date in ISO 8601 format
!   Maintenance date is now carried in a variable to expedite
!   creation of metadata in output files. The date is held in local.f90

write (stdout,fmt='(//10X,A/10X,A)')&      ! initial message
'            Welcome to EXAMS Release '//VERSN,&
'           Exposure Analysis Modeling System'
write (stdout,fmt='(6(/10X,A),//10X,A)')&
'      Technical Contact: Lawrence A. Burns, Ph.D.',&
'          U.S. Environmental Protection Agency',&
'                960 College Station Road',&
'               Athens, GA 30605-2700 USA',&
'         Phone: (706) 355-8119  (Fax) 355-8104',&
'             Email: burns.lawrence@epa.gov',&
'            Latest Maintenance '//Maintenance_Date
write (stdout,fmt='(4(/10X,A))')&
' Type HELP and press the RETURN key for command names,',&
'      HELP USER  for a summary of command functions,',&
'      HELP PAGES for a list of information pages,',&
' or   HELP EXAMS for introductory information.'
write (stdout,fmt='(2(/5X,A)/)')&
' Please stand by while EXAMS checks the computational precision',&
' of this computer and initializes the Activity Data Base.'

! Compute machine-dependent precision for use by integrators
FOURU = 4.0D+00*epsilon(1.0D+00)
! Calculate maximum light extinction
Xtes = abs(log(tiny(1.0E+00)))
return
end subroutine ANNOUN
