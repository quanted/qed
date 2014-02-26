subroutine UNPPRO(RECNUM)
! Purpose--to move individual variables to a single
! array to optimize output of many variables
! Arguments--RECORD - number of product chemistry to be processed
! Revised 21-DEC-85 (LAB); bug fix 2-APR-87; 22-APR-87
! Revisions 10/21/88--run-time implementation of machine dependencies
! Revised 11/17/88 to accommodate VAX multi-user environment
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
Implicit None
real :: IO(2*NTRAN), BUFFER(VARREC)
integer :: IOI(4*NTRAN),OFFSET,IBUFF(VARIEC)
integer, intent(in) :: RECNUM
integer :: RRECS,IRECS,CRECS,TRECS,NREALS,NINTS,NCHARS
integer :: RECDAT(FILDAT),HRECS,I,M,L,ISET,J,NUSED
! RECDAT carries the file information, HRECS is the number of
! header records required.
character(len=1) :: CBUFF(VARCEC), IOC(62)
! Clear buffer vectors
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

RRECS = RECDAT(39)
IRECS = RECDAT(40)
CRECS = RECDAT(57)
TRECS = RRECS+IRECS+CRECS
! NREC   = RECDAT(41)
NREALS = RECDAT(43)
NINTS = RECDAT(44)
NCHARS = RECDAT(53)
ISET = RECDAT(47)-1
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

!
! Load real datastream
NUSED = 0
do I = 1, NTRAN
   YIELDG(I) = IO(NUSED+1)
   EAYLDG(I) = IO(NUSED+2)
   NUSED = NUSED+2
end do
! Load Integer datastream
NUSED = 0
do I = 1, NTRAN
   CHPARG(I) = IOI(NUSED+1)
   TPRODG(I) = IOI(NUSED+2)
   NPROCG(I) = IOI(NUSED+3)
   RFORMG(I) = IOI(NUSED+4)
   NUSED = NUSED+4
end do
! Load Character datastream
do I = 1, 50
   PRODNM(I:I) = IOC(I)
end do
NUSED = 50
do I = 1, 6
   RPASS(4)(I:I) = IOC(NUSED+1)
   WPASS(4)(I:I) = IOC(NUSED+2)
   NUSED = NUSED+2
end do
return
end subroutine UNPPRO
