subroutine ENVOUT(LUNNUM,KOUNTER,SetCommand)
! This routine writes the environmental ADB to the
! sequential file connected to LUN RWLUN. (16-MAY-1985, LAB)
! Revised 24-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
use Implementation_Control
use Global_Variables
use Local_Working_Space
Implicit None
! Local variables in this subroutine MAXDAT is
! parameter (sensu Fortran) set in size.f90 (module Initial_Sizes)
real (kind(0E0)), allocatable :: OUT1(:), OUT2(:), OUT3(:,:)
integer, allocatable :: LOC1(:), LOC2(:)
integer :: J, KNT, NSPEC1, NSPEC2, N, NFIRST, NLAST, LUNNUM, J_End
integer, intent(in) :: KOUNTER
logical, intent(in) :: SetCommand ! to indicate a set command is underway
! LUNNUM is logical unit number for reading data files.
! J and N are loop counters.
! NSPEC1 is number of active advective interconnections. It is written as the
! first element in the block of data describing advection in the input data
! file. NSPEC2 is number of active dispersive interconnections, written as
! first element in data describing dispersive connections.
! N, NFIRST, and NLAST control the output of time-variable data.
allocate (OUT1(size(JFRADG)), OUT2(size(JFRADG)), OUT3(size(JFRADG),MAXDAT))
allocate (LOC1(size(JFRADG)), LOC2(size(JFRADG)))

NFIRST=1; NLAST=13 ! for 12 months and one average value
! Write name of ecosystem
write (LUNNUM,fmt='(A)',err=5050) ECONAM
! Write environmental data to the file
write (LUNNUM,5010,err=5050) KOUNTER
write (LUNNUM,5020,err=5050) (TYPEG(J),J=1,KOUNTER)
write (LUNNUM,5000,err=5050) LATG,LONGG,ELEVG
write (LUNNUM,5000,err=5050) (VOLG(J),J=1,KOUNTER)
write (LUNNUM,5000,err=5050) (AREAG(J),J=1,KOUNTER)
write (LUNNUM,5000,err=5050) (DEPTHG(J),J=1,KOUNTER)
write (LUNNUM,5000,err=5050) (XSAG(J),J=1,KOUNTER)
write (LUNNUM,5000,err=5050) (LENGG(J),J=1,KOUNTER)
write (LUNNUM,5000,err=5050) (WIDTHG(J),J=1,KOUNTER)
! Determine number of entries used to specify advective flow:
! Clear compression vectors:
LOC1 = 0
LOC2 = 0
OUT1 = 0.0
KNT = 0
! If a set command is in progress, all locations that refer to
! elements no longer appropriate to the new system are cleared
if (SetCommand) then
   do J = 1, size(JFRADG)
      if (JFRADG(J)>KOUNTER) JFRADG(J)=0
      if (ITOADG(J)>KOUNTER) ITOADG(J)=0
      if (JTURBG(J)>KOUNTER) JTURBG(J)=0
      if (ITURBG(J)>KOUNTER) ITURBG(J)=0
   end do
end if
! Load compression vector from database:
! Establish size of decriptor vectors
J_End = size(JFRADG)
do J = 1, J_End
   if (JFRADG(J) == 0 .and. ITOADG(J) == 0) cycle
   KNT = KNT+1
   LOC1(KNT) = JFRADG(J)
   LOC2(KNT) = ITOADG(J)
   OUT1(KNT) = ADVPRG(J)
end do
! Clean up the ADB:
   JFRADG = LOC1
   ITOADG = LOC2
   ADVPRG = OUT1
NSPEC1 = KNT
write (LUNNUM,5010,err=5050) NSPEC1
write (LUNNUM,5010,err=5050) (JFRADG(J),J=1,NSPEC1)
write (LUNNUM,5010,err=5050) (ITOADG(J),J=1,NSPEC1)
write (LUNNUM,5000,err=5050) (ADVPRG(J),J=1,NSPEC1)
! Determine number of entries used to specify dispersive flow:
! Clear the compression vector:
LOC1 = 0
LOC2 = 0
OUT1 = 0.0
OUT2 = 0.0
OUT3 = 0.0
! Load compression vectors from activity database
KNT = 0
do J = 1, J_End
   if (JTURBG(J) == 0 .and. ITURBG(J) == 0) cycle
   KNT = KNT+1
   LOC1(KNT) = JTURBG(J)
   LOC2(KNT) = ITURBG(J)
   OUT1(KNT) = XSTURG(J)
   OUT2(KNT) = CHARLG(J)
   do N = NFIRST, NLAST
      OUT3(KNT,N) = DSPG(J,N)
   end do
end do
! Clean up the ADB
JTURBG = LOC1
ITURBG = LOC2
XSTURG = OUT1
CHARLG = OUT2
DSPG   = OUT3
! Download data to file
NSPEC2 = KNT
write (LUNNUM,5010,err=5050) NSPEC2
write (LUNNUM,5010,err=5050) (JTURBG(J),J=1,NSPEC2)
write (LUNNUM,5010,err=5050) (ITURBG(J),J=1,NSPEC2)
write (LUNNUM,5000,err=5050) (XSTURG(J),J=1,NSPEC2)
write (LUNNUM,5000,err=5050) (CHARLG(J),J=1,NSPEC2)

do N = NFIRST, NLAST
   write (LUNNUM,5000,err=5050) (DSPG(J,N),J=1,NSPEC2)
   write (LUNNUM,5000,err=5050) (WINDG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (STFLOG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (STSEDG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (NPSFLG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (NPSEDG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (SEEPSG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) RAING(N)
   write (LUNNUM,5000,err=5050) CLOUDG(N)
   write (LUNNUM,5000,err=5050) OZONEG(N)
   write (LUNNUM,5000,err=5050) RHUMG(N)
   write (LUNNUM,5000,err=5050) ATURBG(N)
   write (LUNNUM,5020,err=5050) AIRTYG(N)
   write (LUNNUM,5000,err=5050) (DFACG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (EVAPG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (SUSEDG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (BULKDG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (PCTWAG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (FROCG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (CECG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (AECG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (TCELG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (PHG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (POHG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) OXRADG(N)
   write (LUNNUM,5000,err=5050) (BACPLG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (BNBACG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (PLMASG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (BNMASG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (KO2G(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (DOCG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (CHLG(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (DISO2G(J,N),J=1,KOUNTER)
   write (LUNNUM,5000,err=5050) (REDAGG(J,N),J=1,KOUNTER)
end do
! End of environmental data entry.
deallocate (OUT1, OUT2, OUT3, LOC1, LOC2)
return
5000  format (1PG10.4,7G10.4)
5010  format (16I5)
5020  format (80A1)
5050  write(stdout,fmt='(/A)') ' Error writing environmental data.',&
      ' Check results before proceeding.'
end subroutine ENVOUT
