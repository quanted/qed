subroutine drivm3(y, runopt)
! File drivm3.f90
! The "driver" routine for EXAMS' mode 3 integration subroutines.
! Created 12-DEC-1983 (L.A. Burns) by disaggregation of DRIVER.
! Revised 27-DEC-1985 (LAB)
! Revisions 10/22/1988--run-time implementation of machine dependencies
! Revised 11/16/1988 to change file handling--added special
! sector for DSI compiler; required because "endfile" has a bug
! Revised 11/3/1989 to add 21-day chronic events to output analysis
! Converted to Fortran90 6/17/1996
! Revised 08-Feb-1999 for floating point comparisons
! Revised 05-Jan-2001 -- new method to capture partial results
! Revised 24-July-2001 - variable "DaysInYear" capturing days for annual means
! Revised 2002-04-10 for capturing ISO date being modeled.
! Revised 2002-04-17 for user-specified durations of event maxima
use Implementation_control
use Statistical_Variables
use Integrator_Working_Storage
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Floating_Point_Comparisons

Implicit None
integer :: runopt ! dummy arguments
real (kind (0D0)), dimension(kount, kchem) :: y
! real (kind (0D0)), dimension(kount*kchem) :: y_pack
real (kind (0D0)) :: abser, reler, toff ! local variables
! TOFF (offset) keeps timer comparisons within range of integer arithmetic
integer :: imove, mon1, nyr, Leap_days, test_year
! Integer valued FRSTYR and LASTYR are located in module
!    Internal_Parameters for use in table headers.
! FRSTYR and LASTYR are the start and end points of the loop
! on the number of years requested for simulation via NYEARG.
! NYR is a loop control variable

integer, dimension(variec) :: ibuff ! IBUFF is data handler for scratch file
logical :: pulse_error
reler = relerr ! transfer of error criteria to integrators
abser = abserr
! IUNITG, in COMMON block CONTRG, controls printing of integrator diagnostics.
! Initially turned OFF, but may be turned ON when the integrator has problems.
iunit = iunitg
imove = stdout  ! The integrator must know the LUN of the terminal
                ! in order to send its "busy" message...
pulse_error = .false.

Dispatch: if (MODEG < 3) then ! Dispatching sector for mode 1 and mode 2
   if (ISOO == 1) call ADMINT (KEQN,Y,WORK,TINIT,TENDL,TINCRL,RELER,&
      ABSER,IUNIT,T,IFLAG,TPRINT,IMOVE,FOURU)
   if (ISOO == 2) call STFINT (KEQN,Y,WORK,IWORK,TINIT,TENDL,TINCRL,&
      RELER,ABSER,IUNIT,T,IFLAG,TPRINT,IMOVE,FOURU,Stiff_Start)
   return
end if Dispatch               ! End of mode 1 and 2 dispatcher

abexit = .false.
! Mode 3 operations depend only on number of years requested
! (NYEARG), which is used as a loop controller. This variable
! must not be 0 or negative -- if so, it defaults to 1...
if (nyearg<1) nyearg = 1
! Set up timer controls
tcodeg = 2  ! Data written to the time series store are in days
! Set values of internal (local) timer controls (in hours)
cintg = 1.0
tincrl = 24.0d+00
tfactr = 24.0
kdtime = tcodeg

! Zero the accumulators for post-simulation analysis
! (except on re-entry from an integrator problem)
Initialize: if (abs(IFLAG) < 3) then
   FLUXCT = 0.0
   YEXPO  = 0.0
   YVOLK  = 0.0
   YHYDR  = 0.0
   YOXID  = 0.0
   YPHOT  = 0.0
   YS1O2  = 0.0
   YRED   = 0.0
   YBIOW  = 0.0
   YBIOS  = 0.0
   YGWAT  = 0.0
   YTOT   = 0.0
   YSUMS  = 0.0
   MAXSEG =  0    ! initialize statistical variables
   MINSEG =  0
   YMINLT = 1.0E+20
   YMINSys = 1.0E+20
   YMINUser=1.0E+20
   YBARLT = -1.0
   YBARSys = -1.0
   YBARUser=-1.0
   PEAKLT = -1.0
   PEAKSys = -1.0
   PEAKUser=-1.0
   DayStart=0.0
   DayEnd=0.0
   Y_start=0.0
   PeakDetectDate=' ';  SysDetectDate=' ';  UserDetectDate=' '
end if Initialize

! RUNOPT is 0 when the RUN command or a batch run invokes the integrators.
! RUNOPT is 1 when entry is via a CONTINUE.

if (runopt==0) then ! set more parameters specific to RUN command entry
   ElapsedYearDays=0.0 ! for counting days elapsed as the years progress
   t = 0.0d+00
   mon1 = 1 ! The starting point for the timer loop is 1 except when
            ! continuing from integrator problems
   if (year1g<1) year1g = 1
   frstyr = year1g
   lastyr = frstyr + nyearg - 1
   ! Start with the presumption that the system is not stiff
   StifEq = .false.
   Stiff_Start=.false.
! For continuations (RUNOPT/=0) do not reset T; it is preserved between calls
elseif (iflag<=2) then
   frstyr = oldyr + 1
   lastyr = oldyr + nyearg
   mon1   = 1
   iflag  = 1
elseif (iflag==10) then ! failsafe: stop attempt to CONTIN from abnormal exit
   write (stdout, fmt='(A,2(/A))')& ! write admonition and abort
      ' Simulation cannot be CONTINued; the loadings are causing',&
      ' a violation of EXAMS linear sorption isthotherm assumption.',&
      ' Decrease the chemical loads and reRUN the simulation.'
   isoo= 0
   return
else
   mon1   = monthl
   frstyr = oldyr
   iflag  = 2
   abexit = .true.
endif

DaysInYear=0.0 ! initialize day counter for this interval
Years_loop: do nyr = frstyr, lastyr
ElapsedMonthDays=0
   if (mod(NYR,4)==0 .and. mod(NYR,100)/=0 .or. mod(NYR,400)==0) then
      NDAYS(2) = 29
   else
      NDAYS(2) = 28
   end if

   if (.not. ABEXIT) then     ! normal entry, not restart after error, so
      IPULSL = 1              ! Initialize pulse counter
      if (IMONG(1) == 0) then ! no need to test pulse loads
         DONE = .true.
      else                    ! need to test pulse loads
         DONE = .false.
      end if
      ! If reporting, set up page header for report on temporal simulation
      if (RPTFIL) call TABE (NYR)
      ! Capture the current year
      write (CurrentDate(1:4),fmt='(I4)') nyr
   end if

   oldyr = nyr ! Store data for possible continue

   Months_loop: do ndat = mon1, 12
      ! Capture the current month
      write (CurrentDate(6:7),fmt='(I2)') ndat
      if (ndat<10) CurrentDate(6:6) = '0'

      monthl = ndat
      call Parameter_Summary (monthl) ! for reach & system-wide averages
      call unpscr(ibuff, abexit, nyr)

      if (.not. ABEXIT) then
         NDAYL = 1    ! Set day counter on day one of this month
         YSUM = 0.0   ! Zero accumulator for Y during this month
      end if

      Days_loop: do
         tinit = t
         if (.not.ABEXIT) then  ! set tendl using pulse data
            call Check_pulses (stdout,pulse_error,isoo,nyr)
            if (pulse_error) return
         else 
            abexit = .false. ! reset indicator for next loop iteration
         endif

         if (t .LessThan. tendl) then ! more integration work needs to be done
            if (.not.stifeq) then
               call admint(keqn, y, work, tinit, tendl, tincrl, reler, abser,&
                  iunit, t, iflag, tprint, imove, fouru)
               if (abs(iflag) == 6) then ! incomplete return due to stiffness
                  stifeq = .true.
                  Stiff_Start = .false.
                  work=0.0
                  iwork=0

!               2005-03-16: no longer a fatal problem ... OUTP recommends
!               Freundlich isotherm but continues working
!               elseif (abs(iflag) == 10) then !violation of isotherm linearity
!                  write (WarnLun,fmt='(A)')&
!                ' ADMINT indicates violation of sorption isotherm linearity.'
               elseif (abs(iflag) > 2) then ! other error returns
                  write (stdout, 5000) namong(ndat), nyr
                  iunitg = 1
                  write (stdout, 5010)
                  isoo = 0
                  return
               end if
            end if
            if (t .LessThan. tendl) then
               tinit = t
               call stfint(keqn, y, work, iwork, tinit, tendl, tincrl, reler,&
                  abser, iunit, t, iflag, tprint, imove, fouru, &
                  Stiff_Start)
               Stiff_Start = .true. ! further calls will be start-ups
               if (abs(iflag) /=2 ) then ! integrator problem
!                  No longer a fatal problem ... OUTP recommends using
!                  Freundlich isotherm and continues
!                  if (IFLAG == 10) then  ! violation of isotherm linearity
!                     write (WarnLun,fmt='(A)')&
!                        ' STFINT indicates violation'//&
!                        ' of sorption isotherm linearity.'
!                     return
!                  end if
                  write (stdout, 5000) namong(ndat), nyr
                  iunitg = 1
                  write (stdout, 5010)
                  isoo = 0
                  return
               end if
            end if
         elseif (t .GreaterThan. tendl) then ! overran output point
            write (stdout, 5000) namong(ndat), nyr
            iunitg = 1
            write (stdout, 5010)
            isoo = 0
            return
         end if
         if (ndayl<ndays(ndat)) then ! not all days of the month are done
            cycle Days_loop
         elseif (ndayl>ndays(ndat) .and. ndayl/=29) then ! The day counter has
            ! advanced beyond the number of days in the month--if this is due
            ! to a leap day pulse, go on. If for some other reason, abort.
            write (stdout, 5020)
            isoo= 0
            return
         endif
         ! Compute elapsed hours at end of month (to test, given that we
         ! have arrived at the last day of the month, whether we are at its
         ! beginning or its end). Compute an offset for T based on the number
         ! of years elapsed and the number of leap days in that sequence
         TOFF = 8760.0D+00*dble(float(NYR-YEAR1G)) ! base hours
         Leap_days = 0
         do Test_year = YEAR1G, NYR-1 ! check years already completed
            if (mod(Test_year,4) == 0 .and. mod(Test_year,100) /= 0 &
               .or. mod(Test_year,400) == 0) Leap_days = Leap_days + 1
         end do
         TOFF = TOFF + dble(float(24*Leap_days)) & ! add hours for leap days
            + dble(float(24*sum(NDAYS(1:NDAT))))   ! and days in current year
         if (t .LessThan. toff) then
            cycle Days_loop
         elseif (t .GreaterThan. toff) then ! overran target time
            write (stdout, 5020)
            write (stdout, fmt='(a)') ' Over-ran target time.'
            isoo= 0
            return
         else ! arrived at end of month, so print month's results and re-up
            if (RPTFIL) call endmon(ndat)
            ! increment days elapsed over months of this year
            ElapsedMonthDays = ElapsedMonthDays + ndays(ndat)
            cycle Months_loop
         endif
      end do Days_loop
   end do Months_loop
   if (RPTFIL) call pricl(nyr) ! print annual summary of loads and pulses
   ! (N.B.--PRICL uses NDAT as loop control--do NOT move it
   ! inside DRIVM3's NDAT loop on months.
   DaysInYear = DaysInYear + sum(ndays)
   ElapsedYearDays = ElapsedYearDays + sum(ndays)
end do Years_loop

isoo= 0 ! set flag to indicate that integration routine terminated
return
5000 format (/' Integrator failure during ',A4,' of year ',I4,'.'/&
              ' Evaluate results before CONTINUing.')
5010 format (/' Integrator diagnostics now switched on (IUNIT=1).')
5020 format (/' System processing error in DRIVM3; RUN aborted.')
contains

Subroutine Check_pulses (ttyout,pulse_error,isoo,nyr)
   integer, intent(in) :: TTYOUT,NYR
   integer :: pfirst, plast, isoo
   ! PFIRST and PLAST are the first and last pulses needing
   ! processing for a given date during a mode 3 simulation.
   logical :: pulse_error
   ! Check for pulse loads specified for leap day, and, if this is
   ! not a leap year, skip over them (by incrementing IPULSL)
   ! If this is a leap year, the test is not executed
   if (ndays(2)==28) then ! not leap year, skip over leap day pulses
      do
         if (imong(ipulsl)/=2 .or. idayg(ipulsl)/=29) exit
         ipulsl = ipulsl + 1 ! leap day pulse, skip it
         if (imong(ipulsl)==0 .or. ipulsl>maxmas) then ! end of series
            done = .true.
            exit
         endif
      enddo
   endif
   
   if (done .or. imong(ipulsl)/=ndat) then      ! no pulses this month, so
      tendl = t + dble(float(24*ndays(ndat)))   ! do the whole month
      ndayl = ndays(ndat)                       ! advance days to month's end
      return
   else  ! current month has one or more pulses
      if (idayg(ipulsl)<ndayl) then    ! problem...passed this pulse without 
         write (ttyout, 5020)          ! processing it
         isoo= 0
         pulse_error = .true.
         return
      elseif (idayg(ipulsl)==ndayl) then
         pfirst = ipulsl
         Find_last_pulse: do
            if (ipulsl<maxmas) then
               if (imong(ipulsl+1)/=ndat) then 
                  if (imong(ipulsl+1)<0) then ! error...negative month
                     write (ttyout, 5020)
                     isoo= 0
                     pulse_error = .true.
                     return
                  elseif (imong(ipulsl+1)==0) then
                     done = .true.
                  endif
                  exit
               else
                  if (idayg(ipulsl)/=idayg(ipulsl+1)) exit ! no more for today
                  ipulsl = ipulsl + 1     ! next pulse also is for today
               endif
            elseif (ipulsl==maxmas) then  ! this is the last pulse
               done = .true.
               exit
            else ! error...passed the last pulse
               write (ttyout, 5020)
               isoo= 0
               pulse_error = .true.
               return
            endif
         enddo Find_last_pulse
   
         plast = ipulsl
         ipulsl = ipulsl + 1 ! set up for processing on next pass
         call ckicm3(y, nyr, pfirst, plast)
         if (iflag == 10) then
            isoo = 0 ! flag to indicate procedure terminated
            write (stderr,fmt='(A)') ' Error in pulse loads.'
            pulse_error = .true.
            return
         elseif (done .or. imong(ipulsl)>ndat) then
            tendl = t + dble(float(24*(ndays(ndat)-ndayl+1)))
            ndayl = ndays(ndat)
            return
         elseif (imong(ipulsl)<ndat) then
            write (ttyout, 5020)
            isoo= 0
            pulse_error = .true.
            return
         endif
      endif
      tendl = t + dble(float(24*(idayg(ipulsl)-ndayl)))
      ndayl = idayg(ipulsl)
   endif
   return
   5020 format (/' System processing error in Check_pulses; RUN aborted.')
end Subroutine Check_pulses
end Subroutine DRIVM3
