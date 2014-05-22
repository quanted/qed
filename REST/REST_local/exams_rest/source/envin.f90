subroutine ENVIN(ECO1,SetCommand)
! This routine acquires the environmental input data from the
!    sequential file "ENCANON" for the Utility program.
! For Exams, Utility processing is bypassed by setting ECO1 to "QQQ" in
!    the calling routine and reading from a user-specified data file.
! Revised 21-DEC-1985 (LAB) to accomodate IBM file structures.
! Revisions 10/21/88: run-time implementation of machine dependencies
! Revisions 12/01/99: permit READ of environments larger than NPX segments
! Revisions April 2001 to support dynamic memory management
use Implementation_Control
use Global_Variables
use Local_Working_Space
Implicit None
! Local variables in this subroutine
integer :: J, NSPEC1, NSPEC2, N, NFIRST, NLAST, WRITER, Eof_check
integer :: IOError, Letter_Case
logical, intent(in) :: SetCommand ! to signal that a SET of KOUNT is underway
character(len=3) :: ECO1, ECO2
logical :: DataBaseBuild ! to signal build of DAF in progress
! ECO1 and ECO2 are 3-letter codes for environment names,
! used to search Utility data files for proper section.
! ENVLUN is logical unit number for reading data files.
! J and N are loop counters.
! NSPEC1 is number of active advective interconnections. It is
! read as the first element in the block of data describing
! advection in the input data file. NSPEC2 is number of active
! dispersive interconnections, read as first element in data
! describing dispersive connections.
! N, NFIRST, and NLAST control the reading of time-variable data.

Purpose: If (ECO1 == 'QQQ') then ! entry from EXAMS interactive interface
   WRITER = stdout
   DataBaseBuild = .false.
Else Purpose ! entry from UTILITY program, so
   DataBaseBuild = .true.
   ! open environmental data file for Utility database generator
   WRITER = printr
   call Assign_LUN (ENVLUN)
   open (unit=ENVLUN,FILE='encanon.dat',status='OLD',position='rewind')
   Eco_find: do       ! find the ecosystem
      read (ENVLUN,fmt='(A3)',iostat=Eof_check) ECO2
      Dead_ball: if (Eof_check == IOeor) then ! Ecosystem not in file
         write (WRITER,fmt='(A/A/A)')&
            ' Data location error--no database found for',&
            ' environment '//ECO1,&
            ' Program execution terminated.'
         IFLAG = 8
         go to 5000
      end if Dead_ball
      if (ECO2 == ECO1) exit ! found ecosystem data, leave the loop
   end do Eco_find
End If Purpose
!****************************************************************************
read (ENVLUN,fmt='(A)') ECONAM ! Read name of ecosystem
! Read environmental data from the file
read (ENVLUN,5020,err=6000,end=6010) KOUNT
if (KOUNT <= 0) then
   write (WRITER,fmt='(/1X,A,I0,A/1X,A)')&
      'Environment is described with "',KOUNT,'" segments.',&
      'Data file not processed.'
   IFLAG = 8
   go to 5000
else if (DataBaseBuild .and. KOUNT>NPX) then
   write (WRITER,fmt='(A,I0,A/A,I0,A)')&
      ' Environment describes ',KOUNT,' segments;',&
      ' no more than ',NPX,' can be used to build the direct access file.'
   IFLAG = 8
   go to 5000
endif

! Allocate storage space for this environment
if (.not.SetCommand) then ! the SET command does its own allocation
   call Allocate_Storage(2,KOUNT,KCHEM)
   ! initialize the environmental data spaces
   call initl(3)
end if
if (DataBaseBuild) then
   backspace ENVLUN
   backspace ENVLUN
else
   rewind ENVLUN
end if
read (ENVLUN,fmt='(A)') ECONAM ! Read name of ecosystem
! Read environmental data from the file
read (ENVLUN,5020,err=6000,end=6010) KOUNT
read (ENVLUN,5040,err=6000,end=6010) (TYPEG(J),J=1,KOUNT)
do J = 1, KOUNT
   IOError = scan (TYPEG(J), Permitted_Compartment_Types)
   if (IOError == 0 .and. .not. SetCommand) then
      write (stderr, fmt='(/A,I4,/A)') ' Error: Compartment number ',J, &
      ' was coded as TYPE "'//TYPEG(J)//'". "READ Environment" cancelled.'
      IFLAG=8
      go to 5000
   end if
   Letter_Case = iachar(TYPEG(J))
   if (Letter_Case > 96 .and. Letter_Case < 123) & ! lower case letter,
      TYPEG(J) = achar (Letter_Case - 32)          ! convert to capital
end do
read (ENVLUN,5010,err=6000,end=6010) LATG,LONGG,ELEVG
read (ENVLUN,5010,err=6000,end=6010) (VOLG(J),J=1,KOUNT)
read (ENVLUN,5010,err=6000,end=6010) (AREAG(J),J=1,KOUNT)
read (ENVLUN,5010,err=6000,end=6010) (DEPTHG(J),J=1,KOUNT)
read (ENVLUN,5010,err=6000,end=6010) (XSAG(J),J=1,KOUNT)
read (ENVLUN,5010,err=6000,end=6010) (LENGG(J),J=1,KOUNT)
read (ENVLUN,5010,err=6000,end=6010) (WIDTHG(J),J=1,KOUNT)
read (ENVLUN,5020,err=6000,end=6010) NSPEC1
if (NSPEC1>size(JFRADG)) then
   write (stderr, fmt='(A/A)')&
   ' The number of advective connections exceeds the available',&
   ' storage capacity of Exams; the environment cannot be read.'
   IFLAG = 8
   go to 5000
end if
read (ENVLUN,5020,err=6000,end=6010) (JFRADG(J),J=1,NSPEC1)
read (ENVLUN,5020,err=6000,end=6010) (ITOADG(J),J=1,NSPEC1)
read (ENVLUN,5010,err=6000,end=6010) (ADVPRG(J),J=1,NSPEC1)
read (ENVLUN,5020,err=6000,end=6010) NSPEC2
if (NSPEC2>size(JTURBG)) then
   write (stderr, fmt='(A/A)')&
   ' The number of dispersive connections exceeds the available',&
   ' storage capacity of Exams; the environment cannot be read.'
   IFLAG = 8
   go to 5000
end if
read (ENVLUN,5020,err=6000,end=6010) (JTURBG(J),J=1,NSPEC2)
read (ENVLUN,5020,err=6000,end=6010) (ITURBG(J),J=1,NSPEC2)
read (ENVLUN,5010,err=6000,end=6010) (XSTURG(J),J=1,NSPEC2)
read (ENVLUN,5010,err=6000,end=6010) (CHARLG(J),J=1,NSPEC2)

! Set up to read required number of blocks of data
NFIRST=1; NLAST=13 ! Modes 1, 2, and 3 read 13 months (12 + mean value)
Months: do N = NFIRST, NLAST
   read (ENVLUN,5010,err=6000,end=6010) (DSPG(J,N),J=1,NSPEC2)
   read (ENVLUN,5010,err=6000,end=6010) (WINDG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (STFLOG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (STSEDG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (NPSFLG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (NPSEDG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (SEEPSG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) RAING(N)
   read (ENVLUN,5010,err=6000,end=6010) CLOUDG(N)
   read (ENVLUN,5010,err=6000,end=6010) OZONEG(N)
   read (ENVLUN,5010,err=6000,end=6010) RHUMG(N)
   read (ENVLUN,5010,err=6000,end=6010) ATURBG(N)

   read (ENVLUN,5040,err=6000,end=6010) AIRTYG(N)
   IOError = scan (AIRTYG(N), Permitted_Air_Mass_Types)
   if (IOError == 0 .and. .not.SetCommand) then
      write (stderr, fmt='(/A,I4,/A)') ' Error: Air Mass Type ',N, &
      ' was coded as "'//AIRTYG(N)//'". "READ Environment" command cancelled.'
      IFLAG=8
      go to 5000
   end if
   Letter_Case = iachar(AIRTYG(N))
   if (Letter_Case > 96 .and. Letter_Case < 123) & ! lower case letter,
      AIRTYG(N) = achar (Letter_Case - 32)          ! convert to capital

   read (ENVLUN,5010,err=6000,end=6010) (DFACG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (EVAPG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (SUSEDG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (BULKDG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (PCTWAG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (FROCG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (CECG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (AECG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (TCELG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (PHG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (POHG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) OXRADG(N)
   read (ENVLUN,5010,err=6000,end=6010) (BACPLG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (BNBACG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (PLMASG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (BNMASG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (KO2G(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (DOCG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (CHLG(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (DISO2G(J,N),J=1,KOUNT)
   read (ENVLUN,5010,err=6000,end=6010) (REDAGG(J,N),J=1,KOUNT)
end do Months

5000 continue
close (unit=ENVLUN,iostat=IOerror)  ! End of environmental data entry
call Release_LUN (ENVLUN)
return

5010  format (8F10.0)
5020  format (16I5)
5040  format (80A1)

6000 write (stderr,fmt='(A)')&
 ' An error occurred while reading the environmental data file.',&
 ' This file must be repaired before the data can be read by Exams.'
IFLAG = 8
go to 5000
6010 write (stderr,fmt='(A)')&
 ' The environmental data file is incomplete.',&
 ' Exams cannot read a partial data file.'
IFLAG=8
go to 5000
end Subroutine ENVIN
