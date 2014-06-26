subroutine PRZMIN (File_Name,Problem)
! Subroutine to read an external file of allochthonous chemical loadings
! from output produced by the Pesticide Root Zone Model
! Revised 09/13/91; 02/29/96; 5/17/96 for PRZM3
! Revised 09-Feb-1999 to use Floating Point Comparison module
! Revised 02/29/00 to read hydrology from PRZM file and create NPS flow/sed
use Floating_Point_Comparisons
use Implementation_Control
use Initial_Sizes
use Global_Variables
use Local_Working_Space
use Input_Output, only: ECHO
Implicit None
logical, intent (out) :: Problem
logical :: PRZM3
! local variables
real :: R1, R2, R3, R4, TRAREA, SPRAYL
! R1,... are used to read data from the PRZM file. In that file,
! following the comment records,
 ! Record 1 in PRZM3 is CAS number and Name of chemical...
 ! write format in PRZM3 is (2X,A16,1X,A20)
 ! Record 2 in PRZM3; record 1 in PRZM1
 !  FLD 1 - Area of Field (ha)
 !  FLD 2 - Year of Simulation
 !  FLD 3 - Number of Pesticide Applications
 ! Record 3 through the Number of Pesticide Applications
 !  FLD 1 - Month
 !  FLD 2 - Day
 !  FLD 3 - Application Rate (kg/ha) ... next 2 fields are PRZM3
 !  FLD 4 - Application Efficiency (as a fraction of the Application Rate)
 !  FLD 5 - Percent drift (as a percentage of the Application Rate)
 ! Record (3+#Apps) to the End of File
 !  FLD 1 - Month
 !  FLD 2 - Day
 !  R1--FLD 3 - Runoff Depth (cm/day)
 !  R2--FLD 4 - Runoff Pesticide Flux ((g/cm2)/day)
 !  R3--FLD 5 - Erosion Soil Loss ((tonnes/ha)/day)
 !  R4--FLD 6 - Erosion Pesticide Flux ((g/cm2)/day)
 !  R5--FLD 7 - Precipitation (cm) (PRZM3 only)
 !  However, as programmed (as of 02/28/2000) "events" are defined by
 !  runoff; as a consequence, not all precipitation is reported!
 !  For that reason, rainfall is developed from the met file and the PRZM
 !  report is ignored.
! TRAREA is size (ha) of treated area, read from PRZM file
! the PRZM file contains grams of toxicant per cm2 of treated area leaving
! the treated area on the day in question
real, parameter :: CFACTR=1.E+05 ! the conversion factor CFACTR
      ! gives kg of toxicant loaded to the EXAMS aquatic system
      ! via 1kg/1000g and 1E8 cm2/ha = 1.E+05
integer :: I, I1, I2, NOYEAR, NOAPPS, I3, I4, Status_Check
! NOYEAR is the calendar year from PRZM
! NOAPPS is the number of application events
integer :: Span, Month
character(4) :: DUMMY
character (len = *) :: File_Name
character (len=16) :: CAS_Number
character (len=20), dimension(KCHEM) :: PRZM_Chemical
Problem = .false.
skip_comments: do     ! Process the header/comment records
   read (unit=PRZLUN,iostat=Status_Check,fmt='(A4)') DUMMY
   if (Status_Check > 0) then
      write (stdout,fmt='(/A/A/A)')&
         ' Error reading comment section of PRZM,',&
         ' transfer file "'//trim(File_Name)//'"',&
         ' No events were acquired.'
      Problem = .true.; PRZM_Transfer_File = .false.
      return
   elseif (Status_Check == IOeof) then ! eof while reading comments
      write(stdout,fmt='(/A/A)')&
       ' No data in PRZM transfer file "'//trim(File_Name)//'"',&
       ' Processing ended; no events were acquired.'
      Problem = .true.; PRZM_Transfer_File = .false.
      return
   elseif (DUMMY == ' !! ') then !! is the last comment field in PRZM1
      PRZM3 = .false.
      exit skip_comments
   elseif (DUMMY == ' !!*') then !!* is the last comment field in PRZM3
      PRZM3 = .true.
      exit skip_comments
   endif
end do skip_comments
! Read the treated area, the year, and the number of applications
if (PRZM3) then
   read (unit=PRZLUN,iostat=Status_Check,&
      fmt='(2X,A16,1X,A20/8X,F10.2,1X,6X,I4,9X,I2)')&
      CAS_number, PRZM_Chemical(MCHEMG), TRAREA, NOYEAR, NOAPPS
else ! PRZM 1 file
   read (unit=PRZLUN,iostat=Status_Check,&
      fmt='(1X,F8.2,2X,I4,2X,I2)') TRAREA, NOYEAR, NOAPPS
end if
! File processing error returns
   if (Status_Check > 0) then
      write (stdout,fmt='(/A/A/A)')&
         ' Error reading first data record(s) of PRZM',&
         ' transfer file "'//trim(File_Name)//'".',&
         ' No events were acquired.'
      Problem = .true.; PRZM_Transfer_File = .false.
      return
   elseif (Status_Check == IOeof) then
      write (stdout,fmt='()')&
         ' PRZM transfer file "'//trim(File_Name)//'"',&
         ' terminated without any application or runoff events.'
      Problem = .true.; PRZM_Transfer_File = .false.
      return
   endif
! End of initial file processing error returns

! If a PRZM-compatible met file has been read, then data are
! available from that file for this simulation year. First, check to be
! sure the met file and the transfer file are commensurate; if the transfer
! file is asking for a year outside the boundaries of the met file
! load averages from the met file that was read...
if (PRZM_Met_File) then
   if ( NOYEAR<FirstYear .or. NOYEAR>LastYear) then
      ! Write warning message
      write (stderr,fmt='(A,I4,A,I4,A/A,I4,A)')&
      ' Warning: the meteorology file spans the years ',FirstYear,&
      ' to ',Lastyear,'.',' Average values will be used for ',NOYEAR,'.'
      ! load averages from the met file
      Span = LastYear - FirstYear + 1
      Months: Do Month= 1,12
         RAING(Month) = sum(Precip(:,Month)) / Span
         Segments: do I = 1, KOUNT
            TCELG(I,Month) = sum(AirTemp(:,Month)) / Span
            if (I==1 .or. (TYPEG(I)/='B'.and.TYPEG(I-1)=='B')) then
               ! surface water, load evaporation and wind speed
               EVAPG(I,Month) = sum(PanEvap(:,Month)) / Span
               ! /2.0 (for 10 m height to 10 cm) = WIND (m/s @10 cm height)
               ! (/1.89 for 6m instrument height)
               ! WindSpeed is converted to WINDG in subroutine WBAN
               WINDG(I,Month) = sum(WindSpeed(:,Month)) / Span
            end if
         End do Segments
      End do Months
   else ! load data for this year
      Do Month = 1,12
         RAING(Month)  = Precip(NOYEAR,Month)
         CLOUDG(Month) = OSCover(NOYEAR,Month)
         RHUMG(Month)  = RelHum(NOYEAR,Month)
         do I = 1, KOUNT
            TCELG(I,Month) = AirTemp(NOYEAR,Month)
            if (I==1 .or. (TYPEG(I)/='B'.and.TYPEG(I-1)=='B')) then
               ! surface water, load evaporation and wind speed
               EVAPG(I,Month) = PanEvap(NOYEAR,Month)
               WINDG(I,Month) = WindSpeed(NOYEAR,Month)
            end if
         end do
      end do
   end if

   ! Check temperature for strangeness, do a little extra quality control
   do Month = 1, 12
      do I = 1, KOUNT
         if (I==1 .or. (TYPEG(I)/='B'.and.TYPEG(I-1)=='B')) then
            ! For our purposes, frozen is frozen; ice is ice.
            if (TCELG(I,Month) .LessThan. 0.0) TCELG(I,Month) = 0.0
         else  ! benthic segment or bottom water
            ! Here 4 degrees is the sensible minimum
            if (TCELG(I,Month) .LessThan. 4.0) TCELG(I,Month) = 4.0
            ! Plus a little extra quality control...
            EVAPG(I,Month) = 0.0
            WINDG(I,Month) = 0.0
         end if
      end do
   end do
   ! Calculate annual averages:
   RAING(13)  = sum(RAING(1:12))/12.0
   CLOUDG(13) = sum(CLOUDG(1:12))/12.0
   RHUMG(13)  = sum(RHUMG(1:12))/12.0
   SegmentMeans: do I = 1, KOUNT
      EVAPG(I,13) = sum(EVAPG(I,1:12))/12.0
      WINDG(I,13) = sum(WINDG(I,1:12))/12.0
      TCELG(I,13) = sum(TCELG(I,1:12))/12.0
   end do SegmentMeans
end if

! Set the number of days in February
   if (mod(NOYEAR,4)==0 .and. mod(NOYEAR,100)/=0 .or. mod(NOYEAR,400)==0) then
      NDAYS(2) = 29
   else
      NDAYS(2) = 28
   end if
! Number of days in February now set

! Every PRZM file for a given year carries the same runoff data;
! so flows are recalculated when product files are read
NPSFLG(1,:)=0.0        ! Non-point-source flow will be acquired from PRZM
NPSEDG(1,:)=0.0

if (Restart_PRZM) then     ! read an entire new series
   I3 = 1                  ! First event will load in slot 1
   Restart_PRZM = .false.  ! Subsequent reads (transformation products
                           ! in particular) will now add to the total
                           ! event inventory
else ! inventory IMASSG to find the next available slot for transformation
     ! products
   Inventory: do I3 = 1, MAXMAS
      if (IMASSG(I3) .GreaterThan. 0.0) then
         cycle Inventory
      else ! current IMASSG(I3) is zero...check for more further on
         do I4 = I3+1, MAXMAS
            if (IMASSG(I4) .GreaterThan. 0.0) then ! hole in vector...fill it
               IMASSG(I3) = IMASSG(I4)
               IMASSG(I4) = 0.0
               ISEGG(I3)  = ISEGG(I4)
               ICHEMG(I3) = ICHEMG(I4)
               IMONG(I3)  = IMONG(I4)
               IDAYG(I3)  = IDAYG(I4)
               IYEARG(I3) = IYEARG(I4)
               ISEGG(I4)  = 0
               ICHEMG(I4) = 0
               IMONG(I4)  = 0
               IDAYG(I4)  = 0
               IYEARG(I4) = 0
               cycle Inventory ! try the next entry
            end if
         end do
         exit Inventory ! I3 has location of the next slot
      end if   
   end do Inventory
end if ! I3 is now set to 1, or to the next available event
read_many_apps: do I=1,NOAPPS ! Read the rate (kg/ha) of the events
   if (I3 > MAXMAS) then ! some events have to be left out, but can proceed
      write (stdout,fmt='(A,I4,4(/,A))')&
         ' EXAMS allows for a maximum of ',MAXMAS,&
         ' events during each year.',&
         ' The PRZM file describes some events that were not loaded.',&
         ' You should remove some small events from PRZM transfer',&
         ' file "'//trim(File_Name)//'" and try again.'
      PRZM_Transfer_File = .true.
      return
   end if
   if (PRZM3) then
!     read month, day, application rate (kg/ha), application efficiency, spray
      read (unit=PRZLUN,iostat=Status_Check,&
         fmt='(1X,I2,1X,I2,2X,3(F10.4,2X))') I1,I2,R1,R2,SPRAYL
   else ! PRZM 1 file - read month, day, application rate (kg/ha)
      read (unit=PRZLUN,iostat=Status_Check,&
         fmt='(1X,I2,1X,I2,2X,F8.3)') I1,I2,R1
         SPRAYL = SPRAYG
   endif
   if (Status_Check /= 0) then ! end of file or read error; either way...
      write (stdout,fmt='(/A)')&
         ' A problem arose reading application events in PRZM transfer',&
         ' file "'//trim(File_Name)//'". Check results using the',&
         ' SHOW PULSE LOADS command.'
      Problem = .true.; PRZM_Transfer_File = .false.
      return
   end if
   Airborne_check: if (R1*SPRAYL .GreaterThan. 0.0) then
                     ! event is impacting system
      ISEGG(I3)  = 1 ! the drift always goes in segment 1
                     ! (or the appropriate segment with air/water interface)
      ICHEMG(I3) = MCHEMG
      IMONG(I3)  = I1
      IDAYG(I3)  = I2
      IYEARG(I3) = NOYEAR
      IMASSG(I3) = R1 * (SPRAYL/100.0) * AREAG(1) * 1.E-04
      I3 = I3 + 1
   end if Airborne_check
end do read_many_apps

! Read the runoff events into the pulse load data structure
! I3 is the location of the next event slot available in the EXAMS data
! structure...the loop allows for elision of zero values of toxicant
! transported from the land surface. The loop terminates on finding
! the end of the file, or upon encountering I3 > MAXMAS.
Runoff_events: do
   if (I3 > MAXMAS) then ! out of room; some events have to be left out
      write (stdout,fmt='(A,I4,4(/A))')&
         ' EXAMS allows for a maximum of ',MAXMAS,&
         ' events during each year.',&
         ' The PRZM file describes some events that were not loaded.',&
         ' You should remove some small events from PRZM transfer',&
         ' file "'//trim(File_Name)//'" and try again.'
      PRZM_Transfer_File = .true. ! O.K. to proceed with what we have
      return
   end if
   if (PRZM3) then
      read (unit=PRZLUN,iostat=Status_Check,&
         fmt='(1X,I2,1X,I2,2X,5(E10.4,1X))') I1,I2,R1,R2,R3,R4
         ! (Don't bother with R5 (rainfall) as it isn't a complete dataset!)
         ! (Rainfall comes from the meteorology file)
         ! (Do, however, retain the if-then-else structure for PRZM changes.)
   else
      read (unit=PRZLUN,iostat=Status_Check,&
         fmt='(1X,I2,1X,I2,2X,4(E10.4,1X))') I1,I2,R1,R2,R3,R4
   endif
   if (Status_Check > 0) then ! error
      write (stdout,fmt='(/A/A)')&
         ' Error reading PRZM input file"'//trim(File_Name)//'"',&
         ' check the results with SHOW PULSE LOAD command.'
      exit Runoff_events
   elseif (Status_Check == IOeof) then ! normal end point: out of events
      exit Runoff_events               ! or perhaps no events for this year
   endif
   ! If dissolved toxicant is present, load it to the water column
   Dissolved: if (R2 .GreaterThan. 0.0) then
     ISEGG(I3)  = 1
     ICHEMG(I3) = MCHEMG
     IMONG(I3)  = I1
     IDAYG(I3)  = I2
     IYEARG(I3) = NOYEAR
     IMASSG(I3) = R2*TRAREA*CFACTR
     I3=I3+1
   endif Dissolved
   ! If sorbed toxicant is present, transmit it to the system
   Sorbed: if (R4  .GreaterThan. 0.0) then
      ! if no sediment, write warning message
      if (R3 .LessThanOrEqual. 0.0) &
      write (stdout,fmt='(A/A,I2,A,I2,A,I4,A/A)')&
      ' WARNING: PRZM is passing sediment-sorbed chemical without sediment!',&
        ' The entry is at ',I1,'/',I2,'/',NOYEAR,'.',&
        ' This message is for information only; the event HAS been processed.'
      ! PRBENG is proportion of sediment-sorbed toxicant that is carried
      ! to the bottom sediment without equilibrating with the water column.
      if (PRBENG .GreaterThan. 0.0) then
         ! some chemical goes straight to the bottom, so
         ! locate the first benthic segment
         Find_bottom: do I4 = 1, KOUNT ! start at one in case only water
            if (TYPEG(I4) == 'B' .or. TYPEG (I4) == 'b') then
               ISEGG(I3)  = I4
               exit Find_bottom
            elseif (I4 == KOUNT) then ! write error message
               write (stdout,fmt='(3(/A))')&
                  ' '//trim(ECONAM)//' lacks a benthic zone.',&
                  ' PRZM events cannot be transmitted to bottom sediment;',&
                  ' they have been routed to the water column.'
               ISEGG(I3) = 1
            end if
         end do Find_bottom
         ICHEMG(I3) = MCHEMG
         IMONG(I3)  = I1
         IDAYG(I3)  = I2
         IYEARG(I3) = NOYEAR
         IMASSG(I3) = R4*TRAREA*CFACTR*PRBENG
      endif
      ! If some sorbed toxicant desorbs into the water column, then it must be
      ! routed to the water column either in the previous or the next slot...
      if (PRBENG .LessThan. 1.0) then
         if (R2  .GreaterTHan. 0.0) then
            IMASSG(I3-1)=IMASSG(I3-1)+R4*TRAREA*CFACTR*(1.0-PRBENG)
         else
         ! This date has sediment movement but no dissolved material (probably
         ! would not happen with PRZM, but not instrinsically impossible to a
         ! computer, and this allows for dust movement from other models).
         ! Increment the counter to point at the next data slot; presumably
         ! the (I3-1) slot was used for something else...if, however, PRBENG
         ! is set at zero to disperse the contaminant in the water column, I3
         ! need not be incremented...
            if (PRBENG .GreaterThan. 0.0) I3=I3+1
               IMASSG(I3)=R4*TRAREA*CFACTR*(1.0-PRBENG)
               ISEGG(I3)  =1
               ICHEMG(I3) =MCHEMG
               IMONG(I3)  =I1
               IDAYG(I3)  =I2
               IYEARG(I3) =NOYEAR
            endif
         endif
      I3=I3+1 ! move on to a new slot for the next read
   endif Sorbed
   ! End of section processing sorbed toxicant

   ! Convert runoff depth from this event to increment on monthly
   ! non-point-source flow. Input datum is cm runoff depth. Factor of 100x
   ! arises from e+08 to convert ha to cm2; e-06 for cm3 to m3
   NPSFLG(1,I1) = NPSFLG(1,I1) + R1 * TRAREA * 100.00
   NPSEDG(1,I1) = NPSEDG(1,I1) + R3 * TRAREA * 1000.00 ! 1000 kg / tonne

   ! End of data processing...go back and read another record
end do Runoff_events

! Calculate monthly mean non-point-source flow
NPSFLG(1,13)    = sum(NPSFLG(1,1:12))
NPSEDG(1,13)    = sum(NPSEDG(1,1:12))
NPSFLG(1,1:12)  = NPSFLG(1,1:12)/(24.0*NDAYS(1:12))
NPSEDG(1,1:12)  = NPSEDG(1,1:12)/(24.0*NDAYS(1:12))
NPSFLG(1,13)    = NPSFLG(1,13)/(24.0*sum(NDAYS(1:12)))
NPSEDG(1,13)    = NPSEDG(1,13)/(24.0*sum(NDAYS(1:12)))

! Report normal completion of file processing to log file or console
if (echo) then
      write (stdout,fmt='(A,I4,A)')&
         ' Processing completed for ',NOYEAR,' PRZM file.'
      if (PRZM3) write (stdout,fmt='(A)')&
         ' These data were for "'//trim(PRZM_Chemical(MCHEMG))//&
         '", CAS Number '//trim(CAS_Number)//'.'
end if
PRZM_Transfer_File = .true.
return
end Subroutine PRZMIN
