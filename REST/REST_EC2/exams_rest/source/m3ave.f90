subroutine M3AVE
! M3AVE computes and reports the average, maximum, and minimum concentrations
! of chemical during the course of a multi-year simulation. M3AVE also gives
! an element-by-element listing of the average concentrations and distribution
! of chemical throughout the ecosystem. M3AVE transmits tabular output to the
! file defined by Fortan Logical Unit Number RPTLUN, and writes to a plotting
! file defined by LUN SSLUN.
! Built 6-DEC-1983 (L.A. Burns) from AVEOUT.
! Revised 28-NOV-1985 (LAB) to accomodate IBM file structures.
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 11/16/88 to change file handling--added special
! sector for DSI; required because "endfile" has a bug.
! Revision 09-Feb-1999 to use Floating Point Comparison module
! Revisions April 2001 for wider format and dynamic memory allocation
! Revisions July 2001 to use "DaysInYear" as day counter for annual averages
use Floating_Point_Comparisons
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Table_Variables
use Statistical_Variables, Only: YMINLT, YBARLT, PEAKLT, MAXSEG, MINSEG,&
      DaysinYear
Implicit None
! Local variables for this subroutine
real :: OUTDAT(6), PERCET, TOTMAS
! ALPHA adresses of ionic species
integer, dimension(7) ::&
  IALPHA =(/25,21,17,1,5,9,13/) ! ALPHA adresses of ionic species
integer :: KKNTW, KKNTS
! KKNTW and KKNTS are integer versions of KOUNTW and KOUNTS
! for output to plot file.
integer :: File_Check ! receives iostat when opening ssout.plt
integer, dimension(2) :: IFIRST, ILAST
integer :: I,ICHEK,ISTART,J,K,K1,KK,IONTES,NNDAT,NTAB,NTABLE,N1,M1,M2
! KK runs the loop on chemicals
! IONTES counts the number of active ions
! NTABLE indicates the number of speciation tables required
logical :: MULTYR
! MULTYR indicates multi-year (.T.) or single-year (.F.) data.
character(len=1), dimension(5) :: NTYPX, NTYPN
! NTYPX and NTYPN register segment types in the SSOUT file.
character(len=1) :: STAR = '*' ! delimiter used in unformatted plotting files
character(len=4) :: YRCH(2)
character(len=78) :: OUTLIN
! YRCH are character strings for entering simulation years
! (e.g., 0001, 1984, etc.) in table headers.

PlotFiles: if (PLTFIL) then ! Identify information written to LUN SSLUN...
call Assign_LUN (SSLUN)
open (unit=SSLUN, status='REPLACE', access='SEQUENTIAL',&
      form='UNFORMATTED', position='REWIND', file='ssout.plt',&
      action='write', iostat=File_Check)
   if (File_Check /= 0) then
      write (stderr,fmt='(3(/A))') &
      ' Results file "ssout.plt" cannot be written.',&
      ' Possibly the file is write-protected, or the device may be full.',&
      ' Exams cannot run until the problem is repaired.'
      call Release_LUN (SSLUN)
      IFLAG = 8
      return
   end if
write (SSLUN) KCHEM,MODEG,KOUNT
do KK = 1, KCHEM
  write (SSLUN) CHEMNA(KK)
end do
write (SSLUN) ECONAM
end if PlotFiles

! Allow for single segment test runs -- fail-safe final check
if (KOUNTW .LessThanOrEqual. 0.0) KOUNTW = 1.0
if (KOUNTS .LessThanOrEqual. 0.0) KOUNTS = 1.0
! Load integer values of KOUNTW and KOUNTS
KKNTW = int(KOUNTW)
KKNTS = int(KOUNTS)

! Convert simulation years to character strings for output
MULTYR =  (LASTYR > FRSTYR) ! set flag for >1 year of output
! Load character string for transmitting year to table headers
write (YRCH(1),fmt='(I4)') FRSTYR
if (MULTYR) then
   write (YRCH(2),fmt='(I4)') LASTYR
   do K = 1, 2
      do I = 1, 4
         if (YRCH(K)(I:I) == ' ') YRCH(K)(I:I) = '0'
      end do
   end do
else ! a single year of output being processed
   do I = 1, 4
      if (YRCH(1)(I:I) == ' ') YRCH(1)(I:I) = '0'
   end do
endif
! Write average concentration (with name of chemical and ecosystem) to file
! for plotting concentration vs. ecosystem, and report to LUN RPTLUN.
Z = 0.0                     ! Zero "Z" matrix
Chemicals: do KK = 1, KCHEM ! Write one block (3 Tables) per chemical
   Z2 = 0.0
   ! compute mean concentrations
   Segments: do J = 1, KOUNT  ! do segments in numerical order
   if (TYPEG(J) /= 'B') then  ! water column segments
         ! dissolved
         Z(1,KK) = Z(1,KK)+VOLG(J)*YSUMS(29,J,KK)/DaysInYear
         ! sorbed mg/kg
         Z(2,KK) = Z(2,KK)+VOLG(J)*YSUMS(30,J,KK)/DaysInYear
         ! mass, kg (1.0E-06 kg/mg)
         Z(5,KK) = Z(5,KK)+YTOT(3,J,KK)/DaysInYear
      else                       ! bottom sediments
         ! mg/L dissolved
         Z(3,KK) = Z(3,KK)+VOLG(J)*YSUMS(29,J,KK)/DaysInYear
         ! sorbed mg/kg
         Z(4,KK) = Z(4,KK)+VOLG(J)*YSUMS(30,J,KK)/DaysInYear
         ! pollutant mass in kg (1.0E-06 kg/mg)
         Z(6,KK) = Z(6,KK)+YTOT(3,J,KK)/DaysInYear
      end if
   end do Segments
! compute averages in water column
   Z(1,KK) = Z(1,KK)/Total_Limnetic_Volume  ! mg/L  dissolved
   Z(2,KK) = Z(2,KK)/Total_Limnetic_Volume  ! mg/kg sorbed
   ! compute averages in bottom sediments
   Z(3,KK) = Z(3,KK)/Total_Benthic_Volume   ! mg/L dissolved
   Z(4,KK) = Z(4,KK)/Total_Benthic_Volume   ! mg/kg sorbed
   Reporting: if (RPTFIL) then
   ! write page header to LUN RPTLUN
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5010) trim(CHEMNA(KK))
   write (RPTLUN,5020) ! dashed line
   ! load character string for transmitting KK to table headers
   write (KOUT,fmt='(I2.2)') KK
   if (MULTYR) then
      write (RPTLUN,fmt='(A)') ' Table 15.'//KOUT//&
      '. Average distribution of chemical during '//YRCH(1)//'-'//YRCH(2)//'.'
   else
      write (RPTLUN,fmt='(A)') ' Table 15.'//KOUT//&
      '. Average distribution of chemical during '//YRCH(1)//'.'
   endif
   write (RPTLUN,5020) ! dashed line
   ! Set up table in LUN RPTLUN:
   write (RPTLUN,fmt=ColumnLabels)& ! Column headers for distribution
      'Seg   Resident Mass   ******** Chemical Concentrations *********',&
      ' #                      Total    Dissolved  Sediments    Biota',&
      '      Kilos      %       mg/*     mg/L **     mg/kg       ug/g',&
      '---  -------- ------  ---------  ---------  ---------  ---------',&
      '     In the Water Column:'
   end if Reporting

   ! Computations for segments--compute and print variables,
   ! accumulate data for mean values.
   Water_column: do J = 1, KOUNT
      if (TYPEG(J) == 'B') cycle Water_column   ! Skip sediment compartments
      ! Compute mass by system element (in kilograms)
      Z2(6) = YTOT(3,J,KK)/DaysInYear
      Z2(5) = 1.0E+03*Z2(6)/AREAG(J) ! Convert mass to grams/square meter
      Z2(7) = Z2(7)+Z2(5)            ! Accumulate for mean value
      if (Z(5,KK) .NotEqual. 0.0) then ! Calculate mass as percent of
         PERCET = Z2(6)*100.0/Z(5,KK)  ! total in water column, but
      else                             ! Allow for entry of some
         PERCET = 0.0                  ! compounds with zero loadings
      end if
      ! Total concentration (mg/L in water column)  
      Z2(1) = YTOT(1,J,KK)/DaysInYear
      Z2(8) = Z2(8)+VOLG(J)*Z2(1) ! Accumulate for mean value
      ! Free (dissolved) chemical in water column
      Z2(2) = YSUMS(29,J,KK)/DaysInYear
      ! Mean already available as Z(1,KK)
      ! Chemical sorbed on suspended sediments (mg/kg)
      Z2(3) = YSUMS(30,J,KK)/DaysInYear
      ! Mean already available as Z(2,KK)
      ! Chemical sorbed on biota (ug/g)
      Z2(4) = YSUMS(32,J,KK)/DaysInYear
      Z2(9) = Z2(9)+VOLG(J)*Z2(4)
      ! Write line to LUN RPTLUN
      if (RPTFIL) write (RPTLUN,Table15a_Format) J,Z2(6),PERCET,(Z2(I),I=1,4)
      ! Write line to LUN SSLUN
      if (PLTFIL) write (SSLUN) KK,J,TYPEG(J),Z2(5),Z2(6),PERCET,(Z2(I),I=1,4)
   end do Water_column   ! End of water column loop

   ! Mark plot file for end of water column values...
   ! Note--most of this line contains dummy values. "STAR" signals
   ! the end of the records; the other values merely let PLOT use a
   ! standard read.
   if (PLTFIL) write (SSLUN) KK,KKNTW,STAR,(Z(I,KK),I=1,6),Z2(1)
   ! Compute average values where needed
   Z2(7) = Z2(7)/KOUNTW  ! Mass (grams/square meter)
   Z2(8) = Z2(8)/Total_Limnetic_Volume  ! Total concentration
   Z2(9) = Z2(9)/Total_Limnetic_Volume  ! Biosorbed concentration
   if (Z(5,KK)+Z(6,KK) .NotEqual. 0.0) then    ! calculate water column mass
      PERCET = Z(5,KK)*100.0/(Z(5,KK)+Z(6,KK)) ! as % of total mass in system,
   else                    ! but allow for entry of some compounds
      PERCET = 0.0         ! with zero allocthonous loadings
   end if
   ! Write subtotal to LUN RPTLUN
   if (RPTFIL) write (RPTLUN,Table15b_Format) Z(5,KK),PERCET
   ! Benthic segments
   ! Label benthic section in LUN RPTLUN
   if (RPTFIL) write (RPTLUN,fmt='(/A)') '      and in the Benthic Sediments:'
   ! Computations for bottom sediments--compute and print
   ! variables, accumulate values for means.
   Benthic_segments: do J = 1, KOUNT
      if (TYPEG(J) /= 'B') cycle Benthic_segments ! Skip water column segments
      ! Compute mass (kilograms) by system element
      Z2(6) = YTOT(3,J,KK)/DaysInYear
      ! Convert mass to grams/square meter
      Z2(5) = 1.E+03*Z2(6)/AREAG(J)
      ! Accumulate for average
      Z2(10) = Z2(10)+Z2(5)
      ! Calculate mass as a percentage of total in bottom sediments.
      ! Allow for entry of some compounds with zero allocthonous loadings
      if (Z(6,KK) .NotEqual. 0.0) then
         PERCET = Z2(6)*100./Z(6,KK)
      else
         PERCET = 0.0
      end if
      Z2(1) = YTOT(2,J,KK)/DaysInYear ! Total concentration, mg/kg
      Z2(11) = Z2(11)+VOLG(J)*Z2(1)       ! Accumulate for average value
      ! No percentages
      ! Free (dissolved) chemical in bottom sediments
      ! (mg/L of interstitial water)
      Z2(2) = YSUMS(29,J,KK)/DaysInYear
      ! Mean already available as Z(3,KK)
      ! Sorbed on bottom sediments
      Z2(3) = YSUMS(30,J,KK)/DaysInYear
      ! Mean value already available as Z(4,KK)
      ! Chemical sorbed on benthic organisms (ug/g)
      Z2(4) = YSUMS(32,J,KK)/DaysInYear
      ! Accumulate sum for mean value
      Z2(12) = Z2(12)+VOLG(J)*Z2(4)
      ! Write line to LUN RPTLUN
      if (RPTFIL) write (RPTLUN,Table15a_Format) J,Z2(6),PERCET,(Z2(I),I=1,4)
      ! Write line to LUN SSLUN
      if (PLTFIL) write (SSLUN) KK,J,TYPEG(J),Z2(5),Z2(6),PERCET,(Z2(I),I=1,4)
   end do Benthic_segments ! End of bottom sediment loop.

   ! Mark plot file for end of bottom sediments
   ! Note--most of this line contains dummy values. "STAR" signals the end of
   ! the records; the other values merely let PLOT use a standard read.
   if (PLTFIL) write (SSLUN) KK,KKNTS,STAR,(Z(I,KK),I=1,6),Z2(1)
   ! Compute averages where needed
   Z2(10) = Z2(10)/KOUNTS ! Mass (grams/square meter)
   Z2(11) = Z2(11)/Total_Benthic_Volume ! Total concentration
   Z2(12) = Z2(12)/Total_Benthic_Volume ! Benthos biosorbed concentration
   ! Bottom sediment mass as percent of total mass
   ! Allow for entry of some compounds with no allocthonous loadings
   if (Z(5,KK) + Z(6,KK) .NotEqual. 0.0) then
      PERCET = Z(6,KK)*100./(Z(5,KK)+Z(6,KK))
   else
      PERCET = 0.0
   end if
   ! Write subtotal to LUN RPTLUN
   if (RPTFIL) then
      write (RPTLUN,Table15b_Format) Z(6,KK),PERCET
      TOTMAS = Z(5,KK)+Z(6,KK)           ! Write total mass to LUN RPTLUN
      write (RPTLUN,fmt='(A,1PG11.4)')&
         ' Total Mass (kilograms) =   ',TOTMAS
      write (RPTLUN,5020) ! dashed line
      write (RPTLUN,5160) ! Write footnotes to table
   end if
   ! Write out table detailing aqueous speciation
   ! Test for number of active chemical species
   IONTES = sum(SPFLGG(:,KK))
   NTABLE = 1
   if (IONTES > 4) NTABLE = 2
   ! Detect the starting point for the ion sequence
   ISTART = 0
   Ion_start: do
      do ICHEK = 7, 5, -1
         ISTART = ISTART+1
         if (SPFLGG(ICHEK,KK) == 1) exit Ion_start
      end do
      do ICHEK = 1, 4
         ISTART = ISTART+1
         if (SPFLGG(ICHEK,KK) == 1) exit Ion_start
      end do
      ! Arrival at this point is a major problem and should never happen.
      ! Should it, write error message and get out as gracefully as possible
      write (stdout,fmt='(A/A)')&
      ' Code malfunction in speciation section of',&
      ' subroutine M3AVE. Please report problem to author.'
      IFLAG = 8
      exit Chemicals
   end do Ion_start
   ! Starting point for ion sequence now loaded into ISTART;
   ! next load end points for ion sequence(s)
   IFIRST(1) = ISTART
   if (IONTES > 4) then             ! 2 tables required
      ILAST(1) = ISTART+3
      IFIRST(2) = ISTART+4
      ILAST(2) = IFIRST(2)+IONTES-5
   else                             ! Only one table required
      ILAST(1) = ISTART+IONTES-1
   end if
   Table_print: if (RPTFIL) then; do NTAB = 1, NTABLE
      ! Write page header
      write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
      write (RPTLUN,5010) trim(CHEMNA(KK))
      write (RPTLUN,5020) ! dashed line
      ! Write title for table
      write (RPTLUN,fmt='(A,I1,A/A)') ' Table 16.'//KOUT//'.',NTAB,&
         '.  Distribution of average concentrations among aqueous',&
         ' chemical species. All concentrations in ug/L (ppb).'
      write (RPTLUN,5020) ! dashed line

      do I = 1, 4
         ITOP(I) = ' ' ! Blank out ion column headings
      end do
      K1 = 1
      do K = IFIRST(NTAB), ILAST(NTAB)
         ITOP(K1) = '     '//PIECE(K)     ! Load column headers
         K1 = K1+1
      end do
      ! Print column headers
      write (RPTLUN,fmt=ColumnLabels) &
'Seg  T*   Total**     DOC      - Dissolved Chemical Species (by valency) -',&
' #   y    Aqueous  Complexed '//ITOP(1)//ITOP(2)//ITOP(3)//ITOP(4)
      write (RPTLUN,5020) ! dashed line
      Segment_print: do J = 1, KOUNT
         OUTDAT = 0.0 ! Pre-zero output sequence
         OUTDAT(1) = 1000.*(YSUMS(29,J,KK)+YSUMS(31,J,KK))/DaysInYear
         ! Multiplication by 1000.0 to convert mg/L to ug/L (ppm to ppb).
         OUTDAT(2) = 1000.0*YSUMS(31,J,KK)/DaysInYear
         ! Load ionic speciation output vector (OUTDAT(3-6))
         NNDAT = 3
         do I = IFIRST(NTAB), ILAST(NTAB)
            OUTDAT(NNDAT) = 1000.0*YSUMS(IALPHA(I),J,KK)/DaysInYear
            NNDAT = NNDAT+1
         end do
         write (OUTLIN,fmt=Table16_Format) J,TYPEG(J),OUTDAT
         if (OUTDAT(2) .Equals. 0.0) OUTLIN(19+Offset:29+Offset) = ' '
         N1 = 3
         do I = 30+Offset, 63+Offset, 11
            if (OUTDAT(N1) .Equals. 0.0) OUTLIN(I:I+10) = ' '
         N1 = N1+1
         end do
         write (RPTLUN,fmt=lineFormat) trim(OUTLIN)
      end do Segment_print
      write (RPTLUN,5020) ! dashed line
      ! Footnote to table
      write (RPTLUN,fmt='(A/A)')&
         '  * Segment types: Littoral, Epilimnetic, Hypolimnetic, Benthic.',&
         ' ** Includes complexes with Dissolved Organic Carbon.'
   end do; end if Table_print

   ! Write out table and plot file of averages, maxima and minima
   if (PLTFIL) write (SSLUN) KK,Z2(8),Z(1,KK),Z(2,KK),Z2(9),Z2(7)
   if (RPTFIL) then
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM) ! Write page header
   write (RPTLUN,5010) trim(CHEMNA(KK))
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt='(A/A)') ' Table 17.'//KOUT//& ! Title for table
      '.  System-wide concentration means and extrema.',&
      ' "Seg)" indicates segment where value was found.'
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt='(A,3(/A))')& ! set up table columns
'            Total            Dissolved        Sediments          Biota',&
'         Seg   mg/*        Seg  mg/L **      Seg  mg/kg        Seg  ug/gram',&
'         -------------     -------------     -------------     -------------',&
' Water Column:'
   write (RPTLUN,fmt=T17Mean) Z2(8),Z(1,KK),Z(2,KK),Z2(9)
   write (RPTLUN,fmt=T17Max) (MAXSEG(I,KK),PEAKLT(I,KK),I=1,4)
   end if
   do J = 1, 5 ! Transfer segment types to output vector
      NTYPX(J) = TYPEG(MAXSEG(J,KK))
      NTYPN(J) = TYPEG(MINSEG(J,KK))
   end do
   if (PLTFIL) then
      write (SSLUN) KK,(MAXSEG(I,KK),I=1,5),NTYPX,(PEAKLT(I,KK),I=1,5)
      write (SSLUN) KK,(MINSEG(I,KK),I=1,5),NTYPN,(YMINLT(I,KK),I=1,5)
      write (SSLUN) KK,Z2(11),Z(3,KK),Z(4,KK),Z2(12),Z2(10)
   end if
   if (RPTFIL) then
   write (RPTLUN,fmt=T17Min) (MINSEG(I,KK),YMINLT(I,KK),I=1,4)
   write (RPTLUN,fmt='(/A)') ' Benthic Sediments:'
   write (RPTLUN,T17Mean) Z2(11),Z(3,KK),Z(4,KK),Z2(12)
   write (RPTLUN,T17Max) (MAXSEG(I,KK),PEAKLT(I,KK),I=6,9)
   end if
   do J = 6, 10 ! Transfer segment types to output vector
      NTYPX(J-5) = TYPEG(MAXSEG(J,KK))
      NTYPN(J-5) = TYPEG(MINSEG(J,KK))
   end do
   if (PLTFIL) then
      write (SSLUN) KK,(MAXSEG(I,KK),I=6,10),NTYPX,(PEAKLT(I,KK),I=6,10)
      write (SSLUN) KK,(MINSEG(I,KK),I=6,10),NTYPN,(YMINLT(I,KK),I=6,10)
   end if
   if (RPTFIL) then
   write (RPTLUN,fmt=T17Min) (MINSEG(I,KK),YMINLT(I,KK),I=6,9)
   ! Enter left parenthesis into location indicators for extrema
   write (RPTLUN,5020) ! dashed line
   ! Units footnote to table
   write (RPTLUN,5160)
   end if
   ! Transfer mean values to YBARLT for output in summary table
   YBARLT(1,KK) = Z2(8)
   YBARLT(2,KK) = Z(1,KK)
   YBARLT(4,KK) = Z2(9)
   YBARLT(6,KK) = Z2(11)
   YBARLT(7,KK) = Z(3,KK)
   YBARLT(9,KK) = Z2(12)
end do Chemicals
if (PLTFIL) then
   close (unit=SSLUN,iostat=File_Check)
   call Release_LUN (SSLUN)
end if

return
5000 format ('1Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2/' Ecosystem: ',A)
5010 format (' Chemical:  ',A)
5020 format (1X,77('-'))
5160 format ('  * Units: mg/L in Water Column; mg/kg in Benthic Zone.'/&
             ' ** Excludes complexes with "dissolved" organics.')
end subroutine M3AVE
