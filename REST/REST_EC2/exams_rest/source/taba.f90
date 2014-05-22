subroutine TABA ! prints Table 4 and Table 5
! Created 10 November 1983 (LAB) by disaggregation of PRENV.
! Revised 21-AUG-85 (LAB) -- table header
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revision 09-Feb-1999 to use floating point comparison module
! Revision April 2001 for wider output format and dynamic memory support
! Revision April 2002 to support not producing report.xms
use Floating_Point_Comparisons
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Table_Variables

Implicit None
logical :: test
integer :: I, J, K, NBLOCL ! Local counters and check variables
character(len=78) :: OUTLIN

! In mode 3, the mean values are calculated for output or use in other modes
if (MODEG==3) then ! calculate means
   do J=1,KOUNT
      OUT4 = 0.0
      do I = 1, 12
         if (TYPEG(J) == 'B') then
            OUT4(2) = OUT4(2)+BNBACG(J,I)
            OUT4(4) = OUT4(4)+BNMASG(J,I)
         else
            OUT4(1) = OUT4(1)+BACPLG(J,I)
            OUT4(3) = OUT4(3)+PLMASG(J,I)
         endif
      end do
      OUT4 = OUT4/12.0
      BACPLG(J,13) = OUT4(1) ! Transfer average values
      BNBACG(J,13) = OUT4(2) ! to sector 13 of database
      PLMASG(J,13) = OUT4(3)
      BNMASG(J,13) = OUT4(4)
   end do

   do J=1,KOUNT
      OUT4 = 0.0
      do I = 1, 12   ! accumulate values over 12 months
         OUT4(1) = OUT4(1)+STFLOG(J,I)
         OUT4(2) = OUT4(2)+STSEDG(J,I)
         OUT4(3) = OUT4(3)+NPSFLG(J,I)
         OUT4(4) = OUT4(4)+NPSEDG(J,I)
         OUT4(5) = OUT4(5)+SEEPSG(J,I)
!          if (J == 1 .or. (TYPEG(J) /= 'B'.and. TYPEG(J-1) == 'B')) &
!             OUT4(6) = OUT4(6)+EVAPG(J,I)
         if (J == 1) then        !2013-05-30
            test=.true.
         else
            test= (TYPEG(J) /= 'B'.and. TYPEG(J-1) == 'B') 
         end if
         if (test) then
            OUT4(6) = OUT4(6)+EVAPG(J,I)
         end if
      end do
      OUT4 = OUT4/12.0 ! Compute mean values
      ! Transfer mean values to sector 13 of database:
      STFLOG(J,13) = OUT4(1)
      STSEDG(J,13) = OUT4(2)
      NPSFLG(J,13) = OUT4(3)
      NPSEDG(J,13) = OUT4(4)
      SEEPSG(J,13) = OUT4(5)
      EVAPG(J,13)  =  OUT4(6)
   end do
end if

! if report file is not to be written, return now
if (.not. RPTFIL) return

! Iinitialize table footnote
if (PRSWG == 1 .and. MODEG == 3) then
   MEAN = .false.
   TAG = '  '
end if

Block_loop: do NBLOCL = NFIRST, NLAST
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5010) ! dashed line
   ! Load NMON: change current value only when printing the entire series
   if (MODEG == 3 .and. PRSWG == 1) then
      NMON = NAMONG(NBLOCL)
     ! When printing the entire series, the last table is mean values
         if (NBLOCL == 13) then
           MEAN = .true.
           TAG = '**'
         end if
   end if
   ! Load character string for transmitting NBLOCL to table headers
   write (KOUT,fmt='(I2.2)') NBLOCL
   write (RPTLUN,fmt='(A)') ' Table 4.'//KOUT//'.  '//NMON//&
      ' environmental input data: biologicals.'//TAG
   write (RPTLUN,5010) ! dashed line
   write (RPTLUN,fmt=ColumnLabels)&
   'Seg  T*    BACPL    BNBAC    PLMAS    BNMAS',&
   ' #   y    cfu/ml   cfu/100g  mg/L    dry g/m2'
   write (RPTLUN,5010) ! dashed line
   Segment_loop: do J = 1, KOUNT
      OUT4 = 0.0     ! Initialize the output vector
      if (TYPEG(J) == 'B') then     ! Transfer data to output vector
         OUT4(2) = BNBACG(J,NBLOCL)
         OUT4(4) = BNMASG(J,NBLOCL)
      else
         OUT4(1) = BACPLG(J,NBLOCL)
         OUT4(3) = PLMASG(J,NBLOCL)
      endif
      OUT4(5) = 0.0 ! note two slots available for more biological data
      OUT4(6) = 0.0
      write (OUTLIN,OUTLIN_Format) J,TYPEG(J),(OUT4(I),I=1,6) ! internal file
      K = 1    ! Blank out zero entries
      do I = 11+Offset, 56+Offset, 9
         if (OUT4(K) .Equals. 0.0) OUTLIN(I:I+8) = '         '
         if (OUTLIN(I+5:I+8) == 'E+00') OUTLIN(I+5:I+8) = '    '
         K = K+1
      end do
      write (RPTLUN,fmt=LineFormat) trim(OUTLIN)
   end do Segment_loop
   write (RPTLUN,5010) ! dashed line
   write (RPTLUN,5020) ! segment type footnote
   if (TAG(1:1) == '*') write (RPTLUN,5030) TAG
end do Block_loop

! Re-initialize table footnote
if (PRSWG == 1 .and. MODEG == 3) then
   MEAN = .false.
   TAG = '  '
end if

Block_loop_2: do NBLOCL = NFIRST, NLAST
   write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,5010) ! dashed line
   ! Load NMON as needed: change current value only when printing
   ! the entire series ...
   if (MODEG == 3 .and. PRSWG == 1) then
      NMON = NAMONG(NBLOCL)
      ! When printing the entire series, the last table is mean values
      if (NBLOCL == 13) then
         MEAN = .true.
         TAG = '*'
      end if
   end if
   ! Load character string for transmitting NBLOCL to table headers
   write (KOUT,fmt='(I2.2)') NBLOCL
   write (RPTLUN,fmt='(A)') ' Table 5.'//KOUT//'.  '//NMON//&
      ' environmental data: hydrologic parameters.'//TAG
   write (RPTLUN,5010) ! dashed line
   write (RPTLUN,fmt=ColumnLabels)&
      'Seg  T*    STFLO    STSED    NPSFL    NPSED    SEEPS     EVAP',&
      ' #   y     m3/hr    kg/hr    m3/hr    kg/hr    m3/hr     mm/mon'
   write (RPTLUN,5010) ! dashed line
   Segment_loop_2: do J = 1, KOUNT
      OUT4 = 0.0     ! Fail-safe: Initialize the vector
      ! Load the output vector
      OUT4(1) = STFLOG(J,NBLOCL)
      OUT4(2) = STSEDG(J,NBLOCL)
      OUT4(3) = NPSFLG(J,NBLOCL)
      OUT4(4) = NPSEDG(J,NBLOCL)
      OUT4(5) = SEEPSG(J,NBLOCL)
!       if (J==1 .or. (TYPEG(J)/='B' .and. TYPEG(J-1)=='B')) then
!          OUT4(6) = EVAPG(J,NBLOCL)
!       else ! the segment is not a water column with an air-water interface, so

      if (J == 1) then        !2013-05-30
         test=.true.
      else
         test= (TYPEG(J)/='B' .and. TYPEG(J-1)=='B') 
      end if
      if (test) then
         OUT4(6) = EVAPG(J,NBLOCL)
      else ! the segment is not a water column with an air-water interface, so

         EVAPG(J,NBLOCL) = 0.0 ! zero out evaporation
         OUT4(6) = EVAPG(J,NBLOCL)
      end if
      write (OUTLIN,OUTLIN_Format) J,TYPEG(J),(OUT4(I),I=1,6) ! internal file
      K = 1    ! Blank out zero entries
      do I = 11+Offset, 56+Offset, 9
         if (OUT4(K) .Equals. 0.0) OUTLIN(I:I+8) = '         '
         if (OUTLIN(I+5:I+8) == 'E+00') OUTLIN(I+5:I+8) = '    '
         K = K+1
      end do
      write (RPTLUN,fmt=LineFormat) trim(OUTLIN)
   end do Segment_loop_2
   write (RPTLUN,5010) ! dashed line
   write (RPTLUN,5020) ! segment type footnote
end do Block_loop_2
if (TAG(1:1) == '*') write (RPTLUN,5030) TAG
return
5000 format ('1','Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2/' Ecosystem: ',A)
5010 format (1X,77('-'))   ! dashed line
5020 format&
   ('  * Segment types: Littoral, Epilimnetic, Hypolimnetic, Benthic.')
5030 format (1X,A2,' Average of 12 monthly mean values.') ! mode 3 footnote
end Subroutine TABA
