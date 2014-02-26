subroutine RUNIT ()
! Purpose of this routine is to initialize variables, allocate storage,
!    and check on values needed to run the simulation
! Subroutines required: none
! Revised 27-DEC-85 (LAB)
! Revisions 10/21/88 to convert machine dependencies to run-time solutions
! Revision 09-Feb-1999 to use floating point comparison module
! Revisions 2002-04-04 to access system clock for time stamping
! Revisions 2002-04-12 to support user-specified event durations
use Floating_Point_Comparisons
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
use Integrator_Working_Storage
use Table_Variables
use Statistical_Variables
Implicit None
real :: Test_SUM
integer :: I, J, J1, K, Isorter
! Isorter is integer temporary for sorting EventDL
logical :: New_Reach ! to decode system structure into reaches

! Parameters to access system clock 
   character (len=10) :: SysClockDate
   character (len=10) :: SysClockTime
   call Date_and_Time (SysClockDate,SysClockTime) ! Read system clock
! rewrite time and date to ISO 8601 format
   RunTime(1:2)=SysClockTime(1:2);RunTime(4:5)=SysClockTime(3:4)
   RunDate(1:4)=SysClockDate(1:4)
   RunDate(6:7)=SysClockDate(5:6)
   RunDate(9:10)=SysClockDate(7:8)
! 
! Set marker to allow RUN; if there are problems it will reset to 0
IRUN = 1

! Set run-time formats and allocate output processing data spaces
call Allocate_Table_Variables
call SetFormats ! if KOUNT>999, output formats are adjusted

! Basic reality checks:
if (TYPEG(1)=='B') then
   write (stderr,fmt='(A)')&
      ' Error: TYPE(1) is "B".',&
      ' The ecosystem cannot start with a Benthic element.',&
      ' Simulation not executed.'
   IRUN=0
   return
elseif (TYPEG(KOUNT)/='B') then
   write (stderr,fmt='(A)')&
      ' Error: TYPE(KOUNT) is not "B".',&
      ' The ecosystem must end with a Benthic element.',&
      ' Simulation not executed.'
   IRUN=0
   return
end if

call GEOCK ! to evaluate alternative means of specifying system geometry

do I=1, NTRAN ! evaluate validity of specifications for product chemistry
   if ((KCHEM > 1) .and. (CHPARG(I)>KCHEM .or. TPRODG(I)>KCHEM)) then
      write (stderr, fmt='(/A,/A)')&
         ' Error: product chemistry contains an ADB specification',&
         ' larger than the number of chemicals under study.'
      IFLAG = 8
      return
   end if
end do

! Make sure that no water solubility is zero.
Do K=1,KCHEM
if (SOLG(1,K) .Equals. 0.0) then ! can't run...notify user
   write (stderr,fmt='(/A,I3,A)')&
      ' Aqueous solubility (SOL(1,',K,') is 0.'
   IRUN=0
   return
endif
end do

! See if a load has been specified.
Test_SUM = sum(STRLDG)+sum(NPSLDG)+sum(PCPLDG)+sum(DRFLDG)+sum(SEELDG)
if (.not. (Test_SUM .GreaterThan. 0.0) .and. MODEG==1) then
   write (stderr,fmt='(/A/A)') ' No load specified.',&
   ' Steady-state contamination cannot be calculated.'
   IRUN=0
   return
end if

if (MODEG <= 0 .or. MODEG > 3) then ! illegal MODE of operation
   write (stderr,fmt='(A/A,I5,A)')&
      ' This version of EXAMS does not have an operating',&
      ' MODE of ',MODEG,'. The RUN has been aborted.'
   IRUN=0
   return
end if

if (KCHEM <= 0) then ! nonsense value--inform user and abort
   write (stderr,fmt='(A,I5,A)')&
      ' The RUN request for ',KCHEM,' chemicals has been cancelled.'
   IRUN=0
   return
end if

! Check to ensure that the number of segments requested by the user
! is not a nonsense (negative or zero) value
if (KOUNT <= 0) then
   write (stderr,fmt='(A,I5,A)')&
   ' The RUN request for a ',KOUNT,' segment model has been cancelled.'
   IRUN=0
   return
end if

if (MODEG==2) then
   ! if the ending time is not on a mesh point...
   if (mod((TENDG-TINITG),CINTG) .GreaterThan. 0.0) then ! fix it
      TENDG = TENDG + CINTG - mod((TENDG-TINITG),CINTG)
      write (stdout,fmt='(/A/A,I6,A)')&
      ' The reporting interval (CINT) extends beyond the ending time.',&
      ' TEND has been extended to ', int(TENDG), ' to give complete results.'
   end if
   TINITG = TINITL
end if

! decode reach structure and allocate storage for this simulation...

deallocate (Reach_ID)
allocate (Reach_ID(KOUNT))
Reach_ID = 0
deallocate (Benthic, Limnetic, Benthos)
allocate (Benthic(KOUNT), Limnetic(KOUNT), Benthos(KOUNT))
! Analyze system compartmental structure and define reach structure for
! use in BASS and HWIR transfer files, output summaries, etc.

Reaches_in_System = 0
New_Reach = .true.
Benthic = .false.
Limnetic = .true.
Benthos = .false.
do J = 1, KOUNT ! (First segment is water -- checked above.)
   if (TYPEG(J)=='B') then ! evaluate benthic compartments
      Benthic(J) = .true.
      do I = 1,13
         if (BNMASG(J,I) .GreaterThan. 0.0) Benthos(J) = .true.
         if (DOCG(J,I)<10.0) DOCG(J,I)=10.0 ! enforce minimum benthic value
      end do
   else ! evaluate limnetic compartments
      do I=1,13
         if (DOCG(J,I)<1.0) DOCG(J,I)=1.0 ! enforce minimum limnetic value
      end do
   end if
   if (New_Reach .and. TYPEG(J)=='B') then
      Reaches_in_System = Reaches_in_System + 1
      New_Reach = .false.
   end if
   if (J < KOUNT) then
      if (TYPEG(J+1)/='B') New_Reach = .true.
   end if
end do

! allocate storage for reach variables
deallocate (Benthic_Count)
allocate (Benthic_Count(Reaches_in_System))
deallocate (Limnion_Count)
allocate (Limnion_Count(Reaches_in_System))
deallocate (Benthos_Count)
allocate (Benthos_Count(Reaches_in_System))

! continue determination of reach structure for this simulation
Benthic_Count=0
Limnion_Count=0
Benthos_Count=0
K=1
do I=1,Reaches_in_System
  do J = K, KOUNT-1
      Reach_ID(J) = I
      if (Benthic(J)) then
         Benthic_Count(I)=Benthic_Count(I)+1
         if (Benthos(J)) Benthos_Count(I)=Benthos_Count(I)+1
         if (TYPEG(J+1)/='B') then
            K=J+1
            exit ! to do next reach
         end if
      else
         Limnion_Count(I)=Limnion_Count(I)+1
      end if
  end do
end do
! last compartment is necessarily a (benthic) member of the last reach, so
Reach_ID(KOUNT) = Reaches_in_System
Benthic_Count(Reaches_in_System) = Benthic_Count(Reaches_in_System)+1
if (Benthos(KOUNT)) &
   Benthos_Count(Reaches_in_System) = Benthos_Count(Reaches_in_System)+1 

! Output statements for testing
! write(*,*) ' Compt. ', (i,i=1,kount)
! write(*,*) ' Type ', (TYPEG(i),i=1,kount)
! write(*,*) ' Reach_ID ', Reach_ID
! write(*,*) ' Reach:    ', (i,i=1,reaches_in_system)
! write(*,*) ' No. Waters', Limnion_Count
! write(*,*) ' No. Benth ', Benthic_Count

! Calculate total water depth & volume of each reach,
!   and system-wide mean depth and total volume
deallocate (Reach_Depth)
   allocate (Reach_Depth(Reaches_in_System))
   Reach_Depth = 0.0E+00
deallocate (Reach_Limnetic_Volume)
   allocate (Reach_Limnetic_Volume(Reaches_in_System))
   Reach_Limnetic_Volume=0.0E+00
deallocate (Reach_Benthic_Volume)
   allocate (Reach_Benthic_Volume(Reaches_in_System))
   Reach_Benthic_Volume=0.0E+00
deallocate (Reach_Benthos_Volume)
   allocate (Reach_Benthos_Volume(Reaches_in_System))
   Reach_Benthos_Volume=0.0E+00

! System totals and averages
Total_Limnetic_Volume=0.0E+00
Total_Benthic_Volume=0.0E+00
Total_Benthos_Volume=0.0E+00
Mean_Water_Depth=0.0E+00 ! System-wide average

K = 1    ! Used to update starting point for compartment summing
do I = 1, Reaches_in_System
  Column: do J = K, KOUNT-1
     if (TYPEG(J)/='B') then ! test needed if last reach ends with 2 "B" segs
        Reach_Depth(I) =  Reach_Depth(I)+ DEPTHG(J)
        Reach_Limnetic_Volume(I) = Reach_Limnetic_Volume(I) + VOLG(J)
     end if
     if (TYPEG(J+1) == 'B') then ! end of water column, so
                                 ! locate the next water column for restart
        K=(J+2)                  ! if only 1 B, it starts here
        do J1 = K, KOUNT         ! but if not, find where it starts
                                 ! Note that J1 could be beyond the end of
                                 ! KOUNT, except that K > KOUNT so the loop
                                 ! will not execute
           if (TYPEG(J1) == 'B') then ! continuing benthic zone, so
             K = K+1
           else                       ! found start of next water column, so
             exit Column              ! exit water column loop, do next reach
           end if
        end do
     end if
  end do Column
end do
Mean_Water_Depth = sum(Reach_Depth)/Reaches_in_System
Total_Limnetic_Volume = sum(Reach_Limnetic_Volume)

deallocate (Calc_Vector)
allocate (Calc_Vector(KOUNT,7))
Calc_vector = 0.0E+00

! Use structure to calculate benthic properties
do I=1, Reaches_in_System
   where (Reach_ID==I .and. benthic)
      Calc_Vector(:,1) = VOLG(1:KOUNT) ! this shouldn't be necessary, and it
                                  ! even looks dangerous, but without it
                                  ! the machine hangs, and it works properly.
                                  ! It's probably an LF90 bug.
   elsewhere
      Calc_Vector(:,1) = 0.0E+00
   end where
!write (*,*) ' Benthic Volume Vector', Calc_vector
   Reach_Benthic_Volume(I) = sum(Calc_Vector)
end do
Total_Benthic_Volume = sum(Reach_Benthic_Volume)

Calc_vector=0.0E+00

! Use structure to calculate benthos properties
do I=1, Reaches_in_System
   where (Reach_ID==I .and. Benthos)
      Calc_Vector(:,1) = VOLG(1:KOUNT) ! this shouldn't be necessary, and it
                                  ! even looks dangerous, but without it
                                  ! the machine hangs, and it works properly.
                                  ! Possibly a compiler bug.
   elsewhere
      Calc_Vector(:,1) = 0.0E+00
   end where
! write (*,*) ' Benthos Volume Vector', Calc_vector
   Reach_Benthos_Volume(I) = sum(Calc_Vector)
end do
Total_Benthos_Volume = sum(Reach_Benthos_Volume)

Calc_vector=0.0E+00

! Program testing
!write (*,*) ' Mean Water Depth       = ', Mean_Water_Depth
!write (*,*) ' Total Water Volume     = ', Total_Limnetic_Volume
!write (*,*) ' Total Benthic Volume   = ', Total_Benthic_Volume
!write (*,*) ' Total Benthos Volume   = ', Total_Benthos_Volume
!write (*,*) ' Reach Water Depths     =  ', Reach_Depth
!write (*,*) ' Reach Volumes          = ', Reach_Limnetic_Volume
!write (*,*) ' Reach Benthic Vol      = ', Reach_Benthic_Volume
!write (*,*) ' Reach Benthos Exposure Volume = ', Reach_Benthos_Volume

! For each reach, the surficial layers represent the primary exposure of
! benthic organisms (not including bacteria). Both the total sediment
! concentration and the exposure concentration could be reported, but
! the deeper layer is buried beyond the reach of the benthos. This ecological
! structuring is established in the scenario by controlling BNMASG.

! allocate and initialize general computational storage
!    for use in the rest of the simulation
deallocate (Bacterioplankton)
allocate (Bacterioplankton(Reaches_in_System))
Bacterioplankton = 0.0

deallocate (Phytoplankton)
allocate (Phytoplankton(Reaches_in_System))
Phytoplankton = 0.0

deallocate (Zooplankton)
allocate (Zooplankton(Reaches_in_System))
Zooplankton = 0.0

deallocate (Plankton_Biomass)
allocate (Plankton_Biomass(Reaches_in_System))
Plankton_Biomass = 0.0

deallocate (Benthos_Biomass)
allocate (Benthos_Biomass(Reaches_in_System))
Benthos_Biomass = 0.0

deallocate (Insects)
allocate (Insects(Reaches_in_System))
Insects = 0.0

deallocate (Periphyton)
allocate (Periphyton(Reaches_in_System))
Periphyton = 0.0

deallocate (Water_Temperature)
allocate (Water_Temperature(Reaches_in_System))
Water_Temperature = 500.0

deallocate (Reach_TSS)
allocate (Reach_TSS(Reaches_in_System))
Reach_TSS = 0.0

deallocate (focbenthic)
allocate (focbenthic(Reaches_in_System))
focbenthic = 0.0

! Computational and output variables for contaminants
deallocate (Reach_cwtot)       ! mg/L in Limnetic Zone
deallocate (Reach_Cwater)      ! mg/L diss in Limn Z
deallocate (Reach_Cplankton)   ! mg/kg FW  in Limn Z
deallocate (Reach_Cbtot)       ! mg/kg DW in Benthic Z

deallocate (Reach_Cbdiss)      ! mg/L pore water - benthos exposure
! (if no benthos in 'B' compartment, no contribution to Reach_Cbdiss)

deallocate (Reach_Cbnths)      ! mg/kg dw for BASS
deallocate (Mean_Cwater, Mean_Cplankton, Mean_Cbtot, Mean_Cbdiss, Mean_Cbnths)

allocate (Reach_cwtot(Reaches_in_System,KCHEM))       ! mg/L in Limnetic Zone
Reach_cwtot = 0.0

allocate (Reach_Cwater(Reaches_in_System,KCHEM))      ! mg/L diss in Limn Z
Reach_Cwater = 0.0

allocate (Reach_Cplankton(Reaches_in_System,KCHEM))   ! mg/kg FW  in Limn Z
Reach_Cplankton = 0.0

allocate (Reach_Cbtot(Reaches_in_System,KCHEM))       ! mg/kg DW in Benthic Z
Reach_Cbtot = 0.0

allocate (Reach_Cbdiss(Reaches_in_System,KCHEM))      ! mg/L pore water
Reach_Cbdiss = 0.0 ! exposure of benthos

allocate (Reach_Cbnths(Reaches_in_System,KCHEM))      ! mg/kg dw for BASS
Reach_Cbnths = 0.0

allocate (Mean_Cwater (KCHEM), Mean_Cplankton(KCHEM), Mean_Cbtot(KCHEM), &
          Mean_Cbdiss(KCHEM), Mean_Cbnths(KCHEM))
Mean_Cwater =0.0; Mean_Cplankton = 0.0; Mean_Cbtot=0.0
          Mean_Cbdiss = 0.0; Mean_Cbnths = 0.0

! BASS requirements not yet implemented; negative values signal
!   to BASS that these variables are unavailable
deallocate (Mean_Cinsct, Mean_Cphytn, Mean_Cpplnk, Mean_Czplnk)

allocate (Mean_Cinsct(KCHEM), Mean_Cphytn(KCHEM), Mean_Cpplnk(KCHEM), &
          Mean_Czplnk(KCHEM))

Mean_Cinsct=-999.0
Mean_Cphytn=-999.0
Mean_Cpplnk=-999.0
Mean_Czplnk=-999.0
! End of pending BASS variables

Deallocate (CONLDL, INTINL, TOTKL, YIELDL)

Allocate (CONLDL(KOUNT,KCHEM), INTINL(KOUNT,KOUNT,KCHEM), TOTKL(KOUNT,KCHEM),&
          YIELDL(KCHEM,KCHEM,KOUNT))
CONLDL = 0.0; INTINL = 0.0; TOTKL = 0.0; YIELDL = 0.0

Deallocate (ALPHA, BIOLKL, BIOTOL, EXPOKL, HYDRKL, OXIDKL, PHOTKL, REDKL, &
            S1O2KL, SEDCOL, SEDMSL, VOLKL, WATVOL, YSATL, KBACWL, KBACSL)

Allocate (ALPHA(32,KOUNT,KCHEM), BIOLKL(KOUNT,KCHEM), BIOTOL(KOUNT), &
          EXPOKL(KOUNT,KCHEM), HYDRKL(KOUNT,KCHEM), OXIDKL(KOUNT,KCHEM), &
          PHOTKL(KOUNT,KCHEM), REDKL (KOUNT,KCHEM), S1O2KL(KOUNT,KCHEM), &
          SEDCOL(KOUNT), SEDMSL(KOUNT), VOLKL(KOUNT,KCHEM), WATVOL(KOUNT), &
          YSATL(7,KOUNT,KCHEM), KBACWL(4,7,KCHEM), KBACSL(4,7,KCHEM))
ALPHA=0.0;  BIOLKL=0.0; BIOTOL=0.0; EXPOKL=0.0; HYDRKL=0.0; OXIDKL=0.0
PHOTKL=0.0; REDKL=0.0;  S1O2KL=0.0; SEDCOL=0.0; SEDMSL=0.0; VOLKL =0.0
WATVOL=0.0; YSATL=0.0;  KBACWL=0.0; KBACSL=0.0

Deallocate (TOTLDL, YSUM)
Allocate (TOTLDL(KOUNT,KCHEM), YSUM(KOUNT,KCHEM))
          TOTLDL=0.0; YSUM = 0.0

Deallocate (YBIOS, YBIOW, YEXPO, YGWAT, YHYDR, YOXID, YPHOT, YRED, &
            YS1O2, YSUMS, YTOT, YVOLK)

Allocate (YBIOS(KCHEM), YBIOW(KCHEM), YEXPO(KCHEM), YGWAT(KCHEM), &
          YHYDR(KCHEM), YOXID(KCHEM), YPHOT(KCHEM), YRED(KCHEM),  &
          YS1O2(KCHEM), YSUMS(32,KOUNT,KCHEM), YTOT(3,KOUNT,KCHEM), &
          YVOLK(KCHEM))
          YBIOS=0.0; YBIOW=0.0; YEXPO=0.0; YGWAT=0.0; YHYDR=0.0; YOXID=0.0
          YPHOT=0.0; YRED=0.0; YS1O2=0.0; YSUMS=0.0; YTOT=0.0; YVOLK=0.0


Deallocate (YMINSys, YMINLT, YMINUser, YBARSys, YBARLT, YBARUser, &
            PEAKSys, PEAKLT, PEAKUser, MAXSEG,   MINSEG)

Allocate (YMINLT(10,KCHEM),     YBARLT(10,KCHEM),     PEAKLT(10,KCHEM), &
          YMINUser(5,10,KCHEM), YBARUser(5,10,KCHEM), PEAKUser(5,10,KCHEM), &
          YMINSys(6,10,KCHEM),  YBARSys(6,10,KCHEM),  PEAKSys(6,10,KCHEM), &
          MAXSEG(10,KCHEM), MINSEG(10,KCHEM))
          YMINLT=1.0E+20;   YBARLT=-1.0;   PEAKLT=-1.0
          YMINUser=1.0E+20; YBARUser=-1.0; PEAKUser=-1.0
          YMINSys=1.0E+20;  YBARSys=-1.0;  PEAKSys=-1.0
          MAXSEG=0.0; MINSEG=0.0

Deallocate (PeakDetectDate, SysDetectDate, UserDetectDate)

! Sort and load local value of user-specified event durations
EventDL=EventD
UserEvent=.false.
Outer: do j = 2, size(EventDL) ! simple straight insertion sort
   Isorter = EventDL(j)
   Inner: do i = j-1,1,-1
      if (EventDL(i) >= Isorter) then
          EventDL(i+1) = Isorter
          cycle outer
      end if
      EventDL(i+1) = EventDL(i)
   end do Inner
   EventDL(1) = Isorter
end do Outer
do i=1,5 ! set the logic flag for events
   if (EventDL(i)>0) UserEvent(i)=.true.
end do
! Count the user-specified event durations
NumEvents = 0
do i=1,5
   if (UserEvent(i)) NumEvents = NumEvents + 1
end do
! End of sections for sorting out user-specified event durations

Allocate (PeakDetectDate(10,KCHEM), UserDetectDate(5,10,KCHEM), &
!           SysDetectDate(5,10,KCHEM))
          SysDetectDate(6,10,KCHEM))  !2013-05-31

          PeakDetectDate  = ' ';  UserDetectDate = ' '; SysDetectDate = ' '


Deallocate (ACCUM2, ACCUM3, ACCUM4)
Allocate   (ACCUM2(6,KOUNT,KCHEM), ACCUM3(7,KOUNT), ACCUM4(6,KOUNT))
            ACCUM2=0.0; ACCUM3=0.0; ACCUM4=0.0

Deallocate (QSSAV,QTSAV,QWSAV,SYSLDL,BIOPCT,CHEMPC,EXPPCT,TRANLD,VOLPCT)
Deallocate (Z,DOMAX)
Allocate  (QSSAV(KCHEM),QTSAV(KCHEM),QWSAV(KCHEM),SYSLDL(KCHEM),&
           BIOPCT(KCHEM),CHEMPC(KCHEM),&
           EXPPCT(KCHEM),TRANLD(KCHEM),VOLPCT(KCHEM))
Allocate  (Z(6,KCHEM),DOMAX(10,KCHEM))
           QSSAV=0.0; QTSAV=0.0; QWSAV=0.0; SYSLDL=0.0; BIOPCT=0.0
           CHEMPC=0.0;EXPPCT=0.0; TRANLD=0.0; VOLPCT=0.0; Z=0.0; DOMAX=0.0

Deallocate (KA1L, KA2L, KA3L, KB1L, KB2L, KB3L, KPSL)
Allocate (KA1L(KOUNT,KCHEM), KA2L(KOUNT,KCHEM), KA3L(KOUNT,KCHEM), &
          KB1L(KOUNT,KCHEM), KB2L(KOUNT,KCHEM), KB3L(KOUNT,KCHEM), &
          KPSL(7,KOUNT,KCHEM))
          KA1L=0.0; KA2L=0.0; KA3L=0.0; KB1L=0.0; KB2L=0.0; KB3L=0.0; KPSL=0.0

Deallocate (NPSCOL,NPSFL,RAINFL,SEDFL,SEDOUL,SEEPSL,STRMFL,STSCOL,&
            WATFL,WATOUL)
Allocate (NPSCOL(KOUNT), NPSFL(KOUNT), RAINFL(KOUNT), &
          SEDFL(KOUNT,KOUNT,KCHEM), SEDOUL(KOUNT), SEEPSL(KOUNT), &
          STRMFL(KOUNT), STSCOL(KOUNT), WATFL(KOUNT,KOUNT), WATOUL(KOUNT))
          NPSCOL=0.0; NPSFL =0.0; RAINFL=0.0
          SEDFL =0.0; SEDOUL=0.0; SEEPSL=0.0
          STRMFL=0.0; STSCOL=0.0; WATFL =0.0; WATOUL=0.0


!***********************************************************
! Photolysis variables
Deallocate (KDPL,OXRADL,S1O2L)
Allocate (KDPL(7,KOUNT), OXRADL(KOUNT), S1O2L(KOUNT))
          KDPL=0.0; OXRADL=0.0; S1O2L=0.0
!***********************************************************
! Variables for DISTRB
Deallocate (KPDOCL,KOCL,KOWL,KPBL)
Allocate   (KPDOCL(7,KCHEM),KOCL(KCHEM),KOWL(KCHEM),KPBL(7,KCHEM))
            KPDOCL=0.0; KOCL=0.0; KOWL=0.0; KPBL=0.0
! end of variables for DISTRB
!***********************************************************
! end of Computational and output variables for contaminants
!***********************************************************
! Set miscellaneous variables to start a new run
ABEXIT = .false. ! ABEXIT is used to control CONTINUE
                 ! after an ABnormal EXIT from the integrator
FLUXCT=0.0
return
end Subroutine RUNIT
