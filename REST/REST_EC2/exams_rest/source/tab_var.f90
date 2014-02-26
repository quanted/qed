module Table_Variables ! File Tab_var.F90
use Initial_Sizes
use Global_Variables, only: KOUNT, KCHEM
Implicit None
Save
! Variables for PRENV et seq.
real (kind(0E0)),  allocatable,     public :: OUT1(:), OUT2(:), OUT3(:)
real (kind(0E0)),  dimension(6),    public :: OUT4
integer, allocatable,               public :: LOC1(:), LOC2(:)
integer, public :: NFIRST, NLAST
logical, public :: MEAN
character(len=2), public ::  KOUT, TAG ! for listing months and for footnote
character(len=4), public ::  NMON
! Up to KountMult*KOUNT values may require printing; 
!    variables are allocated as needed
! NFIRST and NLAST are loop controllers in the called routines.
! MEAN signals the need to compute mean values.
! NMON is the name of a month, transferred from NAMONG.
integer, private :: NumX ! the space required for integer representation of
                         ! KOUNT to adjust formats when KOUNT>999
integer :: Offset ! for blanking zeros in output text
character (len=14) :: ColumnLabels = '(1X,A:/1X,A)  '
character (len=7)  :: LineFormat = '(A)    ' ! write formatted line to report
character (len=11), private :: KountKOUNT
character(len=11), dimension(4) :: ITOP
character(len=4), dimension(7) :: PIECE = &
   (/'(-3)','(-2)','(-1)',' (0)','(+1)','(+2)','(+3)'/)
! Write data to formatted line (internal file) for preparation for report
character (len=35) :: OUTLIN_Format = '(1X,I3,2X,A1,3X,1PE9.2,5E9.2)      '
! Format for Table 13 water column segments with air/water interface
character (len=35) :: T13F1 = '(1X,I3,2X,A1,3F6.1,1PG9.1,I5,4G9.1)'
! Format for Table 13 water column segments lacking air/water interface
character (len=38) :: T13F2 = '(1X,I3,2X,A1,3F6.1,9X,I5,1PG9.1,3G9.1)'
! Format for Table 13 Benthic segments
character (len=39) :: T13F3 = '(1X,I3,2X,A1,3F6.1,14X,1PG9.1,18X,G9.1)'

character (len=50) :: Table15a_Format =&
      '(1X,I3,1X,1PG9.2,1X,0PF6.2,1X,1PG10.3,3(1X,G10.3))'
character (len=41) :: Table15b_Format =&
      "(6X,8('='),1X,6('=')/5X,1PG9.2,1X,0PF6.2)"
character (len=28) :: Table16_Format = '(1X,I3,2X,A1,1PE11.2,5E11.2)'
character (len=36) :: T17Mean = "(' Mean       ',1PG10.3,3(8X,G10.3))"
character (len=29) :: T17Max  = "(' Max',4(I6,')',1X,1PG10.3))"
character (len=29) :: T17Min  = "(' Min',4(I6,')',1X,1PG10.3))"

contains
subroutine Allocate_Table_Variables
if (allocated(OUT1)) deallocate (OUT1,OUT2,OUT3,LOC1,LOC2)
allocate (OUT1(KountMult*KOUNT), OUT2(KountMult*KOUNT), &
          OUT3(KountMult*KOUNT),&
          LOC1(KountMult*KOUNT), LOC2(KountMult*KOUNT))
end subroutine Allocate_Table_Variables

subroutine SetFormats
! Adjust format statements if need more than 3 spaces (KOUNT>999)
if (KOUNT>999) then ! adjustments required -- executed in RUNIT
   write (KOUNTkount,fmt='(I0)') KOUNT
   NumX = len_trim(KOUNTkount)
   write (ColumnLabels, fmt='(A1,I0,A5,I0,A)')'(', NumX-2,'X,A:/',NumX,'X-2,A)'
   write (LineFormat, fmt='(A1,I0,A4)') '(',NumX-3,'X,A)'
   write (OUTLIN_Format,fmt='(A5,I0,A)') '(1X,I',NumX,',2X,A1,3X,1PE9.2,5E9.2)'
write (T13F1,fmt='(A5,I0,A)') '(1X,I',NumX,',2X,A1,3F6.1,1PG9.1,I5,4G9.1)'
write (T13F2,fmt='(A5,I0,A)') '(1X,I',NumX,',2X,A1,3F6.1,9X,I5,1PG9.1,3G9.1)'
write (T13F3,fmt='(A5,I0,A)') '(1X,I',NumX,',2X,A1,3F6.1,14X,1PG9.1,18X,G9.1)'
   write (Table15a_Format,fmt='(A5,I0,A)')&
      '(1X,I',NumX,',1X,1PG9.2,1X,0PF6.2,1X,1PG10.3,3(1X,G10.3))'
   write (Table15b_Format,fmt='(A1,I0,A19,I0,A)') '(', NumX+3,&
      "X,8('='),1X,6('=')/",NumX+2,"X,1PG9.2,1X,0PF6.2)"
   write (Table16_Format,fmt='(A5,I0,A)')'(1X,I',NumX,',2X,A1,1PE11.2,5E11.2)'
   Offset = NumX-3
else ! standard formats adequate; reload here in case KOUNT was decreased
   write (ColumnLabels,   fmt='(A)')  '(1X,A,:/1X,A)'
   write (LineFormat,     fmt='(A)')  '(A)'
   write (OUTLIN_Format,  fmt='(A)')  '(1X,I3,2X,A1,3X,1PE9.2,5E9.2)'
   write (T13F1,          fmt='(A)')  '(1X,I3,2X,A1,3F6.1,1PG9.1,I5,4G9.1)'
   write (T13F2,          fmt='(A)')  '(1X,I3,2X,A1,3F6.1,9X,I5,1PG9.1,3G9.1)'
   write (T13F3,          fmt='(A)')  '(1X,I3,2X,A1,3F6.1,14X,1PG9.1,18X,G9.1)'
   write (Table15a_Format,fmt='(A)')&
      '(1X,I3,1X,1PG9.2,1X,0PF6.2,1X,1PG10.3,3(1X,G10.3))'
   write (Table15b_Format, fmt='(A)')&
      "(6X,8('='),1X,6('=')/5X,1PG9.2,1X,0PF6.2)"
   write (Table16_Format, fmt='(A)')  '(1X,I3,2X,A1,1PE11.2,5E11.2)'
   Offset=0
end if; end subroutine SetFormats; end module Table_Variables
