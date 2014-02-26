subroutine PACLDS(RECNUM)
! Purpose--to move individual loadings variables to a single
! array to optimize output of many variables to the daf
! ARGUMENTS--Record - number of load to be written
! Revised    15-JAN-85, 22-APR-87 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
use Implementation_Control
! Revised 11/17/88 to accommodate VAX multi-user environment
! Revised March 2001 to add KCHEM and KOUNT to load specifications
use Input_Output
use Global_Variables
use Local_Working_Space
Implicit None
real :: BUFFER(VARREC)
real, allocatable :: IO(:)
integer, allocatable :: IOI(:)
integer :: IBUFF(VARIEC), RECNUM, OFFSET
integer :: RRECS, IRECS, CRECS, TRECS, NREALS, NINTS, NCHARS
integer :: RECDAT(FILDAT), HRECS
integer :: I,NUSED,J,K,M,L,ISET
! RECDAT carries the file information, HRECS is the number of
! header records required.
! integer NREC
! character buffer for data transfer; 50-character name,
! plus 2 6-letter passwords
character(len=1) :: CBUFF(VARCEC), IOC(62)
! allocate to the size of the daf
Allocate (IO(NPX*5*NCHEM*MAXDAT+MAXMAS), IOI(5*MAXMAS+2))
! Clear buffers
CBUFF = ' '
IBUFF = 0
BUFFER = 0.0
IO=0.0
IOI=0
! Load real datastream
NUSED = 0
! Load the MAXMAS vector
do I = 1, MAXMAS
   IO(NUSED+I) = IMASSG(I)
end do
NUSED = NUSED+MAXMAS

do I = 1, MAXDAT      ! Load the KOUNT x KCHEM x MAXDAT matrices
   do J = 1, KCHEM
      do K = 1, KOUNT
         IO(NUSED+1) = STRLDG(K,J,I)
         IO(NUSED+2) = NPSLDG(K,J,I)
         IO(NUSED+3) = PCPLDG(K,J,I)
         IO(NUSED+4) = DRFLDG(K,J,I)
         IO(NUSED+5) = SEELDG(K,J,I)
         NUSED = NUSED+5
      end do
   end do
end do
! Load the Integer datastream
! Load MAXMAS vectors
IOI(1) = max (KOUNT,1)
IOI(2) = max (KCHEM,1)
NUSED = 2
do I = 1, MAXMAS
   IOI(NUSED+1) = ISEGG(I)
   IOI(NUSED+2) = ICHEMG(I)
   IOI(NUSED+3) = IMONG(I)
   IOI(NUSED+4) = IDAYG(I)
   IOI(NUSED+5) = IYEARG(I)
   NUSED = NUSED+5
end do
! Load the Character datastream
do I = 1, 50
   IOC(I) = LOADNM(I:I)
end do
NUSED = 50
do I = 1, 6
   IOC(NUSED+1) = RPASS(3)(I:I)
   IOC(NUSED+2) = WPASS(3)(I:I)
   NUSED = NUSED+2
end do

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
RRECS = RECDAT(33)
IRECS = RECDAT(34)
CRECS = RECDAT(56)
TRECS = RRECS+IRECS+CRECS
! Load number of entries for this database
! NREC   = RECDAT(35)
NREALS = RECDAT(37)
NINTS = RECDAT(38)
NCHARS = RECDAT(52)
! Load address of first record in this database
ISET = RECDAT(45)-1
OFFSET = (RECNUM-1)*TRECS+ISET
! Transfer Real variables
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
! Write out Integer variables
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
! Transfer Character variables to file
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
deallocate (IO,IOI)
return
end subroutine PACLDS
