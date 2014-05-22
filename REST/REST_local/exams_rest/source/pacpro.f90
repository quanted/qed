subroutine PACPRO(RECNUM)
! Purpose--to move individual variables to a single
! array to optimize output of many variables
! Arguments--RECORD - number of product chemistry to be written
! Revised 27-DEC-85 (LAB)
! Revisions 10/21/88--run-time implementation of machine dependencies
use Implementation_Control
! Revised 11/17/88 to accommodate VAX multi-user environment
use Input_Output
!use Initial_Sizes
use Global_Variables
use Local_Working_Space
Implicit None
real :: BUFFER(VARREC), IO(2*NTRAN)
integer :: IBUFF(VARIEC), IOI(4*NTRAN), RRECS, IRECS, CRECS, TRECS,&
NREALS, NINTS, NCHARS, RECNUM, OFFSET
integer :: RECDAT(FILDAT), HRECS
! RECDAT carries the file information, HRECS is the number of
! header records required.
integer :: I,NUSED,M,L,ISET,J,K
character(len=1) :: CBUFF(VARCEC), IOC(62)
! Clear buffers
CBUFF = ' '
IBUFF = 0
BUFFER = 0.0

! Load Real datastream
NUSED = 0
do I = 1, NTRAN
   IO(NUSED+1) = YIELDG(I)
   IO(NUSED+2) = EAYLDG(I)
   NUSED = NUSED+2
end do
! Load Integer datastream
NUSED = 0
do I = 1, NTRAN
   IOI(NUSED+1) = CHPARG(I)
   IOI(NUSED+2) = TPRODG(I)
   IOI(NUSED+3) = NPROCG(I)
   IOI(NUSED+4) = RFORMG(I)
   NUSED = NUSED+4
end do
! Load Character datastream
do I = 1, 50
   IOC(I) = PRODNM(I:I)
end do
NUSED = 50

do I = 1, 6
   IOC(NUSED+1) = RPASS(4)(I:I)
   IOC(NUSED+2) = WPASS(4)(I:I)
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
RRECS = RECDAT(39)
IRECS = RECDAT(40)
CRECS = RECDAT(57)
TRECS = RRECS+IRECS+CRECS
! Load number of entries in this database
! NREC   = RECDAT ( 41 )
NREALS = RECDAT(43)
NINTS = RECDAT(44)
NCHARS = RECDAT(53)
! VARREC = RECDAT ( 13 )
! VARIEC = RECDAT ( 14 )
ISET = RECDAT(47)-1
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
! Transfer Integer variables
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
! Transfer Character variables
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
return
end subroutine PACPRO
