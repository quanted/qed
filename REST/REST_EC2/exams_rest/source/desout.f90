subroutine DESOUT(INDX,NAME,NAME_SIZE,TTYOUT)
! Purpose: to format output record for DESCRIBE command and first line of HELP
! Example outputs:
!  NAME is a real scalar. (TEND)
!  NAME is a character vector with 10 elements. (AIRTY)
!  NAME is an integer matrix with 10 rows and 25 columns. (SPFLG)
!  NAME is a real table with dimensions (10,5,15). (QUANT)
! Subroutines required: none
use Model_Parameters
Implicit None
integer, intent (in) :: TTYOUT, INDX, NAME_SIZE
! INDX is the number of the variable to be reported
! NAME_SIZE is the number of characters in the name of the variable
! NAME is the (input) name of the variable
! OUTLIN is output line, constructed as an internal file and written to TTYOUT
! TTYOUT is the output Logical Unit Number
! TEMP is an internal file for writing dimensions...set to 10 for huge size
character :: OUTLIN*80,TEMP*10
integer :: I, TOP
character, intent(in) :: NAME(NAME_SIZE)
character(len=17), dimension(5) :: TYDAT=&
(/' complex         ',' high   precision',' real            ',&
  ' integer         ',' character       '/)
character(len=6),dimension(4) :: STTYP=(/'scalar','vector','matrix','table '/)
OUTLIN = ' ' ! Initialize output line
! Enter the name of the variable--name should be no more than 6 or so...
write (OUTLIN,FMT='(80A1)') (NAME(I),I=1,NAME_SIZE)
OUTLIN = trim(outlin)//' is a'
if (TD(INDX) == 4) OUTLIN = trim(outlin)//'n' ! If an integer, make it "is an"
! Add the data type (complex, high precision, real, etc.)
OUTLIN=trim(outlin)//TYDAT(TD(INDX)) ! the TYDAT include a leading blank
! Add the storage type (scalar, vector, matrix, table;
OUTLIN=trim(outlin)//' '//STTYP(TS(INDX)) ! here must add leading blank)
! Now separate storage types
scalar: if (TS(INDX) == 1) then ! scalar--add period and finish
   OUTLIN=trim(outlin)//'.'
   write (TTYOUT,FMT='(/,1X,A)') trim(OUTLIN)
   return
endif scalar
OUTLIN=trim(outlin)//' with' ! Not a scalar
if (TS(INDX) == 4) OUTLIN=trim(outlin)//' dimensions ('
write (TEMP,FMT='(I10)') TCL1(INDX)
select case (TS(INDX)) ! for matrix and vector, need ' ' after "with", but
case (4) ! for table, start dimension numbers directly following "("
   do I = 1, 10 ! Note the use of "trim" within loop to cut off the leading
      OUTLIN=trim(outlin)//TEMP(I:I)  ! blanks from the I10 format. Further
   end do ! down, this is done by a loop cyle on blank elements of TEMP.
case (2,3) ! for vectors and matrices, start after added space
   TOP = len_trim(OUTLIN)+1
   OUTLIN(TOP:TOP) = ' '
   do I = 1, 10   ! only write the non-blank characters
      if (TEMP(I:I) == ' ') cycle
      TOP = TOP + 1
      OUTLIN(TOP:TOP) = TEMP(I:I)
   end do
end select
vector: if (TS(INDX) == 2) then ! If a Vector, add term and finish
   OUTLIN=trim(outlin)//' elements.'
   write (TTYOUT,FMT='(/,1X,A)') trim(OUTLIN)
   return
endif vector
if (TS(INDX) == 3) then ! for a matrix
   OUTLIN=trim(outlin)//' rows and'
else ! for a table
   OUTLIN=trim(outlin)//','
endif
write (TEMP,FMT='(I10)') TCL2(INDX)
TOP = len_trim(OUTLIN)
if (TS(INDX) == 3) then ! add space after "rows" for a matrix
   TOP = TOP+1
   OUTLIN(TOP:TOP) = ' '
end if
do I = 1, 10 ! write the non-blank elements (only)
   if (TEMP(I:I) == ' ') cycle
   TOP=TOP+1
   OUTLIN(TOP:TOP) = TEMP(I:I)
end do
if (TS(INDX) == 3) then               ! If a matrix,
   OUTLIN=trim(outlin)//' columns.'   ! add "columns" and finish
   write (TTYOUT,FMT='(/,1X,A)') trim(OUTLIN)
   return
else ! a table
   OUTLIN=trim(outlin)//','
endif
write (TEMP,FMT='(I10)') TCL3(INDX)
do I = 1, 10 ! add on non-blank elements
   if (TEMP(I:I) /= ' ') OUTLIN=trim(outlin)//TEMP(I:I)
end do
outlin = trim(outlin)//').'
write (TTYOUT,FMT='(/,1X,A)') trim(OUTLIN)
end Subroutine DESOUT
