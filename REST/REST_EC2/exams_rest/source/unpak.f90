subroutine UNPAK(RECNUM,KT)
! Purpose--to move individual chemical variables to a single
! array to optimize input of many variables from the daf
! Arguments
      ! RECNUM - UDB number of chemical to be read
      ! KT     - ADB number of chemical being recalled
! Revised 21-DEC-85, 22-APR-87 (LAB)
! Revised 11/17/88 to accommodate VAX multi-user environment
! Revised 2004-05-17 to include biolysis study temperatures
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
Implicit None
real :: BUFFER(VARREC), IO(847)
integer :: IBUFF(VARIEC),IOI(7),I,M,L,ISET,J
integer, intent (in) :: RECNUM, KT
integer :: OFFSET,NUSED
! NUSED is number of locations used in datastreams.
integer :: TRECS,RRECS,IRECS,CRECS,NREALS,NINTS,NCHARS
integer :: RECDAT(FILDAT),HRECS
! RECDAT carries the file information
! HRECS is the number of header records required
character(len=1) :: CBUFF(VARCEC),IOC(62)

! Clear buffers
CBUFF = ' '
IBUFF = 0
BUFFER = 0.0
! Input the database characteristics for the specified chemical
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

RRECS = RECDAT(15)
IRECS = RECDAT(16)
CRECS = RECDAT(54)
TRECS = RRECS+IRECS+CRECS
! Load total number of chemicals in database
! NREC   = RECDAT(17)
NREALS = RECDAT(19)
NINTS = RECDAT(20)
NCHARS = RECDAT(50)
! VARREC = RECDAT(13)
! VARIEC = RECDAT(14)
! Load starting record number of chemical database
ISET = RECDAT(9)-1
! Locate starting record of database for this chemical
OFFSET = (RECNUM-1)*TRECS+ISET
! Load Real variables
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

! Load Integer variables
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

! Load real datastream
MWTG(KT) = IO(1)
KOCG(KT) = IO(2)
KOWG(KT) = IO(3)
MPG(KT) = IO(4)
HENRYG(KT) = IO(5)
EHENG(KT) = IO(6)
VAPRG(KT) = IO(7)
EVPRG(KT) = IO(8)
AerMet(KT) = IO(9)
AnaerM(KT) = IO(10)
NUSED = 10
! Load 6-location elements
do I = 1, 6
   PKG(I,KT) = IO(NUSED+1)
   EPKG(I,KT) = IO(NUSED+2)
   KIECG(I,KT) = IO(NUSED+3)
   NUSED = NUSED+3
end do

! Load 7-location elements
do I = 1, 7
   SOLG(I,KT) = IO(NUSED+1)
   ESOLG(I,KT) = IO(NUSED+2)
   KPSG(I,KT) = IO(NUSED+3)
   KPBG(I,KT) = IO(NUSED+4)
   KPDOCG(I,KT) = IO(NUSED+5)
   KDPG(I,KT) = IO(NUSED+6)
   RFLATG(I,KT) = IO(NUSED+7)
   LAMAXG(I,KT) = IO(NUSED+8)
   NUSED = NUSED+8
end do

do J = 1, 7             ! Do 3x7 matrices
   do I = 1, 3
      QYield(I,J,KT) = IO(NUSED+1)
      KAHG(I,J,KT) = IO(NUSED+2)
      EAHG(I,J,KT) = IO(NUSED+3)
      KNHG(I,J,KT) = IO(NUSED+4)
      ENHG(I,J,KT) = IO(NUSED+5)
      KBHG(I,J,KT) = IO(NUSED+6)
      EBHG(I,J,KT) = IO(NUSED+7)
      KOXG(I,J,KT) = IO(NUSED+8)
      EOXG(I,J,KT) = IO(NUSED+9)
      K1O2G(I,J,KT) = IO(NUSED+10)
      EK1O2G(I,J,KT) = IO(NUSED+11)
      KREDG(I,J,KT) = IO(NUSED+12)
      EREDG(I,J,KT) = IO(NUSED+13)
      NUSED = NUSED+13
   end do
end do

do J = 1, 7             ! Do the 4x7 matrices
   do I = 1, 4
      KBACWG(I,J,KT) = IO(NUSED+1)
      QTBAWG(I,J,KT) = IO(NUSED+2)
      KBACSG(I,J,KT) = IO(NUSED+3)
      QTBASG(I,J,KT) = IO(NUSED+4)
      QTBTWG(I,J,KT) = IO(NUSED+5)
      QTBTSG(I,J,KT) = IO(NUSED+6)
      NUSED = NUSED+6
   end do
end do

do J = 1, 7             ! Do the chemical absorption spectrum
   do I = 1, 46
      ABSORG(I,J,KT) = IO(NUSED+I)
   end do
   NUSED = NUSED+46
end do

do I = 1, 50            ! Do the Character entries
   CHEMNA(KT)(I:I) = IOC(I)
end do
NUSED = 50
do I = 1, 6
   RPASS(1)(I:I) = IOC(NUSED+1)
   WPASS(1)(I:I) = IOC(NUSED+2)
   NUSED = NUSED+2
end do

do I = 1, 7             ! do the Integer variables
   SPFLGG(I,KT) = IOI(I)
end do
NUSED = 7
return
end subroutine UNPAK
