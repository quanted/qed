Subroutine DRIVER(Y,RUNOPT)
! The "driver" routine for EXAMS' integration subroutines.
! The integration routines are described in
!  Malanchuk, J., J. Otis, and H. Bouver. 1980.
!  "Efficient algorithms for solving systems of ordinary
!   differential equations for ecosystem modeling."
!   EPA-600/3-80-037. NTIS, Springfield Va. 148 pp.
!
! Created August 1979 by L.A. Burns.
! Revised 28-NOV-1985 (LAB) to accomodate IBM file structures.
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 09/11/91 to process output files for the FGETS program
! ...further fgets revisions January 1992, October-November 1998
! Revisions 08-Feb-1999 - floating point comparisons
! Revisions April 2002 to add short-form and long-form output files
! Revisions April 2002 to allow user to enter a period for event maxima
!  (DayStack dimensioned 366 rather than 90)
! Revisions 2003-03-31 to report annual absolute maxima in ecorisk files
! Revisions 2004-04-12 to correct minor file management bug
use Implementation_Control
use Statistical_Variables
use Integrator_Working_Storage
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Floating_Point_Comparisons
Implicit None
real (kind (0D0)), dimension(KOUNT,KCHEM) :: Y
real :: LOGP(KCHEM)
! real (kind (0D0)), dimension(kount*kchem) :: y_pack
! local values for output only...
real :: OUTVAR(2)
integer :: RUNOPT, IOerr
integer :: I, K, Col_Count, Leap_days ! General counters
integer :: J, FieldCount
integer, parameter :: Integer_One=1, Integer_Zero=0
real, parameter :: Real_One=1.0E+00, Real_Zero=0.0E+00
character(len=6)  :: TUNITS
character(len=25) :: OUTCHR
logical :: OldFile ! to check for file clutter during run setup
! Check input accuracy requests
if (ABSERG .LessThan. amax1(sngl(FOURU),1.0e-15)) then
   ABSERG = amax1(sngl(FOURU),1.0e-15)
   write (stdout,fmt='(/,A)')&
      ' The requested absolute error tolerance is too'
   write (stdout,5010) ABSERG
   5010  format (' stringent for the precision of this computer.',&
      /' It has been increased to:',ES9.2,'.')
endif
if (RELERG .LessThan. amax1(sngl(FOURU),1.0e-11)) then
   RELERG = amax1(sngl(FOURU),1.0e-11)
   write (stdout,fmt='(/,A)')&
      ' The requested relative error tolerance is too'
   write (stdout,5010) RELERG
endif
ABSERR = dble(ABSERG)   ! Transfer integrator controls
RELERR = dble(RELERG)
corrupted_mode: if (MODEG < 1 .or. MODEG > 3) then ! Fail-safe check
   write (stdout,fmt='(A,I5,/,A)')&
      ' MODE has a value of ',MODEG,'. RUN aborted.'
   IFLAG=8; return
end if corrupted_mode
ISOO = 0  ! initialization of control flag ISOO
IBACK = 1 ! initialization of control flag IBACK
! IBACK reminds the DRIVMn routines which integration method was requested.
! Set number of equations to be integrated
KEQN = KCHEM*KOUNT
! Initialize plotting files when entering via RUN; set file to
! append additional data when entering via CONTINUE.
! Identify time trace written to LUN KINLUN
run_option: select case (RUNOPT)
case (0) run_option ! RUN command--RUNOPT=0
   PlotFiles: if (PLTFIL) then ! if plot files are requested....
      ! Plotting file for kinetic output
      call Assign_LUN (KINLUN)
      open (unit=KINLUN, status='REPLACE', access='SEQUENTIAL',&
         form='UNFORMATTED', position='REWIND', file='kinout.plt',&
         action='write',iostat=IOerr)
      if (IOerr /= 0) then ! problem with results file...
         call Messenger (1000,"kinout.plt")
         call Release_LUN (KINLUN)
         call KillFile(3); call KillFile(2)
         return
      end if
      write (KINLUN) KCHEM,MODEG,KOUNT,TCODEG,YEAR1G
      do K = 1, KCHEM
         write (KINLUN) CHEMNA(K)
      end do
      write (KINLUN) ECONAM
      write (KINLUN) (TYPEG(I),I=1,KOUNT)
   else
      call KillFile(3); call KillFile(2) ! User doesn't want tty plot files
   end if PlotFiles

   FGETS_Files: if (FGTFIL) then
   ! Exposure file for data transfer to Fgets
   call Assign_LUN (FG1LUN)
   open (unit=FG1LUN, status='REPLACE', access='SEQUENTIAL',&
         form='FORMATTED', position='REWIND',file='fgetsexp.xms',&
         action='write',iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "fgetsexp.xms")
      call Release_LUN (FG1LUN)
      call KillFile(4); call KillFile(5)
      return
   end if

   ! Program control file for Fgets
   call Assign_LUN (FG2LUN)
   open (unit=FG2LUN, status='REPLACE', access='SEQUENTIAL',&
         form='FORMATTED', position='REWIND', file='fgetscmd.xms',&
         action='write',iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "fgetscmd.xms")
      call Release_LUN (FG2LUN)
      call KillFile(4); call KillFile(5)
      return
   end if
   else ! User does not want FGETS transfer files; delete old versions 
      call KillFile(4); call KillFile(5)
   end if FGETS_Files

   ! Initialize program control area of BASS transfer file
   BASS_File: if (BASFIL) then
   call Assign_LUN (BASSLUN)
   open (unit=BASSLUN, status='REPLACE', access='SEQUENTIAL',&
         form='FORMATTED', position='REWIND', file='bassexp.xms',&
         action='write', iostat=IOerr)
   if (IOerr /= 0) then
      call Messenger (1000, "bassexp.xms")
      call Release_LUN (BASSLUN)
      call KillFIle(6) ! file problem; delete old version
      return
   end if
   else
   call KillFIle(6) ! User doesn't want BASS transfer file; delete old version
   end if BASS_File

   ! Initialize program control area of HWIR transfer file
   HWIR_File: if (HWRFIL) then
   call Assign_LUN (HWIRLUN)
   open (unit=HWIRLUN, status='REPLACE', access='SEQUENTIAL',&
         form='FORMATTED', position='REWIND', file='hwirexp.xms',&
         action='write', iostat=IOerr)
   if (IOerr /= 0) then
      call Messenger (1000, "hwirexp.xms")
      call Release_LUN (HWIRLUN)
      call KillFile(7) ! if HWIR transfer file problem, delete old version
      return
   end if
   else
   call KillFile(7) ! if no HWIR transfer file, delete old version
   end if HWIR_File

   ! Initialize program control area of compartment-oriented EcoToxC.xms file
   if (TOXFILC .and. MODEG==1) then
      TOXFILC = .false.
      OutFil(6) = 'N'
      write (stderr,fmt='(A)')&
      " Exams' EcoTox files cannot be written from Mode 1."
      call KillFile(8) ! delete any existing version of EcoToxC.xms
   end if

   EcoToxC_File: if (TOXFILC) then   
   call Assign_LUN (ToxCLUN)
   open (unit=ToxCLUN, status='REPLACE', access='SEQUENTIAL',&
         form='FORMATTED', position='REWIND', file='EcoToxC.xms',&
         action='write', iostat=IOerr)
   if (IOerr /= 0) then
      call Messenger (1000, "EcoToxC.xms")
      call Release_LUN (ToxCLUN)
      call KillFile(8) ! delete any existing version of EcoToxC.xms
      return
   end if
   else
   call KillFile(8) ! delete any existing version of EcoToxC.xms
   end if EcoToxC_File

   ! Initialize program control area of reach-oriented EcoToxR.xms file
   if (TOXFILR .and. MODEG==1) then
      TOXFILR = .false.
      OutFil(8) = 'N'
      write (stderr,fmt='(A)')&
      " Exams' EcoTox files cannot be written from Mode 1."
      call KillFile(10) ! delete any existing version of EcoToxR.xms
   end if

   EcoToxR_File: if (TOXFILR) then   
   call Assign_LUN (ToxRLUN)
   open (unit=ToxRLUN, status='REPLACE', access='SEQUENTIAL',&
         form='FORMATTED', position='REWIND', file='EcoToxR.xms',&
         action='write', iostat=IOerr)
   if (IOerr /= 0) then
      call Messenger (1000, "EcoToxR.xms")
      call Release_LUN (ToxRLUN)
      call KillFile(10) ! delete any existing version of EcoToxR.xms
      return
   end if
   else
   call KillFile(10) ! delete any existing version of EcoToxR.xms
   end if EcoToxR_File

   ! Initialize program control area of compartment EcoRiskC.xms file 
   if (RSKFILC .and. MODEG<3) then
      RSKFILC = .false.
      OutFil(7) = 'N'
      write (stderr,fmt='(A)')&
      " Exams' EcoRisk files cannot be written from Mode 1 or Mode 2."
      call KillFile(9)  ! delete old versions of EcoRiskC.xms
      call KillFile(13) ! and associated scratch file
   end if

   EcoRiskC_File: if (RSKFILC) then
      ! check for old version of scratchfile, delete it if necessary
      Inquire (File = 'CptRisk.tmp', Exist=OldFile)
      if (OldFile) call KillFile(13) ! to clear the way for a new scratch file
      call Assign_Lun (TmpLUN1)
      open (unit=TmpLUN1, file = 'CptRisk.tmp',&
         access='SEQUENTIAL', position='REWIND', form='FORMATTED')
      YearCount = 1 ! initialize counter of file entries
      call Assign_LUN (RSKCLUN)
      open (unit=RSKCLUN, status='REPLACE', access='SEQUENTIAL',&
         form='FORMATTED', position='REWIND', file='EcoRiskC.xms',&
         action='write', iostat=IOerr)

      if (IOerr /= 0) then
         call Messenger (1000, "EcoRiskC.xms")
         call Release_LUN (RSKCLUN)
         call KillFile(9)  ! delete old versions of EcoRiskC.xms
         call KillFile(13) ! delete old versions of CptRisk.tmp scratch file
         return
      end if
   else ! Compartment-oriented ecorisk file not requested for this Run, so
      call KillFile(9)  ! to delete old versions of EcoRiskC.xms
      call KillFile(13) ! to delete old versions of CptRisk.tmp scratch file
   end if EcoRiskC_File
   !
   ! Initialize program control area of reach-oriented EcoRiskR.xms file 
   if (RSKFILR .and. MODEG<3) then
      RSKFILR = .false.
      OutFil(9) = 'N'
      write (stderr,fmt='(A)')&
      " Exams' EcoRisk files cannot be written from Mode 1 or Mode 2."
      call KillFile(11) ! delete old versions of EcoRiskR.xms
      call KillFile(14) ! and associated scratch file
   end if

   EcoRiskR_File: if (RSKFILR) then
      ! check for old version of scratchfile, delete it if necessary
      Inquire (File = 'RchRisk.tmp', Exist=OldFile)
      if (OldFile) call KillFile(14) ! to clear the way for a new scratch file
      call Assign_Lun (TmpLUN2)
      open (unit=TmpLUN2, file = 'RchRisk.tmp',&
         access='SEQUENTIAL', position='REWIND', form='FORMATTED')
      YearCount = 1 ! initialize counter of file entries
      call Assign_LUN (RSKRLUN)
      open (unit=RSKRLUN, status='REPLACE', access='SEQUENTIAL',&
         form='FORMATTED', position='REWIND', file='EcoRiskR.xms',&
         action='write', iostat=IOerr)
      if (IOerr /= 0) then
         call Messenger (1000, "EcoRiskR.xms")
         call Release_LUN (RSKRLUN)
         call KillFile(11) ! delete old versions of EcoRiskR.xms
         call KillFile(14) ! and associated scratch file
         return
      end if
   else
      call KillFile(11) ! delete old versions of EcoRiskR.xms
      call KillFile(14) ! and associated scratch file
   end if EcoRiskR_File
   !
   ! Initialize program control area of full compartment output file 
   Full_File: if (FULFIL) then
   call Assign_LUN (FULLUN)
   open (unit=FULLUN, status='REPLACE', access='SEQUENTIAL',&
         form='FORMATTED', position='REWIND', file='FullOut.xms',&
         action='write', iostat=IOerr)
   if (IOerr /= 0) then
      call Messenger (1000, "FullOut.xms")
      call Release_LUN (FULLUN)
      call KillFile(12) ! delete old versions of FullOut.xms
      return
   end if
   else
   call KillFile(12) ! delete old versions of FullOut.xms
   end if Full_File
   !
   !
   ! All files now open; commence writing file headers and metadata
   ! Set up documentation of time frame
      ! The fgets/bass command sequences contain information needed to
      ! set up a run that matches the analysis done in Exams...
      ! The EcoTox files written in Mode 2 begin each record with elapsed time
      ! The EcoTox files written in Mode 3 begin each record with the date
      ! Determine value of time units (known as tunits in fgets & hwir)
      mode_select: select case (MODEG)
      case (1) mode_select  ! fgets authors want the following
         tunits='years'     ! for steady-state analysis
         OUTVAR(1)=0.0
         OUTVAR(2)=1.0
         OUTCHR='steady_state'
      case (2) mode_select
         OUTVAR(1)=TINITG
         OUTVAR(2)=TENDG
         OUTCHR='segmented_initial_value'
         mode_2_time: select case (TCODEG)
            case (1); tunits='hours'
            case (2); tunits='days'
            case (3); tunits='months'
            case (4); tunits='years'
            case default; tunits='error'
         end select mode_2_time
      case (3) mode_select
         OUTCHR='seasonal_dynamics' ! in mode 3, reports are in days
         OUTVAR(1)=TINITG
         OUTVAR(2)=real(NYEARG)*365. ! this statement neglects leap years
         ! add in leap days
         Leap_days = 0
         do I = YEAR1G, (Year1G+NYEARG-1)
            if (mod(I,4) == 0 .and. mod(I,100) /= 0 &
              .or. mod(I,400) == 0) Leap_days = Leap_days + 1
         end do
         OUTVAR(2) = OUTVAR(2)+real(Leap_days)
         tunits='days'
      case default mode_select
         OUTVAR(1)=0
         OUTVAR(2)=0
         tunits='error'
         OUTCHR='error_in_mode'
      end select mode_select
   ! Time frame doumentation now in place

   !
   ! write program control comments and headers in Fgets comment format
   FGETS_Files2: if (FGTFIL) then
   write (FG1LUN,fmt='(6(A/),A,A)')&
      '! File FGETSEXP.XMS for exams to fgets exposure data transfer',&
      '! Data fields are time in "tunits", temperature in degrees C,',&
      '! plankton standing stock in units of mg(fw)/L ,',&
      '! aqueous concentrations of N chemicals in units of mg/L,',&
      '! N toxicant concentrations in benthos in units of mg/kg (fw),',&
      '! N toxicant concentrations in plankton in units of mg/kg (fw).',&
      '! Concentrations are (volume-weighted) average across',&
         &' the entire ecosystem.'
   ! compute logP if possible...
   do I=1,KCHEM
      if (KOWG(I) .GreaterThan. 0.0) then
         LOGP(I) = alog10(KOWG(I))
      elseif (KOCG(I) .GreaterThan. 0.0) then
         LOGP(I) = alog10(KOCG(I)/0.41)
      else
         LOGP(I) = -999.
      endif
   end do
   write (FG2LUN,5040) trim(ECONAM), TUNITS,&
   & OUTVAR(1), OUTVAR(2), KCHEM, MODEG, OUTCHR
   5040  format(&
   &'/title "',A,'" ',/&
   &'/tunits ',A6/&
   &'/tstart', 1PE12.5,/&
   &'/tend'  , E12.5,/&
   &'/cwunits mg/L'/&
   &'/cfunits mg/L'/&
   &'/chemicals ',I3/&
   &'/exams_mode ',I3,' ! ',A25)
   do K=1,KCHEM
      if (K == 1) then
         if (KCHEM == 1) then
            write (FG2LUN,5042) trim(CHEMNA(K))
         else
            write (FG2LUN,5043) trim(CHEMNA(K))
         endif
      elseif (K < KCHEM) then
         write (FG2LUN,5044) trim(CHEMNA(K))
      else
         write (FG2LUN,5045) trim(CHEMNA(K))
      endif
   end do
   5042  format('/toxlab "',A,'"')
   5043  format('/toxlab "',A,'" &')
   5044  format('        "',A,'" &')
   5045  format('        "',A,'"')
   write (FG2LUN,5046) (MWTG(I),I=1,KCHEM)
   5046  format('/molwt', 500(1X,e12.5))
   write (FG2LUN,5047) (LOGP(I),I=1,KCHEM)
   5047  format('/logp ', 500(1x,e12.5))
   do  K = 1, KCHEM
    write (FG1LUN,5048) K, trim(CHEMNA(K))
   end do
   write (FG1LUN,5049) trim(ECONAM)
   5048  format('! Chemical No.',I2,': ',A)
   5049  format('! Ecosystem:      ',A,/'!')
   end if FGETS_Files2

   ! Write the header for the HWIR transfer file
   HWIR_File2: if (HWRFIL) then
   write (HWIRLUN,fmt='(A,I2/A/A)') &
      '! HWIR transfer file written from Exams in Mode ',MODEG,&
      '! Ecosystem: '//trim(ECONAM),&
      '/001 time['//trim(tunits)//']'

   Col_Count=2
   Reaches:   do I = 1, Reaches_in_System
      write (HWIRLUN,fmt='(1(A,I3.3,A,I3.3,A/),A,I3.3,A,I3.3,A)')&
      ! Total suspended solids in the water column.
      '/',Col_Count,' TSSwater (rch',I,')',&
      ! Organic carbon content of benthic sediments
      '/',Col_Count+1,' focbenth (rch',I,')'
      Col_Count = Col_Count + 2
   end do Reaches

   Chemicals: do K = 1, KCHEM
      Reaches_Again:   do I = 1, Reaches_in_System
      write (HWIRLUN,fmt='(3(A,I3.3,A,I3.3,A/),A,I3.3,A,I3.3,A)')&
      ! Total concentration in water column
      '/',Col_Count,' Cwtot[mg/L]('//trim(CHEMNA(K))//'_rch',I,')',&
      ! Total dissolved concentration in water column
      '/',Col_Count+1,' Cwater[mg/L]('//trim(CHEMNA(K))//'_rch',I,')',&
      ! Total concentration in benthic zone in mg/kg dry weight
      '/',Col_Count+2,' Cbtot[mg/kg]('//trim(CHEMNA(K))//'_rch',I,')',&
      ! Total dissolved concentration in benthic zone pore water
      '/',Col_Count+3,' Cbdiss[mg/L]('//trim(CHEMNA(K))//'_rch',I,')'
      Col_Count = Col_Count + 4
      end do Reaches_Again
   end do Chemicals

   write (HWIRLUN,fmt='(A)')&
      '/START_DATA'
   ! End of header data for the HWIR transfer file
   end if HWIR_File2

 
   ! Write the header for the BASS transfer file
   BASS_File2: if (BASFIL) then
   write (BASSLUN,fmt='(A,I2/8(A/),A)') &
      '! BASS transfer file written from Exams in Mode',MODEG,&
      '! Ecosystem: '//trim(ECONAM),&
      '/001 time['//trim(tunits)//']',& ! time is the Exams units
      '/002 temperature[Celsius]',&     ! Temperature in Celsius
      '/003 depth[m]',&                 ! Mean water depth
      '/004 phytoplankton[mg/L]',&      ! dry weight
      '/005 zooplankton[mg/L]',&        ! dry weight
      '/006 periphyton[mg/m^2]',&       ! dry weight
      '/007 benthos[mg/m^2]',&          ! dry weight
      '/008 insects[mg/m^2]'            ! dry weight
   Col_Count = 9 ! Counter to increment the column number
   do K = 1, KCHEM
   write (BASSLUN,fmt='(5(A,I3.3,A/),A,I3.3,A)')&
   ! Total dissolved concentration in water column
      '/',Col_Count,' cwater[mg/L]('//trim(CHEMNA(K))//')',&
   ! Concentration in benthos as mg/kg dry weight
      '/',Col_Count+1,' cbnths[mg/kg]('//trim(CHEMNA(K))//')',&
   ! Concentration in insects as mg/kg dry weight
      '/',Col_Count+2,' cinsct[mg/kg]('//trim(CHEMNA(K))//')',&
   ! Concentration in periphyton as mg/kg dry weight
      '/',Col_Count+3,' cphytn[mg/kg]('//trim(CHEMNA(K))//')',&
   ! Concentration in phytoplankton as mg/kg dry weight
      '/',Col_Count+4,' cpplnk[mg/kg]('//trim(CHEMNA(K))//')',&
   ! Concentration in zooplankton as mg/kg dry weight
      '/',Col_Count+5,' czplnk[mg/kg]('//trim(CHEMNA(K))//')'
   Col_Count = Col_Count+6
   end do
   write (BASSLUN,fmt='(A)')&
      '/START_DATA'
   ! End of header data for the BASS transfer file
   end if BASS_File2
!*****************************************************************************
!*****************************************************************************
   EcoTox_File2a: if (TOXFILC) then
   ! Start of header and metadata for the compartment-oriented
   ! EcoTox Exposure Output File EcoToxC.xms
   write (ToxCLUN,fmt='(A)') &
      '! EcoTox Compartment Exposure File from Exams version '&
      &//VERSN//' dated '//Maintenance_Date//'.'
   write (ToxCLUN,fmt='(A)') '! File "EcoToxC.xms" created on '//Rundate&
      &//' at '//RunTime//' hours.'
   write (TOXCLUN, fmt='(A,I0)') '! Number of chemicals: ',KCHEM
   do I=1,KCHEM
      write (ToxCLUN, fmt='(A,I0,A)') '! Chemical ',I, ': '//trim(CHEMNA(I))
   end do
   write (ToxCLUN, fmt='(A)') '! Environment: '//trim(ECONAM)
   call CPTSHOW(ToxCLUN)
   ! If working with PRZM meteorology file
   if (PRZM_Met_File) call WeatherHeader(ToxCLUN)
   write (ToxCLUN, fmt='(A)') '!'
   if (MODEG==2) then
      write (ToxCLUN, fmt='(A)') '! File Format: (fields are blank-delimited)'
      write (ToxCLUN, fmt='(A)') '! Field 1: Time in '//trim(tunits)
   elseif (MODEG==3) then
      write (ToxCLUN, fmt='(A)')  '! File Format:'
      write (ToxCLUN, fmt='(A)') '! Field 1: ISO 8601 Date'
   else
      write (stderr, fmt='(A)') ' System failure D0001. Notify author.'
      IFLAG=8
      return
   end if
   FieldCount=2

  do K=1,KCHEM
    write (ToxCLUN, fmt='(A,I0,A/A,I0,A)')&
     '! Field ', FieldCount,& ! In Outp: Z(1,K)
     ': Volume-weighted average concentration [mg/L] of',&
     '!           dissolved chemical (',K,') in the limnetic zone',&
     '! Field ', FieldCount+1,& ! In Outp: Z(3,K)
     ': Volume-weighted average concentration [mg/L] of',&
     '!           dissolved chemical (',K,') in the benthic zone'
     FieldCount=FieldCount+2
     do J=1,KOUNT
        if (TYPEG(J)/='B') then
           write (ToxCLUN, fmt='(A,I0,A,I0/A,I0)') &
             '! Field ',FieldCount,': dissolved concentration'//&
            &' [mg/L] of chemical ',K,&
            &'!           in limnetic compartment ',J,&
            &'! Field ',FieldCount+1,': biomass concentration'//&
            &' [ug/g dry weight] of chemical ',K,&
            &'!           in plankton of limnetic compartment ',J
        else
           write (ToxCLUN, fmt='(A,I0,A,I0/A,I0)') &
             '! Field ',FieldCount,': dissolved concentration'//&
             &' [mg/L] of chemical ',K,&
             &'!           in pore water of benthic compartment ',J,&
             &'! Field ',FieldCount+1,': biomass concentration'//&
             &' [ug/g dry weight] of chemical ',K,&
             &'!           in benthos of compartment ',J
         end if
         FieldCount=FieldCount+2
     end do
   end do
   ! Document external loadings in the EcoTox file
!  do K=1,KCHEM ! daily (Mode 3) or other time-step system-level loadings
!   write (ToxCLUN, fmt='(A,I0,A,I0,A)')&
!  '! Field ',FieldCount,&
!      ': Chemical (',K,') Surface Water Runoff Loading to Limnetic Zone',&
!  '! Field ',FieldCount+1,&
!      ': Chemical (',K,') Surface Water Runoff Loading to Benthic Zone',&
!  '! Field ',FieldCount+2,&
!      ': Chemical (',K,') Groundwater Loading', &
!  '! Field ',FieldCount+3,&
!      ': Chemical (',K,') Drift Loading'
!   FieldCount=FieldCount+4
!  end do

! If working with PRZM transfer file and meteorology files
!if (PRZM_Met_File) then
!   write (ToxCLUN, fmt='(A,I0,A)')& ! if meteorology file has been read
!  '! Field ',FieldCount,  ': Rainfall (mm)'
!    FieldCount=FieldCount+1
!end if
!if (PRZM_Transfer_File) then
!   write (ToxCLUN, fmt='(A,I0,A)')&  ! if przm transfer file has been read
!  '! Field ',FieldCount,&
!      ': Surface Water Runoff Volume (cubic meters)', &
!  '! Field ',FieldCount+1,&
!      ': Runoff Sediment Load (kilograms)', &
!  '! Field ',FieldCount+2,&
!      ': Groundwater Flow Volume (cubic meters)'
!   FieldCount=FieldCount+3
!end if

   end if EcoTox_File2a
   ! End of header and metadata for the compartment-oriented EcoTox file
! ****************************************************************************
   EcoTox_File2b: if (TOXFILR) then
   ! Start of header and metadata for the reach-oriented EcoTox Output File
   ! EcoTox Exposure Output File
   write (ToxRLUN,fmt='(A)') &
      '! EcoTox Reach Exposure File from Exams version '&
      &//VERSN//' dated '//Maintenance_Date//'.'
   write (ToxRLUN,fmt='(A)') '! File "EcoToxR.xms" created on '//Rundate&
      &//' at '//RunTime//' hours.'
   do i=1,kchem
      write (ToxRLUN, fmt='(A,I0,A)') '! Chemical ',I, ': '//trim(CHEMNA(I))
   end do
   write (ToxRLUN, fmt='(A)') '! Environment: '//trim(ECONAM)
   call CPTSHOW(ToxRLUN)
!   write (ToxRLUN, fmt='(A)') '! Reach Structure:'
!   write (ToxRLUN, fmt='(A)') '! Under Construction'
   ! If working with PRZM meteorology file
   if (PRZM_Met_File) call WeatherHeader(ToxRLUN)
   write (ToxRLUN, fmt='(A)') '!'
   if (MODEG==2) then
      write (ToxRLUN, fmt='(A)') '! File Format: (blank-delimited fields)'
      write (ToxRLUN, fmt='(A)') '! Field 1:     Time in '//trim(tunits)
   elseif (MODEG==3) then
      write (ToxRLUN, fmt='(A)') '! File Format:'
      write (ToxRLUN, fmt='(A)') '! Field 1:     ISO 8601 Date'
   else
      write (stderr, fmt='(A)') ' System failure D0001. Notify author.'
      IFLAG=8
      return
   end if
   FieldCount=2

!   write (ToxRLUN, fmt='(A,I0,A/A)') &
!   '! Fields ',FieldCount,' et seq. are dissolved exposure concentrations ',&
!      &'!   for each reach of the environment.'
   do K=1,KCHEM
   do J=1,Reaches_in_System
   write (ToxRLUN, fmt='(A,I0,A,I0/A,I0,A)') &
     '! Field ',FieldCount,': dissolved concentration'//&
     &' [mg/L] of chemical ',K,&
     '!           in limnetic zone of reach ',J,'.'

   write (ToxRLUN, fmt='(A,I0,A,I0/A,I0,A)') &
     '! Field ',FieldCount+1,': dissolved concentration'//&
     &' [mg/L] of chemical ',K,&
     '!           benthos exposure to pore water of sediments of reach ',&
     J,'.'

   write (ToxRLUN, fmt='(A,I0,A,I0/A,I0,A)') &
     '! Field ',FieldCount,': plankton contamination'//&
     &' [ug/g dry weight] of chemical ',K,&
     '!           in limnetic zone of reach ',J,'.'

   write (ToxRLUN, fmt='(A,I0,A,I0/A,I0,A)') &
     '! Field ',FieldCount+1,': benthos contamination'//&
     &' [ug/g dry weight] of chemical ',K,&
     '!           in sediments of reach ',&
     J,'.'

   FieldCount=FieldCount+4
   end do; end do

   ! Document external loadings
!  do K=1,KCHEM ! daily (Mode 3) or other time-step system-level loadings
!   write (ToxRLUN, fmt='(A,I0,A,I0,A)')&
!  '! Field ',FieldCount,&
!      ':     Chemical (',K,') Surface Water Runoff Loading to Limnetic Zone',&
!  '! Field ',FieldCount+1,&
!      ':     Chemical (',K,') Surface Water Runoff Loading to Benthic Zone',&
!  '! Field ',FieldCount+2&
!      ,':     Chemical (',K,') Groundwater Loading', &
!  '! Field ',FieldCount+3,&
!      ':     Chemical (',K,') Drift Loading'
!   FieldCount=FieldCount+4
!  end do
! If working with PRZM transfer file and meteorology files
!if (PRZM_Met_File) then
!   write (ToxRLUN, fmt='(A,I0,A)')& ! if meteorology file has been read
!  '! Field ',FieldCount,  ':     Rainfall (mm)'
!    FieldCount=FieldCount+1
!end if
!if (PRZM_Transfer_File) then
!   write (ToxRLUN, fmt='(A,I0,A)')&  ! if przm transfer file has been read
!  '! Field ',FieldCount,&
!      ':     Surface Water Runoff Volume (cubic meters)', &
!  '! Field ',FieldCount+1,&
!      ':     Runoff Sediment Load (kilograms)', &
!  '! Field ',FieldCount+2,&
!      ':     Groundwater Flow Volume (cubic meters)'
!   FieldCount=FieldCount+3
!end if

   end if EcoTox_File2b
   ! End of header and metadata for the reach-oriented EcoTox file
!****************************************************************************
   ! Start of header and metadata for the compartment-oriented
   ! EcoRisk Output File
   EcoRisk_File2a: if (RSKFILC) then
   write (RSKCLUN,fmt='(A/A)') &
       '! Compartment-oriented Ecological Risk Assessment Output File',&
      &'! Created by Exams version '//VERSN//' dated '//Maintenance_Date//'.'
   write (RSKCLUN,fmt='(A)') '! File "EcoRiskC.xms" created on '//Rundate&
      &//' at '//RunTime//' hours.'
   write (RSKCLUN,fmt='(A,I6)') '! Number of Event Durations: ', 6+NumEvents
   write (RSKCLUN,fmt='(A,11(I4))') '! Event Durations (days): ',&
      (SysEventDur(I),I=1,6), (EventDL(J),J=NumEvents,1,-1)
   write (RSKCLUN,fmt='(A,I6)') '! Number of Chemicals: ', KCHEM
   do i=1,kchem
      write (RSKCLUN, fmt='(A,I0,A)') '! Chemical ',I, ': '//trim(CHEMNA(I))
   end do
   write (RSKCLUN, fmt='(A)') '! Environment: '//trim(ECONAM)
   call CPTSHOW(RSKCLUN)
   ! If working with PRZM meteorology file
   if (PRZM_Met_File) call WeatherHeader(RSKCLUN)
   write (RSKCLUN, fmt='(A)') '! File Format:'
   ! Weibull plotting position is the first field in the data stream.
   ! F(x) = m/(n+1) is the Weibull plotting position formula. It is widely
   ! used for exceedence probability p, but there are alternatives. These
   ! include Gringorton (p=[m-0.44]/[n+0.12]) and Cunnane (p=[m-0.4/[n+0.2]).
   ! Exceedence probability is calculated after the observed data are sorted
   ! from largest to smallest values so that the largest value is associated
   ! with m=1.
   ! The "recurrence interval" or return period "T" is the inverse of the
   ! exceedence probability: T = 1/p = (n+1)/m.
   ! Conceivably analysis of the annual maximum series might make use of
   ! Gumbel's extreme-value frequency distribution.
   write (RSKCLUN,fmt='(A,A/A)') '! Field 1: Weibull Plotting Position ',&
      &'(100 m/(n+1))','!'
   FieldCount=2
   do K=1,KCHEM
   write (RSKCLUN, fmt='(A,I0,A,I0,A)') &
     '! Field ',FieldCount,': Peak dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in limnetic zone'
   write (RSKCLUN, fmt='(A,I0,A,I0)') '! Field ',FieldCount+1,&
     &':    Date of occurrence of event in Field ',FieldCount
   write (RSKCLUN, fmt='(A,I0,A,I0,A)') &
     '! Field ',FieldCount+2,': Peak dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in benthic zone'
   write (RSKCLUN, fmt='(A,I0,A,I0/A)') '! Field ',FieldCount+3,&
     &':    Date of occurrence of event in Field ',FieldCount+2,'!'
   FieldCount = FieldCount+4
   do I=1,size(SysEventDur) ! document fields for system events
   write (RSKCLUN, fmt='(A,I0,A,I0,A,I0,A)') &
     '! Field ',FieldCount,': ',SysEventDur(I),'-day mean dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in limnetic zone'
   write (RSKCLUN, fmt='(A,I0,A,I0)') '! Field ',FieldCount+1,&
     &':    Date of occurrence of event in Field ',FieldCount
   write (RSKCLUN, fmt='(A,I0,A,I0,A,I0,A)') &
     '! Field ',FieldCount+2,': ',SysEventDur(I),'-day mean dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in benthic zone'
   write (RSKCLUN, fmt='(A,I0,A,I0/A)') '! Field ',FieldCount+3,&
     &':    Date of occurrence of event in Field ',FieldCount+2,'!'
   FieldCount=FieldCount+4
   end do

   do I=NumEvents,1,-1 ! document fields for user-specified events
   write (RSKCLUN, fmt='(A,I0,A,I0,A,I0,A)') &
     '! Field ',FieldCount,': ',EventDL(I),'-day mean dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in limnetic zone'
   write (RSKCLUN, fmt='(A,I0,A,I0)') '! Field ',FieldCount+1,&
     &':    Date of occurrence of event in Field ',FieldCount
   write (RSKCLUN, fmt='(A,I0,A,I0,A,I0,A)') &
     '! Field ',FieldCount+2,': ',EventDL(I),'-day mean dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in benthic zone'
   write (RSKCLUN, fmt='(A,I0,A,I0/A)') '! Field ',FieldCount+3,&
     &':    Date of occurrence of event in Field ',FieldCount+2,'!'
   FieldCount=FieldCount+4
   end do
   end do
   end if EcoRisk_File2a
   ! End of header and metadata for the compartment-oriented EcoRisk file

!****************************************************************************
   ! Start of header and metadata for the reach-oriented EcoRisk Output File
   ! This file is not materially different from the compartment-oriented
   !   file, because the compartment maximum happens at some point in a reach
   EcoRisk_File2b: if (RSKFILR) then
   write (RSKRLUN,fmt='(A/A)') &
       '! Reach-oriented Ecological Risk Assessment Output File',&
      &'! Created by Exams version '//VERSN//' dated '//Maintenance_Date//'.'
   write (RSKRLUN,fmt='(A)') '! File "EcoRiskR.xms" created on '//Rundate&
      &//' at '//RunTime//' hours.'
   write (RSKRLUN,fmt='(A,I6)') '! Number of Event Durations: ', 6+NumEvents
   write (RSKRLUN,fmt='(A,11(I4))') '! Event Durations (days): ',&
      (SysEventDur(I),I=1,6), (EventDL(J),J=NumEvents,1,-1)
   write (RSKRLUN,fmt='(A,I6)') '! Number of Chemicals: ', KCHEM
   do i=1,kchem
      write (RSKRLUN, fmt='(A,I0,A)') '! Chemical ',I, ': '//trim(CHEMNA(I))
   end do
   write (RSKRLUN, fmt='(A)') '! Environment: '//trim(ECONAM)
   ! If working with PRZM meteorology file
   if (PRZM_Met_File) call WeatherHeader(RSKRLUN)
   write (RSKRLUN, fmt='(A/A)') '!','! File Format:'
   ! Weibull plotting position is the first field in the data stream.
   ! F(x) = m/(n+1) is the Weibull plotting position formula. It is widely
   ! used for exceedence probability p, but there are alternatives. These
   ! include Gringorton (p=[m-0.44]/[n+0.12]) and Cunnane (p=[m-0.4/[n+0.2]).
   ! Exceedence probability is calculated after the observed data are sorted
   ! from largest to smallest values so that the largest value is associated
   ! with m=1.
   ! The "recurrence interval" or return period "T" is the inverse of the
   ! exceedence probability: T = 1/p = (n+1)/m.
   ! Conceivably analysis of the annual maximum series might make use of
   ! Gumbel's extreme-value frequency distribution.
   write (RSKRLUN,fmt='(A,A/A)') '! Field 1: Weibull Plotting Position ',&
      &'(100 m/(n+1))','!'
   FieldCount=2
   do K=1,KCHEM
   write (RSKRLUN, fmt='(A,I0,A,I0,A)') &
     '! Field ',FieldCount,': Peak dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in limnetic zone'
   write (RSKRLUN, fmt='(A,I0,A,I0)') '! Field ',FieldCount+1,&
     &':    Date of occurrence of event in Field ',FieldCount
   write (RSKRLUN, fmt='(A,I0,A,I0,A)') &
     '! Field ',FieldCount+2,': Peak dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in benthic zone'
   write (RSKRLUN, fmt='(A,I0,A,I0/A)') '! Field ',FieldCount+3,&
     &':    Date of occurrence of event in Field ',FieldCount+2,'!'
   FieldCount = FieldCount+4
   do I=1,size(SysEventDur) ! document fields for system events
   write (RSKRLUN, fmt='(A,I0,A,I0,A,I0,A)') &
     '! Field ',FieldCount,': ',SysEventDur(I),'-day mean dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in limnetic zone'
   write (RSKRLUN, fmt='(A,I0,A,I0)') '! Field ',FieldCount+1,&
     &':    Date of occurrence of event in Field ',FieldCount
   write (RSKRLUN, fmt='(A,I0,A,I0,A,I0,A)') &
     '! Field ',FieldCount+2,': ',SysEventDur(I),'-day mean dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in benthic zone'
   write (RSKRLUN, fmt='(A,I0,A,I0/A)') '! Field ',FieldCount+3,&
     &':    Date of occurrence of event in Field ',FieldCount+2,'!'
   FieldCount=FieldCount+4
   end do
   do I=NumEvents,1,-1 ! document fields for user-specified events
   write (RSKRLUN, fmt='(A,I0,A,I0,A,I0,A)') &
     '! Field ',FieldCount,': ',EventDL(I),'-day mean dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in limnetic zone'
   write (RSKRLUN, fmt='(A,I0,A,I0)') '! Field ',FieldCount+1,&
     &':    Date of occurrence of event in Field ',FieldCount
   write (RSKRLUN, fmt='(A,I0,A,I0,A,I0,A)') &
     '! Field ',FieldCount+2,': ',EventDL(I),'-day mean dissolved conc.'//&
     &' [mg/L] of chemical ',K,' in benthic zone'
   write (RSKRLUN, fmt='(A,I0,A,I0/A)') '! Field ',FieldCount+3,&
     &':    Date of occurrence of event in Field ',FieldCount+2,'!'
   FieldCount=FieldCount+4
   end do
   end do
   end if EcoRisk_File2b
   ! End of header and metadata for the reach-oriented EcoRisk file
! ****************************************************************************
   if (FULFIL) then
   ! Start of header and metadata for the compartment-oriented
   ! Exams Concentrations Output File
   write (FULLUN,fmt='(A)') &
      '! Compartment Concentration File from Exams version '&
      &//VERSN//' dated '//Maintenance_Date//'.'
   write (FULLUN, fmt='(A)') '! File "FullOut.xms" created on '//Rundate&
      &//' at '//RunTime//' hours.'
   write (FULLUN, fmt='(A,I0)') '! Number of chemicals: ',KCHEM
   do i=1,kchem
      write (FULLUN, fmt='(A,I0,A)') '! Chemical ',I, ': '//trim(CHEMNA(I))
   end do
   write (FULLUN, fmt='(A)') '! Environment: '//trim(ECONAM)
   call CPTSHOW(FULLUN)
   ! If working with PRZM meteorology file
   if (PRZM_Met_File) call WeatherHeader(FULLUN)
   write (FULLUN, fmt='(A)') '!'
   if (MODEG==2) then
      write (FULLUN, fmt='(A)') '! File Format: (fields are blank-delimited)'
      write (FULLUN, fmt='(A)') '! Field 1: Time in '//trim(tunits)
   elseif (MODEG==3) then
      write (FULLUN, fmt='(A)') '! File Format:'
      write (FULLUN, fmt='(A)') '! Field 1: ISO 8601 Date'
   else
      write (stderr, fmt='(A)') ' System failure D0003. Notify author.'
      IFLAG=8
      return
   end if
   FieldCount=2

  do K=1,KCHEM
     write (FULLUN, fmt='(A,I0,A/A,I0,A)')&
     ! In Outp: Z(1,K)
     '! Field ', FieldCount,&
     ': Volume-weighted average concentration [mg/L] of',&
     '!           dissolved chemical (',K,') in the limnetic zone',&
     ! In Outp: Z(2,K)
     '! Field ', FieldCount+1,&
     ': Volume-weighted average concentration [mg/kg] of',&
     '!           sorbed chemical (',K,') in the limnetic zone',&
     ! In Outp: Z(3,K)
     '! Field ', FieldCount+2,&
     ': Volume-weighted average concentration [mg/L] of',&
     '!           dissolved chemical (',K,') in the benthic zone',&
     ! In Outp: Z(4,K)
     '! Field ', FieldCount+3,&
     ': Volume-weighted average concentration [mg/kg] of',&
     '!           sorbed chemical (',K,') in the benthic zone'
     write (FULLUN, fmt='(A,I0,A,A,I0,A)')&
     ! In Outp: Z(5,K)
     '! Field ', FieldCount+4,': Total mass [kg] of',&
      ' chemical (',K,') in the limnetic zone',&
     ! In Outp: Z(6,K)
     '! Field ', FieldCount+5,': Total mass [kg] of',&
      ' chemical (',K,') in the benthic zone'

     FieldCount=FieldCount+6

      do J=1,KOUNT
         if (TYPEG(J)/='B') then
            write (FULLUN, fmt='(A,I0,A/A,I0,A,I0)') &
            '! Field ',FieldCount,': total concentration [mg/L]',&
            '!            of chemical ',K,' in (limnetic) compartment ',J
         else ! benthic compartment
            write (FULLUN, fmt='(A,I0,A/A,I0,A,I0)') &
            '! Field ',FieldCount,': total concentration [mg/kg]',&
            '!            of chemical ',K,' in (benthic) compartment ',J
         end if
         write (FULLUN, fmt='(A,I0,A,A,I0,A,I0)') &
         '! Field ',FieldCount+1,': dissolved concentration [mg/L]',&
          ' of chemical ',K,' in compartment ',J,&
         '! Field ',FieldCount+2,': sorbed concentration [mg/kg]',&
          ' of chemical ',K,' in compartment ',J,&
         '! Field ',FieldCount+3,': biomass concentration [ug/g]',&
          ' of chemical ',K,' in compartment ',J,&
         '! Field ',FieldCount+4,': chemical mass [grams/square meter]',&
          ' of chemical ',K,' in compartment ',J,&
         '! Field ',FieldCount+5,': complexed concentration [mg/L]',&
          ' of chemical ',K,' in compartment ',J

         FieldCount=FieldCount+6
      
      end do
    end do
!  Document external loadings within output file
!  do K=1,KCHEM ! daily (Mode 3) or other time-step system-level loadings
!   write (FULLUN, fmt='(A,I0,A,I0,A)')&
!  '! Field ',FieldCount,&
!      ': Chemical (',K,') Surface Water Runoff Loading to Limnetic Zone',&
!  '! Field ',FieldCount+1,&
!      ': Chemical (',K,') Surface Water Runoff Loading to Benthic Zone',&
!  '! Field ',FieldCount+2&
!      ,': Chemical (',K,') Groundwater Loading', &
!  '! Field ',FieldCount+3,&
!      ': Chemical (',K,') Drift Loading'
!   FieldCount=FieldCount+4
!  end do

    write (FULLUN, fmt='(A)') '!' ! Blank line to start output sequence
   end if
   ! End of header and metadata for the compartment-oriented full data
   !    output file
! ****************************************************************************
! ****************************************************************************
   ! In mode 1 (steady-state), write the steady-state concentrations
   ! into the exposure files now, as they are present as the I.C. for the
   ! simulation that develops the final persistence estimate.
   ! If none of the files are requested, ex2fgt will return without taking
   !   any action
   Mode_1_Only:  If (MODEG==1 .and. (FGTFIL .or. BASFIL .or. HWRFIL)) then
      call ex2fgt (Y,Integer_One,Real_Zero,Integer_Zero,'Stdy-State')
      call ex2fgt (Y,Integer_One,Real_One,Integer_Zero,'Stdy-State')
   endif Mode_1_Only

case (1) run_option  ! if entry is via continue command (RUNOPT=1)
                     ! set files to append more data

   PlotFiles2: if (PLTFIL) then
   call Assign_LUN (KINLUN)
   open (unit=KINLUN, status='old', access='sequential',&
      position='append', form='unformatted', file='kinout.plt',&
      action='readwrite', iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "kinout.plt")
      call Release_LUN (KINLUN)
      return
   end if; end if PlotFiles2

   FGETS_Files3: if (FGTFIL) then
   call Assign_LUN (FG1LUN)
   open (unit=FG1LUN,status='old',access='sequential',&
         position='append',form='formatted', file='fgetsexp.xms',&
         action='readwrite', iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "fgetsexp.xms")
      call Release_LUN (FG1LUN)
      return
   end if

   call Assign_LUN (FG2LUN)
   open (unit=FG2LUN,status='old',access='sequential',&
         position='append',form='formatted', file='fgetscmd.xms',&
         action='readwrite',iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "fgetscmd.xms")
      call Release_LUN (FG2LUN)
      return
   end if
    if (MODEG == 2) then  ! mark the new ending
      OUTVAR(2) = TENDG   ! time in the file
    else
      OUTVAR(2) = real(LASTYR-YEAR1G+NYEARG+1)*365.
      ! add in leap days
      Leap_days = 0
      do I = YEAR1G, (LASTYR+NYEARG)
         if (mod(I,4) == 0 .and. mod(I,100) /= 0 &
         .or. mod(I,400) == 0) Leap_days = Leap_days + 1
      end do
      OUTVAR(2) = OUTVAR(2)+real(Leap_days)
    endif
   write (FG2LUN,fmt='(A,1PE12.5)') '/tend ', OUTVAR(2)
   end if FGETS_Files3

   BASS_File3: if (BASFIL) then
   call Assign_LUN (BASSLUN)
   open (unit=BASSLUN,status='old',access='sequential',&
         position='append',form='formatted', file='bassexp.xms',&
         action='readwrite', iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "bassexp.xms")
      call Release_LUN (BASSLUN)
      return
   end if
   end if BASS_File3

   HWIR_File3: if (HWRFIL) then
   call Assign_LUN (HWIRLUN)
   open (unit=HWIRLUN, status='old', access='sequential',&
         position='append',form='formatted', file='hwirexp.xms',&
         action='readwrite', iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "hwirexp.xms")
      call Release_LUN (HWIRLUN)
      return
   end if
   end if HWIR_File3

   EcoTox_File3a: if (TOXFILC) then
   call Assign_LUN (TOXCLUN)
   open (unit=TOXCLUN, status='old', access='sequential',&
         position='append',form='formatted', file='EcoToxC.xms',&
         action='readwrite', iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "EcoToxC.xms")
      call Release_LUN (TOXCLUN)
      call KillFile(8)
      return
   end if
   end if EcoTox_File3a

   EcoTox_File3b: if (TOXFILR) then
   call Assign_LUN (TOXRLUN)
   open (unit=TOXRLUN, status='old', access='sequential',&
         position='append',form='formatted', file='EcoToxR.xms',&
         action='readwrite', iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "EcoToxR.xms")
      call Release_LUN (TOXRLUN)
      call KillFile(10)
      return
   end if
   end if EcoTox_File3b

   EcoRisk_File3a: if (RSKFILC) then
   call Assign_LUN (RSKCLUN)
   open (unit=RSKCLUN, status='old', access='sequential',&
         position='append',form='formatted', file='EcoRiskC.xms',&
         action='readwrite', iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "EcoRiskC.xms")
      call Release_LUN (RSKCLUN)
      call KillFile(9)
      return
   end if
   end if EcoRisk_File3a

   EcoRisk_File3b: if (RSKFILR) then
   call Assign_LUN (RSKRLUN)
   open (unit=RSKRLUN, status='old', access='sequential',&
         position='append',form='formatted', file='EcoRiskR.xms',&
         action='readwrite', iostat=IOerr)
   if (IOerr /= 0) then ! problem with results file...
      call Messenger (1000, "EcoRiskR.xms")
      call Release_LUN (RSKRLUN)
      call KillFile(11)
      return
   end if
   end if EcoRisk_File3b

   if (FULFIL) then
      call Assign_LUN (FULLUN)
      open (unit=FULLUN, status='old', access='sequential',&
         position='append',form='formatted', file='FullOut.xms',&
         action='readwrite', iostat=IOerr)
      if (IOerr /= 0) then ! problem with results file...
         call Messenger (1000, "FullOut.xms")
         call Release_LUN (FULLUN)
         call KillFile(12)
         return
      end if
   end if


case default run_option ! RUNOPT has unknown value...
   write (stderr,fmt='(A,I2)') ' Command cancelled; RUNOPT = ',RUNOPT
   return
end select run_option

! Process integrator selection according to Run/Continue
  if (RUNOPT==0) then ! entry via Run command, start with Adam
     Stifeq=.false.
  elseif (RUNOPT==1) then ! entry via Continue command
     ! if in Mode 2, a pulse will often introduce a non-stiff transient
     ! best dealt with by Adam:
     if (MODEG==2 .and. (sum(IMASSG) .GreaterThan. 0.0)) Stifeq = .false.
     ! Otherwise, if the problem has been adjudged stiff, leave it alone.
   else; end if
  ! On both Run and Continue, the starting conditions must be written
  ! to the output files because of the possibility of Dirac delta "events."
  If (StifEq) then
    Stiff_Start = .true. ! Gear method will write I.C.
  else
    Stiff_Start = .false. ! Not starting with Gear, Gear need not write I.C.
  end if

! RUNOPT cases processed, call driver subroutines
if (.not.(allocated(WORK))) allocate (WORK(max(19,KEQN*KEQN+17*KEQN)))
if (.not.(allocated(IWORK))) allocate (IWORK(KEQN))
WORK = 0.0
IWORK=0

Driver_loop: do
   if (MODEG == 1) call DRIVM1()
   if (MODEG == 2) call DRIVM2()
   if (MODEG == 3) then
      if (.not.(allocated(DayStack))) allocate (DayStack(366,10,KOUNT,KCHEM))
      if (.not.(allocated(DayStart))) allocate (DayStart(10,KOUNT,KCHEM))
      if (.not.(allocated(DayEnd))) allocate (DayEnd(10,KOUNT,KCHEM))
      if (.not.(allocated(Y_start))) allocate (Y_start(KOUNT,KCHEM))
      DayStack=0.0; DayStart=0.0; DayEnd=0.0; Y_start=0.0
   end if
   call DRIVM3 (Y,RUNOPT)
   if (ISOO == 0 .or. IFLAG==10) exit Driver_loop
end do Driver_loop
if (allocated(DayStack)) deallocate (DayStack)
if (allocated(DayStart)) deallocate (DayStart)
if (allocated(DayEnd)) deallocate (DayEnd)
if (allocated(Y_start)) deallocate (Y_start)
if (allocated(WORK)) deallocate (WORK)
if (allocated(IWORK)) deallocate (IWORK)

if (PLTFIL) then
   endfile KINLUN; close (unit=KINLUN,iostat=IOerr); call Release_LUN (KINLUN)
end if

if (FGTFIL) then ! if FGETS transfer files were produced...
   endfile FG1LUN; close (unit=FG1LUN,iostat=IOerr); call Release_LUN (FG1LUN)
   endfile FG2LUN; close (unit=FG2LUN,iostat=IOerr); call Release_LUN (FG2LUN)
end if

if (BASFIL) then ! if BASS transfer file was produced...
   endfile BASSLUN; close (unit=BASSLUN,iostat=IOerr)
   call Release_LUN (BASSLUN)
end if

if (HWRFIL) then ! if HWIR transfer file was produced
   endfile HWIRLUN; close (unit=HWIRLUN,iostat=IOerr)
   call Release_LUN (HWIRLUN)
end if

if (TOXFILC) then ! if EcoTox compartment-oriented exposure file was produced
   endfile ToxCLUN; close (unit=ToxCLUN,iostat=IOerr)
   call Release_LUN (ToxCLUN)
end if

if (TOXFILR) then ! if EcoTox reach-oriented exposure file was produced
   endfile ToxRLUN; close (unit=ToxRLUN,iostat=IOerr)
   call Release_LUN (ToxRLUN)
end if

if (RSKFILC) then ! If compartment-oriented EcoRisk file was produced
   endfile RSKCLUN; close (unit=RSKCLUN,iostat=IOerr)
   call Release_LUN (RSKCLUN)
end if

if (RSKFILR) then ! If reach-oreiented EcoRisk file was produced
   endfile RSKRLUN; close (unit=RSKRLUN,iostat=IOerr)
   call Release_LUN (RSKRLUN)
end if

if (FULFIL) then ! If compartmental full output file was produced
   endfile FULLUN; close (unit=FULLUN,iostat=IOerr)
   call Release_LUN (FULLUN)
end if

return

contains
!****************************************************************************
Subroutine Messenger (Error_Number,Detail)
Implicit None
integer, intent (in) :: Error_Number
character(len=*) :: Detail

select case (Error_Number)

case (1000)
write (stderr,fmt='(3(/A))') &
  ' Results file "'//Detail//'" cannot be written.',&
  ' Possibly the file is write-protected, or the device may be full.',&
  ' Exams cannot execute simulations until the problem is repaired.'

end select
IFLAG=8
return
end Subroutine Messenger
!****************************************************************************
Subroutine KillFile(I)
! Procedure to delete old results file if user does not want this file type
character(len=12), parameter :: Result_File (14) = (/'report.xms  ',&
'ssout.plt   ', 'kinout.plt  ', 'fgetscmd.xms', 'fgetsexp.xms',&
'bassexp.xms ', 'hwirexp.xms ', 'EcoToxC.xms ', 'EcoRiskC.xms',&
'EcoToxR.xms ', 'EcoRiskR.xms', 'FullOut.xms ', 'CptRisk.tmp ', 'RchRisk.tmp '/)
integer :: Killer_LUN, I
logical :: In_use, Found_It
   Inquire (File = trim(Result_File(I)), exist = Found_It, opened=In_use,&
            number=Killer_LUN) ! If the file is open, the LUN is noted
   if (Found_It) then
      if (.not.In_Use) then
         call Assign_LUN (Killer_LUN)
         open (unit=Killer_LUN, file=trim(Result_File(I)), action='read', &
            status='old', iostat=IOerr)
      end if
      ! In either case, now close and delete the file
      close (Killer_Lun, status = 'DELETE', iostat=IOerr)
      call Release_LUN (Killer_LUN)
   end if
return
end Subroutine KillFile
!*****************************************************************************
subroutine CPTSHOW (TargetLUN) ! created 2002-04-27
! purpose--to list the segment numbers and type of each compartment
! in output files
Implicit None
integer, intent(in) :: TargetLUN
integer :: J, Jstart, Jstop, KOUNTER
! Output file headers are restricted to ca. 80 columns to make them readable
! in most ASCII file editors.

write (TargetLUN,fmt='(A,I0)') '! Total number of segments (KOUNT) = ',KOUNT
write (TargetLUN,fmt='(A)')&
'! Compartment structure: sequential pipe-delimited number-type pairs.'
! Reported 10 per line; each line begins with an "!".
!
!write (TargetLUN,fmt='(20(A))') (TYPEG(J),J=1,KOUNT)
JStart = 1
if (KOUNT <=10) then
   Jstop=KOUNT
else 
   Jstop=10
end if
KOUNTER = KOUNT
SPrint: do 
   write (TargetLUN,fmt='(A,10(I0,A))')&
       '! |',(J,TYPEG(J)//'|',J=Jstart,Jstop)
   KOUNTER=KOUNTER-10
   if (KOUNTER <= 0) exit SPrint
   Jstart=Jstart+10
   Jstop=Jstop+min(10,KOUNTER)
end do SPrint
return
end subroutine CPTSHOW


!****************************************************************************
end Subroutine DRIVER

! Revisions of integration routines occasioned by problems.
!
! Problem:  Some compartments were contaminated by contributions from other
!      compartments, although the structure of the system did not allow for
!      such contributions.
! 
! The contamination was traced to the solution of the linear system (equations
! 6-10 of Malanchuk [1]) returned by "DECOMP", used by GRSUB2 to solve a
! stiff system of equations. "DECOMP" was replaced by its newer counterpart,
! LU_Decomp. The f77 code was converted to f90 and tailored for EXAMS. See
! comments in subroutine LU_Decomp (file grsub2.f90) for the Internet address
! of the site and other documentation.  The section of subroutine GRSUB2 that
! computed the solution of the linear system was replaced by LU_Solve, which
! solves the LU system generated by LU_Decomp. No contamination was detected
! after these modifications.
! 
! 
! Problem:  The Adams methods could not detect that the ODE system was
!           stiff. The symptoms were:
!               a) Negative values for some of the state variables;
!               b) Iflag == 10 errors: "violation of isotherm linearity"
!               c) solutions like -2.0e+30.
! 
! 1) While determining the cause of these symptoms, errors in both the manual
!  (Malanchuk [1]) and the Fortran code (step.f90, array GSTR) were corrected.
!  The correct values were obtained from Gear [3], and Shampine & Gordon [4].
!  Mathematica [7] was used to compute the values used for the array GSTR
!  (in step.f90). Shampine and Gordon [4] contains a complete theoretical
!  analysis of the integration methods described in Malanchuk [1], as well
!  as experimental results and a discussion.
! 
! 2) The Adams methods were still unable to detect numerical instability in
!    systems that had an initial nonstiff transient phase. This problem was
!    solved using the method described by Bader [6]. The test is essentially
!    the normalized product of the current step size and Root Mean Square
!    (RMS) of the derivatives at the current point. The test is initialized in
!    subroutine "Admint" (variable h_standard, file admint.f90) and the
!    Local Stiffness Function (LSF) computed in subroutine "Adam"
!    (variable Local_stiff_function, file adam.f90). A typical sequence of
!    values of the LSF for systems migrating from nonstiffness to stiffness
!    is 10E-10, 10E-7, 10E-4, 10E-2, 100.
! 
!    Debugging output of the LSF test is enabled by "set iunit=1" : a message
!    will be displayed when the LSF test detects stiffness. The command
!    "set iunit=2" displays the value of the LSF at every step of the
!    integration.
! 
! 
! References and useful collateral materials:
! [1] Malanchuk, J., J. Otis, and H. Bouver. 1980.
!     "Efficient Algorithms for Solving Systems of Ordinary
!     Differential Equations for Ecosystem Modeling."
!     EPA-600/3-80-037. NTIS, Springfield Va. 148 pp.
! 
! [2] Krishnan Radhakrishnan and Alan C. Hindmarsh. December 1993.
!     Description and Use of LSODE, the Livermore Solver for Ordinary
!     Differential Equations. NASA Reference Publication 1327. Lawrence
!     Livermore National Laboratory Report UCRL-ID-113855.
! 
! [3] Gear, C.W. 1971. Numerical Initial Value Problems in Ordinary
!     Differential Equations. Prentice-Hall, Englewood Cliffs, N.J.
! 
! [4] Shampine, L.F., and M.K. Gordon. 1975. Computer Solution of Ordinary
!     Differential Equations: The Initial Value Problem. W.H. Freeman,
!     San Francisco, 318 pp.
! 
! [5] Engeln-Mullges, G. and F. Uhlig. 1996. Numerical Algorithms with Fortran.
!     Springer Verlag, 602 pp.
! 
! [6] Bader, M. 1998. A new technique for the early detection of stiffness in
!     coupled differential equations and application to standard Runge-Kutta
!     algorithms. Theoretical Chemistry Accounts 99:215-219.
! 
! [7] Mathematica 3.0, Wolfram Research, Inc.
!     100 Trade Center Drive, Champaign, IL 61820-7237, USA.
!     web: http://www.wolfram.com; email: info@wolfram.com
!     phone: +1-217-398-0700 (USA)
! 
! [8] Dekker K., and J.G. Verwer. 1984. Stability of Runge-Kutta Methods
!     for Stiff Nonlinear Differential Equations. CWI monograph. Elsevier
!     Science Publishers B.V. 307 pp.
! 
! [9] Petzold, L. 1983. Automatic selection of methods for solving stiff and
!     nonstiff systems of ordinary differential equations. SIAM J. Sci.
!     Stat. Comput. 4:136-148.
! 
! [10] Shampine, L.F., and C.W. Gear. 1979. A User's view of solving stiff
!      ordinary differential equations. SIAM Review. 21:1-17.
