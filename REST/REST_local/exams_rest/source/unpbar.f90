subroutine UNPBAR(IBUFF)
! This routine unloads a set of intermediate computational
! variables from a compressed buffer.
! Author, Date: L.A. Burns, 25-Apr-84
! Revised 03 May 1984 (LAB) to retain Dec. CONLDL.
! Revised 01 Feb 2002 to properly allocate transfer buffers
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
! For the material to be transferred from the scratch file
! (all elements of labeled COMMON "SECTR1") we have:
! Number of REAL*4 variables = NREAL4 = KOUNT * (4 + 47*KCHEM)
! and the number of real (kind (0D0)) (REAL*8) variables is:
! = NREAL8 = KOUNT * KCHEM * (2 + KOUNT + KCHEM)
! Dimensioning of I/O transfer buffers to encompass (implicitly)
! the variables to be transferred:
Implicit None
real (kind(1.0e0)), allocatable, dimension(:) :: BUFF1
real (kind(1.0d0)), allocatable, dimension(:)  :: BUFF2
! Dimension the vector for information about the file
integer :: IBUFF(VARIEC)
! Local counters etc.:
integer :: I, J, K, NSP, NSTART, NEND
! NSP is used to count through chemical species vectors (e.g. SPFLGG).
! NSTART and NEND match sectors of the transfer buffers to the records.
integer :: OFFSET, NVAR, NRECS, FIRREC, LASTRC, ITRAIL
integer, dimension(7) :: IALPHA = (/1,5,9,13,17,21,25/)
! OFFSET is the number of records already used by previous file entries.
! NVAR is the number of variables in the current block of data.
! NRECS is the number of records used to contain the current block.
! FIRREC and LASTRC are the record numbers for the current block.
! ITRAIL is the number of variables in the last record of the block.
! IALPHA is addresses for alpha matrix.

allocate (BUFF1 ( KOUNT * (4+47*KCHEM)))
allocate (BUFF2 ( KOUNT * KCHEM * (2+KOUNT+KCHEM)))

! First record reserved for file descriptors
if (NDAT == 1) read (WRKLUN,rec=1) (IBUFF(I),I=1,4)
! Determine the number of records already in use, i.e., compute
! the offset needed for positioning the next blocks of data:
OFFSET = 1+(NDAT-1)*(IBUFF(1)+IBUFF(3))
! IBUFF(1) indicates the number of records required to retrieve the
! REAL*4 data, and IBUFF(2) indicates the number of variables actually
! stored on the last record:
NRECS = IBUFF(1)
ITRAIL = IBUFF(2)
! Read out the buffer from the file up to (but not including) the last record
FIRREC = OFFSET+1
LASTRC = FIRREC+NRECS-1
NSTART = 1   ! Set write index to point to first member of transfer buffer
Many_recs: if (NRECS > 1) then
   NEND = VARREC              ! Set termination index to length of records
   do K = FIRREC, LASTRC-1    ! Begin reading records
      read (WRKLUN,rec=K) (BUFF1(I),I=NSTART,NEND)
      NSTART = NEND+1         ! Update write indices to get
      NEND = NEND+VARREC      ! next sector of the buffer
   end do
end if Many_recs
! Position the write index for the last active member of the buffer
NEND = (NRECS-1)*VARREC+ITRAIL
! Read the last (or the only) record:
read (WRKLUN,rec=LASTRC) (BUFF1(I),I=NSTART,NEND)
!
! Unload the single precision transfer buffer
NVAR = 1  ! Load the counter for transferring real variables
Chemicals: do K = 1, KCHEM
   Segments: do J = 1, KOUNT
      Species: do NSP = 1, 7
         if (SPFLGG(NSP,K) == 0) cycle Species
         do I = IALPHA(NSP), IALPHA(NSP)+3
            ALPHA(I,J,K) = ALPHA(I,J,K)+BUFF1(NVAR)
            NVAR = NVAR+1
         end do
      end do Species
      do I = 29, 32
         ALPHA(I,J,K) = ALPHA(I,J,K)+BUFF1(NVAR)
         NVAR = NVAR+1
      end do
   end do Segments
end do Chemicals

do K = 1, KCHEM
   do J = 1, KOUNT
      BIOLKL(J,K) = BIOLKL(J,K)+BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do J = 1, KOUNT
   BIOTOL(J) = BIOTOL(J)+BUFF1(NVAR)
   NVAR = NVAR+1
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      EXPOKL(J,K) = EXPOKL(J,K)+BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      HYDRKL(J,K) = HYDRKL(J,K)+BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      OXIDKL(J,K) = OXIDKL(J,K)+BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      PHOTKL(J,K) = PHOTKL(J,K)+BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      REDKL(J,K) = REDKL(J,K)+BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      S1O2KL(J,K) = S1O2KL(J,K)+BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do J = 1, KOUNT
   SEDCOL(J) = SEDCOL(J)+BUFF1(NVAR)
   NVAR = NVAR+1
end do

do J = 1, KOUNT
   SEDMSL(J) = SEDMSL(J)+BUFF1(NVAR)
   NVAR = NVAR+1
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      VOLKL(J,K) = VOLKL(J,K)+BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do J = 1, KOUNT
   WATVOL(J) = WATVOL(J)+BUFF1(NVAR)
   NVAR = NVAR+1
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      Species_again: do NSP = 1, 7
         if (SPFLGG(NSP,K) == 0) cycle Species_again
         YSATL(NSP,J,K) = YSATL(NSP,J,K)+BUFF1(NVAR)
         NVAR = NVAR+1
      end do Species_again
   end do
end do

! Transfer real (kind (0D0)) variables
OFFSET = LASTRC
NVAR = 1        ! Reset the counter of variables actually loaded
! IBUFF(3) contains the total number of records needed to store the
! REAL*8 (real (kind (0D0))) variables. IBUFF(4) gets the number of
! variables actually in the last record
NRECS = IBUFF(3)
ITRAIL = IBUFF(4)
! Read out the buffer from the file up to (but not including) the last record
FIRREC = OFFSET+1
LASTRC = FIRREC+NRECS-1

NSTART = 1      ! Set write index to point to first member of transfer buffer
Many_records: if (NRECS > 1) then ! Set termination index to length of records
   NEND = VARDEC  ! VARDEC is number of real (kind (0D0)) variables per record
   do K = FIRREC, LASTRC-1 ! Begin reading records
      read (WRKLUN,rec=K) (BUFF2(I),I=NSTART,NEND)
      NSTART = NEND+1 ! Update write indices to get next sector of the buffer
      NEND = NEND+VARDEC
   end do
end if Many_records
! Position the write index for the last active member of the buffer
NEND = (NRECS-1)*VARDEC+ITRAIL
! Read the last (or the only) record:
read (WRKLUN,rec=LASTRC) (BUFF2(I),I=NSTART,NEND)

! See comment in M12BAR for reasons for deactivating
! this CONLDL transfer -- note, however, that NVAR
! nonetheless must be updated to reach INTINL.
! Unload the transfer buffer:
do K = 1, KCHEM
   do J = 1, KOUNT
      ! CONLDL(J,K) = CONLDL(J,K) + BUFF2(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      do I = 1, KOUNT
         INTINL(I,J,K) = INTINL(I,J,K)+BUFF2(NVAR)
         NVAR = NVAR+1
      end do
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      TOTKL(J,K) = TOTKL(J,K)+BUFF2(NVAR)
      NVAR = NVAR+1
   end do
end do
do J = 1, KOUNT
   do K = 1, KCHEM
      do I = 1, KCHEM
         YIELDL(I,K,J) = YIELDL(I,K,J)+BUFF2(NVAR)
         NVAR = NVAR+1
      end do
   end do
end do
deallocate (BUFF1,BUFF2)
return
end Subroutine UNPBAR
