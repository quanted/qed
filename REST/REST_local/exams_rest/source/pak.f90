subroutine PAK(RECNUM,KT)
! Purpose--to move individual chemical variables to a single
! array to optimize output of many variables to the daf
! Arguments--RECNUM - number of chemical to be written
!            KT     - ADB number of chemical data
! Revised 21-DEC-85, 22-APR-87 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
! Revised 11/17/88 to accommodate VAX multi-user environment
! Revised April 2001 to add aquatic metabolism half-lives
! Revised May 2004 to add metabolic study temperatures
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
! VARREC, VARIEC, and FILDAT are parameters sensu Fortran
Implicit None
real :: BUFFER(VARREC),IO(847)
integer :: IBUFF(VARIEC),IOI(7),RECNUM,OFFSET,NUSED,RECDAT(FILDAT),HRECS
! RECDAT carries the file information
! HRECS is the number of header records required
! NUSED is number of locations used in datastreams
integer :: TRECS,RRECS,IRECS,CRECS,NREALS,NINTS,NCHARS
integer :: I,KT,J,M,L,ISET,II,K
character(len=1) :: CBUFF(VARCEC), IOC(62)
CBUFF = ' '             ! Clear buffers
IBUFF = 0
BUFFER = 0.0

IO(1) = MWTG(KT)        ! Load real datastream (10 reals)
IO(2) = KOCG(KT)
IO(3) = KOWG(KT)
IO(4) = MPG(KT)
IO(5) = HENRYG(KT)
IO(6) = EHENG(KT)
IO(7) = VAPRG(KT)
IO(8) = EVPRG(KT)
IO(9)  = AerMet(KT)
IO(10) = AnaerM(KT)
NUSED = 10

do I = 1, 6             ! Load 6-location elements (3x6=18 reals)
   IO(NUSED+1) = PKG(I,KT)
   IO(NUSED+2) = EPKG(I,KT)
   IO(NUSED+3) = KIECG(I,KT)
   NUSED = NUSED+3
end do

do I = 1, 7             ! Load 7-location elements (8x7=56 reals)
   IO(NUSED+1) = SOLG(I,KT)
   IO(NUSED+2) = ESOLG(I,KT)
   IO(NUSED+3) = KPSG(I,KT)
   IO(NUSED+4) = KPBG(I,KT)
   IO(NUSED+5) = KPDOCG(I,KT)
   IO(NUSED+6) = KDPG(I,KT)
   IO(NUSED+7) = RFLATG(I,KT)
   IO(NUSED+8) = LAMAXG(I,KT)
   NUSED = NUSED+8
end do

do J = 1, 7             ! Do 3x7 matrices (13x3x7=273 reals)
   do I = 1, 3
      IO(NUSED+1) = QYield(I,J,KT)
      IO(NUSED+2) = KAHG(I,J,KT)
      IO(NUSED+3) = EAHG(I,J,KT)
      IO(NUSED+4) = KNHG(I,J,KT)
      IO(NUSED+5) = ENHG(I,J,KT)
      IO(NUSED+6) = KBHG(I,J,KT)
      IO(NUSED+7) = EBHG(I,J,KT)
      IO(NUSED+8) = KOXG(I,J,KT)
      IO(NUSED+9) = EOXG(I,J,KT)
      IO(NUSED+10) = K1O2G(I,J,KT)
      IO(NUSED+11) = EK1O2G(I,J,KT)
      IO(NUSED+12) = KREDG(I,J,KT)
      IO(NUSED+13) = EREDG(I,J,KT)
      NUSED = NUSED+13
   end do
end do

do J = 1, 7             ! Do the 4x7 matrices (6x4x7=168 reals)
   do I = 1, 4
      IO(NUSED+1) = KBACWG(I,J,KT)
      IO(NUSED+2) = QTBAWG(I,J,KT)
      IO(NUSED+3) = KBACSG(I,J,KT)
      IO(NUSED+4) = QTBASG(I,J,KT)
      IO(NUSED+5) = QTBTWG(I,J,KT)
      IO(NUSED+6) = QTBTSG(I,J,KT)
      NUSED = NUSED+6
   end do
end do

do J = 1, 7             ! Do the chemical absorption spectrum
   do I = 1, 46         ! (46x7=322 reals)
      IO(NUSED+I) = ABSORG(I,J,KT)
   end do
   NUSED = NUSED+46
end do
! Total number of real chemical variables = 847
!
do i=1,50               ! Do the 62 chemical CHARACTER entries
   IOC(I) = CHEMNA(KT)(I:I)
end do
NUSED = 50

do I = 1, 6
   IOC(NUSED+1) = RPASS(1)(I:I)
   IOC(NUSED+2) = WPASS(1)(I:I)
   NUSED = NUSED+2
end do

do I = 1, 7         ! Do the 7 chemical INTEGER variables
   IOI(I) = SPFLGG(I,KT)
end do
NUSED = 7

HRECS = FILDAT/VARIEC ! Read the header record for file control information
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
! NREC   = RECDAT ( 17 )
NREALS = RECDAT(19)
NINTS = RECDAT(20)
NCHARS = RECDAT(50)
ISET = RECDAT(9)-1 ! Load the number of the first record in the database
II = RECNUM        ! Set number of record to be written from input argument
OFFSET = (II-1)*TRECS+ISET

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

! Locate first Integer record
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
! Locate first character record
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
return
end subroutine PAK
