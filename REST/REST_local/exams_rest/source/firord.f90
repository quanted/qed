subroutine FIRORD
! Created August 1979 by L.A. Burns
! Revised 17-JAN-1986 (LAB)
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 05-Feb-1999 to use floating point comparisons
! Revised April 2001 to support dynamic memory allocation
! Revised April 2002 to support optional printing of report.xms
! Revised March 2004 to repair minor bug in report.xms printer controls
use Implementation_Control
! FIRORD reduces the kinetic behavior of chemicals to pseudo-first-order form
! by coupling characteristics of the chemical and the environment. If the
! input data permits, the properties of the chemical are adjusted to reflect
! the effect of temperature in each physical element of the system. The
! pseudo-first-order reaction rate constants are computed from the interactive
! effects of partitioning, temperature, and other characteristics of the
! environment for each species or form. FIRORD also converts the input
! loadings and advective and dispersive flow field to pseudo-first-order
! effects on chemical concentrations, and writes both a kinetic profile of the
! chemical and a chemical reactivity profile of the system to LUN RPTLUN.
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Process_Controls
use Floating_Point_Comparisons
use Table_Variables
Implicit None
! Local variables
logical :: test
real :: OUT(9)
real, parameter :: LN_TWO =  0.69314718
! OUT is an I/O control vector, LN_TWO is natural log of 2.
! Exports from compartments that do not leave the ecosystem
real :: INTOUL(KOUNT), KO2L(KOUNT), FACTOR
real, dimension(KOUNT) :: LIGHTL
! INTOUL holds exports from segments that recirculate, that is,
! removals that leave one segment and then enter another.
! KO2L is local value of reaeration rate for FIRORD and VOLAT
! LIGHTL is average light intensity for output tables; set = IOUT
integer :: I, IOUT, J, K, N1
integer :: IEND ! IEND supresses printing of zero values of REDAG
logical :: print
character(len=78) :: outlin
character(len=2),dimension(2) :: kout_local
! kout_local for character representation of number of chemical, month.
character(len=3) asterisk  ! asterisk is * for footnote
character :: BLANK = ' '
character (len=64) :: T12ColHead1 = &
'Seg  T*    Local pseudo-first-order process half-lives (hours)'
character (len=65) :: T12ColHead2 = &
' #   y    Biolysis  Photol   Oxidat   Hydrol   Reduct   Volatil'
character (len=74) :: T13_Col1 = &
'Seg  T*   pH   pOH  Temp  Piston  Mean   Bact.   Oxidant  Singlet  Reduct.'
character (len=74) :: T13_Col2 = &
' #   y              Deg.  Veloc.  Light  Popn.    Conc.   Oxygen   (REDAG)'
character (len=73) :: T13_Col3 = &
'     p               C.    m/hr     %    cfu/**   Molar    Molar    Molar'

! Set indicator for table printing
print = (.not. (PRSWG == 0 .and. NDAT /= 12))
if (.not. RPTFIL) print=.false.
! Set indicator that average values are to be computed
MEAN = (PRSWG == 0 .or. MODEG == 3)
! When printing tables, set up headings and footnotes
Header_setup: if (print) then
   if (.not.(PRSWG==1 .and. MODEG==3) .and. MEAN) then
      asterisk = '***'
      NMON = NAMONG(13)
      kout_local(2) = '13'
   else
      asterisk = '   '
      NMON = NAMONG(NDAT)
      write (kout_local(2),fmt='(I2.2)') NDAT
   endif
end if Header_setup
! Initialize flags for monitoring calls to photolysis routines
JSAV1 = 0; JSAV2 = 0; ICALL = 0; SINCAL = 0
YIELDL = 0.0D+00 ! Set local matrix YIELDL to zero
! Zero LIGHTL and convert WLAML for processing
LIGHTL = 0.0 ! Zero average local light intensity
! In this code sector the light field at the water surface
! is adjusted for effects of cloudiness and for the wavelength
! intervals (e.g. for 750 nm, the initial datum is per 10 nm, but
! the total wavelength interval is 50 nm, thus the 5* correction)
! All the computations incorporate a linear numerical conversion
! factor with several components; this factor is pre-computed at
! this point and the local values for overall light intensity are
! pre-multiplied by the factor.
  FACTOR = 1.3764E-17 * (1.0-0.056*CLOUDG(NDAT))
! FACTOR = 2.3026*1000.*3600.*(1.0 - 0.056*CLOUDG)/6.022E+23
!          ln 10. ml/L  sec/hr                    Avogadro's #
! Natural log of 10. = 2.3026 (conversion of decadic molar
! extinction coefficients for chemical to Naperian basis). Factor
! of 1000.0 corrects volume units (light is /sq.cm., chemical's
! absorption is /cm, outcome is on a cc. volumetric basis,
! multiplied by 1000. cc/liter). Division by Avogadro's number
! (6.022E+23) converts photons to "molar" basis.
! Cloudiness correction is conventional Buttner method.
WLAML(1:35) = WLAML(1:35)*FACTOR
WLAML(36) = WLAML(36)*1.75*FACTOR
WLAML(37:43) = WLAML(37:43)*2.5*FACTOR
WLAML(44) = WLAML(44)*3.75*FACTOR
WLAML(45) = WLAML(45)*5.0*FACTOR
WLAML(46) = WLAML(46)*5.0*FACTOR
! Initialize process rate constant matrices to zero
BIOLKL = 0.0; HYDRKL = 0.0; OXIDKL = 0.0; PHOTKL = 0.0
REDKL = 0.0;  S1O2KL = 0.0; VOLKL  = 0.0

Chemicals: do K = 1, KCHEM ! Begin loop on all active chemicals
! Load character string for transmitting K to table headers
write (kout_local(1),fmt='(I2.2)') K
KDPL = 0.0  ! Zero the matrix of photochemical light absorption coefficients
call DATACK (K) ! Evaluate input data. If only one chemical is being studied
if (KCHEM == 1) PRODSW = .false. ! disregard the product chemistry
Print_page_head: if (print) then ! Print if ready
   ! Write page header for tables of pseudo-first-order kinetics
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5010) trim(CHEMNA(K))
   write (RPTLUN,5020) ! dashed line
   ! Write column headings for table of pseudo-first-order kinetics
   write (RPTLUN,5050) kout_local(1),kout_local(2),NMON,asterisk
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt=ColumnLabels) T12ColHead1,T12ColHead2
   write (RPTLUN,5020) ! dashed line
end if Print_page_head

! Calculate pseudo-first-order rate constants etc. for
! printing kinetics table and for computations
if (PHOTSW) call SUNLYS (LIGHTL,K) ! Photochemical processes
! SUNLYS should be called at least once to generate LIGHTL
if (K == KCHEM .and. ICALL == 0) call SUNLYS (LIGHTL,K)
if (HYDRSW) call HYDLYS (K) ! Hydrolytic transformations
if (REDSW) call REDUCT (K)  ! Reductive transformations
if (BIOSW) call BIOLYS (K)  ! Biotransformations
if (VOLSW .or. K == KCHEM) call VOLAT (KO2L,K) ! Volatilization
! VOLAT called at least once to compute local, temperature
! corrected value of reaeration coefficient (KO2) for liquid-phase
! resistance, so that "Canonical Profile" table will not have zero
! KO2 for compounds that do not volatilize.
call TRANSP (INTOUL,K) ! Transport processes

Segments1: do J = 1, KOUNT
! Compute total pseudo-first-order rate coefficient
TOTKL(J,K) = 0.0D+00 ! Load upper bytes of TOTKL with zero
TOTKL(J,K) = (EXPOKL(J,K)+INTOUL(J))/WATVOL(J)+VOLKL(J,K)+PHOTKL(J,K)+&
   BIOLKL(J,K)+OXIDKL(J,K)+HYDRKL(J,K)+S1O2KL(J,K)+REDKL(J,K)
Add_data: if (MEAN) then ! Add data into accumulators
   ACCUM2(1,J,K) = ACCUM2(1,J,K)+BIOLKL(J,K)
   ACCUM2(2,J,K) = ACCUM2(2,J,K)+PHOTKL(J,K)
   ACCUM2(3,J,K) = ACCUM2(3,J,K)+OXIDKL(J,K)+S1O2KL(J,K)
   ACCUM2(4,J,K) = ACCUM2(4,J,K)+HYDRKL(J,K)
   ACCUM2(5,J,K) = ACCUM2(5,J,K)+REDKL(J,K)
   ACCUM2(6,J,K) = ACCUM2(6,J,K)+VOLKL(J,K)
   ! Compute average values if needed...
   ! When Mode 3/Prsw 1, when all months processed (ndat=12), then
   ! compute mean values...note that to get here, mean must be .true.
   if (print .and. NDAT == 12) ACCUM2(:,J,K) = ACCUM2(:,J,K)/12.
end if Add_data
! If time to print, output the table
Table_print: if (print) then ! Load output vector
   Table_flavor: if ((.not.MEAN) .or. (PRSWG == 1 .and. MODEG == 3)) then
      OUT(1) = BIOLKL(J,K) ! Load output vector with individual values
      OUT(2) = PHOTKL(J,K)
      OUT(3) = OXIDKL(J,K)+S1O2KL(J,K)
      OUT(4) = HYDRKL(J,K)
      OUT(5) = REDKL(J,K)
      OUT(6) = VOLKL(J,K)
      do I = 1, 6
         if (OUT(I) .NotEqual. 0.0) OUT(I) = LN_TWO/OUT(I)
      end do
   else ! calculate from accumulated values
      do I = 1, 6
         if (ACCUM2(I,J,K) .Equals. 0.0) then
            OUT(I) = 0.0
         else
            OUT(I) = LN_TWO/ACCUM2(I,J,K)
         endif
      end do
   end if Table_flavor
   ! Write line to internal file
   write (OUTLIN,OUTLIN_Format) J,TYPEG(J),(OUT(I),I=1,6)
   N1 = 1 ! Blank out inactive processes
   do I = 11+Offset, 56+Offset, 9
      if (OUT(N1) .Equals. 0.0) OUTLIN(I:I+8) = '         '
      if (OUTLIN(I+5:I+8) == 'E+00') OUTLIN(I+5:I+8) = '    '
      N1 = N1+1
   end do
   write (RPTLUN,fmt=LineFormat) trim(OUTLIN)
end if Table_print
end do Segments1 ! End of segment loop

if (print) then ! If printing
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,5030) ! print footnotes to table
   if (asterisk(1:1) == '*') write (RPTLUN,5100) BLANK,asterisk
end if

! Section for computing product chemistry
if (PRODSW) call TRPROD (K)
! Special section for printing average value table when PRSWG=1 and MODEG=3
if (.not. (PRSWG == 1 .and. MODEG == 3 .and. NDAT == 12)) cycle Chemicals
! If, hoever, the report file is not being printed, skip ...
if (.not. print) cycle chemicals
asterisk = '***'
NMON = NAMONG(13)
! Write page header for tables of pseudo-first-order kinetics
write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
write (RPTLUN,5010) trim(CHEMNA(K))
write (RPTLUN,5020) ! dashed line
! Load character string for transmitting month to table headers
kout_local(2) = '13'
write (RPTLUN,5050) kout_local(1),kout_local(2),NMON,asterisk
write (RPTLUN,5020) ! dashed line
write (RPTLUN,fmt=ColumnLabels) T12ColHead1,T12ColHead2
write (RPTLUN,5020) ! dashed line

Segments2: do J = 1, KOUNT
   do i=1,6
      if (ACCUM2(i,J,K) .Equals. 0.0) then
         OUT(i) = 0.0
      else
         OUT(i) = LN_TWO/ACCUM2(i,J,K)
      end if
   end do
   ! Write line to internal file
   write (OUTLIN,OUTLIN_Format) J,TYPEG(J),(OUT(I),I=1,6)
   N1 = 1 ! Blank out inactive processes
   do I = 11+Offset, 56+Offset, 9
      if (OUT(N1) .Equals. 0.0) OUTLIN(I:I+8) = '         '
      if (OUTLIN(I+5:I+8) == 'E+00') OUTLIN(I+5:I+8) = '    '
      N1 = N1+1
   end do
   write (RPTLUN,fmt=LineFormat) trim(OUTLIN)
end do Segments2

write (RPTLUN,5020) ! dashed line
write (RPTLUN,5030)
write (RPTLUN,5100) BLANK,asterisk
! Restore December values
asterisk = '   '
NMON = NAMONG(12)
kout_local(2) = '12'
end do Chemicals ! End of loop on chemicals

! If computing average values, skip table until time to print
Table_head: if (print) then
   ! Print chemical reactivity profile of environment in report
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,5110) kout_local(2),NMON,asterisk ! Set up table for report
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt=ColumnLabels) T13_Col1,T13_Col2,T13_Col3
   write (RPTLUN,5020) ! dashed line 
end if Table_head

Segments3: do J = 1, KOUNT
! Fail-safe load of null values in bacterial population densities
if (TYPEG(J) /= 'B') BNBACG(J,NDAT) = 0.0
if (TYPEG(J) == 'B') BACPLG(J,NDAT) = 0.0
Accumulate: if (MEAN) then
ACCUM3(1,J) = ACCUM3(1,J)+10.**(-PHG(J,NDAT))
ACCUM3(2,J) = ACCUM3(2,J)+10.**(-POHG(J,NDAT))
ACCUM3(3,J) = ACCUM3(3,J)+TCELG(J,NDAT)
ACCUM3(4,J) = ACCUM3(4,J)+KO2L(J)
ACCUM3(5,J) = ACCUM3(5,J)+LIGHTL(J)*100. ! Convert light index to percenasteriske
if (TYPEG(J) /= 'B') then
   ACCUM3(6,J) = ACCUM3(6,J)+BACPLG(J,NDAT)
else
   ACCUM3(6,J) = ACCUM3(6,J)+BNBACG(J,NDAT)
endif

ACCUM3(7,J) = ACCUM3(7,J)+OXRADL(J)
ACCUM4(1,J) = ACCUM4(1,J)+S1O2L(J)
ACCUM4(2,J) = ACCUM4(2,J)+REDAGG(J,NDAT)
! Compute averages if need be
Calculate: if (MEAN.and.print .and. NDAT == 12) then
! Also, for mode 3/prsw 1 skip until complete full year
ACCUM3(1,J) = -alog10(ACCUM3(1,J)/12.) ! Average values
ACCUM3(2,J) = -alog10(ACCUM3(2,J)/12.)
do I = 3, 7
   ACCUM3(I,J) = ACCUM3(I,J)/12.
end do
ACCUM4(1,J) = ACCUM4(1,J)/12.
ACCUM4(2,J) = ACCUM4(2,J)/12.
! Transfer mean values to sector 13 of database
PHG(J,13)   = ACCUM3(1,J)
POHG(J,13)  = ACCUM3(2,J)
TCELG(J,13) = ACCUM3(3,J)
if (TYPEG(J) /= 'B') then
   BACPLG(J,13) = ACCUM3(6,J)
else
   BNBACG(J,13) = ACCUM3(6,J)
endif
REDAGG(J,13) = ACCUM4(2,J)
end if Calculate
end if Accumulate
! If not time to print, simply increment segment loop
if (.not.print) cycle Segments3
! Transfer data to output vectors
if (PRSWG == 0) then
   do I = 1, 7
      OUT(I) = ACCUM3(I,J)
   end do
   IOUT = int(OUT(5))
   OUT(8) = ACCUM4(1,J)
   OUT(9) = ACCUM4(2,J)
else
   OUT(1) = PHG(J,NDAT)
   OUT(2) = POHG(J,NDAT)
   OUT(3) = TCELG(J,NDAT)
   OUT(4) = KO2L(J)
   OUT(5) = LIGHTL(J)*100.
   IOUT = int(OUT(5))
   if (TYPEG(J) /= 'B') then
      OUT(6) = BACPLG(J,NDAT)
   else
      OUT(6) = BNBACG(J,NDAT)
   endif
   OUT(7) = OXRADL(J)
   OUT(8) = S1O2L(J)
   OUT(9) = REDAGG(J,NDAT)
endif
if (OUT(9) .Equals. 0.0) then
  IEND = 8              ! Set flag to omit zero values of REDAG
else
  IEND = 9
end if
! Separate Benthic and non-Benthic segments in output 
if (TYPEG(J) == 'B') then ! WRITE Benthic segments
 if (OUT(9) .GreaterThan. 0.0) then
  write (RPTLUN,T13F3) J,TYPEG(J),(OUT(I),I=1,3),OUT(6),OUT(9)
 else
  write (RPTLUN,T13F3) J,TYPEG(J),(OUT(I),I=1,3),OUT(6)
 endif
else ! Water column segments--skip volatility if no air/water interface
 ! Segment 1 is always a water column with an air/water interface.
 ! For segments >1, if the just prior segment is Benthic, then it has an
 ! if (J==1 .or. (J>1 .and. (TYPEG(J-1) == 'B'))) then ! air/water interface
 if (J==1) then      !2013-05-30
     test=.true.
 else 
     test=(TYPEG(J-1) == 'B')
 end if
 If (test) then
  write (RPTLUN,T13F1) J,TYPEG(J),(OUT(I),I=1,4),IOUT,(OUT(I),I=6,IEND)
 else    ! WRITE statment for water column segments without air/water
  write (RPTLUN,T13F2) J,TYPEG(J),(OUT(I),I=1,3),IOUT,(OUT(I),I=6,IEND)
 end if
end if
end do Segments3

! If not printing, skip footnotes
if (.not.print) return
! Write footnote to table
write (RPTLUN,5020) ! dashed line
write (RPTLUN,5030)
write (RPTLUN,5160)
BLANK = '*'
if (asterisk(1:1) == '*') write (RPTLUN,5100) BLANK,asterisk
BLANK = ' '
! Special section for table of average values when PRSWG=1 and MODEG=3
if (.not.(PRSWG == 1.and.MODEG == 3.and.NDAT == 12)) return
asterisk = '***'
NMON = NAMONG(13)
kout_local(2) = '13'
write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
write (RPTLUN,5020) ! dashed line
write (RPTLUN,5110) kout_local(2),NMON,asterisk ! Set up table for report
write (RPTLUN,5020) ! dashed line
write (RPTLUN,fmt=ColumnLabels) T13_Col1,T13_Col2,T13_Col3
write (RPTLUN,5020) ! dashed line

Segments4: do J = 1, KOUNT ! Segment loop
   OUT(1:7) = ACCUM3(1:7,J)
   IOUT = int(OUT(5))
   OUT(8) = ACCUM4(1,J)
   OUT(9) = ACCUM4(2,J)
   if (OUT(9) .Equals. 0.0) then
      IEND = 8
   else
      IEND = 9
   end if
   ! Write separate lines for Benthic segments and water column segments
   ! with/without air/water interface
   if (TYPEG(J) == 'B') then
      if (OUT(9) .GreaterThan. 0.0) then
         write (RPTLUN,T13F3) J,TYPEG(J),(OUT(I),I=1,3),OUT(6),OUT(9)
      else
         write (RPTLUN,T13F3) J,TYPEG(J),(OUT(I),I=1,3),OUT(6)
      endif
   elseif (J==1 .or. (J>1 .and. TYPEG(J-1)=='B')) then
      write (RPTLUN,T13F1)&
         J,TYPEG(J),(OUT(I),I=1,4),IOUT,(OUT(I),I=6,IEND)
   else
      write (RPTLUN,T13F2)&
         J,TYPEG(J),(OUT(I),I=1,3),IOUT,(OUT(I),I=6,IEND)
   endif
end do Segments4

! Write footnotes
write (RPTLUN,5020) ! dashed line
write (RPTLUN,5030)
write (RPTLUN,5160)
BLANK = '*'
write (RPTLUN,5100) BLANK,asterisk
BLANK = ' '

! Table headers, column heads, footnotes
5000 format('1Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode ',I0/' Ecosystem: ',A)
5010 format(' Chemical:  ',A)
5020 format(1X,77('-')) ! dashed line
5030 format('   * Segment types: Littoral, Epilimnetic, Hypolimnetic,',&
   ' Benthic')
5050 format(' Table 12.',A2,'.',A2,'.  ',A4,&
   ' kinetic profile of synthetic chemical,'/&
   ' computed from chemical and environmental reactivity data. ',A2)
5100 format(1X,A1,A2,' Average of 12 monthly mean values.')
5110 format&
   (' Table 13.',A2,'. ',A4,' chemical reactivity profile of ecosystem. ',A3)
5160 format&
   ('  ** Active bacterial populations as cfu/mL in water column, and',/&
    '     as cfu/100 g (dry weight) of sediments in benthic segments.')
end Subroutine FIRORD
