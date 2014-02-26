subroutine UNPSCR(IBUFF,ABEXIT,NYR)
! This routine loads a set of intermediate computational variables
! into a buffer and transmits it to a direct access scratch file.
! Author, Date: L.A. Burns, 06-MAR-84
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revisions 31-Jan-2001: allocatable I/O transfer buffers based on
!   actual size of study model rather than full size of daf storage
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums

Implicit None

! For the material to be transferred from the scratch file, the
! number of single precision variables  KOUNT*(4+47*KCHEM)
! and the number of double precision variables is:
! KOUNT * KCHEM * (2 + KOUNT + KCHEM)
real (kind(1.0e0)), allocatable, dimension(:) :: BUFF1
real (kind(1.0d0)), allocatable, dimension(:)  :: BUFF2
! Dimension the vector for information about the file
integer :: IBUFF(VARIEC), NYR
logical :: ABEXIT
! NYR passes the number of the year underway in DRIVM3, to test
! whether the ALPHA etc. dataspace needs to be initialized.

! Local counters etc.
integer :: I, J, K, NSP, NSTART, NEND
! NSP is used to count through chemical species vectors (e.g., SPFLGG).
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

! Temporary test initialization of R*4 buffer:
!     NPEND = KOUNT*(4+47*KCHEM)
!     DO I=1, NPEND
!       BUFF1(I) = FLOAT(I)
!     END DO
! Zero the data space at first entry
if (ABEXIT .or. NDAT==1 .or. NYR==FRSTYR) then
   ALPHA = 0.0
   BIOLKL = 0.0
   EXPOKL = 0.0
   HYDRKL = 0.0
   OXIDKL = 0.0
   PHOTKL = 0.0
   REDKL = 0.0
   S1O2KL = 0.0
   VOLKL = 0.0
   YSATL = 0.0
   CONLDL = 0.0D+00
   INTINL = 0.0D+00
   TOTKL = 0.0D+00
   BIOTOL = 0.0
   SEDCOL = 0.0
   SEDMSL = 0.0
   WATVOL = 0.0
   YIELDL = 0.0D+00
end if ! End of re-initialization of data space.

! First record reserved for file descriptors
if (NDAT == 1 .or. ABEXIT) read (WRKLUN,rec=1) (IBUFF(I),I=1,4)
! Determine the number of records already in use, i.e., compute the
! offset needed for positioning the next blocks of data:
OFFSET = 1+(NDAT-1)*(IBUFF(1)+IBUFF(3))
! IBUFF(1) indicates the number of records required to retrieve the
! REAL*4 data, and IBUFF(2) indicates the number of variables actually
! stored on the last record:
NRECS = IBUFF(1)
ITRAIL = IBUFF(2)
! Read out the buffer from the file up to (but not including) the last record
FIRREC = OFFSET+1
LASTRC = FIRREC+NRECS-1
! WRITE(2,*)' Processing month number: ', NDAT
! WRITE(2,*)' UNPSCR record numbers (REAL*4) encompass ', FIRREC
! WRITE(2,*)' through                                  ', LASTRC
! Set index to point to first member of transfer buffer:
NSTART = 1
Many_records: if (NRECS > 1) then
   NEND = VARREC             ! Set termination index to length of records
   do K = FIRREC, LASTRC-1   ! Begin reading records
      read (WRKLUN,rec=K) (BUFF1(I),I=NSTART,NEND)
      !      WRITE(2,*)' RECNO: ',K
      !      WRITE(2,*)' CONTENTS:', (BUFF1(I),I=NSTART,NEND)
      !      WRITE(2,*)' End of contents of BUFF1.'
      NSTART = NEND+1        ! Update indices to get the
      NEND = NEND+VARREC     ! next sector of the buffer
   end do
end if Many_records
! Position the index for the last active member of the buffer:
NEND = (NRECS-1)*VARREC+ITRAIL
! Read the last (or the only) record:
read (WRKLUN,rec=LASTRC) (BUFF1(I),I=NSTART,NEND)
! WRITE(2,*) 'RECNO: ',LASTRC
! WRITE(2,*) 'CONTENTS:', (BUFF1(I),I=NSTART,NEND)
! WRITE(2,*) 'End of contents of last record in BUFF1.'

          ! Unload the single precision transfer buffer
NVAR = 1  ! Load the counter for transferring real variables

Chemicals: do K = 1, KCHEM
   Segments: do J = 1, KOUNT
      Species: do NSP = 1, 7
         if (SPFLGG(NSP,K) == 0) cycle Species
         do I = IALPHA(NSP), IALPHA(NSP)+3
            ALPHA(I,J,K) = BUFF1(NVAR)
            NVAR = NVAR+1
         end do
      end do Species
      do I = 29, 32
         ALPHA(I,J,K) = BUFF1(NVAR)
         NVAR = NVAR+1
      end do
   end do Segments
end do Chemicals

do K = 1, KCHEM
   do J = 1, KOUNT
      BIOLKL(J,K) = BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do J = 1, KOUNT
   BIOTOL(J) = BUFF1(NVAR)
   NVAR = NVAR+1
end do
!
do K = 1, KCHEM
   do J = 1, KOUNT
      EXPOKL(J,K) = BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      HYDRKL(J,K) = BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      OXIDKL(J,K) = BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      PHOTKL(J,K) = BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      REDKL(J,K) = BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      S1O2KL(J,K) = BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do J = 1, KOUNT
   SEDCOL(J) = BUFF1(NVAR)
   NVAR = NVAR+1
end do

do J = 1, KOUNT
   SEDMSL(J) = BUFF1(NVAR)
   NVAR = NVAR+1
end do
!
do K = 1, KCHEM
   do J = 1, KOUNT
      VOLKL(J,K) = BUFF1(NVAR)
      NVAR = NVAR+1
   end do
end do

do J = 1, KOUNT
   WATVOL(J) = BUFF1(NVAR)
   NVAR = NVAR+1
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      Species_again : do NSP = 1, 7
         if (SPFLGG(NSP,K) == 0) cycle Species_again
         YSATL(NSP,J,K) = BUFF1(NVAR)
         NVAR = NVAR+1
      end do Species_again
   end do
end do

! Transfer real (kind (0D0)) variables
OFFSET = LASTRC
NVAR = 1          ! Reset the counter of variables actually loaded
! IBUFF(3) contains the total number of records needed to store the
! REAL*8 (real (kind (0D0))) variables.  IBUFF(4) gets the number of
! variables actually in the last record:

NRECS = IBUFF(3)
ITRAIL = IBUFF(4)
! Read out the buffer from the file up to (but not including) the
! last record:
FIRREC = OFFSET+1
LASTRC = FIRREC+NRECS-1
!      WRITE(2,*)' Processing month number: ', NDAT
!      WRITE(2,*)' UNPSCR record numbers (REAL*8) encompass ', FIRREC
!      WRITE(2,*)' through                                  ', LASTRC
NSTART = 1   ! Set index to point to first member of transfer buffer
if (NRECS > 1) then
   NEND = VARDEC ! Set termination index to length of records
   do K = FIRREC, LASTRC-1 ! Begin reading records
      read (WRKLUN,rec=K) (BUFF2(I),I=NSTART,NEND)
      !      WRITE(2,*)' RECNO: ',K
      !      WRITE(2,*)' CONTENTS:', (BUFF2(I),I=NSTART,NEND)
      !      WRITE(2,*)' End of contents of BUFF2.'
      NSTART = NEND+1      ! Update indices to get
      NEND = NEND+VARDEC   ! next sector of the buffer
   end do
end if
! Position the index for the last active member of the buffer
NEND = (NRECS-1)*VARDEC+ITRAIL
! Read the last (or the only) record
read (WRKLUN,rec=LASTRC) (BUFF2(I),I=NSTART,NEND)
! WRITE(2,*) 'RECNO: ',   LASTRC
! WRITE(2,*) 'CONTENTS:', (BUFF2(I),I=NSTART,NEND)
! WRITE(2,*) 'End of contents of last record in BUFF2.'

do K = 1, KCHEM ! Unload the transfer buffer
   do J = 1, KOUNT
      CONLDL(J,K) = BUFF2(NVAR) ! SHOULD THIS BE COMMENTED OUT???
      NVAR = NVAR+1
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      do I = 1, KOUNT
         INTINL(I,J,K) = BUFF2(NVAR)
         NVAR = NVAR+1
      end do
   end do
end do

do K = 1, KCHEM
   do J = 1, KOUNT
      TOTKL(J,K) = BUFF2(NVAR)
      NVAR = NVAR+1
   end do
end do

do J = 1, KOUNT
   do K = 1, KCHEM
      do I = 1, KCHEM
         YIELDL(I,K,J) = BUFF2(NVAR)
         NVAR = NVAR+1
      end do
   end do
end do

! WRITE(2,*) 'WRITING FROM UNPSCR: NDAT = ',NDAT
! WRITE(2,*) 'ALPHA: ', ALPHA
! WRITE(2,*) 'BIOLKL: ', BIOLKL
! WRITE(2,*) 'BIOTOL: ', BIOTOL
! WRITE(2,*) 'EXPOKL: ', EXPOKL
! WRITE(2,*) 'HYDRKL: ', HYDRKL
! WRITE(2,*) 'OXIDKL: ', OXIDKL
! WRITE(2,*) 'PHOTKL: ', PHOTKL
! WRITE(2,*) 'REDKL: ', REDKL
! WRITE(2,*) 'S1O2KL: ', S1O2KL
! WRITE(2,*) 'SEDCOL: ', SEDCOL
! WRITE(2,*) 'SEDMSL: ', SEDMSL
! WRITE(2,*) 'VOLKL: ', VOLKL
! WRITE(2,*) 'WATVOL: ', WATVOL
! WRITE(2,*) 'YSATL: ', YSATL
! WRITE(2,*) 'CONLDL: ', CONLDL
! WRITE(2,*) 'INTINL: ', INTINL
! WRITE(2,*) 'TOTKL: ', TOTKL
! WRITE(2,*) 'YIELDL: ', YIELDL
deallocate (BUFF1,BUFF2)
return
end Subroutine UNPSCR
