subroutine PAKENV(RECNUM)
! Purpose--to move the individual elements of the environmental
! data to a single variable to facilate output to the daf
! Revised 21-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
use Implementation_Control
! Revised 11/17/88 to accommodate VAX multi-user environment
use Input_Output
use Global_Variables
use Local_Working_Space
use Environmental_Data_Space
Implicit None
real    :: BUFFER(VARREC)
integer :: IBUFF(VARIEC), RRECS, IRECS, CRECS, TRECS,NREALS, NINTS, NCHARS
integer :: RECNUM, OFFSET, NUSED
integer :: RECDAT(FILDAT),HRECS,M,L,ISET,I,J,K
! RECDAT carries the file information, HRECS is the number of
! header records required.
character(len=1) :: CBUFF(VARCEC)
! 12.30.1999: IOC contains the pre-sets for data access passwords and thus
! cannot be made allocatable.
if (Allocated(IO))  Deallocate(IO)
if (Allocated(IOI)) Deallocate(IOI)
Allocate (IO(IOSIZ),IOI(IOISIZ))
IO  = 0.0              ! Zero the main input/output transfer area
IOI = 0

! Read the header record for file control information
HRECS = FILDAT/VARIEC
if (FILDAT-VARIEC*HRECS /= 0) HRECS = HRECS+1
M = 0
Outer_0: do I = 1, HRECS
   read (RANUNT,rec=I) IBUFF
   Inner_0: do L = 1, VARIEC
      M = M+1
      if (M > FILDAT) exit Outer_0
      RECDAT(M) = IBUFF(L)
   end do Inner_0
end do Outer_0

NREALS = RECDAT(25)
NINTS = RECDAT(26)
NCHARS = RECDAT(51)
RRECS = RECDAT(21)
IRECS = RECDAT(22)
CRECS = RECDAT(55)
TRECS = RRECS+IRECS+CRECS
! Load number of ecosystems in database
! NREC   = RECDAT ( 23 )
! Load starting record number of this database
ISET = RECDAT(11)-1
!
! Clear buffer vectors
CBUFF = ' '
IBUFF = 0
BUFFER = 0.0
! Load real datastream, beginning with scalars
IO(1) = LATG
IO(2) = LONGG
IO(3) = ELEVG
NUSED = 3
! Load the environmental vectors
do I = 1, KOUNT
   IO(NUSED+1) = VOLG(I)
   IO(NUSED+2) = AREAG(I)
   IO(NUSED+3) = DEPTHG(I)
   IO(NUSED+4) = XSAG(I)
   IO(NUSED+5) = LENGG(I)
   IO(NUSED+6) = WIDTHG(I)
   NUSED = NUSED+6
end do
! Load the dispersive transport vectors and DSPG
do I = 1, size(XSTURG)
   IO(NUSED+1) = XSTURG(I)
   IO(NUSED+2) = CHARLG(I)
   IO(NUSED+3) = ADVPRG(I)
   NUSED = NUSED+3
   do J = 1, MAXDAT
      IO(NUSED+J) = DSPG(I,J)
   end do
   NUSED = NUSED+MAXDAT
end do
!
! Load the MAXDAT vectors
do I = 1, MAXDAT
   IO(NUSED+1) = OXRADG(I)
   IO(NUSED+2) = CLOUDG(I)
   IO(NUSED+3) = RAING(I)
   IO(NUSED+4) = OZONEG(I)
   IO(NUSED+5) = RHUMG(I)
   IO(NUSED+6) = ATURBG(I)
   NUSED = NUSED+6
end do
! Load the MAXDAT X KOUNT matrices
do I = 1, MAXDAT
   do J = 1, KOUNT
      IO(NUSED+1) = FROCG(J,I)
      IO(NUSED+2) = CECG(J,I)
      IO(NUSED+3) = AECG(J,I)
      IO(NUSED+4) = PCTWAG(J,I)
      IO(NUSED+5) = TCELG(J,I)
      IO(NUSED+6) = PHG(J,I)
      IO(NUSED+7) = POHG(J,I)
      IO(NUSED+8) = REDAGG(J,I)
      IO(NUSED+9) = BACPLG(J,I)
      IO(NUSED+10) = BNBACG(J,I)
      IO(NUSED+11) = PLMASG(J,I)
      IO(NUSED+12) = BNMASG(J,I)
      IO(NUSED+13) = KO2G(J,I)
      IO(NUSED+14) = STFLOG(J,I)
      IO(NUSED+15) = STSEDG(J,I)
      IO(NUSED+16) = NPSFLG(J,I)
      IO(NUSED+17) = NPSEDG(J,I)
      IO(NUSED+18) = SEEPSG(J,I)
      IO(NUSED+19) = DOCG(J,I)
      IO(NUSED+20) = CHLG(J,I)
      IO(NUSED+21) = DFACG(J,I)
      IO(NUSED+22) = DISO2G(J,I)
      IO(NUSED+23) = EVAPG(J,I)
      IO(NUSED+24) = WINDG(J,I)
      IO(NUSED+25) = BULKDG(J,I)
      IO(NUSED+26) = SUSEDG(J,I)
      NUSED = NUSED+26
   end do
end do
! Load the Integer variables
IOI(1) = KOUNT
NUSED = 1
do I = 1, size(JFRADG)
   IOI(NUSED+1) = JFRADG(I)
   IOI(NUSED+2) = ITOADG(I)
   IOI(NUSED+3) = JTURBG(I)
   IOI(NUSED+4) = ITURBG(I)
   NUSED = NUSED+4
end do
! Load the Character variables
do I = 1, 50
   IOC(I) = ECONAM(I:I)
end do
NUSED = 50
do I = 1, 6
   IOC(NUSED+1) = RPASS(2)(I:I)
   IOC(NUSED+2) = WPASS(2)(I:I)
   NUSED = NUSED+2
end do
do I = 1, KOUNT
   IOC(NUSED+I) = TYPEG(I)
end do
NUSED = NUSED+KOUNT
do I = 1, MAXDAT
   IOC(NUSED+I) = AIRTYG(I)
end do
NUSED = NUSED+MAXDAT ! true but currently irrelevant

! Write the data to the random access file
OFFSET = (RECNUM-1)*TRECS+ISET
Outer_1: do I = 1, RRECS
   J = (I-1)*VARREC
   K = J+VARREC
   J = J+1
   M = 0
   Inner_1: do L = J, K
      M = M+1
      if (L > NREALS) exit Inner_1
      BUFFER(M) = IO(L)
   end do Inner_1
   J = OFFSET+I
   write (RANUNT,rec=J) BUFFER
end do Outer_1

! Load the Integer variables
OFFSET = OFFSET+RRECS
Outer_2: do I = 1, IRECS
   J = (I-1)*VARIEC
   K = J+VARIEC
   J = J+1
   M = 0
   Inner_2: do L = J, K
      M = M+1
      if (L > NINTS) exit Inner_2
      IBUFF(M) = IOI(L)
   end do Inner_2
   J = OFFSET+I
   write (RANUNT,rec=J) IBUFF
end do Outer_2
! Load the character variables
! Calculate starting record number
OFFSET = OFFSET+IRECS
Outer_3: do I = 1, CRECS
   J = (I-1)*VARCEC
   K = J+VARCEC
   J = J+1
   M = 0
   Inner_3: do L = J, K
      M = M+1
      if (L > NCHARS) exit Inner_3
      CBUFF(M) = IOC(L)
   end do Inner_3
   J = OFFSET+I
   write (RANUNT,rec=J) CBUFF
end do Outer_3
Deallocate (IO,IOI)
return
end subroutine PAKENV
