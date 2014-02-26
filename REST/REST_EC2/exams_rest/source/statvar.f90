module Statistical_Variables ! File Statvar.F90
! Revised 2002-04-11 to add ElapsedYearDays, a counter of the total
!   of days elapsed over the years of a Mode 3 simulation, and
!   ElapsedMonthDays, a counter of the days elapsed during the months of
!   the current year

Implicit None
Save
! DayStack is sequence of latest set of mean daily concentrations,
! calculated as (DayStart+DayEnd)/2.
real, dimension(:,:,:,:), allocatable :: DayStack
! DayStart and DayEnd are today's starting and ending concentrations,
! for each tracked variable, compartment, and chemical
real, dimension(:,:,:), allocatable :: DayStart, DayEnd
! Y_start is start-of-day Y state variable
real, dimension(:,:), allocatable :: Y_start
! CurrentDate is the current date in the simulation. It is constructed
! in ISO 8601 format as yyyy-mm-dd. 
character (len=10) :: CurrentDate = '    -  -  '
! DetectDate is the date in the simulation study at which an extreme event
! is detected. It is transferred from CurrentDate.
character (len=10), allocatable :: PeakDetectDate(:,:), SysDetectdate(:,:,:),&
      UserDetectDate(:,:,:)
! Up to five user-selectable event durations for annual maximum series
! System extremes include the RUN period absolute maxima and five
!   standard toxicological periods, and the annual average value (for FQPA): 
!     24-hour (1-day), 96-hour (4 days), 21-day, 60-day, 90-day
!   If these are changed, the column headings in M3FLUX also need changes.
!   Note, however, that the 24-hour period is not reported in Table 20.
integer, dimension(6) :: SysEventDur = (/1,4,21,60,90,365/)
! For counting the number of user-specified event durations
integer :: NumEvents = 0

integer :: ElapsedYearDays =  0  ! counts elapsed days per year in Mode 3
integer :: ElapsedMonthDays = 0  ! counts elapsed days per month in Mode 3
real :: DaysInYear = 0.0

! accumulators and analysis variables
! extreme event analysis variables
real, allocatable :: YMINLT(:,:), YMINUser(:,:,:), YMINSys(:,:,:), &
                     YBARLT(:,:), YBARUser(:,:,:), YBARSys(:,:,:), &
                     PEAKLT(:,:), PEAKUser(:,:,:), PEAKSys(:,:,:)
integer, allocatable :: MAXSEG(:,:), MINSEG(:,:)
logical, dimension(5) :: UserEvent = .false. ! indicates user requested event
integer, dimension(5) :: EventDL = 0 ! local version of EventD for processing

end module Statistical_Variables
