subroutine UNPLDS(RECNUM)
! Purpose--to move individual variables to a single 
! array to optimize output of many variables to the daf
! Arguments--RECORD - number of load to be processed
! Revised  21-DEC-85 (LAB); bug fix 2-APR-87; 27-APR-87
! Revisions 10/21/88--run-time implementation of machine dependencies
! Revised 11/17/88 to accommodate VAX multi-user environment
! Revised March 2001 to add KCHEM and KOUNT to load specifications
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
Implicit None
real :: BUFFER(VARREC)
real, allocatable :: IO(:)
integer, allocatable :: IOI(:)
integer, intent(in) :: RECNUM
integer :: OFFSET,IBUFF(VARIEC)
integer :: RRECS, IRECS, CRECS, TRECS, NREALS, NINTS, NCHARS
integer :: RECDAT(FILDAT),HRECS,I,M,L,ISET,J,NUSED,K
integer :: KOUNT_test=1, KCHEM_test=1
! RECDAT carries the file information, HRECS is the number of
! header records required.
character(len=1) :: CBUFF(VARCEC), IOC(62)
! alocate to the maximum size of the daf
Allocate (IO(NPX*5*NCHEM*MAXDAT+MAXMAS), IOI(5*MAXMAS+2))
! Clear buffers
CBUFF = ' '
IBUFF = 0
BUFFER = 0.0
IO=0.0
IOI=0
! Load real datastream
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
! Load number of entries in database
! NREC   = RECDAT(35)
NREALS = RECDAT(37)
NINTS = RECDAT(38)
NCHARS = RECDAT(52)
! VARREC = RECDAT(13)
! VARIEC = RECDAT(14)

! Transfer Real variables
! Load address in database
ISET = RECDAT(45)-1
OFFSET = (RECNUM-1)*TRECS+ISET
M = 0
Outer_1: do I = 1, RRECS
   J = I+OFFSET
   read (RANUNT,rec=J) BUFFER
   J = J+1
   Inner_1: do L = 1, VARREC
      M = M+1
      if (M > NREALS) exit Inner_1
      IO(M) = BUFFER(L)
   end do Inner_1
end do Outer_1

! Transfer Integer variables
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

! Load the Integer datastream
! Load MAXMAS vectors
KOUNT_test = IOI(1)
KCHEM_test = IOI(2)
! Check the structure of this load pattern versus the current problem set
if (KOUNT/=KOUNT_test .or. KCHEM/=KCHEM_test) then
   write (stderr,fmt='(a,i0,a/a,i0,a/a,i0,a,i0,a/a)') &
      ' The stored load pattern specifies ',KOUNT_test,' environmental',&
      ' segments and ',KCHEM_test,' chemicals. The current problem setup',&
      ' specifies ',KOUNT,' segments and ',KCHEM,' chemicals.',&
      ' The requested load has not been recalled.'
   deallocate (IO,IOI)
   return
end if
NUSED = 2
do I = 1, MAXMAS
   ISEGG(I) = IOI(NUSED+1)
   ICHEMG(I) = IOI(NUSED+2)
   IMONG(I) = IOI(NUSED+3)
   IDAYG(I) = IOI(NUSED+4)
   IYEARG(I) = IOI(NUSED+5)
   NUSED = NUSED+5
end do
! Load real datastream
NUSED = 0
! Load the MAXMAS vector
do I = 1, MAXMAS
   IMASSG(I) = IO(NUSED+I)
end do
NUSED = NUSED+MAXMAS
! Load the KOUNT x KCHEM x MAXDAT matrices
do I = 1, MAXDAT
   do J = 1, KCHEM
      do K = 1, KOUNT
         STRLDG(K,J,I) = IO(NUSED+1)
         NPSLDG(K,J,I) = IO(NUSED+2)
         PCPLDG(K,J,I) = IO(NUSED+3)
         DRFLDG(K,J,I) = IO(NUSED+4)
         SEELDG(K,J,I) = IO(NUSED+5)
         NUSED = NUSED+5
      end do
   end do
end do
! Load the Character datastream
do I = 1, 50
   LOADNM(I:I) = IOC(I)
end do
NUSED = 50
do I = 1, 6
   RPASS(3)(I:I) = IOC(NUSED+1)
   WPASS(3)(I:I) = IOC(NUSED+2)
   NUSED = NUSED+2
end do
deallocate (IO,IOI)
return
end subroutine UNPLDS
