module Local_Working_Space ! File Local.f90
! Parameters needed by the command processor and the
! simulation, but not available for user modification.
! Local_Working_Space communicates between the batch DISPATcher,
! the routines that access the input data, and the simulation code.
! Modified 2002-06-05 to add meteorological station data
! Revised 2005-02-17 (LAB) to default the production of report.xms

use Initial_Sizes
Implicit None
Save

integer :: StartYear = 0, EndYear = 0 ! for meteorological data
character (len=64) :: Station = 'Unknown'! for meteorological station name
character (len=10) :: State = '--',LRR='-'
character (len=64) :: MLRA='--'
character (len=5)  :: WBANumber = ' ' ! Weather Bureau Army Navy Station Num.
character (len=5)  :: WMOnumber = ' ' ! World Meterological Org Station Num.
character (len=70) :: Note            ! for any special met file notes

real (kind (0D0))  :: T, TENDL, TINCRL, TPRINT, FOURU, TINITL=0.0D+00, TFACTR
real (kind (0E0))  :: KOUNTS, KOUNTW

! version number for output files
character (len=7), parameter :: VERSN = '2.98.04'

character (len=10), parameter :: Maintenance_Date = '2005-04-05'

! QSSAV et al. will be allocated to size (KCHEM)
real (kind (0E0)), allocatable, dimension(:) :: QSSAV, QTSAV, QWSAV, SYSLDL, &
      BIOPCT, CHEMPC, EXPPCT, TRANLD, VOLPCT

! Z will be allocated (6,KCHEM). DOMAX will be allocated (10,KCHEM)
real (kind (0E0)), allocatable :: Z(:,:), DOMAX(:,:)
real (kind (0E0)) :: Z2(12) ! for temporary miscellaneous computations

! storage for meteorological data from .met, .dvf, and .hvf files
! Precip is Precipitation (cm)
! PanEvap is Pan Evaporation (cm)
! AirTemp is air temperature (degrees Celsius)
! WindSpeed is Wind Speed (cm/s)
! SolarRad is Solar Radiation (Langleys)
real (Kind (0E0)), Allocatable :: &
      Precip(:,:), PanEvap(:,:), AirTemp(:,:), WindSpeed(:,:), SolarRad(:,:)
! RelHum is Relative Humidity; OSCover is Opaque Sky Cover
real (Kind (0E0)), allocatable :: RelHum(:,:), OSCover(:,:)
integer :: FirstYear, LastYear
! FirstYear and LastYear establish the time span covered by the met file
logical :: PRZM_Met_File
! PRZM_Met_File is set .true. when a met file has been successfully processed
logical :: PRZM_Transfer_File
! PRZM_Transfer_File is set .true. when a PRZM data transfer files
!    has been successfully processed
real (Kind (0E0)) :: STFLOG_saved(1,13),STSEDG_saved(1,13)
! In modes 1-3, base flow into segment 1 may be augmented to preserve
! the hydrologic balance. The original value is stored and recovered.

integer :: IFLAG=0
integer :: BATCH=0,ICALL,IPULSL,JSAV1,JSAV2,KDTIME,LASTYR,&
           MONTHL,NDAT,NDAYL,NPULSE,OLDYR,SINCAL
integer, dimension(12) :: NDAYS = & ! days in each month
         (/31,29,31,30,31,30,31,31,30,31,30,31/)
logical :: DONE, STIFEQ = .false.

character (len=4), parameter, dimension(13) :: NAMONG = &
(/'Jan.','Feb.','Mar.','Apr.','May ','June','July',&
  'Aug.','Sep.','Oct.','Nov.','Dec.','Mean'/)

! Variables to capture the date and time of the run from the system clock
! They will be used in output file headers in ISO 8601 format
character (len=10) :: RunDate = '    -  -  ' ! yyyy-mm-dd
character (len=5)  :: RunTime = '  :  '      ! hh:mm

logical :: RPTFIL=.true., PLTFIL=.false., BASFIL=.false., FGTFIL=.false., &
      HWRFIL=.false., TOXFILC=.false., RSKFILC=.false., TOXFILR=.false., &
      RSKFILR=.false., FULFIL=.false.
! Logicals to control output file production. These are matched
! to the vector of Y/N entries in "OutFil" in globals.f90
! RPTFIL  OutFil(1):  Standard report file (report.xms)
! PLTFIL  OutFil(2):  Standard plotting files (ssout.plt, kinout.plt)
! BASFIL  OutFil(3):  BASS data transfer file (bassexp.xms)
! FGTFIL  OutFil(4):  FGETS data transfer files (fgetscmd.xms, fgetsexp.xms)
! HWRFIL  OutFil(5):  HWIR data transfer file (HWIRExp.xms)
! TOXFILC OutFil(6):  Compartment Ecotox exposure file (EcoToxC.xms)
! RSKFILC OutFil(7):  Compartment event analysis & report file (EcoRiskC.xms)
! TOXFILR OutFil(8):  Reach Ecotox exposure file (EcoToxR.xms)
! RSKFILR OutFil(9):  Reach event analysis & report file (EcoRiskR.xms)
! FULFIL  OutFil(10): Full output of compartment concentrations 

! Counter for number of years in Mode 3, for EcoRisk files
integer :: YearCount
!  BATCH is used to signal the current type of operation.
!          BATCH = 0 - interactive operations,
!                = 1 - batch or RUN operations.
!  DONE indicates that all chemical pulses have been processed.
!  FOURU is 4 times the computer unit roundoff error (see ANNOUN)
!  * IPULSL -- number of the chemical pulse to be processed next.
!  * LASTYR is the end year in the sequence.
!  * MONTHL preserves the number of the month being processed.
!  NAMONG holds the names of the months (Jan., Feb., ... , Mean).
!  * NDAYL tracks the day of chemical pulses.
!  * NDAT is the number of the month (or data block) of
!      environmental data being processed. NDAT is a loop
!      control in GHOST, where it is incremented; it is used as
!      a pointer in the routines called by GHOST. It is then
!      reused as a loop counter in DRIVER.
!  NPULSE is a counter for tracking the number of pulse loadings
!  * OLDYR preserves the number of the year being processed.
!  SINCAL is counter of calls to routine SINGO2
!  STIFEQ is a Logical set .true. when properties of the Jacobian warrant it,
!  and it provides memory when stiff equations are found during simulation.
!
!  *  Variables marked with '*' preserve the state of the integration
!     upon abnormal exit during mode 3 -- they enable restart
!     via a CONTINUE command.
!
end module Local_Working_Space
