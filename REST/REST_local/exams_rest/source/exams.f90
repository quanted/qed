program EXAMS  ! main routine for Exposure Analysis Modeling System (EXAMS)
! local variable identification--
!      Name     Type    Length             Definition
!     ======  =======   ======    ===============================
!     CMD     Integer     01      Index of command to be executed
! revised 27-DEC-1985 (LAB)
! revisions 10/21/1988 to convert machine dependencies to run-time formats
! revised 11/17/1988 to accommodate VAX multi-user environment
! revised 11/18/1988 to load ADB with null values on invocation
! revised 08/27/1990 to accommodate revisions in "read" and "write" commands
! Converted to Fortran90 12-Feb-1996 et seq.
! Revised 04/05/2001 to allow entry of name of batch input file, log file,
!    and error file on command line. This uses a non-Fortran feature of
!    Lahey, but is necessitated by the unreliability of the DOS pipe
! Revised 2002-04-04 to emit time stamp when RUN is started
! Revised 2002-04-17 for user-requested event maxima
! Revised 2002-04-24 to implement the ECHO command
! Revised 2002-07-17 to default Mode to 3
! Revised 2002-07-18 to look for DAFs in .exe directory
! Revised 2004-04-06 to suppress processing of EcoRisk files if no RUN
! Revised 2004-05-17 (LAB) to specify the temperature of biolysis studies
! Revised 2004-06-30 (LAB) to streamline Arrhenius rate computation
! Revised 2005-02-16 (LAB) to correct file names for deletion upon error
! Revised 2005-03-25 (LAB) to reduce linear isotherm violation from fatal error to warning
use Implementation_Control
use Input_Output
use Initial_Sizes
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
use Statistical_Variables
use SetValue
use F2KCLI ! Fortran 2000 features -- interim implementation by Winteracter
Implicit None

real (kind(0D0)), allocatable, dimension(:,:) :: Y
! Y is constituent concentration (mg/L) referred to the
!  AQUEOUS phase of the compartment

integer :: CMD,HOPT,RUNOPT,I,IT,IS,IOerr,KOUNT_Save,KCHEM_Save
integer, parameter:: Number_Zero=0
logical :: Found_It ! for locating exams.daf and ozone.daf
integer :: It_is_OK=0, N_Args=0
! It_is_OK for testing file integrity via 'iostat' and file lengths via 'flen'
! N_Args is the number of arguments on the command line
character (len=Max_File) :: CommandFile=' ', Exe_Name=' '
character (len=Max_File) :: LogFile=' ',ErrorFile=' ', Path = ' ', WarnFile = ' '

call Set_File_Sizes () ! to record file structure
call Detect_File_Codes ! for end-of-file signal
R_Factor = R_Gas/log10(exp(1.0))

! Reserve LUN for Warnings File
call Assign_LUN(WarnLUN)

! Check the program invocation for existence of file specifications:
N_Args = Command_Argument_Count()
call Get_Command_Argument(0,Exe_Name) ! acquire the path\exams.exe string
I = max((Index(Exe_Name, '\', Back = .true.)),&
        (Index(Exe_Name, '/', Back = .true.))) ! in case OS doesn't translate
Path = Exe_Name(1:I)
if (N_Args > 0) then
   BatchRun = .true.
   ! Four files may be present on the command line:
   ! 1. The name of the command file driving the run
   ! 2. The name of the log file for the screen dump
   ! 3. The name of a file to receive fatal error messages
   ! 4. The name of a file to receive non-fatal warning messages
   
   ! First get the name of the command file
   call Get_Command_Argument(1,CommandFile)
   ! then the LogFile
   If (N_args > 1) call Get_Command_Argument(2,Logfile)
   ! then the ErrorFile
   If (N_args > 2) call Get_Command_Argument(3,ErrorFile)
   ! and finally the Warnings File
   If (N_args > 3) call Get_Command_Argument(4,WarnFile)
   ! Default any unspecified files
   if (len_trim(ErrorFile) == 0) ErrorFile = 'Exams.err'
   open(Unit=stderr, File=trim(ErrorFile),    Status='REPLACE')
   if (len_trim(WarnFile) == 0)  WarnFile  = 'Exams.wrn'
   open(Unit=WarnLun, File=trim(WarnFile),    Status='REPLACE')
   ! This next was the first file name listed on the command line.
   ! If the file cannot be found as specified, the batch run must abort.
   open(Unit=stdin,  File=trim(CommandFile),  Status='OLD', iostat=It_is_OK)
      if (It_is_OK /= 0) then
         call Kill_Files ! Delete any existing output files
         ! The stop error message will go to the error file
         stop ' Error: Exams command file not found.'
      end if
   if (len_trim(LogFile) == 0) LogFile = 'Exams.log'
   open(Unit=stdout, File=trim(LogFile),      Status='REPLACE')
else ! stdin, stdout, stderr write to terminal if not in batch mode
   ! in interactive mode, open a warnings file to store warnings written to the terminal
   WarnFile  = 'Exams.wrn'
   open(Unit=WarnLun, File=trim(WarnFile),    Status='REPLACE')
end if

! initial allocation done separately so main allocation routine need not
! check before deallocating variables and reallocating to required sizes
call Allocate_Variables()

! initialize data structures
MCHEMG=1
call initl(2) ! chemistry
call initl(3) ! environment
call initl(4) ! load
call initl(5) ! product chemistry

call ZERO (Y,1,.true.) ! zero all loads
call ANNOUN () ! initial terminal screen as program starts

! load database ... locate primary database direct access file
inquire (file=trim(DAFile_Name),Exist=Found_It)
if (.not.Found_It) then ! file may be in same directory as Exams.exe
   DAFile_Name = trim(Path)//trim(DAFile_Name)
   inquire (file=trim(DAFile_Name),Exist=Found_It) ! try again
end if

! Open main data file
Open_Main_File: do
  if (Found_It) then 
    call Assign_LUN (RANUNT)
!     open (unit=RANUNT, file=trim(DAFile_Name), status='old',&
!         action='readwrite', recl=LENREC, access='direct',&
!         form='UNformatted', blocksize=LENREC, iostat=It_is_OK) !  modified 2013-05-29
    open (unit=RANUNT, file=trim(DAFile_Name), status='old',&
          action='readwrite', recl=LENREC, access='direct',&
          form='UNformatted', iostat=It_is_OK)


    if (It_is_OK == 0) then
      exit Open_Main_File
    else
      Stop " Exams' primary datafile (exams.daf) is invalid -- shutting down."
    end if
  else ! main data file was NOT found
      Stop ' STOP: unable to find main datafile (usually "exams.daf").'
  end if
end do Open_Main_File

! load database ... locate total column ozone database direct access file
! derived from Total Ozone Mapping Spectrometer (TOMS) on Nimbus7 spacecraft
inquire (file=trim(OZFile_Name),Exist=Found_It)
if (.not.Found_It) then ! file may be in same directory as Exams.exe
   OZFile_Name = trim(Path)//trim(OZFile_Name)
   inquire (file=trim(OZFile_Name),Exist=Found_It) ! try again
end if

Zonal_Data = .false. ! assume we will be able to use the TOMS dataset
if (Found_It) then ! the file was located; test its integrity
  call Assign_LUN (Oz_UNT)
  open (unit=Oz_UNT, file=trim(OzFile_Name), status='old',&
        action='read', recl=1152, access='direct',&
        form='unformatted', iostat=It_is_OK)
end if
if (.not.Found_It .or. It_is_OK /=0) then
      Zonal_Data = .true.
      write (WarnLUN,fmt='(A)')&
      ' The TOMS ozone datafile was not found or is damaged. Average zonal',&
      ' data (5 degree latitude zones) will be used instead of the',&
      ' 1 degree latitude by 1.25 degree longitude gridded TOMS dataset.'
end if

KOUNT=1
KCHEM=1
! load ADB with templates from first entries in UDB
call UNPAK (1,1); call UNPENV (1); call UNPLDS (1); call UNPPRO (1)
IRUN = 0
Restart_PRZM = .true. ! set flag for initialized loading from PRZM
PRZM_Met_File = .false. ! set true when a met file is read
! Blank out the name fields
CHEMNA = ' '; ECONAM = ' '; LOADNM = ' '; PRODNM = ' '
! Set the passwords for default global access
WPASS = 'GLOBAL'; RPASS = 'GLOBAL'

read_command_line: do
call WHTCMD (CMD) ! get a command

Commands: select case (CMD)
case default
   ! not a valid command--WHTCMD should catch this
   if (CMD==0 .and. BatchRun) exit read_command_line
      ! batch command file has no exit statement

   ! if the syntax analyzer should return a non-functional index
   write (stderr,fmt='(/A)') ' EXAMS system error. Please try again.'
case (1); call NEWNAM (Number_Zero) ! process the "CHEMICAL" command
case (2); call SHOW (IT,IS) ! process the "SHOW" command
   if (IT == 8) then ! SHOW PLOT requested before run was made--write message
      write (stderr,fmt='(3(/,A),//A//)')&
         ' You cannot SHOW the available PLOTs until you RUN a simulation.',&
         ' If results exist from a previous simulation,',&
         ' they can be accessed by issuing the command',&
         '           SET FIXFIL TO 1'
      cycle read_command_line  ! and go get next command
   end if
   if (IS /= 0) then ! process messages and errors from SHOW et seq.
      call PRTMSG (IS); cycle read_command_line
   end if
   if (IT /= 0) then
      BATCH = 1; 
      call GHOST(Y,IT)
      cycle read_command_line
   endif
case (3); exit read_command_line ! process the "QUIT/EXIT" command
case (4)   ! process the "RUN" command
   call RUNIT() ! check on basic data availability
   if (IRUN/=1 .or. IFLAG==8) then
      write (stderr,fmt='(A)') ' Simulation not executed.'
      call Kill_Files ! Delete any existing output files
      Restart_PRZM = .false.
      cycle read_command_line
   end if
   RUNOPT = 0
   if (echo) write (stdout,fmt='(/A,/A)')&
        ! RunDate and RunTime are set in RUNIT
        ' Simulation beginning on '//RunDate//' at '//RunTime//' for: ',&
        ' Environment: '//trim(ECONAM)
   if (echo) then
      do I = 1, KCHEM
         write (stdout,fmt='(A,I2,A)')' Chemical ',I,': '//trim(CHEMNA(I))
      end do
   end if
   close (unit=RANUNT,iostat=IOerr); call Release_LUN (RANUNT) ! Close UDB
   BATCH = 0
   ! Allocate storage for RUN
   if(allocated(Y)) deallocate (Y)
   allocate (Y(KOUNT,KCHEM))
   Y=0.0D+00
   ! Acquire total column ozone from TOMS dataset
   call Ozone(latg,longg,ozoneg,.false.,stdout,Oz_UNT,Zonal_Data)
   call CONTRL (Y,RUNOPT,Number_Zero)
      if (IFLAG >= 8) then ! Returned with severe problem.
         call Kill_Files   ! Delete any existing output files, protecting
                           ! against faulty analysis (user oversight)
      else
         if (echo) write (stdout,fmt='(/A)') ' RUN command completed.'
         FIXFIL = 1; IRUN = 1
      end if
      call Assign_LUN (RANUNT) ! reload UDB
      open (unit=RANUNT, file=trim(DAFile_Name), status='old',&
            action='readwrite', recl=LENREC, access='direct',&
            form='UNformatted',iostat=It_is_OK)
      if (It_is_OK /= 0) Stop ' Database file damaged -- shutting down.'
      Restart_PRZM = .true. ! next run or continue needs a full PRZM file
case (5); exit read_command_line ! process the "QUIT/EXIT" command
case (6) ! process the "HELP" command
   HOPT = 0; call HELP(HOPT)
case (7) ! process the "PRINT" command
   if (FIXFIL == 0) then ! PRINT requested before RUN--write message
      write (stdout,fmt='(3(/,A),//A//)')&
         ' Results cannot be PRINTed until you have RUN a simulation.',&
         ' If results exist from a previous simulation, these',&
         ' can be accessed by issuing the command',&
         '           SET FIXFIL TO 1'
      cycle read_command_line  ! and go get next command
   endif
   call LIST (printr, .true.)
case (8) ! process the "LIST" command
   if (FIXFIL == 0) then ! LIST requested before RUN--write message
      write (stdout,fmt='(3(/,A),//A//)')&
         ' Results cannot be LISTed until you have RUN a simulation.',&
         ' If results exist from a previous simulation,',&
         ' they can be accessed by issuing the command',&
         '           SET FIXFIL TO 1'
      cycle read_command_line  ! and go get next command
   endif
   call LIST (stdout, .false.)
case (9); KOUNT_Save=KOUNT; KCHEM_Save=KCHEM
   call MODIFY(IT,Y); call PRTMSG(IT) ! process "CHANGE" command
   ! SET/CHANGE may modify KOUNT or KCHEM; if so must reallocate Y
   ! at this point to support the SHOW command.
   if (KOUNT_Save/=KOUNT .or. KCHEM_Save/=KCHEM) then
      if (allocated(Y)) deallocate (Y)
      allocate (Y(KOUNT,KCHEM))
      Y=0.0D+00
   end if
case (10) ! process the "PLOT" command
   if (FIXFIL == 0) then ! PLOT requested before a run was made--write message
      write (stdout,fmt='(3(/,A),//A//)')&
         ' You cannot PLOT until you have RUN a simulation.',&
         ' If results exist from a previous simulation,',&
         ' they can be accessed by issuing the command',&
         '           SET FIXFIL TO 1'
      cycle read_command_line  ! and go get next command
   end if
   call PLOTX (FIXFIL,MCHEMG,KOUNT)
case (11); call NEWNAM(1) ! process the "ENVIRONMENT" command
case (12)   ! process the "DESCRIBE" command
   HOPT = 1; call HELP(HOPT)
case (13) ! process the "STORE" command
   call STORE()
case (14)
   KOUNT_Save = KOUNT
   call RECALL ! process the "RECALL" command
   ! RECALL environment may modify KOUNT, if so must reallocate Y
   ! at this point to support the SHOW command.
   if (KOUNT_Save /= KOUNT) then
      if (allocated(Y)) deallocate (Y)
      allocate (Y(KOUNT,KCHEM))
      Y=0.0D+00
   end if
case (15); call ERASE ! process the "ERASE" command
case (16); call AUDOPT ! process the "AUDIT" command
case (17); call ZERO (Y,Number_Zero,.false.) ! process the "ZERO" command
case (18) ! process the "CONTINUE" command
   if (MODEG==1) then
      write (stderr,fmt='(//A)')&
         ' The CONTINUE command cannot run in Mode 1.'
      Restart_PRZM = .true.
      cycle read_command_line
   end if
   if (IRUN /= 1) then
      write (stderr,fmt='(//A,A)')&
         ' A simulation must be RUN before the',&
         ' CONTINUE command can be issued.'
      Restart_Przm = .false.
      cycle read_command_line
   end if
   call CONTIN (I) ! To establish the ending time for the "continuation"
      if (I == 1) cycle read_command_line ! end time not set
   RUNOPT = 1
   if (echo) then
   write (stdout,fmt='(/A,/A)')&
      ' Simulation continuing for: ',' Environment: '//trim(ECONAM)
   do I = 1, KCHEM
     write (stdout,fmt='(A,I2,A)')' Chemical ',I,': '//trim(CHEMNA(I))
   end do
   end if
   close (unit=RANUNT,iostat=IOerr); call Release_LUN (RANUNT) ! Close UDB
   BATCH = 0
   call CONTRL (Y,RUNOPT,Number_Zero)
      if (IFLAG >= 8) then ! Returned with severe problem.
         call Kill_Files   ! Delete any existing output files
                           ! (protects against faulty anlysis)
      else
         if (echo) write (stdout,fmt='(/A/)') ' CONTINUE command completed.'
         FIXFIL=1; IRUN=1
      end if
   call Assign_LUN (RANUNT) ! reload database
   open (unit=RANUNT, file=trim(DAFile_Name), status='old',&
         action='readwrite', recl=LENREC, access='direct',&
         form='UNformatted', iostat=It_is_OK)
      if (It_is_OK /= 0) Stop ' Database file damaged -- shutting down.'
   Restart_PRZM = .true. ! next run or continue needs a full PRZM file
case (19); KOUNT_Save=KOUNT; KCHEM_Save=KCHEM
           call MODIFY(IT,Y); call PRTMSG (IT) ! same as case (09)...
   ! SET/CHANGE environment may modify KOUNT or KCHEM; if so
   ! must reallocate Y at this point to support the SHOW command.
   if (KOUNT_Save/=KOUNT .or. KCHEM_Save/=KCHEM) then
      if (allocated(Y)) deallocate (Y)
      allocate (Y(KOUNT,KCHEM))
      Y=0.0D+00
   end if
case (20) ! process the "DO" or "@" command
   if (DOFLAG == 0) then
      call DOIT
   else
      write (stderr,fmt='(/A//)')' Nesting of DO files not supported.'
   end if
case (21); call NEWNAM (3) ! process the "PRODUCT"  command
case (22); call NEWNAM (2) ! process the "LOAD"     command
case (23); call CATLG      ! process the "CATALOG"  command
case (24); KOUNT_Save=KOUNT
    call READER     ! process the "READ"     command
    ! READ environment may modify KOUNT, if so must reallocate Y
    ! at this point to support the SHOW command.
    if (KOUNT_Save /= KOUNT) then
       if (allocated(Y)) deallocate (Y)
       allocate (Y(KOUNT,KCHEM))
       Y=0.0D+00
    end if
case (25); call WRITER     ! process the "WRITE"    command
case (26); call SETPSW     ! process the "PASSWORD" command
case (27); call NEWNAM (4) ! process the "NAME"     command
case (28); call EchoSet    ! process the "ECHO"     command
end select Commands
end do read_command_line

! Program is terminating
! Complete EcoRisk files as necessary
if (IRUN .eq. 1) then ! i.e., when data is available from a successful run
   if (RskFilC) then
      call EndRskC
   end if
   if (RskFilR) then
      call EndRskR
   end if
end if

! release allocated storage
call Release_Storage ()
close (RANUNT,iostat=IOerr)
close (Oz_UNT,iostat=IOerr)

if (BatchRun) then
   ! file names were specified and opened at invocation
   ! close out the files (CommandFile,LogFile,ErrorFile)
   close(stdin); close(stdout); close (stderr)
   ! check for zero-length error file and clean up (i.e., remove zero-byte
   ! file clutter)
!   inquire (file=ErrorFile, flen=It_is_OK) ! flen is Lahey Fortran extension modified 2013-05-29
  inquire (file=ErrorFile, size=It_is_OK) ! flen is Lahey Fortran extension modified 2013-05-29
!    inquire (file=ErrorFile) ! flen is Lahey Fortran extension
   if (It_is_OK==0) then ! zero-byte file (i.e., clutter)
      open  (Unit=stderr, File=trim(ErrorFile), Status='OLD')
      close (Unit=stderr, Status='DELETE')
   end if
end if
! Close out warnings file; delete if no warnings were written
close (WarnLUN)
! check for zero-length warnings file and clean up (i.e., remove zero-byte
! file clutter)
! inquire (file=WarnFile, flen=It_is_OK) ! flen is Lahey Fortran extension modified 2013-05-29
inquire (file=WarnFile, size=It_is_OK) ! flen is Lahey Fortran extension modified 2013-05-29
! inquire (file=WarnFile) ! flen is Lahey Fortran extension

if (It_is_OK==0) then ! zero-byte file (i.e., clutter)
   open  (Unit=WarnLun, File=trim(WarnFile), Status='OLD')
   close (Unit=WarnLun, Status='DELETE')
end if
call Release_Lun(WarnLun)
stop

contains

Subroutine Kill_Files
! Procedure to delete results files if errors occur during simulation
implicit none
integer :: Killer_LUN
character(len=12), parameter :: Result_File (14) = (/'report.xms  ',&
'ssout.plt   ','kinout.plt  ','fgetscmd.xms','fgetsexp.xms','bassexp.xms ',&
'HWIRExp.xms ','EcoToxC.xms ','EcoRiskC.xms','CptRisk.xms ','RchRisk.xms ',&
'FullOut.xms ','EcoToxR.xms ','EcoRiskR.xms'/)
logical :: In_use, Found_It
FIXFIL = 0
IFLAG  = 0
IRUN   = 0
do I = 1,14
   Inquire (File = trim(Result_File(I)), exist = Found_It, opened=In_use,&
            number=Killer_LUN) ! If the file is open, the LUN is noted
   if (Found_It) then
      if (.not.In_Use) then ! re-connect the file
         call Assign_LUN (Killer_LUN)
         open (unit=Killer_LUN, file=trim(Result_File(I)), action='read', &
            status='old', iostat=IOerr)
      end if
      ! File is present and connected
      close (Killer_Lun, status = 'DELETE', iostat=IOerr)
      if (IOerr /= 0) write (stderr,fmt='(/A)') &
         ' Error deleting file "'//trim(Result_File(I))//'".'
      call Release_LUN (Killer_LUN)
   end if
end do
write (stderr,fmt='(A)') ' Results files deleted.'
return
end Subroutine Kill_Files

Subroutine Allocate_Variables ()

! Initial (dummy) allocation of data spaces
! This lets other routines deallocate/re-allocate without need to test for
! prior allocation, and protects initial calls to "show" routines
allocate (Y(1,1))       ! chemical state variable matrix
Y=0.0D00
! environmental data
! transport field
   allocate (JFRADG(1), ITOADG(1), JTURBG(1), ITURBG(1))
   allocate (ADVPRG(1), XSTURG(1), CHARLG(1), DSPG(1,MAXDAT))
! sediment descriptors
allocate (SUSEDG(1,MAXDAT),BULKDG(1,MAXDAT),FROCG(1,MAXDAT),&
   CECG(1,MAXDAT),AECG(1,MAXDAT),PCTWAG(1,MAXDAT))
! water quality data
allocate (TCELG(1,MAXDAT),PHG(1,MAXDAT),POHG(1,MAXDAT)&
   &,OXRADG(MAXDAT),REDAGG(1,MAXDAT),BACPLG(1,MAXDAT)&
   &,BNBACG(1,MAXDAT),PLMASG(1,MAXDAT),BNMASG(1,MAXDAT)&
   &,KO2G(1,MAXDAT))
! solar light field
allocate (DOCG(1,MAXDAT),CHLG(1,MAXDAT),DFACG(1,MAXDAT),DISO2G(1,MAXDAT))
! geometry
allocate (VOLG(1),AREAG(1),DEPTHG(1),XSAG(1),LENGG(1),WIDTHG(1))
! climate
allocate (EVAPG(1,MAXDAT),WINDG(1,MAXDAT))
! hydrology
allocate (STFLOG(1,MAXDAT),STSEDG(1,MAXDAT),&
   NPSFLG(1,MAXDAT),NPSEDG(1,MAXDAT),SEEPSG(1,MAXDAT))
! structure
allocate (TYPEG(1))

!loads
allocate (STRLDG(1,1,MAXDAT),NPSLDG(1,1,MAXDAT),&
   PCPLDG(1,1,MAXDAT),DRFLDG(1,1,MAXDAT),SEELDG(1,1,MAXDAT))

allocate (CHEMNA(1))
! physical chemistry
allocate (MWTG(1),SOLG(7,1),MPG(1),ESOLG(7,1),&
   PKG(6,1),EPKG(6,1),SPFLGG(7,1))
! partitioning and sorption
allocate (KOCG(1),KOWG(1),KPBG(7,1),KPDOCG(7,1),KPSG(7,1),KIECG(6,1), Freundlich(1))
! volatilization
allocate (HENRYG(1),EHENG(1),VAPRG(1),EVPRG(1))
! direct photolysis
allocate (QYield(3,7,1),KDPG(7,1),RFLATG(7,1),ABSORG(46,7,1),LAMAXG(7,1))
! hydrolysis
allocate (KAHG(3,7,1),EAHG(3,7,1),&
   KNHG(3,7,1),ENHG(3,7,1),KBHG(3,7,1),EBHG(3,7,1))
! redox chemistry
allocate (KOXG(3,7,1),EOXG(3,7,1),&
   K1O2G(3,7,1),EK1O2G(3,7,1),KREDG(3,7,1),EREDG(3,7,1))
! biolysis
allocate (KBACWG(4,7,1),QTBAWG(4,7,1),KBACSG(4,7,1),QTBASG(4,7,1))
allocate (QTBTSG(4,7,1),QTBTWG(4,7,1))
allocate (AerMet(1),AnaerM(1))

allocate (Reach_ID(1))          ! Reach numbering vector
allocate (Reach_Depth(1))       ! meters
allocate (Limnetic(1))          ! logical tag for compartments
allocate (Benthic(1))           ! logical tag for compartments
allocate (Benthos(1))           ! logical tag for compartments
allocate (Bacterioplankton(1))  ! cfu/ml (colony forming units per milliliter)
allocate (Phytoplankton(1))     ! mgDW/L (milligrams Dry Weight per Liter)
allocate (Zooplankton(1))       ! mgDW/L (milligrams Dry Weight per Liter)
allocate (Plankton_Biomass(1))  ! mgDW/L (milligrams Dry Weight per Liter)
allocate (Benthos_Biomass(1))   ! mgDW/m^2 (mg Dry Weight per square meter)
allocate (Insects(1))           ! mgDW/m^2 (mg Dry Weight per square meter)
allocate (Periphyton(1))        ! mgDW/m^2 (mg Dry Weight per square meter)
allocate (Water_Temperature(1)) ! Celsius
allocate (Limnion_Count(1))     ! Number of Limnetic compartments in reaches
allocate (Benthic_Count(1))     ! Number of Benthic compartments in reaches
allocate (Benthos_Count(1))     ! Number of Benthos compartments in reaches
allocate (Reach_Limnetic_Volume(1))! Water column total volume of each reach
allocate (Reach_Benthic_Volume(1)) ! Total Benthic volume of each reach
allocate (Reach_Benthos_Volume(1)) ! Total Benthos volume of each reach
allocate (Calc_Vector(1,1))     ! working storage for output streams
! HWIR-specific variables
allocate (Reach_TSS(1))         ! Total suspended solids in each reach
allocate (focbenthic(1))        ! Fraction organic carbon of bed sediments
allocate (Reach_cwtot(1,1))     ! mg/L in Limnetic Zone
allocate (Reach_Cwater(1,1))    ! mg/L dissolved in Limnetic Zone
allocate (Reach_Cplankton(1,1)) ! mg/kg FW (Fresh Weight)in Limnetic Zone
allocate (Reach_Cbtot(1,1))     ! mg/kg DW (Dry Weight) in Benthic Zone
allocate (Reach_Cbdiss(1,1))    ! mg/L dissolved in pore water
allocate (Reach_Cbnths(1,1))    ! mg/kg Dry Weight for BASS

Allocate (Mean_Cwater(1), Mean_Cplankton(1), Mean_Cbtot(1), &
          Mean_Cbdiss(1), Mean_Cbnths(1), Mean_Cinsct(1), &
          Mean_Cphytn(1), Mean_Cpplnk(1), Mean_Czplnk(1))
Allocate (CONLDL(1,1), INTINL(1,1,1), TOTKL(1,1), YIELDL(1,1,1), &
          ALPHA(1,1,1), BIOLKL(1,1), BIOTOL(1), EXPOKL(1,1), HYDRKL(1,1), &
          OXIDKL(1,1), PHOTKL(1,1), REDKL(1,1), S1O2KL(1,1), SEDCOL(1), &
          SEDMSL(1), VOLKL(1,1), WATVOL(1), YSATL(1,1,1), TOTLDL(1,1), &
          YSUM(1,1), YBIOS(1), YBIOW(1), YEXPO(1), YGWAT(1), YHYDR(1), &
          YOXID(1), YPHOT(1), YRED(1), YS1O2(1), YSUMS(1,1,1), &
          YTOT(1,1,1), YVOLK(1))
Allocate (YMINLT(1,1), YBARLT(1,1), PEAKLT(1,1),&
          MAXSEG(1,1), MINSEG(1,1))
Allocate (YMINSys(1,1,1),  YBARSys(1,1,1),  PEAKSys(1,1,1),&
          YMINUser(1,1,1), YBARUser(1,1,1), PEAKUser(1,1,1))
Allocate (PeakDetectDate(1,1), UserDetectDate(1,1,1), SysDetectDate(1,1,1))
Allocate (ACCUM2(1,1,1), ACCUM3(1,1), ACCUM4(1,1))
Allocate (KBACWL(1,1,1), KBACSL(1,1,1))
Allocate (KA1L(1,1), KA2L(1,1), KA3L(1,1), KB1L(1,1), KB2L(1,1), &
          KB3L(1,1), KPSL(1,1,1))
Allocate (NPSCOL(1), NPSFL(1),  RAINFL(1), SEDFL(1,1,1), SEDOUL(1), &
          SEEPSL(1), STRMFL(1), STSCOL(1), WATFL(1,1),   WATOUL(1))
Allocate (KDPL(1,1), OXRADL(1), S1O2L(1))
Allocate (KPDOCL(1,1), KOCL(1), KOWL(1), KPBL(1,1))
Allocate (Precip(1,1),PanEvap(1,1),AirTemp(1,1),WindSpeed(1,1),SolarRad(1,1),&
          RelHUm(1,1),OSCover(1,1))
Allocate (QSSAV(1),QTSAV(1),QWSAV(1),SYSLDL(1),BIOPCT(1),CHEMPC(1),&
          EXPPCT(1),TRANLD(1),VOLPCT(1))
Allocate  (Z(6,1),DOMAX(10,1))
end Subroutine Allocate_Variables


Subroutine Release_Storage ()
! Release all allocated storage while closing down Exams
deallocate (Y, Reach_ID, Reach_Depth, Limnetic, Benthic, Benthos, &
Bacterioplankton, Phytoplankton, Zooplankton, Plankton_Biomass, &
Benthos_Biomass, Insects, Periphyton, &
Water_Temperature, Benthic_Count, Limnion_Count, Benthos_Count, &
Reach_Limnetic_Volume, Reach_Benthic_Volume, Reach_Benthos_Volume, &
Calc_Vector,Reach_TSS, focbenthic, Reach_cwtot, &
Reach_Cwater, Reach_Cplankton, Reach_Cbtot, Reach_Cbdiss, Reach_Cbnths, &
Mean_Cwater , Mean_Cplankton, Mean_Cbtot, Mean_Cbdiss, Mean_Cbnths, &
Mean_Cinsct, Mean_Cphytn, Mean_Cpplnk, Mean_Czplnk, CONLDL, INTINL, TOTKL, &
YIELDL, ALPHA, BIOLKL, BIOTOL, EXPOKL, HYDRKL, OXIDKL, PHOTKL, REDKL, &
S1O2KL, SEDCOL, SEDMSL, VOLKL, WATVOL, YSATL, TOTLDL, YSUM, YBIOS, YBIOW, &
YEXPO, YGWAT, YHYDR, YOXID, YPHOT, YRED, YS1O2, YSUMS, YTOT, YVOLK)
Deallocate (MAXSEG, MINSEG, ACCUM2, ACCUM3, YMINLT, YBARLT, PEAKLT, &
YMINUser, YBARUser, PEAKUser, YMINSys, YBArSys, PEAKSys, &
ACCUM4, KA1L, KA2L, KA3L, KB1L, KB2L, KB3L, KPSL, NPSCOL, NPSFL, RAINFL, &
SEDFL, SEDOUL, SEEPSL, STRMFL, STSCOL, WATFL, WATOUL, KDPL, OXRADL, S1O2L, &
KPDOCL, KOCL, KOWL, KPBL, KBACWL, KBACSL)
Deallocate (PeakDetectDate, SysDetectDate, UserDetectDate)
deallocate (Precip,PanEvap,AirTemp,WindSpeed,SolarRad,RelHum,OSCover)
deallocate (QSSAV,QTSAV,QWSAV,SYSLDL,BIOPCT,CHEMPC,EXPPCT,TRANLD,VOLPCT)
deallocate (Z,DOMAX)

deallocate (JFRADG,ITOADG,JTURBG,ITURBG,ADVPRG,XSTURG,CHARLG,DSPG)
deallocate (SUSEDG, BULKDG, FROCG,CECG,AECG,PCTWAG)
deallocate (TCELG,PHG,POHG,OXRADG,REDAGG,BACPLG,BNBACG,PLMASG,BNMASG,KO2G)
deallocate (DOCG,CHLG,DFACG,DISO2G)
deallocate (VOLG,AREAG,DEPTHG,XSAG,LENGG,WIDTHG)
deallocate (EVAPG,WINDG)
deallocate (STFLOG,STSEDG,NPSFLG,NPSEDG,SEEPSG)
deallocate (STRLDG,NPSLDG,PCPLDG,DRFLDG,SEELDG)
deallocate (TYPEG)
deallocate (CHEMNA)
deallocate (MWTG,SOLG,MPG,ESOLG,PKG,EPKG,SPFLGG)  ! physical chemistry
deallocate (KOCG,KOWG,KPBG,KPDOCG,KPSG,KIECG)     ! partitioning and sorption
deallocate (Freundlich)                           ! partitioning and sorption
deallocate (HENRYG,EHENG,VAPRG,EVPRG)             ! volatilization
deallocate (QYield,KDPG,RFLATG,ABSORG,LAMAXG)     ! direct photolysis
deallocate (KAHG,EAHG,KNHG,ENHG,KBHG,EBHG)        ! hydrolysis
deallocate (KOXG,EOXG,K1O2G,EK1O2G,KREDG,EREDG)   ! redox chemistry
deallocate (KBACWG,QTBAWG,KBACSG,QTBASG)          ! biolysis
deallocate (QTBTSG,QTBTWG,AerMet,AnaerM)          ! biolysis
end Subroutine Release_Storage

end program EXAMS
