subroutine READER
! Created 16-MAY-1985 to upload EXAMS ADB sectors from disk files
! Revised 29-MAY-1986 (LAB) -- add call to INITL
! Revised 10/25/1988 (LAB) -- run-time formats for implementation-
! dependent cursor control. Converted to Fortran90 2/20/1996.
! Revised 10/26/1988 to unify command abort style to "quit"
! Revised 09/13/1991 to read PRZM output files
! Revised 10/22/1998 to add LOAD and PRODUCT chemistry files
! Revised 02/29/2000 to read PRZM meteorology file
! Revised 2002-06-11 to use 10 m anemometer height (.dvf standard)
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
use MultiScan
use StationData
Implicit None
integer :: READLUN, WHICH, EOF, IMBED, MATCH
integer, parameter :: RSPSIZ = 57 ! total characters in valid responses
integer, dimension(8), parameter :: NORESP = (/8,11,8,7,4,11,4,4/)
! NORESP holds the full length of the responses to the prompt
integer, dimension(8), parameter :: MNRESP = (/1,1,1,3,3,1,1,1/)
! MNRESP is the minimum allowable length for uniqueness of responses
character(len=1), dimension(RSPSIZ) ::  RESP = (/ &
   'C','H','E','M','I','C','A','L',&
   'E','N','V','I','R','O','N','M','E','N','T',&
   'L','O','A','D','I','N','G','S',&
   'P','R','O','D','U','C','T',  'P','R','Z','M', &
   'M','E','T','E','O','R','O','L','O','G','Y', &
   'H','E','L','P',   'Q','U','I','T'/)

integer :: Err_check
integer, parameter :: Zero=0, Eight=8
logical :: Chemical, Environment, Load, PROduct, PRZM, MetFile
logical :: Problem, File_Exists
! "QQQ" is a dummy identifier to bypass batch file searching
! in ENVIN and CHEMIN
character(len=1), dimension(1), parameter :: BLANK=' '
character(len=3), parameter :: QQQ = 'QQQ'
character(len=3), dimension(NCHEM) :: CHEM1
logical :: test ! [lsr]
CHEM1 = 'QQQ'! Initialize control parameters
Chemical =     .false.
Environment  = .false.
Load =         .false.
PROduct =      .false.
PRZm =         .false.
MetFile =      .false.
! More information in input record? (START = location of next
! non-blank, non-tab character, or -999 if there is none such.)
START = IMBED(INPUT,STOPIT)
Inquiry: do
   Need_input: if (START == -999) then
      write (stdout,fmt='(A)')&
         ' Enter Chemical, Environment, Load, PROduct, PRZM,'
      write (stdout,fmt='(A)',advance='NO')&
         ' Meteorology, Help, or Quit-> '
      call INREC (EOF,stdin)
      if (EOF == 1) then
         write (stderr,fmt='(A)')&
            ' End-of-file marker--READ command cancelled.'
         return
      endif
      START = IMBED(INPUT,Zero)
      if (START == -999) cycle Inquiry
   end if Need_input
   ! Locate the next blank in the input
   call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
   if (TYPE == 100) STOPIT = Key_Buffer+1 ! no blanks; line is all non-blanks
   ! WHICH - 0 = no match
   ! WHICH - 1 = Chemical
   ! WHICH - 2 = Environment
   ! WHICH - 3 = Load
   ! WHICH - 4 = PROduct chemistry
   ! WHICH - 5 = PRZM transfer files
   ! WHICH - 6 = Meteorology site file
   ! WHICH - 7 = Help
   ! WHICH - 8 = Quit
   WHICH = MATCH(Eight,RSPSIZ,NORESP,RESP,MNRESP)
   File_type: select case (WHICH)
   case (0) File_type
      write (stderr,fmt='(/A)')&
         ' Response not recognized, please try again.'
      INPUT = ' '
      START = -999
      cycle Inquiry
   case (1) File_type
      Chemical = .true.; exit Inquiry
   case (2) File_type
      Environment =  .true.; exit Inquiry
   case (3) File_type
      Load = .true.; exit Inquiry
   case (4) File_type
      PROduct = .true.; exit Inquiry
   case (5) File_type
      PRZM = .true.; exit Inquiry
   case (6) File_Type
     MetFile= .true.; exit Inquiry
   case (7) File_type ! Help requested
      write (stdout,fmt='(/,10(A/))')&
!  Text of the Help ----------------------------------------------------------
'  The READ command is used to load the Activity Data Base (ADB,',&
'  or foreground memory) from a specified data file on your disk.',&
'  In response to the prompt, indicate one of the following',&
'    C   to read a  Chemical data (.chm) file,',&
'    E   to read an Environmental data (.env) file,',&
'    L   to read a  chemical Loadings data (.lod) file,',&
'    PRO to read a  chemical transformation PROduct data (.prd) file,',&
'    PRZ to read a  PRZM transfer (.Dnn, nn the year) file,',&
'    M   to read a  Meteorology (.dvf) file,',&
' or Quit to return to the EXAMS prompt.'
!  End of the Help text ------------------------------------------------------
      INPUT = ' '
      START = -999
      cycle Inquiry
   case (8) File_type ! QUIT requested
      write (stderr,fmt='(A)') ' READ cancelled.'
      return
   end select File_type
end do Inquiry

if (Chemical) then
   call Get_File_Name ('READ Chemical', FILNAM(2), File_Exists, 'READ')
         ! Acquire the file name. If the file doesn't exist, bail out.
   if (.not.File_Exists) Return 
   call Assign_LUN (READLUN)
   open (unit=READLUN,status='OLD',access='SEQUENTIAL',action='read',&
   form='FORMATTED',position='rewind',iostat=Err_check,file=trim(FILNAM(2)))
   if (Err_check /= 0) then
      write (stderr,fmt='(/A)')&
         ' Error opening disk file. READ Chemical command cancelled.'
      call Release_LUN (READLUN)
   else
      IRUN = 0 ! prevent "continue" until "run" has been executed
      call INITL (2)
      call CHEMIN(CHEM1,READLUN)
      ! close file and release LUN
      close (unit=READLUN,iostat=Err_check)
      call Release_LUN (READLUN)
      if (IFLAG == 8) then ! return with problem
         call INITL (2) ! to re-zero the dataset
         IFLAG = 0
         write (stderr,fmt='(/A)')&
         ' Chemical data file "'//trim(FILNAM(2))//'" was not processed.'
      else ! Normal termination
         if (echo) write (stdout,fmt='(/A)')&
         ' Chemical data file "'//trim(FILNAM(2))//'" has been READ.'
      end if
   end if

elseif (Environment) then
   call Get_File_Name ('READ Environment', FILNAM(2), File_Exists, 'READ')
         ! Acquire the file name. If the file doesn't exist, bail out.
   if (.not.File_Exists) Return 
   call Assign_LUN (ENVLUN)
   open (unit=ENVLUN,status='OLD',access='SEQUENTIAL',action='read',&
   form='FORMATTED',position='rewind',iostat=Err_check,file=trim(FILNAM(2)))
   if (Err_check /= 0) then
      write (stderr,fmt='(/A)')&
         ' Error opening disk file. READ Environment command cancelled.'
      call Release_LUN (ENVLUN)
   else
      IRUN = 0 ! prevent "continue" until "run" has been executed
      ! ENVIN allocates and initializes dataspace and then reads the file
      call ENVIN (QQQ,.false.)! .false. to signal NOT a SET command sequence
      ! ENVIN closes the file and releases the LUN
      if (IFLAG == 8) then ! return with problem
         call INITL (3) ! to re-zero the dataset
         IFLAG = 0
      else ! normal return
         if (echo) write (stdout,fmt='(/A)')&
         ' Environmental data file "'//trim(FILNAM(2))//'" has been READ.'
      end if
   endif

elseif (Load) then
   call Get_File_Name ('READ Load', FILNAM(2), File_Exists, 'READ')
         ! Acquire the file name. If the file doesn't exist, bail out.
   if (.not.File_Exists) Return 
   call Assign_LUN (READLUN)
   open (unit=READLUN,status='OLD',access='SEQUENTIAL',action='read',&
   form='FORMATTED',position='rewind',iostat=Err_check,file=trim(FILNAM(2)))
   if (Err_check /= 0) then
      write (stderr,fmt='(/A)')&
         ' Error opening disk file. READ Load command cancelled.'
      call Release_LUN (READLUN)
   else
      call INITL (4)
      call Loadin (READLUN,Problem,KOUNT,KCHEM)
      ! Loadin neither closes the file nor releases the LUN
      if (Problem) then ! return with problem
         call INITL (4) ! to re-zero the dataset
         write (stderr,fmt='(/A/A)')&
         ' Input loadings data file "'//trim(FILNAM(2))//'" could not be',&
         ' READ. The data were discarded.'
      else ! no problem
         if(echo) write (stdout,fmt='(/A)')&
         ' Loadings file "'//trim(FILNAM(2))//'" has been READ.'
      end if
      close (Unit=READLUN,iostat=Err_check)
      call Release_LUN (READLUN)
   endif

elseif (PROduct) then
   call Get_File_Name ('READ PROduct', FILNAM(2), File_Exists, 'READ')
         ! Acquire the file name. If the file doesn't exist, bail out.
   if (.not.File_Exists) Return 
   call Assign_LUN (READLUN)
   open (unit=READLUN,status='OLD',access='SEQUENTIAL',action='read',&
   form='FORMATTED',position='rewind',iostat=Err_check,file=trim(FILNAM(2)))
   if (Err_check /= 0) then
      write (stderr,fmt='(/A)')&
         ' Error opening disk file. READ PROduct chemistry command cancelled.'
      call Release_LUN (READLUN)
   else
      call INITL (5)
      call PRODIN (READLUN,Problem)
      ! PRODIN neither closes the file nor releases the LUN
      if (Problem) then  ! return with problem
         call INITL (5) ! to re-zero the dataset
         write (stderr,fmt='(/A/A)')&
         ' Transformation Product file "'//trim(FILNAM(2))//'" could not be',&
         ' READ. The data were discarded.'
      else  ! no problem
         if (echo) write (stdout,fmt='(/A)')&
         ' Transformation Product file "'//trim(FILNAM(2))//'" has been READ.'
         if (KCHEM==1 .and. echo) write (stdout,fmt='(A)')&
         ' These data will not be visible, however, until KCHEM is increased.'
      end if
      close (Unit=READLUN,iostat=Err_check)
      call Release_LUN (READLUN)
   endif

elseif (PRZM) then
   call Get_File_Name ('READ PRZM', FILNAM(2), File_Exists, 'READ')
         ! Acquire the file name. If the file doesn't exist, bail out.
   if (.not.File_Exists) Return 
   call Assign_LUN (PRZLUN)
   open (unit=PRZLUN,status='OLD',access='SEQUENTIAL',action='read',&
   form='FORMATTED',position='rewind',iostat=Err_check,file=trim(FILNAM(2)))
   if (Err_check /= 0) then
      write (stderr,fmt='(/A)')&
         ' Error opening disk file. READ of PRZM transfer file cancelled.'
   elseif (.not. (AREAG(1) .GreaterThan. 0.0)) then
      write (stderr,fmt='(/A/A)')&
         ' The surface area of the aquatic ecosystem is not set.',&
         ' The PRZM transfer file cannot be READ.'
   else
      if (Restart_PRZM) call INITL (4)
      call PRZMIN (FILNAM(2),Problem)
      if (echo .and. .not.Problem) write (stdout,fmt='(A)')&
         ' PRZM transfer file "'//trim(FILNAM(2))//'" has been READ.'
   endif
   ! PRZMIN neither closes the file nor releases the LUN
   close (unit=PRZLUN,iostat=Err_check) ! close the external file
   call Release_LUN (PRZLUN)

elseif (MetFile) then
   call Get_File_Name ('READ Meteorology', FILNAM(2), File_Exists, 'READ')
         ! Acquire the file name. If the file doesn't exist, bail out.
   if (.not.File_Exists) then
      PRZM_Met_File = .false.
      return 
   end if
   call Assign_LUN (READLUN)
   open (unit=READLUN,status='OLD',access='SEQUENTIAL',action='read',&
   form='FORMATTED',position='rewind',iostat=Err_check,file=trim(FILNAM(2)))
   if (Err_check /= 0) then
      write (stderr,fmt='(/A)')&
         ' Error opening disk file. READ Meteorology command cancelled.'
      PRZM_Met_File = .false.
      call Release_LUN (READLUN)
   else
      call WBAN (READLUN,Problem)
      ! WBAN neither closes the file nor releases the LUN
      if (Problem) then  ! return with problem
         write (stderr,fmt='(/A)')&
            ' Error processing meteorology file. READ command cancelled.'
         PRZM_Met_File = .false.
      else  ! no problem
         if (echo) write (stdout,fmt='(/A/)')&
         ' Meteorology file "'//trim(FILNAM(2))//'" has been READ.'
         PRZM_Met_File = .true.
         ! Report station identity from meteorology file database
         if (echo) call WeatherHeader (stdout)
      end if
      close (Unit=READLUN,iostat=Err_check)
      call Release_LUN (READLUN)
   endif

else
   write (stderr,fmt='(A)') ' READ command failed.'
endif
return

contains

Subroutine WBAN (READLUN,Problem) ! Weather Bureau Army/Navy stations
! All NOAA data files (*.dvf) used by PRZM3 have the format:
!
! Field  Columns   Description            Units           Type        Format
! -----  --------  ---------------------- --------------  ---------   ------
!   1        1     blank                  N/A             Character   1x
!   2     02 - 07  Date                   mmddyy          Integer     3i2
!   3     08 - 17  Precipitation          cm/day          Real        f10.2
!   4     18 - 27  Pan Evaporation        cm/day          Real        f10.2
!   5     28 - 37  Temperature (mean)     degrees C       Real        f10.1
!   6     38 - 47  Wind Speed @10 meter   cm/second       Real        f10.1
!   7     48 - 57  Solar Radiation        Langleys/day    Real        f10.1
!   8     58 - 63  FAO Short Grass Eto    mm/day          Real        f6.1
!   9     64 - 73  Daylight Station       kiloPascal      Real        f10.1
!                    Pressure
!  10     74 - 77  Daylight Relative      percent         Integer     i4
!                    Humidity
!  11     78 - 80  Daylight Opaque        tenths of sky   Integer     i3
!                    Sky Cover              covered
!  12     81 - 90  Daylight Temperature   degrees C       Real        f10.1
!  13     91 - 96  Daylight Broadband     optical depth   Real        f6.3
!                    Aerosol
!  14     97 -102  Daylight Prevailing    meter/second    Real        f6.1
!                    Wind Speed @10 meter
!  15    103 -106  Daylight Prevailing    degrees (N=0,   Integer     i4
!                    Wind Direction       E=90, ...)
!
! Daily values file format: 
! (1x,3i2, t8,f10.2, t18,f10.2, t28,f10.1, t38,f10.1,&
!  t48,f10.1, t58,f6.1, t64,f10.1, t74,i4, t78,i3, &
!  t81,f10.1, t91,f6.3, t97,f6.1, t103,i4)
!
!Example lines:
!010161      0.00      0.15      -3.9     632.3     286.8   1.0      78.6  71  0       0.3 0.036   7.4  50
!010261      0.00      0.17      -4.1     475.3     298.1   1.4      78.8  53  0       0.4 0.016   6.2  50
!010361      0.00      0.17      -5.2     576.0     295.2   1.1      79.3  56  0      -1.9 0.028   6.9  50
!010461      0.00      0.16      -5.2     497.7     288.4   1.5      79.1  51  0       0.6 0.019   6.1  50
!234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456
!
! PRZM3 files developed for FOCUS include 29 comment lines beginning with
! a "*" in column 1. These are accomodated her by discarding any line
! that begins with "*" instad of " ".


integer, intent(in)  :: READLUN ! LUN on which the file was opened
logical, intent(out) :: Problem

! local variables
! transient storage for reading a record
real :: R1=0.0,R2=0.0,R3=0.0,R4=0.0,R5=0.0,R6=0.0,R7=0.0
integer :: Days, Span, I, Letter_Case
integer :: Month, Day, Year
logical :: DVF
character (len=1) :: LeadChar
! [lsr] 2013-06-04
! * debugging
    Logical :: isyearleap
    Namelist /xyz/ Year,Month, R1,R2,R3,R4,R5,R6,R7
! convert all lower-case characters in FileName to upper case
do I=1,len_trim(FilNam(2))
   Letter_Case = iachar(FilNam(2)(I:I))
   if (Letter_Case > 96 .and. Letter_Case < 123) &      ! lower case letter,
      FilNam(2)(I:I) = achar (Letter_Case - 32)         ! convert to capital
end do

! Find out if this is a Daily Values File (.dvf)
DVF = (index(FILNAM(2),'.DVF')>0)

! FirstYear and LastYear establish the time span covered by the met file
! (stored in module Local_Working_Space)

do ! skip any leading comment lines until get to first data line
   read (READLUN,fmt='(A1)',advance='NO') LeadChar
   if (LeadChar == '*') then
      read (READLUN,fmt='(t1,A1)', advance='YES') LeadChar
      cycle ! read the next record
   else
!       read (READLUN,fmt='(t6,I2)',err=100) FirstYear   ! 2013-06-04
      read (READLUN,fmt='(t5,I2)',err=100) FirstYear 
!       FirstYear=61 ! [lsr] 2013-06-04, DEBUGGING!!!
      exit
   end if
end do
! find the last year by reading through until data runs out

do
   read (READLUN,fmt='(A1)',advance='NO', end=50) LeadChar
   if (LeadChar=='*') then
      read (READLUN,fmt='(A1)',advance='YES', end=50) LeadChar
      cycle
   else
!       read (READLUN,fmt='(t6,I2)', end=50) LastYear   ! 2013-06-04
      read (READLUN,fmt='(t5,I2)', end=50) LastYear
!       LastYear=90 ! [lsr] 2013-06-04, DEBUGGING!!!
   end if
end do
50 continue

! write(stderr, *) "FirstYear, LastYear == ", FirstYear, LastYear  ! [lsr] 

! Current PRZM3 met files have 2-digit year field.
if (LastYear-FirstYear < 0 ) then; LastYear = LastYear + 2000
else;                              LastYear = Lastyear + 1900; end if
    FirstYear = FirstYear + 1900


deallocate (Precip,PanEvap,AirTemp,WindSpeed,SolarRad)
if (DVF) deallocate (RelHum,OSCover)
Allocate (Precip(FirstYear:LastYear,12),  PanEvap(FirstYear:LastYear,12),&
         AirTemp(FirstYear:LastYear,12),  WindSpeed(FirstYear:LastYear,12),&
         SolarRad(FirstYear:LastYear,12))
if (DVF) Allocate (RelHum(FirstYear:LastYear,12),&
         OSCover(FirstYear:LastYear,12))
Precip=0.0; PanEvap=0.0; AirTemp=0.0; WindSpeed=0.0; SolarRad=0.0
RelHum=0.0; OSCover=0.0
rewind READLUN

Years: do Year = FirstYear,LastYear
   ! Allow for leap years...
   isyearleap=.false.
!    if (mod(Year,4)==0 .and. mod(Year,100)/=0 .or. &
!        mod(Year,400)==0) then
   if (mod(Year,4)==0 .and. mod(Year,100)/=0 ) then
      isyearleap=.True.  !2013-06-04
   Elseif (mod(Year,400)==0) then
      isyearleap=.True.
   endif
   If (isyearleap) then
      Days = 366
      NDAYS(2) = 29
   else
      Days = 365
      NDAYS(2) = 28
   end if
   AllDays: do Day = 1, Days ! process the records for this year
      read (READLUN,fmt='(A1)',advance='NO') LeadChar
      if (LeadChar == '*') then
         read (READLUN,fmt='(t1,A1)',advance='YES') LeadChar
         cycle AllDays ! skip all comment lines
      end if
      if (.not.DVF) then ! older '.met' file
         read (READLUN,fmt=&
            '(t2,i2, t8,f10.2, t18,f10.2, t28,f10.1, t38,f10.1, t48,f10.1)',err=100)&
            Month,R1,R2,R3,R4,R5
      else ! DVF file
         read (READLUN,fmt=&
!             '(t2,i2, t8,f10.2, t18,f10.2, t28,f10.1, t38,f10.1, t48,f10.1, t74,f4.0, t78,f3.0)',err=100)&
!             Month,R1,R2,R3,R4,R5,R6,R7
!         123456789 
!        " 010161      0.00"
            '(i2, t8,f10.2, t18,f10.2, t28,f10.1, t38,f10.1, t48,f10.1, t74,f4.0, t78,f3.0)',err=100)&  !2013-06-04
            Month,R1,R2,R3,R4,R5,R6,R7
!        write(stderr,NML=xyz)


      end if
      ! The file format is 1x, month, day, year (2 digits each ), ...
      ! Extra checks could be imposed by declaring a variable Year2Digit
      !   integer :: Year2Digit
      ! reading the variable and making sure the file is consistent...
      ! and could do days as well...Currently judged to be overkill, however.
      !   read (READLUN,fmt='(1x,i2,2x,i2,5(f10.0))',err=100) &
      !     Month,Year2Digit,R1,R2,R3,R4,R5

      ! Accumulate the data
      Precip(Year,Month)    = Precip(Year,Month)    + R1
      PanEvap(Year,Month)   = PanEvap(Year,Month)   + R2
      AirTemp(Year,Month)   = AirTemp(Year,Month)   + R3
      WindSpeed(Year,Month) = WindSpeed(Year,Month) + R4
      SolarRad(Year,Month)  = SolarRad(Year,Month)  + R5
      if (DVF) RelHum(Year,Month)    = RelHum(Year,Month)  + R6
      if (DVF) OSCover(Year,Month)   = OSCover(Year,Month) + R7
   end do AllDays

   ! Calculate the monthly means where necessary...
   ! Precipitation and evaporation are monthly totals
   do Month=1,12
      AirTemp(Year,Month)   = AirTemp(Year,Month)   / NDAYS(Month)
      WindSpeed(Year,Month) = WindSpeed(Year,Month) / NDAYS(Month)
      SolarRad(Year,Month)  = SolarRad(Year,Month)  / NDAYS(Month)
      if (DVF) RelHum(Year,Month) = RelHum(Year,Month)   / NDAYS(Month)
      if (DVF) OSCover(Year,Month) = OSCover(Year,Month) / NDAYS(Month)
   end do
end do Years

! Convert to Exams' units:
Precip = Precip * 10.0        ! 10 mm/cm
! Convert WindSpeed by height of measuring instrument, and from cm to m.
! /2.0 (for 10 m height to 10 cm)
! (/1.89 for 6m instrument height)
WindSpeed = WindSpeed / 200.0 ! m/s @10 cm height
PanEvap = PanEvap * 10.0      ! 10 mm/cm
! Load the grand means into the current environment, if there is one...
GrandMeans: if (AREAG(1) .GreaterThan. 0.0) then
   Span = LastYear - FirstYear + 1
   Months: Do Month= 1,12
      RAING(Month) =      sum(Precip(:,Month))  / Span
      if (DVF) CLOUDG(Month)= real(sum(OSCover(:,Month)) / Span)
      if (DVF) RHUMG(Month) = real(sum(RelHum(:,Month))  / Span)
      Segments: do I = 1, KOUNT
         TCELG(I,Month) = sum(AirTemp(:,Month)) / Span
!          if (I==1 .or. (TYPEG(I)/='B'.and.TYPEG(I-1)=='B')) then
            ! surface water, load evaporation and wind speed

            test=.False.
            If (I==1) then   !2013
               test=.True.
            elseIf (TYPEG(I)/='B'.and.TYPEG(I-1)=='B') then
                  test=.true.
            end if
            if (test) then



            EVAPG(I,Month) = sum(PanEvap(:,Month)) / Span
            WINDG(I,Month) = sum(WindSpeed(:,Month)) / (Span)
            ! For our purposes, frozen is frozen; ice is ice.
            if (TCELG(I,Month) .LessThan. 0.0) TCELG(I,Month) = 0.0
         else  ! benthic segment or bottom water
            ! Here 4 degrees is the sensible minimum
            if (TCELG(I,Month) .LessThan. 4.0) TCELG(I,Month) = 4.0
            ! Plus a little extra quality control...
            EVAPG(I,Month) = 0.0
            WINDG(I,Month) = 0.0
         end if
      End do Segments
   End do Months
   RAING(13) = sum(RAING(1:12))/12.0
   if (DVF) CLOUDG(13) = sum(CLOUDG(1:12))/12.0
   if (DVF) RHUMG(13) = sum(RHUMG(1:12))/12.0
   SegmentMeans: do I = 1, KOUNT
      EVAPG(I,13) = sum(EVAPG(I,1:12))/12.0
      WINDG(I,13) = sum(WINDG(I,1:12))/12.0
      TCELG(I,13) = sum(TCELG(I,1:12))/12.0
   end do SegmentMeans
end if GrandMeans

! Retrieve the station name and location
call LoadStationData (trim(FilNam(2)))
problem=.false.
return
100 problem=.true.
return
end subroutine WBAN

end subroutine READER
