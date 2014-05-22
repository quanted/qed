subroutine OUTP(TIME,Y,DY,JFLAG,KFLAG)
! Subroutine to record time-trace computations in output files
! Revised 29 February 1984 for scratch pad file handler
! Revised 29 April 1987 to add complexed concentration to KINOUT plotting file
!  (not implemented in plot file; present as commented area of code)
! Revisions 10/22/1988 run-time implementation of machine dependencies.
! Revisions 11/03/1989 added toxicity event stack
! Revisions 01/23/1992 call to fgets data transmission routine
! Revision  02/08/1999 to use floating point comparison module
! Revisions 03/25/1999 YSATL includes crystal energy correction (see CKLOAD)
! Revisions 07/20/2001 computational procedure for arriving at Mode 3
!    averages (essentially trapezoidal integration of output points)
!    made more efficient and corrected for the annual average
! Revisions 2002-04-10 to capture the simulated date in Mode 3
! Revisions 2002-04-12 for user-specified event durations in the period maxima
! Revisions 2002-04-26 to produce EcoTox, EcoRisk, Fullout files
! As of 2002-06-12, fullout.xms can report both day start and day end values,
!    or it can be restricted to end-of-day values (current state of affairs).
! EcoTox.xms files report end-of-day values; start-of-day values are elided
!   to simplify plot routines, i.e., so plot routines do not have to deal with
!   discontinuities -- time points that have two values
! EcoRisk.xms files report period mean values (including 24-hour for the 
!    one-day means)
! Report.xms reports the start-of-day peak in Table 20.
use Floating_Point_Comparisons
use Implementation_Control
use Statistical_Variables
use Global_Variables
use Local_Working_Space
use Internal_Parameters
Implicit None
! computational variables
real (kind (0D0)) :: Y(KOUNT,KCHEM), DY(KOUNT,KCHEM), TIME
real :: SATST, CHECK
integer, intent (in) :: JFLAG
integer, intent(inout) :: KFLAG
integer :: DayofMonth ! Calculated day of the month in Mode 3
! local variables for this subroutine
real :: TTEMP, YTEMP, TESTXX, RTIMER
! TTEMP is R4 version of dp TIME for unformatted write to Kinlun.
integer :: I, II, ITIMER, J, K, LBEGIN, LEND, IZ, ISTK, DaysElapsed
! ISTK is counter for incrementing the concentration stack
integer :: UE ! to count the User-specified-Events (up to 5)
! load timer outputs tailored for plot files...Time is measured from the
! beginning of the simulation. For example, in Mode 3 time is in days;
! the first year runs from 0-365 (or 366), the second from 366 to 760,etc.
! DaysElapsed indicates the number of days elapsed in the current year
!    The exposure event stack does not start until enough days have passed
!    for it to be meaningful
TTEMP = TIME
ITIMER = int(TIME/TFACTR)
RTIMER = TIME/TFACTR

if (ModeG==3) then ! Calculate and register the date
   ! In Mode 3, ITIMER is the total number of days elapsed in the simulation
   DaysElapsed = ITIMER - ElapsedYearDays
   DayofMonth  = ITIMER - ElapsedYearDays - ElapsedMonthDays
   ! Calls with pulse loads at the start of a month generate a zero day. This
   ! is actually the start (0000 hours) of the first day of the month, so:
   if (DayofMonth == 0) DayofMonth=1
write (CurrentDate(9:10),fmt='(i2)') DayofMonth
if (DayofMonth<10) CurrentDate(9:9) = '0'
end if

! If using simple partitioning, make sure Exams' isotherm 
! linearity assumptions are not violated
Segment_Loop: do J = 1,KOUNT
  Chemical_Loop: do K = 1,KCHEM
   if (Freundlich(K)) cycle Chemical_loop
   ! Using linear isotherm, test this chemical
   II = -3 ! initial value of counter to locate distribution factors (ALPHA)
   Species_loop: do I = 1, 7
      II = II+1 ! Increment counter for ALPHA address
      ! Increment the species loop if the species does not exist:
      if (SPFLGG(I,K) == 0) cycle Species_loop
      ! Check for supersaturation (actually 50% of saturation to keep in
      ! range of linear isotherms; YSATL includes crytal energy correction)
      SATST = ALPHA(3*I+II,J,K)*abs(Y(J,K))
      CHECK = 0.50*YSATL(I,J,K)
      if (SATST .GreaterThan. CHECK) then
         ! Solubility limits exceeded during simulation; notify user and abort
         write (WarnLun,fmt='(A/A,I0,A/A)')&
            " The concentration of "//trim(CHEMNA(K)),&
            " in segment ",J,&
            " reached a level at which Exams' assumption of sorption",&
            " isotherm linearity is violated. Consider using a Freundlich isotherm."
      end if
   End do Species_loop
  End do Chemical_Loop
End do Segment_Loop


Z = 0.0 ! zero "Z" array for all chemicals
Chemicals: do K = 1, KCHEM
   Z2 = 0.0 ! zero "Z2" values for each chemical in turn
   ! calculate concentrations and total ecosystem chemical masses
   ! First, accumulate values for computing mean concentrations
   Segments: do J = 1, KOUNT ! do segments in numerical order
      ! In the multiple chemical version, Y can end up as small negative
      ! values because a very reactive chemical is being decayed over long
      ! time periods due to the need to calculate for a refractive compound.
      ! This results in errors in routine SUMUP when persistence is estimated.
      ! Therefore, Z is computed from the absolute value of Y...
      YTEMP = dabs(Y(J,K))
      Water_column: if (TYPEG(J) /= 'B') then ! water column compartments
         Z(1,K) = Z(1,K)+VOLG(J)*YTEMP*ALPHA(29,J,K)          ! dissolved mg/L
         Z(2,K) = Z(2,K)+VOLG(J)*ALPHA(30,J,K)*YTEMP/SEDCOL(J)! sorbed mg/kg
         Z(5,K) = Z(5,K)+YTEMP*WATVOL(J)*1.0E-06 ! mass, kg (1.E-6 kg/mg)
      else ! bottom sediments
         Z(3,K) = Z(3,K)+VOLG(J)*YTEMP*ALPHA(29,J,K)          ! dissolved mg/L
         Z(4,K) = Z(4,K)+VOLG(J)*ALPHA(30,J,K)*YTEMP/SEDCOL(J)! sorbed mg/kg
         Z(6,K) = Z(6,K)+YTEMP*WATVOL(J)*1.0E-06 ! mass in kg (1.E-6 kg/mg)
      end if Water_column
   end do Segments
   ! Now compute averages in water column
   ! volume-weighted average mg/L dissolved:
     Z(1,K) = Z(1,K)/Total_Limnetic_Volume
   ! volume-weighted average mg/kg sorbed:
     Z(2,K) = Z(2,K)/Total_Limnetic_Volume
   ! Now compute averages in bottom sediments
   ! volume-weighted average mg/L dissolved
     Z(3,K) = Z(3,K)/Total_Benthic_Volume
   ! volume-weighted average mg/kg sorbed
     Z(4,K) = Z(4,K)/Total_Benthic_Volume

   ! Report time course in run log (except in mode 3, where calls to
   ! OUTP are more frequent (daily) than its monthly entries to the run log).
   if (MODEG < 3 .and. RPTFIL) write(RPTLUN,&
       fmt='(1X,I6,1PG9.2,3(1X,G9.2),2X,G9.2,G9.2)') ITIMER,(Z(J,K),J=1,6)

   ! For all modes, enter data in plot file for kinetics (when required)
   if (PLTFIL) write (KINLUN) K,TTEMP,(Z(J,K),J=1,6)

   ! For mode 3, enter data in Full Output file and Compartment EcoTox file
   if (MODEG==3) then
      ! To skip day start values, use this conditional:
      if (FULFIL .and. JFLAG /= 1) then ! output values are end-of-day
      ! To include day-start values, use this conditional
      ! if (FULFIL) then
         if (K==1) write (FULLUN,fmt='(1X,A10)',advance='no') CurrentDate
         write (FULLUN, fmt='(6ES9.2E2)',advance='no') (Z(J,K),J=1,6)
      end if
      ! To skip day start values, use this conditional:
       if (TOXFILC .and. JFLAG /=1) then
      ! To include day start values, use this conditional:
      ! if (TOXFILC) then
         if (K==1) write(TOXCLUN,fmt='(1X,A10)',advance='no') CurrentDate
         write (TOXCLUN, fmt='(2ES9.2E2)',advance='no') Z(1,K),Z(3,K)
      end if
   end if

   ! For mode 2, enter data in Full Output file and Compartment EcoTox file
   if (MODEG==2) then
      if (FULFIL) then
         if (K==1) write(FULLUN,fmt='(1X,I0)',advance='no') ITIMER
         write(FULLUN,fmt='(6ES9.2E2)',advance='no') (Z(J,K),J=1,6)
      end if
      if (TOXFILC) then
         if (K==1) write(TOXCLUN,fmt='(1X,I0)',advance='no') ITIMER
         write(TOXCLUN,fmt='(2ES9.2E2)',advance='no') Z(1,K), Z(3,K)
      end if
   end if

   ! write complete state variable vector to plotting file
   Compartments: do J = 1, KOUNT
      YTEMP = dabs(Y(J,K))
      ! First element in kinetics plot file (LUN KINLUN) is total conc.
      ! (mg/L in water column compartments, mg/kg in bottom sediments)
      Z2(1) = YTEMP
      if (TYPEG(J) == 'B') Z2(1) = YTEMP/SEDCOL(J)

      ! Next element in plot file is dissolved chemical in water phase (mg/L).
      Z2(2) = YTEMP*ALPHA(29,J,K)

      ! Then chemical sorbed in/on sediment solids (mg/kg solids)
      Z2(3) = ALPHA(30,J,K)*YTEMP/SEDCOL(J)

      ! Next is chemical sorbed in/on biota in ug/g (biotol (biomass/water)
      Z2(4) = ALPHA(32,J,K)*YTEMP/BIOTOL(J) ! computed in subroutine DISTRB)

      ! Finally, segment mass in grams/square meter
      ! 1.0E-03 factor converts mg to grams
      Z2(5) = 1.0E-03*YTEMP*WATVOL(J)/AREAG(J)

      ! Write these quantities to kinetics file (LUN KINLUN)
      if (PLTFIL) write (KINLUN) K,TTEMP,J,(Z2(I),I=1,5)
      Z2(6) = ALPHA(31,J,K)*YTEMP   ! Total complexed concentration
      ! Could add complexed concentration to standard plots if desired, i.e.
      ! change output line to 
      ! if (PLTFIL) write (KINLUN) K,TTEMP,J,(Z2(I),I=1,6)
      ! and revise plotting routines

      ! To skip the day-start values, use this conditional:
      if (MODEG==2 .or. (MODEG==3.and.JFLAG/=1)) then
      ! To include the day-start values, use this conditional:
      ! if (MODEG==2 .or. MODEG==3) then
         if (FULFIL) then
            if (J==KOUNT .and. K==KCHEM) then
               write (FULLUN, fmt='(6ES9.2E2)', advance='yes') (Z2(I),I=1,6)
            else
               write (FULLUN, fmt='(6ES9.2E2)', advance='no') (Z2(I),I=1,6)
            end if
         end if
         if (TOXFILC) then
            if (J==KOUNT .and. K==KCHEM) then
               write (TOXCLUN, fmt='(2ES9.2E2)', advance='yes') Z2(2),Z2(4)
            else
               write (TOXCLUN, fmt='(2ES9.2E2)', advance='no') Z2(2),Z2(4)
            end if
         end if
       end if

      ! If NOT in mode 3 go on to next compartment for writing output file
      if (MODEG /= 3) cycle Compartments

      ! IN mode 3, check for new critical toxicity events and update sums
      if (JFLAG==1) then
        Y_start(J,K) = dabs(Y(J,K))
      else
        YSUM(J,K)=YSUM(J,K) +((Y_start(J,K)+dabs(Y(J,K)))/2.0)
        Y_start(J,K) = dabs(Y(J,K))
      end if
      ! separate benthic and water column data by setting loop bounds
      if (TYPEG(J) /= 'B') then ! water column segments
         LBEGIN = 1
         LEND = 5
      else ! benthic segments
         LBEGIN = 6
         LEND = 10
      endif

      IZ = 1 ! initialize index for access to concentration variables
      Data_loop: do I = LBEGIN, LEND
         if (JFLAG == 1) then
         ! For initial values, load the start-of-day values
            DayStart(I,J,K) = Z2(IZ)
            IZ = IZ+1
            cycle Data_loop
         endif
         ! For end-of-day, capture the current concentrations in DayEnd
         DayEnd(I,J,K) = Z2(IZ)

         ! Push the stack of concentrations up one day, clearing day one
         ! ...this could be done with EOSHIFT, but eoshift is much slower
         ! than a loop (run times increased by 60%), so don't do it; instead
         do ISTK = 366, 2, -1
            DayStack(ISTK,I,J,K) = DayStack(ISTK-1,I,J,K)
         end do

         ! Calculate the current day average values
         DayStack(1,I,J,K) = (DayStart(I,J,K) + DayEnd(I,J,K)) / 2.0

         ! maxima...
         ! PEAKLT tracks period-of-record (i.e., RUN period and CONTIN
         ! intervals) maxima for tables

         ! This method tracks the maximum daily average:
         ! TESTXX = amax1(PEAKLT(I,K), DayStack(1,I,J,K))

         ! This method tracks the abolute start-of-day peak:
         TESTXX = amax1(PEAKLT(I,K), DayStart(I,J,K))

         ! Any input pulse arrives all at once
         ! For an initial pulse of 1.0 mg/L, half-life of 2 days,
         ! the Mode 3 daily average is 0.854 mg/L.
         ! Testing with Mode 2 gave a peak of 0.8485 when the same
         ! load arrives over 12 hours, and a peak of 0.9888 when
         ! the same load arrives over 4 hours. Thus, carrying the
         ! the pulse peak as the overall (annual) peak concentration
         ! seems appropriate.
         ! N.B. The EcoTox files report the end-of-day values, but the
         ! EcoRisk files track the day start values for the long-term peak
         if (TESTXX .GreaterThan. PEAKLT(I,K)) then
            PEAKLT(I,K) = TESTXX
            MAXSEG(I,K) = J
            PeakDetectDate(I,K) = CurrentDate
         endif
         ! minima...
         ! YMINLT tracks period-of-record minima for tables
         TESTXX = amin1(YMINLT(I,K), DayStart(I,J,K), DayEnd(I,J,K))
         if (TESTXX .LessThan. YMINLT(I,K)) then
            YMINLT(I,K) = TESTXX
            MINSEG(I,K) = J
         endif

         ! then update the current end-of-day value, which becomes
         ! the start-of-day value for tomorrow...although the
         ! start-of-day value can change if there is a pulse into
         ! the system, in which case the call to OUTP with JFLAG=1
         ! will update DayStart
         DayStart(I,J,K) = DayEnd(I,J,K)

         ! Process the stack to see if a new system event values are needed.
         ! Note that system event 1 is the 24-hourly mean value

!                !2013-05-30
!                write(stderr,*) "size(YBARSys) ==",size(YBARSys)
!                write(stderr,*) "UBound(YBARSys) ==",UBound(YBARSys)
!                write(stderr,*) "YBARSys ==",YBARSys
!                write(stderr,*) "size(SysEventDur) ==",size(SysEventDur)
!                write(stderr,*) "UBound(SysEventDur) ==",UBound(SysEventDur)
!                write(stderr,*) "SysEventDur ==",SysEventDur
!                write(stderr,*) "size(SysDetectDate) ==",size(SysDetectDate)
!                write(stderr,*) "UBound(SysDetectDate) ==",UBound(SysDetectDate)
!                write(stderr,*) "SysDetectDate ==",SysDetectDate
         SysEvents: do UE=1,size(SysEventDur)
         ! if the simulation has reached System Event Duration (ue) days
         if (DaysElapsed >= SysEventDur(UE)) then
!                         write(stderr,*) "UE1",UE

         TESTXX=(sum(DayStack(1:SysEventDur(UE),I,J,K)))/real(SysEventDur(UE))
         ! If a new value is needed, recompute its peak and minimum values
         if (TESTXX .GreaterThan. YBARSys(UE,I,K)) then
            YBARSys(UE,I,K) = TESTXX
            PEAKSys(UE,I,K) = maxval(DayStack(1:SysEventDur(UE),I,J,K))
            YMINSys(UE,I,K) = minval(DayStack(1:SysEventDur(UE),I,J,K))
!                write(stderr,*) "UE",UE
            SysDetectDate(UE,I,K) = CurrentDate
         end if; end if
         end do SysEvents

!          SysEvents: do UE=1,size(SysEventDur)   !2013-05-30
!          ! if the simulation has reached System Event Duration (ue) days
!          if (DaysElapsed >= SysEventDur(UE)) then
!                            write(stderr,*) "UE1",UE

!             TESTXX=(sum(DayStack(1:SysEventDur(UE),I,J,K)))/real(SysEventDur(UE))
!          ! If a new value is needed, recompute its peak and minimum values
!          else
!             if (TESTXX .GreaterThan. YBARSys(UE-1,I,K)) then
!                YBARSys(UE-1,I,K) = TESTXX
!                PEAKSys(UE-1,I,K) = maxval(DayStack(1:SysEventDur(UE-1),I,J,K))
!                YMINSys(UE-1,I,K) = minval(DayStack(1:SysEventDur(UE-1),I,J,K))
!                write(stderr,*) "UE",UE
!                write(stderr,*) "SysDetectDate",SysDetectDate

!                SysDetectDate(UE-1,I,K) = CurrentDate
!             end if; 
!          end if
!          end do SysEvents

         ! now examine the user-specified event stack(s) ...
         ! If such have been requested, reprocess and update as needed
         UserEvents: do UE=1,5
            Event: if (UserEvent(UE) .and. DaysElapsed>=EventDL(UE)) then
              TESTXX = &
               (sum(DayStack(1:EventDL(UE),I,J,K)))/real(EventDL(UE))
              ! if a new value is indicated, recompute
              ! the peak and minimum values by processing the stack
              if (TESTXX .GreaterThan. YBARUser(UE,I,K)) then
                 YBARUser(UE,I,K) = TESTXX
                 PEAKUser(UE,I,K) = maxval(DayStack(1:EventDL(UE),I,J,K))
                 YMINUser(UE,I,K) = minval(DayStack(1:EventDL(UE),I,J,K))
                 UserDetectDate(UE,I,K) = CurrentDate
              endif
            endif Event
         end do UserEvents

         IZ = IZ+1 ! increment index for access to concnetration variables
      end do Data_loop
   end do Compartments
end do Chemicals
! call the FGETS/BASS/HWIR transfer routines
! (In mode 1, concentrations are written from steady-state routines)
if (MODEG==1) return
! Write Fgets, Bass, HWIR transfer files, & Reach-oriented EcoTox file
if (FGTFIL.or.BASFIL.or.HWRFIL.or.TOXFILR)&
  call EX2FGT(Y,JFLAG,RTIMER,ITIMER,CurrentDate)
return

end subroutine OUTP
