subroutine TABB
! Created 10 November 1983 (LAB) by disaggregation of PRENV.
! Revised 01-MAY-1985 (LAB) -- conversion from FORTRAN66 to FORTRAN77
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revision 09-Feb-1999 to use new floating point comparison module
! Revisions April 2001 to support dynamic memory allocation
use Floating_Point_Comparisons
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Table_Variables
Implicit None
integer :: I, J, K, NBLOCL ! Local counters
character (len=78) :: OUTLIN ! internal file for pre-processing output

! Data evaluation section
Evaluate: do I = 1,13
   Compartments: do J = 1,KOUNT
      if (TYPEG(J)=='B') then
         ! Check bulk density of benthic sediments:
         if (BULKDG(J,I) .LessThanOrEqual. 0.0) BULKDG(J,I) = 1.85
         ! Fail-safe check on percent water of benthic sediments
         if (PCTWAG(J,I) .LessThan. 100.0) PCTWAG(J,I) = 137.
         ! These values are common enough and allow the simulation to proceed
         ! They may, however, be replaced in the averaging section below.
         ! Ensure non-benthic variables are zero:
         DFACG(J,I)  = 0.0
         DISO2G(J,I) = 0.0
         CHLG(J,I)   = 0.0

      else ! water column compartment

         ! An absolute zero value for suspended sediments is not
         ! permissable because it produces erroneous calculations of the
         ! dispersive exchange of sediments between the water column and
         ! the bottom sediment. If an absolute zero is loaded, it is
         ! adjusted to a non-zero value small enough to preclude effect
         ! on the other computations:
         if (SUSEDG(J,I) .Equals. 0.0) SUSEDG(J,I) = 0.001
         ! Reaeration and wind only apply to segments with an air-water
         ! interface. These are detected by the requirement that each
         ! water column segment (>1) must be preceded by a benthic sediment
         if (J/=1) then   !2013-05-30
            if (TYPEG(J-1)/='B') then ! no air/water interface
               KO2G(J,I) = 0.0
               WINDG(J,I) = 0.0
            end if
         end if
      end if
      ! All compartments:
      ! Data evaluation step: absolute zero values for FROCG, CECG, and
      ! AECG are both unrealistic and computationally invalid. If
      ! loaded, they are replaced at this point by their probable lower
      ! bounds. A user can enter yet smaller values without interference
      ! from EXAMS, but absolute zero is not permitted
      if (FROCG(J,I) .Equals. 0.0) FROCG(J,I) = 0.0001
      if (CECG(J,I)  .Equals. 0.0) CECG(J,I)  = 0.01
      if (AECG(J,I)  .Equals. 0.0) AECG(J,I)  = 0.01
   end do Compartments
end do Evaluate ! end of data evaluation section


Averages: if (MODEG==3 .or. (MODEG<3.and.PRSWG==0.and.MONTHG==13)) then 
! calculate average values
! In Modes 1 and 2, when PRSWG=0 the average values are to be calculated
! when MONTHG=13, else the user-entered values for month 13 are used directly.
   Cpts1: do J = 1,KOUNT
      OUT4 = 0.0  ! Initialize calculation vector
      ! Compute averages 
      do I = 1, 12
         OUT4(5) = OUT4(5)+DOCG(J,I)
         if (TYPEG(J) == 'B') cycle
         OUT4(1) = OUT4(1)+DFACG(J,I)
         OUT4(2) = OUT4(2)+DISO2G(J,I)
         OUT4(3) = OUT4(3)+KO2G(J,I)
         OUT4(4) = OUT4(4)+WINDG(J,I)
         OUT4(6) = OUT4(6)+CHLG(J,I)
      end do
      OUT4 = OUT4/12.0
      ! Transfer mean values to sector 13 of database:
      DFACG(J,13) =  OUT4(1)
      DISO2G(J,13) = OUT4(2)
      KO2G(J,13) =   OUT4(3)
      WINDG(J,13) =  OUT4(4)
      DOCG(J,13) =   OUT4(5)
      CHLG(J,13) =   OUT4(6)
   end do Cpts1
   Cpts2: do J = 1, KOUNT
      OUT4 = 0.0     ! Initialize the calculation vector
      do I = 1, 12   ! Average the input data
         if (TYPEG(J) == 'B') then
            OUT4(2) = OUT4(2)+BULKDG(J,I)
            OUT4(3) = OUT4(3)+PCTWAG(J,I)
         else ! water column compartment
            OUT4(1) = OUT4(1)+SUSEDG(J,I)
         endif
         OUT4(4) = OUT4(4)+FROCG(J,I)
         OUT4(5) = OUT4(5)+CECG(J,I)
         OUT4(6) = OUT4(6)+AECG(J,I)
      end do
      OUT4 = OUT4/12.0  ! Compute average values
      ! Transfer average values to sector 13 of database
      SUSEDG(J,13) = OUT4(1)
      BULKDG(J,13) = OUT4(2)
      PCTWAG(J,13) = OUT4(3)
      FROCG(J,13)  = OUT4(4)
      CECG(J,13)   = OUT4(5)
      AECG(J,13)   = OUT4(6)
   end do Cpts2
end if Averages

if (.not. RPTFIL) return

! Initialize footnote
if (PRSWG == 1 .and. MODEG == 3) then
   MEAN = .false.
   TAG = '  '
end if
Blocks: do NBLOCL = NFIRST, NLAST
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5010) ! dashed line
   ! Load NMON as needed: change current value only when
   if (MODEG == 3 .and. PRSWG == 1) then ! printing the entire series
      NMON = NAMONG(NBLOCL)
      ! When printing the entire series, the last table is mean values
      if (NBLOCL == 13) then
         MEAN = .true.
         TAG = '**'
      end if
   end if
   ! Load character string for transmitting K to table headers
   write (KOUT,fmt='(I2.2)') NBLOCL
   write (RPTLUN,fmt='(A)') ' Table 6.'//KOUT//'.  '//NMON//&
      ' environmental inputs: sediment properties.'//TAG
   write (RPTLUN,5010) ! dashed line
   write (RPTLUN,fmt=ColumnLabels)&
      'Seg  T*    SUSED    BULKD    PCTWA    FROC      CEC       AEC',&
      ' #   y     mg/L     g/cm3      %                meq/100g (dry)'
   write (RPTLUN,5010) ! dashed line
   ! Begin loop on segments
   Segments: do J = 1, KOUNT
      ! Transfer data to output vector
      if (TYPEG(J) == 'B') then
         OUT4(1) = 0.0
         OUT4(2) = BULKDG(J,NBLOCL)
         OUT4(3) = PCTWAG(J,NBLOCL)
      else
         OUT4(1) = SUSEDG(J,NBLOCL)
         OUT4(2) = 0.0
         OUT4(3) = 0.0
      endif
      OUT4(4) = FROCG(J,NBLOCL)
      OUT4(5) = CECG(J,NBLOCL)
      OUT4(6) = AECG(J,NBLOCL)
      ! Write line to internal file:
      write (OUTLIN,fmt=OUTLIN_Format) J,TYPEG(J),(OUT4(I),I=1,6)
      K = 1    ! Blank out zero entries
      do I = 11+Offset, 56+Offset, 9
         if (OUT4(K) .Equals. 0.0) OUTLIN(I:I+8) = '         '
         if (OUTLIN(I+5:I+8) == 'E+00') OUTLIN(I+5:I+8) = '    '
         K = K+1
      end do
      write (RPTLUN,fmt=LineFormat) trim(OUTLIN)
   end do Segments
   write (RPTLUN,5010) ! dashed line
   write (RPTLUN,5020) ! key to segment types
   if (TAG(1:1) == '*') write (RPTLUN,5030) TAG
end do Blocks

write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
write (RPTLUN,5010) ! dashed line
write (RPTLUN,fmt='(A)')&   ! Table header
   ' Table 7.  Environmental input data: physical geometry.'
write (RPTLUN,5010) ! dashed line
write (RPTLUN,fmt=ColumnLabels)&
   'Seg  T*   VOLume    AREA     DEPTH    XSA      LENGth   WIDTH',&
   ' #   y      m3       m2        m       m2        m        m'
write (RPTLUN,5010) ! dashed line
do J = 1, KOUNT ! Load output vector
   OUT4(1) = VOLG(J)
   OUT4(2) = AREAG(J)
   OUT4(3) = DEPTHG(J)
   OUT4(4) = XSAG(J)
   OUT4(5) = LENGG(J)
   OUT4(6) = WIDTHG(J)
   ! Write line to internal file
   write (OUTLIN,fmt=OUTLIN_Format) J,TYPEG(J),(OUT4(I),I=1,6)
   K = 1    ! Blank out zero entries
   do I = 11+Offset, 56+Offset, 9
      if (OUT4(K) .Equals. 0.0) OUTLIN(I:I+8) = '         '
      if (OUTLIN(I+5:I+8) == 'E+00') OUTLIN(I+5:I+8) = '    '
      K = K+1
   end do
   write (RPTLUN,fmt=LineFormat) trim(OUTLIN)
end do
write (RPTLUN,5010) ! dashed line
write (RPTLUN,5020) ! key to segment types


if (PRSWG == 1 .and. MODEG == 3) then ! Reblank footnote if necessary
   MEAN = .false.
   TAG = '  '
end if
Data_blocks: do NBLOCL = NFIRST, NLAST
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5010) ! dashed line
   ! Load NMON as needed: change current value only when
   if (MODEG == 3 .and. PRSWG == 1) then ! printing the entire series
      NMON = NAMONG(NBLOCL)
      ! When printing the entire series, last table is of mean values
      if (NBLOCL == 13) then
         MEAN = .true.
         TAG = '**'
      end if
   end if
   ! Load character string for transmitting K to table headers:
   write (KOUT,fmt='(I2.2)') NBLOCL
   write (RPTLUN,fmt='(A)') ' Table 8.'//KOUT//'.  '//NMON//&
      ' miscellaneous environmental input data.'//TAG
   write (RPTLUN,5010) ! dashed line
   write (RPTLUN,fmt=ColumnLabels)&
      'Seg  T*    DFAC     DISO2     KO2     WIND     DOC     CHL pgmt',&
      ' #   y     m/m      mg/L    cm/hr@20 m/s@10cm  mg/L      mg/L'
   write (RPTLUN,5010) ! dashed line
   Segment_print: do J = 1, KOUNT
      ! Load output vector
      OUT4(1) = DFACG(J,NBLOCL)
      OUT4(2) = DISO2G(J,NBLOCL)
      OUT4(3) = KO2G(J,NBLOCL)
      OUT4(4) = WINDG(J,NBLOCL)
      OUT4(5) = DOCG(J,NBLOCL)
      OUT4(6) = CHLG(J,NBLOCL)
      ! Write line to internal file
      write (OUTLIN,fmt=OUTLIN_Format) J,TYPEG(J),(OUT4(I),I=1,6)
      K = 1 ! Blank out zero entries
      do I = 11+Offset, 56+Offset, 9
         if (OUT4(K) .Equals. 0.0) OUTLIN(I:I+8) = '         '
         if (OUTLIN(I+5:I+8) == 'E+00') OUTLIN(I+5:I+8) = '    '
         K = K+1
      end do
      write (RPTLUN,fmt=LineFormat) trim(OUTLIN)
   end do Segment_print
   write (RPTLUN,5010) ! dashed line
   write (RPTLUN,5020) ! key to segment types
   if (TAG(1:1) == '*') write (RPTLUN,5030) TAG
end do Data_blocks
return
5000 format ('1','Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2/' Ecosystem: ',A)
5010 format (1X,77('-')) ! dashed line
5020 format('  * Segment types: Littoral, Epilimnetic, Hypolimnetic, Benthic.')
5030 format (1X,A2,' Average of 12 monthly mean values.') ! mode 3 footnote
end Subroutine TABB
