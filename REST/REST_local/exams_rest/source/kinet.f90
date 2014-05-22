subroutine KINET(KIN,MCHEMG,KOUNT)
! Purpose: To print the contents of the kinetics file to a print file.
! Subroutines required: KINHED, KINLIS, KINPLT, KINRED, KINSEL
! Revised 24-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
! Revisions 11/22/88 to generalize header code using NSLINE
! Converted to Fortran90 6/18/96
! Revised 08-Feb-1999 to use floating point comparisons
use Implementation_Control
use Floating_Point_Comparisons
Implicit None
real :: TABLE(132),OUTPUT(7),PMIN(7),PMAX(7),P
integer, dimension(7) :: SELECT
integer :: DUMP = 0, MAXP = 7
integer :: IERR,KOUNT,ICODE,MCHEMG,KNT,K,J,II,K1,K2
integer :: I,NSEL,IHIT,IOFF,L,KIN
! NSLINE is the Number of Segments per output LINE (3 spaces per)
integer, parameter :: NSLINE=20
character(len=50) :: CHEMNA, ECONAM
character(len=1), dimension(kount) :: TYPEG
character(len=6), dimension(4) :: TUNIT = &
   (/'Hours ','Days  ','Months','Years '/)
! zero data area
table=0.0; output=0.0
! Get the descriptive information
rewind PLTLUN
call KINHED (IERR,CHEMNA,ECONAM,KOUNT,TYPEG,ICODE,MCHEMG)
if (IERR == 1) return
if (IERR == 2) then
   write (stdout,fmt='(//A,I5)')&
      ' No data available with MCHEM set to: ',MCHEMG
   return
end if
write (stdout,fmt='(/,2(/,A))')&
   ' Chemical: '//trim(CHEMNA),' Environment: '//trim(ECONAM)
write (stdout,fmt='(/A/A,I4)')&
   ' Simulation units:   '//TUNIT(ICODE),' Number of segments: ',KOUNT
KNT = KOUNT
K = KNT/NSLINE
J = KNT-NSLINE*K
if (J /= 0) K = K+1
do II = 1, K
   K1 = (II-1)*NSLINE+1
   K2 = K1+NSLINE-1
   if (K2 > KNT) K2 = KNT
   write (stdout,5020) (I,I=K1,K2)
   write (stdout,5030) (TYPEG(I),I=K1,K2)
end do
call KINSEL (MAXP,KOUNT,NSEL,SELECT)
if (NSEL==0) then ! Plot cancelled by user
   return
elseif (NSEL==1) then ! if NSEL = 1, only an abcissa, no ordinate
   write (stdout,fmt='(//A)')&
      ' No parameters selected; PLOT cancelled.'
   return
end if
do I = 1, NSEL
   PMAX(I) = -1.0E+30
   PMIN(I) =  1.0E+30
end do
rewind PLTLUN
call KINHED (IERR,CHEMNA,ECONAM,KOUNT,TYPEG,ICODE,MCHEMG)

if (IERR /= 1) then
   if (DUMP /= 0) then
      write (stdout,fmt='(/2(/A))')&
         ' Chemical: '//trim(CHEMNA),' Environment: '//trim(ECONAM)
      write (stdout,fmt='(/A/A,I4)')&
         ' Simulation units:   '//TUNIT(ICODE),' Number of segments: ',KOUNT
      KNT = KOUNT
      K = KNT/10
      J = KNT-10*K
      if (J /= 0) K = K+1
      do II = 1, K
         K1 = (II-1)*10+1
         K2 = K1+9
         if (K2 > KNT) K2 = KNT
         write (stdout,5020) (I,I=K1,K2)
         write (stdout,5030) (TYPEG(I),I=K1,K2)
      end do
   end if
   do
      call KINRED (IERR,KOUNT,TABLE,IHIT,MCHEMG)
      if (IERR == 2) exit
      if (DUMP /= 0) then
         write (stdout,fmt='(" $AVE",7G10.3)') (TABLE(I),I=1,7)
         do I = 1, KOUNT
            IOFF = (I-1)*5+7
            K = IOFF+5
            J = IOFF+1
            write (stdout,fmt='(A,G10.3,3X,A1,1X,5E10.3)')&
               ' $COM',TABLE(1),TYPEG(I),(TABLE(L),L=J,K)
         end do
      end if
      do I = 1, NSEL
         K = SELECT(I)
         P = TABLE(K)
         if (P .GreaterThan. PMAX(I)) PMAX(I) = P
         if (P .LessThan. PMIN(I)) PMIN(I) = P
      end do
   end do
end if
if (DUMP /= 0) then
   do I = 1, NSEL
      K = SELECT(I)
      write (stdout,fmt='(/A,I3,A,1PE10.3,A,E10.3)')&
         ' DATUM (K) ',K,' MIN: ',PMIN(I),' MAX: ',PMAX(I)
   end do
end if
if (KIN == 1) call KINLIS (KOUNT,SELECT,NSEL,TABLE,OUTPUT,TYPEG,&
   CHEMNA,ECONAM,MCHEMG)
if (KIN == 2) call KINPLT (KOUNT,SELECT,NSEL,TABLE,OUTPUT,TYPEG,&
   CHEMNA,ECONAM,PMAX,PMIN,MCHEMG)
return
! format statements are set up for 10000 groups as a maximum
! overkill because "parameter" stmnt can't be used in format
5020  format (' Segment Number: ',10000(I2,1X))
5030  format (' Segment "TYPE": ',10000(1X,A1,1X))
end Subroutine KINET
