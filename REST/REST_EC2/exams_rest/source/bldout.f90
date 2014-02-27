subroutine BLDOUT(SUBS,NAME) ! Purpose: to complete the creation of the output
                             ! format and associated variable.
! Internal subroutine required: ITOS
! Revised 24-DEC-1985, 24-APR-1987 (LAB)
! Revisions 10/21/1988--run-time implementation of machine dependencies
! Revision 02/05/2000 -- to get single-spaced output on "show" command
! Revision 02/07/2001 -- L1 converted to len=50 to capture Names;
!   revisions implemented at format of output of L1
use Implementation_Control
use Alias_Transfer
Implicit None
integer :: CRDCOL, SUBS(6), LENGTH(3)
integer :: ITS,ITDTD,LENT,I,IM1,LENX,J
character(len=1) :: SEP, NAME(6), ARRAY(5,3), OUTPUT(13)
character(len=1), dimension (34) :: fmt =&
!(/'(',' ','/',',','1','X',',',' ','A','1',',',' ',' ','A','1',',','1','X',&
!           |
! note deletion of '/' -- this now gives single-spaced output on "show" cmd
!          |
(/'(',' ',' ',',','1','X',',',' ','A','1',',',' ',' ','A','1',',','1','X',&
',','2','A','1',',','1','X',',',' ',' ',' ',' ',' ',' ',' ',')'/)
character(len=1) :: IS(2) = (/'i','s'/), LGN(6) = (/'1','2','3','4','5','6'/)
character(len=1), dimension(7,5) :: OUTFMT = reshape (&
   (/'1', 'P', 'G', '1', '1', '.', '4',&
     '1', 'P', 'G', '1', '1', '.', '4',&
     '1', 'P', 'G', '1', '1', '.', '4',&
     ' ', ' ', 'I', '1', '1', ' ', ' ',&
     ' ', ' ', 'A', '1', ' ', ' ', ' '/), (/7,5/))
! Get arguments
ICL1 = SUBS(1)
ICL2 = SUBS(2)
ICL3 = SUBS(3)
ITS = SUBS(4)
ITDTD = SUBS(5)
LENT = SUBS(6)
fmt(8) = LGN(LENT)
do I = 1, 7
   fmt(I+26) = OUTFMT(I,ITDTD)
end do
LENGTH = 0
CRDCOL = 1
OUTPUT(1) = ' '
if (ITS /= 1) then
   if (ITS > 1) call ITOS (ICL1,ARRAY(1,1),LENGTH(1))
   if (ITS > 2) call ITOS (ICL2,ARRAY(1,2),LENGTH(2))
   if (ITS > 3) call ITOS (ICL3,ARRAY(1,3),LENGTH(3))
   CRDCOL = 0
   do I = 2, 4
      IM1 = I-1
      if (I > ITS) cycle
      SEP = '('
      if (IM1 > 1) SEP = ','
      CRDCOL = CRDCOL+1
      OUTPUT(CRDCOL) = SEP
      LENX = LENGTH(IM1)
      do J = 1, LENX
         CRDCOL = CRDCOL+1
         OUTPUT(CRDCOL) = ARRAY(J,IM1)
      end do
   end do
   CRDCOL = CRDCOL+1
   OUTPUT(CRDCOL) = ')'
end if
call ITOS (CRDCOL,ARRAY(1,1),LENX)
if (LENX == 2) then
   fmt(12) = ARRAY(1,1)
   fmt(13) = ARRAY(2,1)
else
   fmt(12) = ' '
   fmt(13) = ARRAY(1,1)
end if
select case (ITDTD)
case (1) ! Complex data type
   write (stdout,fmt='(/A/)')&
      ' Complex data specified, not implemented.'
case (2) ! real (kind (0D0)),i.e., high precision data type
   write (stdout,fmt=fmt)&
      (NAME(I),I=1,LENT),(OUTPUT(I),I=1,CRDCOL),IS,R8
case (3) ! real (kind (0E0)) data type
   write (stdout,fmt=fmt)&
      (NAME(I),I=1,LENT),(OUTPUT(I),I=1,CRDCOL),IS,R4
case (4) ! integer data type
   write (stdout,fmt=fmt)&
      (NAME(I),I=1,LENT),(OUTPUT(I),I=1,CRDCOL),IS,I2
case (5) ! character ("logical") data type
! Conversion of names to len=50 characters required revision of output command
!OLD   write (stdout,fmt=fmt)&
!OLD      (NAME(I),I=1,LENT),(OUTPUT(I),I=1,CRDCOL),IS,L1
   write (stdout,fmt=fmt, advance='NO')&
      (NAME(I),I=1,LENT),(OUTPUT(I),I=1,CRDCOL),IS
   write (stdout,fmt='(A)') trim(L1)
end select
contains
subroutine ITOS(INPUT,OUTPUT,LENGTH)
! Purpose: to convert an integer in the range of 1 to 99999
! to a character string and store the results in an array section
integer :: I, LENGTH
integer, intent (in) :: INPUT
character(len=1), intent (out) :: OUTPUT(1)
character(len=5) :: TEMP
write (TEMP,fmt='(I5)') INPUT ! Load character value in TEMP
LENGTH = 0
do I = 1, 5    ! Load output array and determine its length
   if (TEMP(I:I) == ' ') cycle ! i.e., skip lead blanks
   LENGTH = LENGTH+1
   OUTPUT(LENGTH) = TEMP(I:I)
end do
end Subroutine ITOS
end Subroutine BLDOUT
