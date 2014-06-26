subroutine AVEOUT(Y)
! AVEOUT computes and reports the average, maximum, and minimum steady-state
! concentrations of chemical. AVEOUT also gives an element by element listing
! of the concentrations and distribution of chemical throughout the ecosystem.
! AVEOUT transmits tabular output to the file defined by Fortan LUN
! RPTLUN, and writes to a plotting file defined by LUN SSLUN.
! Created August 1979 by L.A. Burns.
! Revised 28-NOV-1985 (LAB) to accomodate IBM file structures.
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revised 11/16/88 to change file handling--added special
! sector for DSI; required because "endfile" had a bug in this compiler.
! Revisions April 2001 for wider format and dynamic memory allocation
use Implementation_control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Floating_Point_Comparisons
use Table_Variables
Implicit None
real (kind (0D0)) :: Y(KOUNT,KCHEM)
! Y is constituent concentration (mg/L) referred to aqueous phase of segment
! Local variables for this subroutine
real (kind (0E0)) :: OUTDAT(6), PERCET, TOTMAS, DOMIN(10), Y_positive
integer :: ICHEK, ISTART, K1, NTAB, M1, M2
integer :: I, J, K, KK, II, IONTES, NTABLE, N1, ioerror
! KK runs the loop on chemicals
! IONTES counts the number of active ions
! NTABLE indicates the number of speciation tables required
integer :: KKNTW, KKNTS
! KKNTW and KKNTS are integer versions of KOUNTW and KOUNTS
! for output to plot file.
integer :: MAXPT(10), MINPT(10)
integer :: IFIRST(2), ILAST(2)
logical :: FIRSTW, FIRSTB
! FIRSTW and FIRSTB detect the first water column and first benthic segment,
! so as to key initialization of MAXPT, MINPT, DOMAX, and DOMIN.
character(len=1) :: NTYPX(5), NTYPN(5), STAR = '*'
! STAR is delimiter used in unformatted plotting files
! NTYPX and NTYPN register segment types in SSOUT file (L,E,H,B)
integer :: File_Check ! receives iostat when opening ssout.plt
character(len=78) :: OUTLIN
! ALPHA adresses for ionic species
integer, dimension(7) :: IALPHA = (/25,21,17,1,5,9,13/)

! Fail-safe insurance, because these are divisors
If (KOUNTW .LessThanOrEqual. 0.0) KOUNTW=1.0
If (KOUNTS .LessThanOrEqual. 0.0) KOUNTS=1.0


PlotFiles: if (PLTFIL) then ! identify information written to LUN SSLUN...
call Assign_LUN (SSLUN)
open (unit=SSLUN, status='REPLACE', access='SEQUENTIAL',&
   form='UNFORMATTED',file='ssout.plt',position='REWIND',&
   action='write',iostat=File_Check)
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

! Load integer values of KOUNTW and KOUNTS
KKNTW = int(KOUNTW)
KKNTS = int(KOUNTS)
! Write steady-state concentration (with name of chemical and
! ecosystem) to file for plotting concentration vs. ecosystem,
! and report steady-state distribution to LUN RPTLUN.
! Find length of ecosystem name
! Write one block (3 Tables) per chemical
Z  = 0.0 ! Initialization--Zero "Z" values
Chemicals: do KK = 1, KCHEM
   Z2 = 0.0
   ! Set detectors of first water column and benthic segment
   FIRSTW = .true.
   FIRSTB = .true.
   ! Compute mean concentrations
   do J = 1, KOUNT   ! Do segments in numerical order
      Y_positive = abs(Y(J,KK))
      if (TYPEG(J) /= 'B') then ! Water column segments
         ! Dissolved
         Z(1,KK) = Z(1,KK)+VOLG(J)*ALPHA(29,J,KK)*Y_positive
         ! Sorbed mg/kg
         Z(2,KK) = Z(2,KK)+VOLG(J)*ALPHA(30,J,KK)*Y_positive/SEDCOL(J)
         ! Mass, kg (1.0E-06 kg/mg)
         Z(5,KK) = Z(5,KK)+Y_positive*WATVOL(J)*1.0E-06
      else ! Bottom sediments
         ! mg/L dissolved in pore water
         Z(3,KK) = Z(3,KK)+VOLG(J)*ALPHA(29,J,KK)*Y_positive
         ! sorbed mg/kg
         Z(4,KK) = Z(4,KK)+VOLG(J)*ALPHA(30,J,KK)*Y_positive/SEDCOL(J)
         ! Pollutant mass in kg (1.0E-06 kg/mg)
         Z(6,KK) = Z(6,KK)+Y_positive*WATVOL(J)*1.0E-06
      end if
   end do
   ! Compute averages in water column
   Z(1,KK) = Z(1,KK)/Total_Limnetic_Volume ! mg/L  dissolved
   Z(2,KK) = Z(2,KK)/Total_Limnetic_Volume ! mg/kg sorbed
   ! Compute averages in bottom sediments
   Z(3,KK) = Z(3,KK)/Total_Benthic_Volume ! mg/L dissolved
   Z(4,KK) = Z(4,KK)/Total_Benthic_Volume ! mg/kg sorbed

   Reporting: if (RPTFIL) then
   ! Write page header to LUN RPTLUN
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5010) trim(CHEMNA(KK))
   write (RPTLUN,5020) ! dashed line
   ! Load character string for transmitting K to table headers
   write (KOUT,fmt='(I2.2)') KK
   write (RPTLUN,fmt='(A)')&
      ' Table 15.'//KOUT//'.  Distribution of chemical at steady state.'
   write (RPTLUN,5020) ! dashed line
   ! Set up table in LUN RPTLUN
   write (RPTLUN,fmt=ColumnLabels)& ! Column headers for distribution
      'Seg   Resident Mass   ******** Chemical Concentrations *********',&
      ' #                      Total    Dissolved  Sediments    Biota',&
      '      Kilos      %       mg/*     mg/L **     mg/kg       ug/g',&
      '---  -------- ------  ---------  ---------  ---------  ---------',&
      '     In the Water Column:'
   end if Reporting

   ! Computations for segments--compute and print variables,
   ! accumulate data for mean values, track maxima and minima.
   do J = 1, KOUNT ! water column
      if (TYPEG(J) == 'B') cycle ! skip sediment compartments
      Y_positive = abs(Y(J,KK))
      Z2(6) = 1.0E-06*Y_positive*WATVOL(J) ! mass by system element (in kg)
      Z2(5) = 1.0E+03*Z2(6)/AREAG(J)    ! convert mass to grams/square meter
      Z2(7) = Z2(7)+Z2(5)               ! accumulate for mean value
      ! calculate mass as percent of total in water column,
      ! allowing for entry of some compounds with zero loadings
      PERCET = 0.0
      if (Z(5,KK) .NotEqual. 0.0) PERCET = Z2(6)*100./Z(5,KK)
      Z2(1) = Y_positive! total concentration (mg/L in water column)
      Z2(8) = Z2(8)+Z2(1)*VOLG(J) ! accumulate for mean value
      ! free (dissolved) chemical in water column
      Z2(2) = ALPHA(29,J,KK) * Y_positive
      ! chemical sorbed on suspended sediments (mg/kg)
      Z2(3) = ALPHA(30,J,KK) * Y_positive / SEDCOL(J)
      ! chemical sorbed on biota (bacteria +), ug/g
      Z2(4) = ALPHA(32,J,KK) * Y_positive / BIOTOL(J)
      Z2(9) = Z2(9)+Z2(4)*VOLG(J) ! accumulate sum for mean value
      ! initialize and track extrema
      if (FIRSTW) then ! first water column segment, initialize variables
         do I = 1, 5
            MAXPT(I) = J
            MINPT(I) = J
            DOMAX(I,KK) = Z2(I)
            DOMIN(I) = Z2(I)
         end do
         FIRSTW = .false.
      else
         do I = 1, 5 ! track extrema
            if (Z2(I) .GreaterThan. DOMAX(I,KK)) MAXPT(I) = J
            if (Z2(I) .LessThan.    DOMIN(I))    MINPT(I) = J
            DOMAX(I,KK) = amax1(DOMAX(I,KK),Z2(I))
            DOMIN(I) = amin1(DOMIN(I),Z2(I))
         end do
      end if
      ! write line to LUN RPTLUN
      if (RPTFIL) write (RPTLUN,Table15a_Format) J,Z2(6),PERCET,(Z2(I),I=1,4)
      ! write line to LUN SSLUN
      if (PLTFIL) write (SSLUN) KK,J,TYPEG(J),Z2(5),Z2(6),PERCET,(Z2(I),I=1,4)
   end do ! end of water column loop

   ! mark plot file for end of water column values--Note: most of
   ! this line contains dummy values. "STAR" signals the end of the
   ! records; the other values merely let PLOT use a standard read.
   if (PLTFIL) write (SSLUN) KK,KKNTW,STAR,(Z(I,KK),I=1,6),Z2(1)
   ! compute average values where needed
   Z2(7) = Z2(7)/KOUNTW ! 1. mass (grams/square meter)
   Z2(8) = Z2(8)/Total_Limnetic_Volume ! 2. total concentration
   Z2(9) = Z2(9)/Total_Limnetic_Volume ! 3. biosorbed concentration
   ! water column mass as percentage of total mass in system,
   ! allowing for entry of some compounds with zero allocthonous loadings
   PERCET = 0.0
   if ((Z(5,KK) .NotEqual. 0.0) .or. (Z(6,KK) .NotEqual. 0.0))&
      PERCET = 100.0*Z(5,KK)/(Z(5,KK)+Z(6,KK))
   ! write subtotal to LUN RPTLUN
   if (RPTFIL) write (RPTLUN,Table15b_Format) Z(5,KK),PERCET

   ! benthic segments...label benthic section in LUN RPTLUN
   if (RPTFIL) write (RPTLUN,fmt='(/A)') '      and in the Benthic Sediments:'
   do J = 1, KOUNT ! computations for bottom sediments--compute and print
      ! variables, accumulate values for means, track maxima and minima
      if (TYPEG(J) /= 'B') cycle ! skip water column segments
      Y_positive = abs(Y(J,KK))
      Z2(6) = 1.0E-06*Y_positive*WATVOL(J) ! mass (kg) by system element
      Z2(5) = 1.E3*Z2(6)/AREAG(J) ! convert mass to grams/square meter
      Z2(10) = Z2(10)+Z2(5)       ! accumulate for average
      ! calculate mass as a percentage of total in bottom sediments,
      ! allowing for chemicals with zero allocthonous loadings
      PERCET = 0.0
      if (Z(6,KK) .NotEqual. 0.0) PERCET = 100.*Z2(6)/Z(6,KK)
      ! (division by SEDMSL is O.K. because sediments in a
      ! "bottom sediment" compartment are never zero.)
      Z2(1) = Y_positive*WATVOL(J)/SEDMSL(J) ! total concentration, mg/kg
      Z2(11) = Z2(11)+VOLG(J)*Z2(1) ! accumulate for average value
      ! free (dissolved) chemical in bottom sediments
      ! (mg/L of interstitial water)
      Z2(2) = ALPHA(29,J,KK)*Y_positive
      Z2(3) = ALPHA(30,J,KK)*Y_positive/SEDCOL(J) ! sorbed on bottom sediments
      ! chemical sorbed on benthic organisms (ug/g)
      Z2(4) = ALPHA(32,J,KK)*Y_positive/BIOTOL(J)
      Z2(12) = Z2(12)+VOLG(J)*Z2(4) ! accumulate sum for mean value
      ! initialize and track extrema
      if (FIRSTB) then ! initialize extreme value trackers and pointers
         do I = 6, 10
            MAXPT(I) = J
            MINPT(I) = J
            DOMAX(I,KK) = Z2(I-5)
            DOMIN(I) = Z2(I-5)
         end do
         FIRSTB = .false.
      else
         do I = 6, 10 ! track extrema
            if (Z2(I-5) .GreaterThan. DOMAX(I,KK)) MAXPT(I) = J
            if (Z2(I-5) .LessThan.    DOMIN(I))    MINPT(I) = J
            DOMAX(I,KK) = amax1(DOMAX(I,KK),Z2(I-5))
            DOMIN(I)    = amin1(DOMIN(I),Z2(I-5))
         end do
      end if
      ! write line to LUN RPTLUN
      if (RPTFIL) write (RPTLUN,Table15a_Format) J,Z2(6),PERCET,(Z2(I),I=1,4)
      ! write line to LUN SSLUN
      if (PLTFIL) write (SSLUN) KK,J,TYPEG(J),Z2(5),Z2(6),PERCET,(Z2(I),I=1,4)
   end do ! end of bottom sediment loop.
   ! mark plot file for end of bottom sediments
   ! note: most of this line contains dummy values.  "STAR" signals
   ! the end of the records; the other values merely let PLOT use a
   ! standardized read.
   if (PLTFIL) write (SSLUN) KK,KKNTS,STAR,(Z(I,KK),I=1,6),Z2(1)
   ! compute averages where needed
   Z2(10) = Z2(10)/KOUNTS               ! 1. mass (grams/square meter)
   Z2(11) = Z2(11)/Total_Benthic_Volume ! 2. total concentration
   Z2(12) = Z2(12)/Total_Benthic_Volume ! 3. benthos biosorbed concentration
   ! bottom sediment mass as percent of total mass...
   ! allow for entry of some compounds with zero allocthonous loadings
   PERCET = 0.0
   if ((Z(5,KK) .NotEqual. 0.0) .or. (Z(6,KK) .NotEqual. 0.0))&
      PERCET = Z(6,KK)*100./(Z(5,KK)+Z(6,KK))

   if (RPTFIL) then
      ! write subtotal to LUN RPTLUN
      write (RPTLUN,Table15b_Format) Z(6,KK),PERCET
      ! write total mass to LUN RPTLUN
      TOTMAS = Z(5,KK)+Z(6,KK)
      write (RPTLUN,fmt='(A,1PG11.4)')&
         ' Total Mass (kilograms) =   ',TOTMAS
      write (RPTLUN,5020) ! dashed line
      write (RPTLUN,5150) ! write footnotes to table
   end if

   ! write out table detailing aqueous speciation
   ! test for number of active chemical species
   IONTES = 0
   do II = 1, 7
      if (SPFLGG(II,KK) == 1) IONTES = IONTES+1
   end do
   NTABLE = 1
   if (IONTES > 4) NTABLE = 2
   ISTART = 0 ! detect the starting point for the ion sequence
   Find_first_ion: do
      do ICHEK = 7, 5, -1
         ISTART = ISTART+1
         if (SPFLGG(ICHEK,KK) == 1) exit Find_first_ion
      end do
      do ICHEK = 1, 4
         ISTART = ISTART+1
         if (SPFLGG(ICHEK,KK) == 1) exit Find_first_ion
      end do
      ! arrival at this point is a major problem and should never
      ! occur--if so, write error message and abort...
      write (stdout,fmt='(A/A)')&
         ' Code malfunction in speciation section of',&
         ' procedure AVEOUT. Please report problem to author.'
      IFLAG = 8
      if (PLTFIL) then
         close (unit=SSLUN,iostat=ioerror)
         call Release_LUN (SSLUN)
      end if
      return
   end do Find_first_ion
   ! starting point for ion sequence loaded into ISTART
   ! load end points for ion sequence(s)
   IFIRST(1) = ISTART
   if (IONTES <= 4) then ! only one table required
      ILAST(1) = ISTART+IONTES-1
   else ! IONTES is greater than 4, 2 tables required
      ILAST(1) = ISTART+3
      IFIRST(2) = ISTART+4
      ILAST(2) = IFIRST(2)+IONTES-5
   end if

   Tables: if (RPTFIL) then; do NTAB = 1, NTABLE
      ! write page header
      write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
      write (RPTLUN,5010) trim(CHEMNA(KK))
      write (RPTLUN,5020) ! dashed line
      ! write title for table
      write (RPTLUN,fmt='(A,I1,A/A)') ' Table 16.'//KOUT//'.',NTAB,&
         '.  Steady-state concentration distribution among aqueous',&
         ' chemical species. All concentrations in ug/L (ppb).'
      write (RPTLUN,5020) ! dashed line
      ! prepare column headers
      ITOP = '         ' ! blank out ion column headings
      K1 = 1        ! load column headers
      do K = IFIRST(NTAB), ILAST(NTAB)
         ITOP(K1) = '     '//PIECE(K)
         K1 = K1+1
      end do
      ! write column headings
      write (RPTLUN,fmt=ColumnLabels)&
'Seg  T*   Total**     DOC      - Dissolved Chemical Species (by valency) -',&
' #   y    Aqueous  Complexed '//ITOP(1)//ITOP(2)//ITOP(3)//ITOP(4)
     write (RPTLUN,5020) ! dashed line
      Segment_loop: do J = 1, KOUNT
         Y_positive = abs(Y(J,KK))
         OUTDAT = 0.0         ! pre-zero output sequence
         ! Total aqueous concentration
         OUTDAT(1) = 1000.0 * (ALPHA(29,J,KK)+ALPHA(31,J,KK)) * Y_positive
         ! multiplication by 1000.0 to convert mg/L to ug/L (ppm to ppb).
         OUTDAT(2) = 1000.0 * ALPHA(31,J,KK) * Y_positive ! DOC-complexed
         ! load ionic speciation output vector (OUTDAT(3-6))
         N1 = 3
         do I = IFIRST(NTAB), ILAST(NTAB)
            OUTDAT(N1) = 1000.0 * ALPHA(IALPHA(I),J,KK) * Y_positive
            N1 = N1+1
         end do
         write (OUTLIN,fmt=Table16_Format)&
            J,TYPEG(J),(OUTDAT(I),I=1,6)
         if(OUTDAT(2) .Equals. 0.0) OUTLIN(19+Offset:29+Offset)=' '
         N1 = 3
         do I = 30+Offset, 63+Offset, 11
            if (OUTDAT(N1) .Equals. 0.0) OUTLIN(I:I+10) = '           '
            N1 = N1+1
         end do
         write (RPTLUN,fmt=LineFormat) trim(OUTLIN)
      end do Segment_loop
      write (RPTLUN,5020) ! dashed line
      ! footnote to table
      write (RPTLUN,fmt='(A/A)')&
         '  * Segment types: Littoral, Epilimnetic, Hypolimnetic, Benthic.',&
         ' ** Includes complexes with Dissolved Organic Carbon.'
   end do; end if Tables

   ! write out plot columns anbd table of averages, maxima and minima
   if (PLTFIL) write (SSLUN) KK,Z2(8),Z(1,KK),Z(2,KK),Z2(9),Z2(7)

   if (RPTFIL) then
   ! write page header
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5010) trim(CHEMNA(KK))
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt='(A/A)')& ! title for table
      ' Table 17.'//KOUT//'. Steady-state concentration means and extrema.',&
      ' Number in parens (Seg) indicates segment where value was found.'
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,fmt='(A,3(/A))')& ! set up table columns
'            Total            Dissolved        Sediments          Biota',&
'         Seg   mg/*        Seg  mg/L **      Seg  mg/kg        Seg  ug/gram',&
'         -------------     -------------     -------------     -------------',&
' Water Column:'
   write (RPTLUN,fmt=T17Mean) Z2(8),Z(1,KK),Z(2,KK),Z2(9)
   write (RPTLUN,fmt=T17Max) (MAXPT(I),DOMAX(I,KK),I=1,4)
   end if

   do J = 1, 5 ! transfer segment types to output vector
      NTYPX(J) = TYPEG(MAXPT(J))
      NTYPN(J) = TYPEG(MINPT(J))
   end do

   if (PLTFIL) then
      write (SSLUN) KK,(MAXPT(I),I=1,5),NTYPX,(DOMAX(I,KK),I=1,5)
      write (SSLUN)KK,(MINPT(I),I=1,5),NTYPN,(DOMIN(I),I=1,5)
   write (SSLUN) KK,Z2(11),Z(3,KK),Z(4,KK),Z2(12),Z2(10)
   end if

   if (RPTFIL) then
   write (RPTLUN,fmt=T17Min) (MINPT(I),DOMIN(I),I=1,4)
   write (RPTLUN,fmt='(/A)') ' Benthic Sediments:'
   write (RPTLUN,fmt=T17Mean) Z2(11),Z(3,KK),Z(4,KK),Z2(12)
   write (RPTLUN,fmt=T17Max) (MAXPT(I),DOMAX(I,KK),I=6,9)
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
   write (RPTLUN,fmt=T17Min) (MINPT(I),DOMIN(I),I=6,9)
   write (RPTLUN,5020) ! dashed line
   write (RPTLUN,5150) ! write footnotes to table
   end if

end do Chemicals

if (PLTFIL) then
   close (unit=SSLUN,iostat=ioerror)
   call Release_LUN (SSLUN)
end if

return
5000 format ('1Exposure Analysis Modeling System -- EXAMS Version ',&
   A,', Mode',I2/' Ecosystem: ',A)
5010  format (' Chemical:  ',A)
5020 format (1X,77('-')) ! dashed line
5150 format ('  * Units: mg/L in Water Column; mg/kg in Benthic Zone.',&
   /' ** Excludes complexes with "dissolved" organics.')
end subroutine AVEOUT
