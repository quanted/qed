subroutine UNPENV(RECNUM)
! Purpose--to move the individual elements of the environmental
! data to a single variable to facilitate input to the daf
! Revised--31-DEC-1985, 22-APR-87 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
! Revised 11/17/88 to accommodate VAX multi-user environment
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
use Environmental_Data_Space
Implicit None
real :: BUFFER(VARREC)
integer :: IBUFF(VARIEC),OFFSET,ISET,I,J,L,M,NUSED
integer, intent(in) :: RECNUM
integer :: RRECS, IRECS, CRECS, TRECS, NREALS, NINTS, NCHARS
integer :: RECDAT(FILDAT), HRECS
! RECDAT carries the file information, HRECS is the number of
! header records required.
character(len=1) :: CBUFF(VARCEC)
if (Allocated(IO))  Deallocate(IO)
if (Allocated(IOI)) Deallocate(IOI)
Allocate (IO(IOSIZ),IOI(IOISIZ))
IO  = 0.0              ! Zero the main input/output transfer area
IOI = 0
! Clear buffers
CBUFF = ' '
IBUFF = 0
BUFFER = 0.0
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
! NREC   = RECDAT(23)
! Load address of first ecosystem record
ISET = RECDAT(11)-1
! Read the requested record
OFFSET = (RECNUM-1)*TRECS+ISET
! Load the Real variables
M = 0
Outer_1: do I = 1, RRECS
   J = OFFSET+I
   read (RANUNT,rec=J) BUFFER
   Inner_1: do L = 1, VARREC
      M = M+1
      if (M > NREALS) exit Inner_1
      IO(M) = BUFFER(L)
   end do Inner_1
end do Outer_1
! Load the Integer variables
OFFSET = OFFSET+RRECS
M = 0
Outer_2: do I = 1, IRECS
   J = OFFSET+I
   read (RANUNT,rec=J) IBUFF
   Inner_2: do L = 1, VARIEC
      M = M+1
      if (M > NINTS) exit Inner_2
      IOI(M) = IBUFF(L)
   end do Inner_2
end do Outer_2
! Load Character variables
OFFSET = OFFSET+IRECS
M = 0
Outer_3: do I = 1, CRECS
   J = OFFSET+I
   read (RANUNT,rec=J) CBUFF
   Inner_3: do L = 1, VARCEC
      M = M+1
      if (M > NCHARS) exit Inner_3
      IOC(M) = CBUFF(L)
   end do Inner_3
end do Outer_3
!
! allocate storage for this environment
KOUNT=IOI(1)
call Allocate_Storage(2,KOUNT,KCHEM)
! initialize the data structure
call initl(3)
! Failsafe reload of the stored size of this environment
KOUNT = IOI(1)
! Load real datastream, beginning with scalars
LATG = IO(1)
LONGG = IO(2)
ELEVG = IO(3)
NUSED = 3
! Load the environmental vectors
do I = 1, KOUNT
   VOLG(I) = IO(NUSED+1)
   AREAG(I) = IO(NUSED+2)
   DEPTHG(I) = IO(NUSED+3)
   XSAG(I) = IO(NUSED+4)
   LENGG(I) = IO(NUSED+5)
   WIDTHG(I) = IO(NUSED+6)
   NUSED = NUSED+6
end do
! Load the dispersive transport vectors and DSPG
do I = 1, size(XSTURG)
   XSTURG(I) = IO(NUSED+1)
   CHARLG(I) = IO(NUSED+2)
   ADVPRG(I) = IO(NUSED+3)
   NUSED = NUSED+3
   do J = 1, MAXDAT
      DSPG(I,J) = IO(NUSED+J)
   end do
   NUSED = NUSED+MAXDAT
end do
!
! Load the MAXDAT vectors
do I = 1, MAXDAT
   OXRADG(I) = IO(NUSED+1)
   CLOUDG(I) = IO(NUSED+2)
   RAING(I) = IO(NUSED+3)
   OZONEG(I) = IO(NUSED+4)
   RHUMG(I) = IO(NUSED+5)
   ATURBG(I) = IO(NUSED+6)
   NUSED = NUSED+6
end do
! Load the MAXDAT x KOUNT matrices
do I = 1, MAXDAT
   do J = 1, KOUNT
      FROCG(J,I) = IO(NUSED+1)
      CECG(J,I) = IO(NUSED+2)
      AECG(J,I) = IO(NUSED+3)
      PCTWAG(J,I) = IO(NUSED+4)
      TCELG(J,I) = IO(NUSED+5)
      PHG(J,I) = IO(NUSED+6)
      POHG(J,I) = IO(NUSED+7)
      REDAGG(J,I) = IO(NUSED+8)
      BACPLG(J,I) = IO(NUSED+9)
      BNBACG(J,I) = IO(NUSED+10)
      PLMASG(J,I) = IO(NUSED+11)
      BNMASG(J,I) = IO(NUSED+12)
      KO2G(J,I) = IO(NUSED+13)
      STFLOG(J,I) = IO(NUSED+14)
      STSEDG(J,I) = IO(NUSED+15)
      NPSFLG(J,I) = IO(NUSED+16)
      NPSEDG(J,I) = IO(NUSED+17)
      SEEPSG(J,I) = IO(NUSED+18)
      DOCG(J,I) = IO(NUSED+19)
      CHLG(J,I) = IO(NUSED+20)
      DFACG(J,I) = IO(NUSED+21)
      DISO2G(J,I) = IO(NUSED+22)
      EVAPG(J,I) = IO(NUSED+23)
      WINDG(J,I) = IO(NUSED+24)
      BULKDG(J,I) = IO(NUSED+25)
      SUSEDG(J,I) = IO(NUSED+26)
      NUSED = NUSED+26
   end do
end do
! Load the Integer variables
KOUNT = IOI(1)
NUSED = 1
do I = 1, size(JFRADG)
   JFRADG(I) = IOI(NUSED+1)
   ITOADG(I) = IOI(NUSED+2)
   JTURBG(I) = IOI(NUSED+3)
   ITURBG(I) = IOI(NUSED+4)
   NUSED = NUSED+4
end do
! Load the Character variables
do I = 1, 50
   ECONAM(I:I) = IOC(I)
end do
NUSED = 50
do I = 1, 6
   RPASS(2)(I:I) = IOC(NUSED+1)
   WPASS(2)(I:I) = IOC(NUSED+2)
   NUSED = NUSED+2
end do
do I = 1, KOUNT
   TYPEG(I) = IOC(NUSED+I)
end do
NUSED = NUSED+KOUNT
do I = 1, MAXDAT
   AIRTYG(I) = IOC(NUSED+I)
end do
NUSED = NUSED+MAXDAT ! true but currently irrelevant
Deallocate (IO,IOI)
return
end subroutine UNPENV
