module Model_Parameters
! File MODNAM.F90
! allocates file storage for the names of the EXAMS model parameters
! Altered 09/14/91 to add PRBENG...for PRZM interface processing
! Altered 03/25/99 to add MPG and delete KVOG...MP for isotherm linearity
! Altered April 2001 to add aquatic aerobic and anaerobic metabolism half-life
! Altered April 2002 to add user-selectable maximum event durations and
!     user control of output file selection
! Altered May 2004 to add metabolic study temperatures
Implicit None
Save
integer, parameter :: COMCNT=18, PARCNT=134, LNMODS=714
! LNMODS is the number of characters used by the parameter names
! COMCNT is the number of parameter groups in EXAMS
! PARCNT is the number of named parameters in EXAMS
integer :: COMVAR(COMCNT),MODLEN(PARCNT),MODMIN(PARCNT),NOCOM,NOMOD,&
TCL1(PARCNT),TCL2(PARCNT),TCL3(PARCNT),TD(PARCNT),TS(PARCNT)
character(len=1) :: MODS(LNMODS)
end module Model_Parameters
