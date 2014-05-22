subroutine M2AVE(Y)
! M2AVE computes and reports the average, maximum, and minimum snap-shot
! concentrations of chemical at the end of each time segment of Mode 2
! simulation. M2AVE also gives an element-by-element listing of the
! concentrations and distribution of chemical throughout the ecosystem.
! M2AVE transmits tabular output to the file defined by FORTAN LUN RPTLUN,
! and writes to a plotting file defined by LUN SSLUN.
! Created 26 April 1984 by L.A. Burns.
! Revised 28-NOV-1985 (LAB) to accomodate IBM file structures.
! Revised 11/16/88 to change file handling--added special
! sector for DSI; required because "endfile" has a bug
! Revision 09-Feb-1999 to use Floating Point Comparison module
! Revisions April 2001 for wider format and dynamic memory allocation
! Revisions April 2002 to support user selection of output files
use Floating_Point_Comparisons
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Table_Variables
Implicit None
real (kind (0D0)) :: Y(KOUNT,KCHEM)
! Y is constituent concentration (mg/L) referred to
! aqueous phase of segment.
! Local variables for this subroutine:
real (kind (0E0)) :: OUTDAT(6), PERCET, TOTMAS, DOMIN(10), ZTEST, Y_positive
integer :: KKNTW, KKNTS, M1, M2
! KKNTW and KKNTS are integer versions of KOUNTW and KOUNTS
! for output to plot file.
integer :: File_Check ! receives iostat when opening ssout.plt
integer :: ICHEK, ISTART, K1, NTAB
integer :: I, J, KTWO, KK, IONTES, NTABLE, N1
! KK runs the loop on chemicals
! IONTES counts the number of active ions
! NTABLE indicates the number of speciation tables required
integer, dimension(10) :: MAXPT, MINPT
integer, dimension(2) ::  IFIRST, ILAST
logical :: FIRSTW, FIRSTB
! FIRSTW and FIRSTB are used to key initialization of MAXPT,
! MINPT, DOMAX, and DOMIN to the values in the first water
! column or benthic segment.
character(len=78) :: OUTLIN
character(len=1), dimension(5) :: NTYPX, NTYPN
! NTYPX and NTYPN register segment types in SSLUN file.
! ALPHA adresses for ionic species
integer, dimension(7) :: IALPHA=(/25,21,17,1,5,9,13/)
character(len=7), dimension(4) :: NAMTIM = &
   (/'hours. ','days.  ','months.','years. '/)
character(len=1), parameter :: STAR='*' ! unformatted plotting files delimiter

PlotFiles: if (PLTFIL) then ! Identify information written to LUN SSLUN...
call Assign_LUN (SSLUN)
open (unit=SSLUN, status='replace', access='sequential',&
     form='unformatted', position='rewind', file='ssout.plt',&
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
write (SSLUN) (ECONAM)
end if PlotFiles

! allow for run of a single compartment
! a.k.a. paranoid insurance against division by zero
if (KOUNTW .LessThanOrEqual. 0.0) KOUNTW = 1.0
! allow for run of a single sediment compartment
if (KOUNTS .LessThanOrEqual. 0.0) KOUNTS = 1.0
! load integer values of KOUNTW and KOUNTS:

KKNTW = int(KOUNTW)
KKNTS = int(KOUNTS)
! write current concentration (with name of chemical and ecosystem) to file
! for plotting concentration vs. ecosystem, and report current
! distribution to LUN RPTLUN.
! find length of name of ecosystem:
! Write one block (3 Tables) per chemical:
Z = 0.0 ! Initialization: Zero "Z" values
Chemicals: do KK = 1, KCHEM
   Z2 = 0.0
   ! Initialize first segment keys
   FIRSTW = .true.
   FIRSTB = .true.

   ! Compute mean concentrations
   Segments: do J = 1, KOUNT    ! Do segments in numerical order
      Y_positive = abs(Y(J,KK))
      if (TYPEG(J) /= 'B') then ! Water column segments
         ! Dissolved
         Z(1,KK) = Z(1,KK)+VOLG(J)*ALPHA(29,J,KK)*Y_positive
         ! Sorbed mg/kg
         Z(2,KK) = Z(2,KK)+VOLG(J)*ALPHA(30,J,KK)*Y_positive/SEDCOL(J)
         ! Mass, kg (1.0E-06 kg/mg)
         Z(5,KK) = Z(5,KK)+Y_positive*WATVOL(J)*1.0E-06
      else    ! Bottom sediments
         ! mg/L dissolved in pore water
         Z(3,KK) = Z(3,KK)+VOLG(J)*ALPHA(29,J,KK)*Y_positive
         ! sorbed mg/kg
         Z(4,KK) = Z(4,KK)+VOLG(J)*ALPHA(30,J,KK)*Y_positive/SEDCOL(J)
         ! Pollutant mass in kg (1.0E-06 kg/mg)
         Z(6,KK) = Z(6,KK)+Y_positive*WATVOL(J)*1.0E-06
      end if
   end do Segments
   ! Compute averages in water column
   Z(1,KK) = Z(1,KK)/Total_Limnetic_Volume ! mg/L  dissolved
   Z(2,KK) = Z(2,KK)/Total_Limnetic_Volume ! mg/kg sorbed
   ! Compute averages in bottom sediments
   Z(3,KK) = Z(3,KK)/Total_Benthic_Volume ! mg/L dissolved
   Z(4,KK) = Z(4,KK)/Total_Benthic_Volume ! mg/kg sorbed
   Reporting: if (RPTFIL) then
   ! Write page header to LUN RPTLUN:
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(KK))
   write (RPTLUN,5020) ! dashed line
   write (KOUT,fmt='(I2.2)') KK
   write (RPTLUN,fmt='(A,I0,A)')&
      ' Table 15.'//KOUT//'.  Distribution of chemical after ',int(TENDG),&
      ' '//NAMTIM(TCODEG)
   write (RPTLUN,5020) ! dashed line
   ! Set up table in LUN RPTLUN:
   write (RPTLUN,fmt=ColumnLabels)& ! Column headers for distribution
      'Seg   Resident Mass   ******** Chemical Concentrations *********',&
      ' #                      Total    Dissolved  Sediments    Biota',&
      '      Kilos      %       mg/*     mg/L **     mg/kg       ug/g',&
      '---  -------- ------  ---------  ---------  ---------  ---------',&
      '     In the Water Column:'
   end if Reporting

   ! accumulate data for mean values, track maxima and minima.
   Water_column: do J = 1, KOUNT
      if (TYPEG(J) == 'B') cycle Water_column ! Skip sediment compartments
      Y_positive = abs(Y(J,KK))  
      Z2(6) = 1.0E-06*Y_positive*WATVOL(J)   ! Compute mass (in kilograms)
      Z2(5) = 1.0E+03*Z2(6)/AREAG(J)      ! Convert mass to grams/square meter
      Z2(7) = Z2(7)+Z2(5)                 ! Accumulate for mean value
      if (Z(5,KK) .GreaterThan. 0.0) then ! Calculate mass as
         PERCET = Z2(6)*100./Z(5,KK)      ! percent of total in water column
      else       ! Allow for entry of some compounds with zero loadings
         PERCET = 0.0
      end if
      Z2(1) = Y_positive! Total concentration (mg/L in water column)
      Z2(8) = Z2(8)+VOLG(J)*Z2(1) ! Accumulate for mean value
      ! Free (dissolved) chemical in water column
      Z2(2) = ALPHA(29,J,KK) * Y_positive
      ! Chemical sorbed on suspended sediments (mg/kg)
      Z2(3) = ALPHA(30,J,KK)*Y_positive/SEDCOL(J)
      ! Chemical sorbed on biota (bacteria +), ug/g
      Z2(4) = ALPHA(32,J,KK)*Y_positive/BIOTOL(J)
      Z2(9) = Z2(9)+VOLG(J)*Z2(4) ! Accumulate sum for mean value
      ! Initialize and track extrema
      if (FIRSTW) then ! First water column segment, initialize variables
         do I = 1, 5
            MAXPT(I) = J
            MINPT(I) = J
            DOMAX(I,KK) = Z2(I)
            DOMIN(I) = Z2(I)
         end do
         FIRSTW = .false.
      else ! Track extrema
         do I = 1, 5
            if (Z2(I) .GreaterThan. DOMAX(I,KK)) MAXPT(I) = J
            if (Z2(I) .LessThan.    DOMIN(I)) MINPT(I) = J
            DOMAX(I,KK) = amax1(DOMAX(I,KK),Z2(I))
            DOMIN(I) = amin1(DOMIN(I),Z2(I))
         end do
      end if
      ! Write line to LUN RPTLUN
      if (RPTFIL) write (RPTLUN,Table15a_Format) J,Z2(6),PERCET,(Z2(I),I=1,4)
      ! Write line to LUN SSLUN
      if (PLTFIL) write (SSLUN) KK,J,TYPEG(J),Z2(5),Z2(6),PERCET,(Z2(I),I=1,4)
   end do Water_column
   ! End of water column loop; mark plot file for end of water column values
   ! Note: most of this line contains dummy values.
   ! "STAR" signals the end of the records; the other values merely let PLOT
   ! use a standard read.
   if (PLTFIL) write (SSLUN) KK,KKNTW,STAR,(Z(I,KK),I=1,6),Z2(1)
   ! Compute average values where needed
   Z2(7) = Z2(7)/KOUNTW                ! Mass (grams/square meter)
   Z2(8) = Z2(8)/Total_Limnetic_Volume ! Total concentration
   Z2(9) = Z2(9)/Total_Limnetic_Volume ! Biosorbed concentration
   ZTEST = Z(5,KK)+Z(6,KK)
   if (ZTEST .GreaterThan. 0.0) then   ! calculate water column mass as
      PERCET = 100.*Z(5,KK)/ZTEST      ! a percentage of total mass
   else ! Allow for entry of some compounds with zero allocthonous loadings
      PERCET = 0.0
   end if
   ! Write subtotal to LUN RPTLUN:
   if (RPTFIL) write (RPTLUN,Table15b_Format) Z(5,KK),PERCET
   ! Benthic segments:
   ! Label benthic section in LUN RPTLUN:
   if (RPTFIL) write (RPTLUN,fmt='(/A)') '      and in the Benthic Sediments:'
   ! Computations for bottom sediments: compute and print variables,
   ! accumulate values for means, track maxima and minima
   Benthic_segments: do J = 1, KOUNT
      if (TYPEG(J) /= 'B') cycle Benthic_segments ! Skip water column segments
      Y_positive = abs(Y(J,KK))
      Z2(6) = 1.0E-06*Y_positive*WATVOL(J)! Compute mass (kilograms)
      Z2(5) = 1.E3*Z2(6)/AREAG(J)         ! Convert mass to grams/square meter
      Z2(10) = Z2(10)+Z2(5)               ! Accumulate for average
      if (Z(6,KK) .GreaterThan. 0.0) then ! Calculate mass, as a
         PERCET = 100.*Z2(6)/Z(6,KK)      ! % of total in bottom sediments
      else                            ! allow for entry of some compounds
         PERCET = 0.0                 ! with zero allocthonous loadings
      end if
      ! Total concentration, mg/kg
      ! (Division by SEDMSL is O.K. because sediments in a
      ! "bottom sediment" compartment are never zero.)
      Z2(1) = Y_positive*WATVOL(J)/SEDMSL(J)
      Z2(11) = Z2(11)+VOLG(J)*Z2(1)   ! Accumulate for average value
      ! Free (dissolved) chemical in bottom sediments
      ! (mg/L of interstitial water)
      Z2(2) = ALPHA(29,J,KK)*Y_positive
      Z2(3) = ALPHA(30,J,KK)*Y_positive/SEDCOL(J) ! Sorbed on bottom sediments
      ! Chemical sorbed on benthic organisms (ug/g)
      Z2(4) = ALPHA(32,J,KK)*Y_positive/BIOTOL(J)
      Z2(12) = Z2(12)+VOLG(J)*Z2(4)  ! Accumulate sum for mean value
      ! Initialize and track extrema
      if (FIRSTB) then ! Initialize extreme value trackers and pointers
         do I = 6, 10
            MAXPT(I) = J
            MINPT(I) = J
            DOMAX(I,KK) = Z2(I-5)
            DOMIN(I) = Z2(I-5)
         end do
         FIRSTB = .false.
      else ! Track extrema
         do I = 6, 10
            if (Z2(I-5)  .GreaterThan. DOMAX(I,KK)) MAXPT(I) = J
            if (Z2(I-5)  .LessThan.    DOMIN(I))    MINPT(I) = J
            DOMAX(I,KK) = amax1(DOMAX(I,KK),Z2(I-5))
            DOMIN(I) = amin1(DOMIN(I),Z2(I-5))
         end do
      endif
      ! Write line to LUN RPTLUN:
      if (RPTFIL) write (RPTLUN,Table15a_Format) J,Z2(6),PERCET,(Z2(I),I=1,4)
      ! Write line to LUN SSLUN:
      if (PLTFIL) write (SSLUN) KK,J,TYPEG(J),Z2(5),Z2(6),PERCET,(Z2(I),I=1,4)
   end do Benthic_segments
   ! Mark plot file for end of bottom sediments
   ! Note: most of this line contains dummy values. "STAR" signals the end
   ! of the records; the other values merely let PLOT use a standard read.
   if (PLTFIL) write (SSLUN) KK,KKNTS,STAR,(Z(I,KK),I=1,6),Z2(1)
   ! Compute averages where needed
   Z2(10) = Z2(10)/KOUNTS               ! Mass (grams/square meter)
   Z2(11) = Z2(11)/Total_Benthic_Volume ! Total concentration
   Z2(12) = Z2(12)/Total_Benthic_Volume ! Benthos Biosorbed concentration
   ZTEST = Z(5,KK) + Z(6,KK)
   if (ZTEST .GreaterThan. 0.0) then    ! Calculate bottom sediment mass
      PERCET = Z(6,KK)*100.0/ZTEST      ! as percent of total mass
   else !  Allow for entry of some compounds with zero allocthonous loadings
      PERCET = 0.0
   end if
   ! Write subtotal to LUN RPTLUN
   if (RPTFIL) then
      write (RPTLUN,Table15b_Format) Z(6,KK),PERCET
      TOTMAS = Z(5,KK)+Z(6,KK) ! Write total mass to LUN RPTLUN
      write (RPTLUN,fmt='(A,1PG11.4)')&
         ' Total Mass (kilograms) =   ',TOTMAS
      write (RPTLUN,5020) ! dashed line
      write (RPTLUN,fmt='(A/A)') & ! Write footnotes to table
         '  * Units: mg/L in Water Column; mg/kg in Benthos.',&
         ' ** Excludes complexes with "dissolved" organics.'
   end if

   ! Write out table detailing aqueous speciation
   ! Test for number of active chemical species
   IONTES = sum(SPFLGG(:,KK))
   NTABLE = 1
   if (IONTES > 4) NTABLE = 2
   ! Detect the starting point for the ion sequence:
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
      ' subroutine M2AVE. Please report problem to author.'
      IFLAG = 8
      exit Chemicals
   end do Ion_start

   ! Starting point for ion sequence loaded into ISTART;
   ! next load end points for ion sequence(s)
   IFIRST(1) = ISTART
   if (IONTES > 4) then ! 2 tables required
      ILAST(1) = ISTART+3
      IFIRST(2) = ISTART+4
      ILAST(2) = IFIRST(2)+IONTES-5
   else! Only one table required
      ILAST(1) = ISTART+IONTES-1
   end if

   Table_print: if (RPTFIL) then; do NTAB = 1, NTABLE
      ! Write page header
      write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
      write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(KK))
      write (RPTLUN,5020) ! dashed line
      ! Write title for table:
      write (RPTLUN,fmt='(A,I1,A/A,F6.0,A)') ' Table 16.'//KOUT//&
         '.',NTAB,'.  Distribution among aqueous chemical species at',&
         ' the end of',TENDG,' '//NAMTIM(TCODEG)//&
         '  All concentrations in ug/L (ppb).'
      write (RPTLUN,5020)  ! dashed line
      ITOP = '    ' ! Blank out ion column headings
      K1 = 1
      do KTWO = IFIRST(NTAB), ILAST(NTAB)
         ITOP(K1) = '     '//PIECE(KTWO)           ! Load column headers
         K1 = K1+1
      end do
      ! Print column headers
      write (RPTLUN,fmt=ColumnLabels) &
'Seg  T*   Total**     DOC      - Dissolved Chemical Species (by valency) -',&
' #   y    Aqueous  Complexed '//ITOP(1)//ITOP(2)//ITOP(3)//ITOP(4)
      write (RPTLUN,5020) ! dashed line
      Segment_print: do J = 1, KOUNT
         OUTDAT = 0.0; Y_positive = abs(Y(J,KK))
         OUTDAT(1) = 1000.0*(ALPHA(29,J,KK)+ALPHA(31,J,KK))*Y_positive
         ! Multiplication by 1000.0 to convert mg/L to ug/L (ppm to ppb).
         OUTDAT(2) = 1000.0*ALPHA(31,J,KK)*Y_positive ! DOC-complexed
         ! Load ionic speciation output vector (OUTDAT(3-6)):
         N1 = 3
         do I = IFIRST(NTAB), ILAST(NTAB)
            OUTDAT(N1) = 1000.0*ALPHA(IALPHA(I),J,KK)*Y_positive
            N1 = N1+1
         end do
          write (OUTLIN,fmt=Table16_Format) J,TYPEG(J),(OUTDAT(I),I=1,6)
         if (OUTDAT(2) .Equals. 0.0) OUTLIN(19+Offset:29+Offset) = ' '
         N1 = 3
         do I = 30+Offset, 63+Offset, 11
            if (OUTDAT(N1) .Equals. 0.0) OUTLIN(I:I+10) = ' '
            N1 = N1+1
         end do
         write (RPTLUN,fmt=LineFormat) trim(OUTLIN)
      end do Segment_print
      write (RPTLUN,5020) ! dashed line
      write (RPTLUN,fmt='(A/A)') & ! Footnote to table
         '  * Segment types: Littoral, Epilimnetic, Hypolimnetic, Benthic.',&
         ' ** Includes complexes with Dissolved Organic Carbon.'
   end do; end if Table_print

   ! Write out table of averages, maxima and minima:
   if (PLTFIL) write (SSLUN) KK,Z2(8),Z(1,KK),Z(2,KK),Z2(9),Z2(7)

   if (RPTFIL) then
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM) ! Write page header
   write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(KK))
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt='(A/A,I0,A)') & ! Title for table
      ' Table 17.'//KOUT//&
      '.  Chemical concentration spatial means, maxima, and minima at the',&
      ' end of ',int(TENDG),' '//NAMTIM(TCODEG)//&
      ' "Seg)" indicates segment where value was found.'
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt='(A,3(/A))')& ! set up table columns
'            Total            Dissolved        Sediments          Biota',&
'         Seg   mg/*        Seg  mg/L **      Seg  mg/kg        Seg  ug/gram',&
'         -------------     -------------     -------------     -------------',&
' Water Column:'
   write (RPTLUN,fmt=T17Mean) Z2(8),Z(1,KK),Z(2,KK),Z2(9)
   write (RPTLUN,fmt=T17Max) (MAXPT(I),DOMAX(I,KK),I=1,4)
   end if

   do J = 1, 5 ! Transfer segment types to output vector
      NTYPX(J) = TYPEG(MAXPT(J))
      NTYPN(J) = TYPEG(MINPT(J))
   end do

   if (PLTFIL) then
      write (SSLUN) KK,(MAXPT(I),I=1,5),NTYPX,(DOMAX(I,KK),I=1,5)
      write (SSLUN) KK,(MINPT(I),I=1,5),NTYPN,(DOMIN(I),I=1,5)
      write (SSLUN) KK,Z2(11),Z(3,KK),Z(4,KK),Z2(12),Z2(10)
   end if

   if (RPTFIL) then
   write (RPTLUN,fmt=T17Min) (MINPT(I),DOMIN(I),I=1,4)
   write (RPTLUN,fmt='(/A)') ' Benthic Sediments:'
   write (RPTLUN,fmt=T17Mean) Z2(11),Z(3,KK),Z(4,KK),Z2(12)
   write (RPTLUN,fmt=T17Max) (MAXPT(I),DOMAX(I,KK),I=6,9)
   write (RPTLUN,fmt=T17Min) (MINPT(I),DOMIN(I),I=6,9)
   end if

   do J = 6, 10 ! Transfer segment types to output vector
      NTYPX(J-5) = TYPEG(MAXPT(J))
      NTYPN(J-5) = TYPEG(MINPT(J))
   end do

   if (PLTFIL) then
      write (SSLUN) KK,(MAXPT(I),I=6,10),NTYPX,(DOMAX(I,KK),I=6,10)
      write (SSLUN) KK,(MINPT(I),I=6,10),NTYPN,(DOMIN(I),I=6,10)
   end if

   if (RPTFIL) then
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt='(A/A)') & ! Write footnotes to table
      '  * Units: mg/L in Water Column; mg/kg in Benthic Zone.',&
      ' ** Excludes complexes with "dissolved" organics.'
   end if

end do Chemicals

if (PLTFIL) then
   close (unit=SSLUN,iostat=File_Check)
   call Release_LUN (SSLUN)
end if

return
5000 format ('1','Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2/' Ecosystem: ',A)
5020  format (1X,77('-')) ! dashed line
end Subroutine M2AVE
