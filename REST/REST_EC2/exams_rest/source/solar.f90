subroutine SOLAR
use SOLAR_data
! Computes solar irradiance just below the water surface.
! Completed 26 November 1983 (L.A. Burns).
! Revised 05-SEP-1985 (LAB) to hardwire result of EXP(-(>=87.4))
! and enter data for SUNIN.
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revisions 02/05/00 -- read total column ozone from TOMS database
! Revisions 06/15/01 -- validation study supports use of full equation
!     for NHI(2)
! Revision 2002-04-23 to support conditional printing to report file
use Floating_Point_Comparisons
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters

Implicit None
! Allocate storage for integration
real (kind (0D0)) :: DINTPT
real :: YTEMP, GLOLIT, TIMER, TNIGHT, XINT(11), YINT(11), TEMP
! Counters, pointers, and intermediate computational variables
real ::  S1, S2, YHI
real :: TAU2, TAU4, FA3, FA4, F1, F2, FB3, FB4
! TAU2 and TAU4 are aerosol optical depths due to scattering and
! absorption, respectively.
! AIREFL is air reflectivity function.
! Results of relative humidity computations
real :: LAMAR, ELAM0R
real :: EXTAER(46) ! Aerosol extinction coefficients
real :: NHI(3), RHUML
! The NHI are elevation corrections for ground station elevation above sea
! level, based on the report of Green, Cross and Smith (GCS, Photochem. Photo-
! biol 31:59-65 (1980)). NHI(1) applies to air (Rayleigh scattering), 
! NHI(2) to aerosols, and NHI(3) to ozone. NHI(2) may
! refer to elevation above the ground rather than station elevation, but
! validation study (06/15/2001) suggests it is appropriate to use it.
! RHUML is local value of relative humidity (RHUMG(%)/100).
real :: HIBEAM, EMM, EXPARG
! HIBEAM is irradiance at bottom of atmosphere for overhead sun.
! EMM is "M" function
! EXPARG is temporary variable (arguments to function exp())
real :: LATL ! LATL is latitude converted to radians for FORTRAN trig funct.
integer :: I, I2, I3, II, J2, K, N2, NFIRST, NLAST, ELEVEN=11, NBLOC, Checked
! I, I3, J2, K are general loop counters
! I2 points at airmass characteristics.
! NFIRST and NLAST set the size of the computational loop.
! Checked is counter for loading AIRVEC, the report vector of air mass types
!
character(len=1) :: AIRVEC(4), CCHAR(2) = (/'1','0'/)
! Vector AIRVEC tracks the airmass types currently in use.
! CCHAR is carriage control character to suppress pagination
! when routine is called from the SHOW command.
!
character :: KOUT*2, NMON*4, TAG*1
! KOUT transfers number of the month to the table headers.
! NMON is the name of a month, transferred from NAMONG
! TAG is asterisk for footnote.
!
logical :: print, MEAN, Single_table, Average_table
! PRINT indicates time to print.
! MEAN signals that mean values are computed.
! Single_table signals that the table of individual values is to be printed
! Average_table signals that the table of mean values is to be printed
!
! CENLAM is the center wavelength of each of the 46 wavelength
! intervals (in nanometers)
real, parameter :: CENLAM(46) = &
 (/280.,282.5,285.,287.5,290.,292.5,295.,297.5,300.,&
   302.5,305.,307.5,310.,312.5,315.,317.5,320.,323.1,330.,340.,350.,360.,&
   370.,380.,390.,400.,410.,420.,430.,440.,450.,460.,470.,480.,490.,503.75,&
   525.,550.,575.,600.,625.,650.,675.,706.25,750.,800./)

! ABFRAC is fraction of total aerosol extinction coefficient that is due to
! light absorption rather than scattering. ABFRAC was computed via regression
! on wavelength using data in GCS.
real, parameter :: ABFRAC(46) = &
 (/.152, .151, .150, .149, .148, .147, .147, .146,&
   .145, .144, .143, .142, .141, .140, .140, .139, .138, .137,&
   .134, .131, .128, .125, .122, .119, .116, .114, .111, .108,&
   .106, .103, .101, .0982, .0959, .0936, .0913, .0883, .0839,&
   .0789, .0743, .0699, .0658, .0619, .0583, .0540, .0486, .0430/)

! Air mass data for computing aerosol extinction coefficients as
! function of wavelength and relative humidity (from Green and
! Schippnick Copenhagen report)--entry 1 is Rural, entry 2 is
! Urban, entry 3 is Maritime, and 4 is Tropospheric air mass.
real, parameter, dimension(4) ::&
   ELAM0=(/ 0.255, 0.288,   0.106,   0.081/),&
   KAER =(/ 1.962, 2.758,   3.393,   2.034/),&
   PAER =(/ 0.345, 0.471,   0.435,   0.328/),&
   LAMA0=(/ 0.439, 0.510,   0.734,   0.412/),&
   CAPEL=(/ 0.122, 0.0827,  1.049,   0.102/)
!           Rural  Urban   Maritime  Tropospheric
! K3 are (Naperian) absorption coefficients for atmospheric ozone
real, parameter :: K3(46) = &
  (/116.8,92.40,71.26,53.80,39.92,29.23,21.18,15.23,10.89,&
      7.776,5.507,3.902,2.760,1.951,1.378,.9725,.6862,.4451,.1697,&
      4.193E-02,1.036E-02,2.557E-03,6.315E-04,1.6E-04,0.,0.,0.,0.,&
      3.E-03,3.E-03,3.E-03,7.E-03,1.15E-02,1.5E-02,2.E-02,2.99E-02,&
      5.30E-02,8.29E-02,0.120,0.124,9.44E-02,6.45E-02,3.91E-02,&
      2.07E-02,9.21E-03,9.E-03/)
! RAYFAC is Rayleigh optical depth (molecular scattering in the
! atmosphere) at sea level pressure of 1013 mb:
real, parameter :: RAYFAC(46) = &
(/ 1.5469,1.4923,1.4412,1.3917,1.3443,1.2990,1.2555,&
   1.2138,1.1739,1.1355,1.0988,1.0635,1.0296,.99702,.96574,.93568,&
   0.90678,.87248,.80176,.71152,.63362,.56610,.50734,.45600,.41100,&
   0.37142,.33649,.30557,.27812,.25369,.23187,.21236,.19485,.17912,&
   0.16494,.14765,.12516,.10391,.086982,.073366,.062314,.053266,&
   0.045802,.038218,.030051,.023214 /)
!
! SUNIN is irradiance (photons/cm2/sec/N nm) at the top of the
! atmosphere at mean solar distance (1 astronomical unit, 1 AU).
! N for bands centered at 280-323.25 nm (entries 1-17) is 2.5 nm bandwidth
! N for 323.1 nm band is 3.75 nm bandwidth
! N for 330-800 nm (entries 19-46) is 10 nm
! Computed from Frolich and Wehrli's table of extraterrestrial irradiance
! given at page 380 of Iqbal,M. 1983.  An Introduction to Solar Radiation.
! Academic Press, New York. 390 pp.
real, parameter :: SUNIN(46)= &
 (/5.74E13, 1.06E14, 8.09E13, 1.39E14, 1.96E14, 2.14E14,&
   2.12E14, 1.97E14, 2.00E14, 2.05E14, 2.10E14, 2.31E14, 2.36E14,&
   2.65E14, 2.82E14, 2.88E14, 3.02E14, 4.17E14, 1.61E15, 1.56E15,&
   1.70E15, 1.80E15, 2.08E15, 2.10E15, 2.07E15, 2.99E15, 3.51E15,&
   3.67E15, 3.48E15, 4.06E15, 4.57E15, 4.75E15, 4.71E15, 4.89E15,&
   4.69E15, 4.91E15, 4.97E15, 5.20E15, 5.33E15, 5.30E15, 5.29E15,&
   5.18E15, 5.08E15, 5.00E15, 4.81E15, 4.57E15/)
!
! Declination is the angular distance of the sun north (+) or south (-)
! of the celestial equator. DECLIN is the declination of the sun  for the
! day of the month which gives mean values for the entire month
! (from Iqbal 1983:62). In degrees (for reference):
! real :: DECLIN(13) = (/ -20.84, -13.32, -2.40, 9.46, 18.78, 23.04, 21.11,
! 13.28, 1.97, -9.84, -19.02, -23.12, 0.00/)
! As radians N and S for use with Fortran standard cosine function:
real, parameter :: DECLIN(13) = &
   (/ -0.3637, -0.2325, -4.189E-02,  0.1651,  0.3278,  0.4021, &
       0.3684,  0.2318,  3.438E-02, -0.1717, -0.3320, -0.4035,  0.00/)

! Orbital eccentricity is the reciprocal of the square of the
! radius vector of the earth--the distance from the center of the
! earth to the center of the sun expressed in terms of the length
! of the semimajor axis of the earth's orbit.
! ECCEN is the eccentricity correction factor to correct for
! variation in the earth-sun distance. These values correspond, as
! above, to the days of characteristic declination (the day of the
! month giving mean monthly irradiance on a horizontal surface).
! Data from (Iqbal 1983, Table 1.2.1 on pp. 4-5)
real, parameter :: ECCEN(13) =  &
(/ 1.0340, 1.0260, 1.0114, 0.9932, 0.9780, 0.9694,&
   0.9674, 0.9754, 0.9902, 1.0082, 1.0240, 1.0326, 1.00/)

! IF construct to separate database and simulation calls:
Call_select: if (BATCH > 0) then
   ! Call for interactive database manipulation
   print = .true.
   if (PRSWG == 0 .and. MONTHG == 13) then
      MEAN = .true.
      NFIRST = 1
      NLAST = 12
      TAG = '*'
      NDAT = 13
      Single_table=.false.
      Average_table=.true.
   else
      MEAN = .false.
      NFIRST = MONTHG
      NLAST = MONTHG
      TAG = ' '
      NDAT = MONTHG
      Single_table=.true.
      Average_table=.false.
   endif
   NMON = NAMONG(MONTHG)
   ! Load character string for transmitting MONTHG to table headers
   write (KOUT,fmt='(I2)') MONTHG
   if (KOUT(1:1) == ' ') KOUT(1:1) = '0'
   ACCUM1 = 0.0 ! Zero accumulator vector

else Call_select
   ! Entry for simulation (Batch=0)
   NFIRST = NDAT
   NLAST = NDAT
   ! Now separate PRSWG cases:
   Print_select: if (PRSWG == 0) then
      MEAN = .true.
      if (NDAT == 12) then
         print = .true.
         Average_table = .true.
         Single_table = .false.
         TAG = '*'
         NMON = NAMONG(13)
         KOUT = '13'
      else
         print = .false.
         TAG = ' '
      endif
   else Print_select ! PRSWG=1; print all tables
      Mode_select: if (MODEG == 3) then
         MEAN = .true.
         print = .true.
         if (NDAT == 12) then
            Average_table = .true.
         else
            Average_table = .false.
         endif
         Single_table  = .true.
         TAG = ' '
         NMON = NAMONG(NDAT)
         ! Load character string for transmitting NDAT to table headers
         write (KOUT,fmt='(I2)') NDAT
         if (KOUT(1:1) == ' ') KOUT(1:1) = '0'
      else Mode_select ! MODES 1 and 2
         MEAN = .false.
         print = .true.
         Single_table = .true.
         Average_table = .false.
         TAG = ' '
         NMON = NAMONG(NDAT)
         ! Load character string for transmitting NDAT to table headers:
         write (KOUT,fmt='(I2)') NDAT
         if (KOUT(1:1) == ' ') KOUT(1:1) = '0'
      end if Mode_select
   end if Print_Select
end if Call_select

Block_loop: do NBLOC = NFIRST, NLAST
! Check for bad value of elevation:
if ((-100.0 .GreaterThan. ELEVG) .or. (ELEVG .GreaterThan. 5930.0)) then
   ! Inappropriate value for elevation--set to sea level,
   ! report problem, and continue
   write (stdout,fmt='(/A,1PG12.6,A,3(/A))')&
      ' The elevation given for this location (',ELEVG,' meters) has been',&
      ' reset to sea level. ELEVG must be in the range -100 to 5930 m. (The',&
      ' crater lake on Lincancabur in the Andes is, at 5930 m, the highest',&
      ' body of water in the world (The Sciences 24(1):27, 1984).'
   ELEVG = 0.0
end if
YHI = ELEVG/1000. ! Convert elevation (m) to km
! Compute correction factors for ground station elevation:
! a. Compute effect on Rayleigh scattering (air pressure):
NHI(1) = 1.437/(0.437+exp(YHI/6.35))
! b. Compute ground station elevation effect on aerosol optical depth
! (This is GCS "average aerosols")
NHI(2) = (.8208/(EXP(YHI/.952)-.145))&
 + (4.0202724E-02/(1.+EXP((YHI-16.33)/3.09)))
! c. Compute ground station elevation corrector for ozone:
NHI(3) = (0.13065/(2.35+exp(YHI/2.66)))+(0.970902341/(1.0+&
   exp((YHI-22.51)/4.92)))

! Load pointer (I2) for parameters for computing aerosol properties
select case (AIRTYG(NBLOC))     ! according to air mass type
case ('R'); I2 = 1              ! (R)ural
case ('U'); I2 = 2              ! (U)rban
case ('M'); I2 = 3              ! (M)aritime
case ('T'); I2 = 4              ! (T)ropospheric
case default             ! If a faulty value was entered for the airmass type,
   write (stdout,fmt='(/A/A/)')&  ! report the error
      ' Warning: Air mass type of "'//AIRTYG(NBLOC)//'" is not appropriate.',&
      ' AIRTY has been defaulted to "R" (Rural).'
   I2 = 1
   AIRTYG(NBLOC) = 'R'                  ! default to "rural," and continue ...
end select

! Convert latitude to radians, after data check
if (abs(LATG) .GreaterThan. 66.5) then
   ! Latitude has bad value, default to 40 N or S and go on:
   write (stdout,fmt='(A,1PG9.3,A,/A)')&
   ' System latitude was entered as ',LATG,' degrees. The method used by',&
   ' EXAMS to compute daylength is not appropriate for polar latitudes;'
   LATG = sign(40.0,LATG)
   if (LATG .GreaterThan. 0.0) then
      write (stdout,fmt='(A,/)')&
      ' LATG has been defaulted to 40.0 degrees North latitude.'
   else
      write (stdout,fmt='(A,/)')&
      ' LATG has been defaulted to 40.0 degrees South latitude.'
   endif
end if
LATL = LATG*0.01745
! Compute constants in equation of time
SLSD = sin(LATL)*sin(DECLIN(NBLOC))
CLCD = cos(LATL)*cos(DECLIN(NBLOC))
! From date and location, compute time (in sec: 13751 s/radian)
! from noon to nightfall:
TNIGHT = 13751.*acos(-(tan(LATL)*tan(DECLIN(NBLOC))))
! Check on relative humidity
if (RHUMG(NBLOC) .GreaterThan. 99.0) &
      RHUMG(NBLOC) = 99.0 ! Data base only goes to 99% R.H.
! Relative humidity negative, default to 50% ...
if (RHUMG(NBLOC) .LessThan. 0.0) then
   TEMP = RHUMG(NBLOC) ! save value for notifying user
   RHUMG(NBLOC) = 50.0 ! set R.H. to default and report change
   write (stdout,fmt='(A,I2,A/A,1PG11.4,/A,0PF5.1,A)')&
   '" "//trim(NAMONG(NBLOC))// relative humidity (RHUMG(',NBLOC,'))',&
   ' was entered as ',TEMP,&
   ' It has been defaulted to',RHUMG(NBLOC),'%.'
end if
! Convert relative humidity (%) to fraction:
RHUML = RHUMG(NBLOC)/100.
! Compute relative humidity component of aerosol extinction coefficient
if (RHUML .GreaterThan. 0.0) then
   EXPARG = (1./RHUML)**3
   ELAM0R = ELAM0(I2)*(1.+((KAER(I2)*(exp(-EXPARG)))/((1.-RHUML)**PAER(I2))))
   LAMAR  = LAMA0(I2)*(1.+((CAPEL(I2)*RHUML)/((1.-RHUML)**PAER(I2))))
else
   ELAM0R = ELAM0(I2) ! i.e., for RH=0, other terms drop out
   LAMAR  = LAMA0(I2)
endif

Wavelengths: do LAMBDA = 1, 46
   ! Computation of irradiance at the water surface:
   ! Compute aerosol extinction coefficients (function of relative
   ! humidity (ELAM0R and LAMAR calculated above) and wavelength):
   EXTAER(LAMBDA) = ELAM0R*exp(-(((CENLAM(LAMBDA)/1000.)-0.3)/LAMAR))
   ! Compute beam reflection for normal incidence and Brewster's Law:
   ! a. normal incidence:
   S1 = REFIND(LAMBDA)-1.0
   S2 = REFIND(LAMBDA)+1.0
   REFRAT = (S1*S1)/(S2*S2)
   ! b. now calculate Brewster's Law (for use when (i+j) = 90 degrees):
   S1 = REFIND(LAMBDA)*REFIND(LAMBDA)
   S2 = (S1-1.0)/(S1+1.0)
   BREW = S2*S2/2.0
   ! Compute optical depths:
   ! Atmosphere--Rayleigh scattering:
   RAYDEP(LAMBDA) = RAYFAC(LAMBDA)*NHI(1)
   ! Aerosol optical depth: product of extinction coefficient and
   ! "equivalent aerosol layer thickness (km)" (Green & Schippnick)
   AERDEP(LAMBDA) = EXTAER(LAMBDA)*NHI(2)*ATURBG(NBLOC)
   ! Ozone optical depth:
   OZDEP(LAMBDA) = NHI(3)*K3(LAMBDA)*OZONEG(NBLOC)
   ! Compute sunlight at top of atmosphere:
   HLAM(LAMBDA) = SUNIN(LAMBDA)*ECCEN(NBLOC)
   ! Compute solar beam for overhead sun:
   EXPARG = RAYDEP(LAMBDA)+AERDEP(LAMBDA)+OZDEP(LAMBDA)
   HIBEAM = HLAM(LAMBDA)*exp(-EXPARG)
   ! Compute "M" function for skylight:
   TAU4 = ABFRAC(LAMBDA)*AERDEP(LAMBDA)
   TAU2 = (1.0-ABFRAC(LAMBDA))*AERDEP(LAMBDA)
   FA3 = 1.0/(1.0+(0.2864*(OZDEP(LAMBDA)**.8244))*(OZONEG(NBLOC)**0.4166))
   FA4 = 1.0/(1.0+2.662*TAU4)
   F1 = 0.8041*(RAYDEP(LAMBDA)**1.389)*FA3
   F2 = 1.437*(TAU2**1.12)
   EMM = FA4*(F1+F2*(1.+F1))
   ! Combine "M" function and vertical beam for transfer to integrator
   EMMHI = EMM*HIBEAM
   ! Compute reflectivity function AIREFL:
   FB3 = 1./(1.+(.2797*(OZDEP(LAMBDA)**.8404))*(OZONEG(NBLOC)**0.1728))
   FB4 = 1./(1.+3.70*TAU4)
   F1 = 0.4424*(RAYDEP(LAMBDA)**.5626)*FB3
   F2 = 0.100*(TAU2**0.878)
   AIREFL = FB4*(F1+F2)
   ! Prepare computational sections of skylight function for integrator
   TTEE = 0.0266-0.00331*YHI
   G3T3 = -OZDEP(LAMBDA)
   GT1GT2 = -(0.5346*RAYDEP(LAMBDA)+0.6077*TAU2)
   EFF = 1.0/(1.0+84.37*((OZDEP(LAMBDA)+TAU4)**0.6776))
   ONEFF = 1.-EFF
   ! Call integration routine to compute irradiance delivered between
   ! local noon and nightfall (method is 11-point quadrature)
   TIMER = 0.0
   TINCRL = TNIGHT/5.0
   call SOLFCT (TIMER,YTEMP,GLOLIT)
   XINT(6) = TNIGHT
   YINT(6) = GLOLIT
   do N2 = 1, 5
      TIMER = TIMER+TINCRL
      call SOLFCT (TIMER,YTEMP,GLOLIT)
      XINT(6+N2) = TIMER+TNIGHT
      XINT(6-N2) = TNIGHT-TIMER
      YINT(6+N2) = GLOLIT
      YINT(6-N2) = GLOLIT
   end do
   ! Convert results of integration to daily means.
   WLAML(LAMBDA) = sngl(DINTPT(ELEVEN,XINT,YINT)/86400.)
end do Wavelengths

if (MEAN) then ! Load accumulator/printer
   ACCUM1(1) = ACCUM1(1)+OXRADG(NBLOC)
   ACCUM1(2) = ACCUM1(2)+RAING(NBLOC)
   ACCUM1(3) = ACCUM1(3)+CLOUDG(NBLOC)
   do II = 4, 49
      ACCUM1(II) = ACCUM1(II)+WLAML(II-3)
   end do
   ACCUM1(50) = ACCUM1(50)+OZONEG(NBLOC)
   ACCUM1(51) = ACCUM1(51)+ATURBG(NBLOC)
   ACCUM1(52) = ACCUM1(52)+RHUMG(NBLOC)
endif
end do Block_loop

if (.not.print) return

! Compute mean values if appropriate
!if ((MEAN) .or. (MODEG == 3 .and. PRSWG == 1 .and. NDAT == 12)) then
if (Average_table) then
   ACCUM1 = ACCUM1/12.
   ! Transfer mean values to sector 13 of database:
   OXRADG(13) = ACCUM1(1)
   RAING(13) = ACCUM1(2)
   CLOUDG(13) = ACCUM1(3)
! Transfer average WLAML to working storage when RUN command
! specifies PRSWG of 1, MODE 1 or 2, and MONTHG 13:
if (BATCH==0 .and. PRSWG==1 .and. MODEG<3 .and. MONTHG==13) &
   WLAML(1:46) = ACCUM1(4:49)
   OZONEG(13) = ACCUM1(50)
   ATURBG(13) = ACCUM1(51)
   RHUMG(13) = ACCUM1(52)
endif   

if (Single_table .and. RPTFIL) then
   ! Section for printing specific global environmental input parameters
   write (RPTLUN,5060) CCHAR(BATCH+1),VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5070) ! dashed line
   write (RPTLUN,5080) KOUT,NMON,TAG
   write (RPTLUN,5070) ! dashed line
   write (RPTLUN,5090) OXRADG(NDAT),RAING(NDAT),CLOUDG(NDAT),LATG
   write (RPTLUN,5100) OZONEG(NDAT),ATURBG(NDAT),RHUMG(NDAT),LONGG
   write (RPTLUN,fmt='(A,F7.1,A)')&
      ' ELEV (m):',ELEVG,'    Air mass type: '//AIRTYG(NDAT)
   ! Write out solar irradiance (mutiply to convert photons/cm2/s/N nm
   ! to milli-Einstiens/cm2/day for the waveband -- divide W(lambda)
   ! by Avogadro's number (6.02205E23); multiply by 86,400 sec/day,
   ! times 1000 for milli-Einsteins
   write (RPTLUN,5120) ((WLAML(I)*1.4347E-16),I=1,4)
   write (RPTLUN,5130) &
      ((WLAML(I)*1.4347E-16),I=5,35),&
        WLAML(36)*1.75*1.4347E-16,&
      ((WLAML(I)*2.5*1.4347E-16),I=37,43),&
        WLAML(44)*3.75*1.4347E-16,&
      ((WLAML(I)*5.0*1.4347E-16),I=45,46)
   write (RPTLUN,5070) ! dashed line
end if

if (Average_table .and. RPTFIL) then
   if (Single_table) then ! arriving via special case of Mode3/PRSW1
      TAG = '*'           ! In this special case, reset TAG, etc.
      NMON = NAMONG(13)   ! Note that for PRSW=1, Mode 1/2, Month 13,
      KOUT = '13'         ! we do NOT want TAG = '*', hence this treatment
   endif
   ! Section for printing average global environmental input parameters:
   write (RPTLUN,5060) CCHAR(BATCH+1),VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5070) ! dashed line
   write (RPTLUN,5080) KOUT,NMON,TAG
   write (RPTLUN,5070) ! dashed line
   write (RPTLUN,5090) (ACCUM1(I),I=1,3),LATG
   write (RPTLUN,5100) (ACCUM1(I),I=50,52),LONGG
   ! Load the report vector with the airmass types
   AIRVEC = ' ' ! Blank vector of air mass types
   Checked = 0  ! Counter for vector of air mass types
   Load_vector: do I3 = 1, 4    ! 4 air mass types are available for use
      Month_loop: do J2 = Checked+1,12
         Checked = Checked + 1
         Do K = I3-1,1,-1
            if (AIRVEC(K) == AIRTYG(J2) ) &    ! Already present, so
               cycle Month_loop                ! test the next month.
         end do                                ! Not yet reported, so
         AIRVEC(I3) = AIRTYG(J2)               ! load output vector and
         cycle Load_vector                     ! move to next element.
      end do Month_loop
   end do Load_vector      
   write (RPTLUN,fmt='(A,F7.1,A,4(" ",A1))')&
      ' ELEV (m):',ELEVG,'    Air mass type(s):',AIRVEC
   ! Write out solar irradiance as milliEinsteins/cm2/day
   write (RPTLUN,5120) (ACCUM1(I)*1.4347E-16,I=4,7)
   write (RPTLUN,5130) &
      ((ACCUM1(I)*1.4347E-16),I=8,38),&
        ACCUM1(39)*1.75*1.4347E-16,&
      ((ACCUM1(I)*2.5*1.4347E-16),I=40,46),&
        ACCUM1(47)*3.75*1.4347E-16,&
      ((ACCUM1(I)*5.0*1.4347E-16),I=48,49)

   write (RPTLUN,5070) ! dashed line
   if (TAG == '*') write (RPTLUN,fmt='(A)')&
      ' '//TAG//' Average of 12 monthly mean values.'
endif

return

! Collected format statements
5060 format (A1,'Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2/' Ecosystem: ',A)
5070  format (1X,77('-')) ! format for dashed line
5080 format (' Table 11.',A2,'.  ',A4,' environmental data: ',&
   ' global parameters.',A1)
5090 format (' OXRAD (M)',1PG9.2,' RAIN(mm/mo)',0PF6.1,'   CLOUD ',F7.2,&
   ' LAT  ',F6.1)
5100 format (' OZONE(cm)',F6.3,'    ATURB(km)',F5.2,'      RHUM(%)',F6.1,&
   ' LONG ',F6.1)
5120  format (' WLAM, mE/cm2/day: ',1PG10.3,3(G10.3))
5130 format (1X,1PG10.3,G10.3,G10.3,G10.3,G10.3,G10.3)
end Subroutine SOLAR
