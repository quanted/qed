subroutine PRPROD(UnitNumber,Problem)
! Revised 25-DEC-1985 (LAB)
! Revised 10/24/88 (LAB) -- run-time formats for implementation-
! dependent cursor control.
! Converted to Fortran90 2/20/96; 5/30/96
! Revisions 09-Feb-2001 to serve the WRITE command
use Global_Variables
use Local_Working_Space
! BATCH is used to control printing
! BATCH = 0 for printing tables during a RUN/CONTINUE
! BATCH = 1 for output in response to the SHOW command
! BATCH = 2 for output in response to the WRITE command

use Internal_Parameters
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Implementation_Control
use Input_Output

! PRPROD records input data in the file specified by LUN UnitNumber.
! The input variables are
! 1. CHPARG -- a vector of integer numbers denoting the
!    CHemical PARent compound, i.e., the source compound
! 2. TPRODG -- a vector of integer numbers denoting the
!    Transformation PRODuct of the pathway deriving from
!    the homologous member of CHPARG
! 3. NPROC -- vector of integers denoting the transformation
!    producing TPROD from CHPAR.  These can be numbered from
!    1 to 9, representing
!          1. specific acid hydrolysis
!          2. neutral hydrolysis
!          3. specific base hydrolysis
!          4. direct photolysis
!          5. singlet oxygen photooxidation
!          6. free radical oxidation
!          7. water column bacterial biolysis
!          8. benthic sediment bacterial biolysis
!          9. reductions, e.g., reductive dechlorination
! 4. RFORM -- vector of integers denoting the Reactive molecular
!    FORM of CHPAR for the current pathway. RFORM is homologous
!    with the ALPHA computational vector (c.f.), that is,
!    RFORM of 1 signifies the dissolved, neutral molecule, etc.,
!    including specification of all dissolved forms, all
!    sorbed forms, etc.
! 5. YIELDG is the product YIELD from the pathway, with
!    dimensions Mole produced per Mole reacted (or dimensionless).
! 6. EAYLDG is an activation energy for computing YIELDG as a
!    function of temperature--the name of the variable is an
!    acronym  for Ea (energy of activation) of the product yield.
!    As with most kinetic constants  in EXAMS, a non-zero value
!    of EAYLD (units are Kcal) invokes a re-evaluation
!    of YIELDG in which YIELDG is interpreted as the pre-
!    exponential factor in an Arrhenius-type function.  When
!    EAYLD is zero, YIELDG is simply the dimensionless
!    molar product yield.

Implicit None
! Local variables for this subroutine
real :: OUT1(NTRAN),OUT2(NTRAN),TEST
integer :: KNT,I,J,K,IPAGE,ITEST,IPASS, NUMBLK, EOF, IPOS, IMBED, Zero=0
integer :: IOError
integer, intent(in) :: UnitNumber ! LUN where data should be written
! NUMBLK is the number of data blocks per output page.
integer LOC1(NTRAN),LOC2(NTRAN),LOC3(NTRAN),LOC4(NTRAN)
! Variables LOC1, LOC2, LOC3, LOC4, OUT1, and OUT2 are local
! variables for compressing the product chemistry specifications.
character(len=78) :: OUTLIN
character(len=1), dimension(2) :: CCHAR=(/'1',' '/)
logical, intent (out) :: Problem ! to signal problem to WRITE command
Problem = .false.
KNT = 0
if (BATCH==0 .or. BATCH==1) write (UnitNumber,5000) CCHAR(BATCH+1),VERSN,MODEG
if (BATCH==2) write (UnitNumber,fmt='(A,I6)') ' Number of chemicals: ',KCHEM
do K = 1, KCHEM
   write (UnitNumber,5010) K,trim(CHEMNA(K))
end do
if (BATCH==0.or.BATCH==1) then ! for reports and console output
   write (UnitNumber,5020) ! dashed line
   write (UnitNumber,5030)
   write (UnitNumber,5020) ! dashed line
end if
if (BATCH==1) & ! additional information for interactive user
   write (UnitNumber,fmt='(A)') ' Product title "'//trim(PRODNM)//'"'
! If only working on one chemical, don't clean up data;
! data will not be emitted unless serving the SHOW command (BATCH=1).

Many_chemicals: if (KCHEM > 1) then
   ! For the sake of the user's sanity during problem
   ! setup, the compressed specification vector is transferred to the
   ! input data. That is, the output vectors are zeroed, the active
   ! (or partially active) input specifications (only) are
   ! transferred to the output vector, and then the input data are
   ! cleaned up.
   LOC1 = 0
   LOC2 = 0
   LOC3 = 0
   LOC4 = 0
   OUT1 = 0.0
   OUT2 = 0.0
   ! Compress the data to eliminate inactive pairs, count the active elements
   do I = 1, NTRAN   ! Up to NTRAN pairings may be available
      TEST=float(CHPARG(I)+TPRODG(I)+NPROCG(I)+RFORMG(I))+YIELDG(I)+EAYLDG(I)
      if (TEST .Equals. 0.0) cycle
      KNT = KNT+1
      LOC1(KNT) = CHPARG(I)
      LOC2(KNT) = TPRODG(I)
      LOC3(KNT) = NPROCG(I)
      LOC4(KNT) = RFORMG(I)
      OUT1(KNT) = YIELDG(I)
      OUT2(KNT) = EAYLDG(I)
   end do
   ! Transfer output vector back to input data to get cleaned up version
   do I = 1, NTRAN
      CHPARG(I) = LOC1(I)
      TPRODG(I) = LOC2(I)
      NPROCG(I) = LOC3(I)
      RFORMG(I) = LOC4(I)
      YIELDG(I) = OUT1(I)
      EAYLDG(I) = OUT2(I)
   end do
end if Many_chemicals

NoChem: if (.not.KCHEM>1 .or. KNT==0) then ! no product chemistry
   if (BATCH==0) then         ! RUN or CONTINUE mode
      write (UnitNumber,fmt='(A)') ' No product chemistry specified.'
   else if (BATCH==2) then    ! WRITE command, tag the file as empty
      write (UnitNumber,fmt='(A,I6)',IOSTAT=IOError)&
         ' Number of product pathways: ',KNT
         if (IOError/=0) then
            Problem = .true.
         end if
      return
   else ! interactive mode, write table sans data to show data elements
      write (UnitNumber,5090)
      write (UnitNumber,5100)
      write (UnitNumber,5110)
      write (UnitNumber,5120)
      write (UnitNumber,5130)
      write (UnitNumber,5140)
      write (UnitNumber,5080)
      if (.not. KCHEM > 1) write (UnitNumber,fmt='(/A)') &
         ' Product chemistry not needed for single chemical studies.'      
   endif
   write (UnitNumber,5020) ! dashed line
   return
end if NoChem
if (BATCH==2) then
   call WriteCommand
   return
end if
! Set number of output blocks per page of output; start print sequence
NUMBLK = 3
if (BATCH==1) NUMBLK = 2 ! interactive, match output to screen size
J = KNT
K = 1
IPASS = 1
IPAGE = 0
if (KNT > 6) J = 6
Output_loop: do
   write (UnitNumber,5090) (LOC1(I),I=K,J)
   write (UnitNumber,5100) (LOC2(I),I=K,J)
   write (UnitNumber,5110) (LOC3(I),I=K,J)
   write (UnitNumber,5120) (LOC4(I),I=K,J)
   write (UnitNumber,5130) (OUT1(I),I=K,J)
   write (OUTLIN,5140)     (OUT2(I),I=K,J)
   ! Blank out zero values
   IPOS = 12
   do I = K, J
      if (OUT2(I) .Equals. 0.0) OUTLIN(IPOS:IPOS+9) = '         '
      IPOS = IPOS+10
   end do
   write (UnitNumber,fmt='(A)') trim(OUTLIN)
   ! Write out pathway number in interactive mode
   if (BATCH > 0) write (UnitNumber,5080) (I,I=K,J)
   KNT = KNT-6
   if (KNT <= 0) exit Output_loop
   IPASS = IPASS+1
   IPAGE = IPAGE+1
   End_page: if (IPAGE == NUMBLK) then
      Interactive: if (BATCH > 0) then
         Query_loop: do
            write (stdout,fmt='(A/A)',advance='NO')&
               ' There are more; do you want to see them?',&
               ' Please enter Yes, No, or Quit-> '
            call INREC (EOF,stdin)
            if (EOF == 1) return
            START = IMBED(INPUT,Zero)
            ! treat null input as yes...
            if (START == -999) exit Query_loop
            if (INPUT(START:START) == 'Q'.or.INPUT(START:START) == 'q'.or.&
                INPUT(START:START) == 'N'.or.INPUT(START:START) == 'n') return
            if (INPUT(START:START) == 'Y'.or.INPUT(START:START) == 'y')&
               exit Query_loop
            write (stdout,fmt='(/A)')&
               ' Response was not understood. Please try again.'
         end do Query_loop
      end if Interactive
      write (UnitNumber,5000) CCHAR(BATCH+1),VERSN,MODEG
      do K = 1, KCHEM
         write (UnitNumber,5010) K,trim(CHEMNA(K))
      end do
      write (UnitNumber,5020) ! dashed line
      write (UnitNumber,5030)
      write (UnitNumber,5020) ! dashed line
      if (BATCH==1) & ! additional information for interactive user
         write (UnitNumber,fmt='(A)')' Product title "'//trim(PRODNM)//'"'
      IPAGE = 0
   end if End_page
   K = 6*IPASS-5
   J = J+KNT
   ITEST = IPASS*6
   if (J > ITEST) J = ITEST
end do Output_loop
return
5000 format (A1,'Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2)
5010 format (' Chemical: ',I0,') ',A)
5020 format (1X,77('-')) ! format for dashed line
5030 format (' Table 2.  Chemical input data: product chemistry.')
5080 format ('  Pathway--',6(I6,4X))
5090 format(/' CH PAR ',   6(I9,1X))
5100 format (' T PROD ',   6(I9,1X))
5110 format (' N PROC    ',6(3X,I3,4X))
5120 format (' R FORM    ',6(3X,I3,4X))
5130 format (' YIELD M/M ',1PG10.3,5G10.3)
5140 format (' EaYLD Kcal',1PG10.3,5G10.3)

contains
subroutine WriteCommand
! write to the flat file requested in the WRITE command.
write (UnitNumber,fmt='(A,I6)') ' Number of product pathways: ',KNT

! write the column headers:
write (UnitNumber,fmt='(A)') &
'  Path CHPAR TPROD NPROC RFORM     YIELD      EAYLD'
do I = 1,KNT
   write (UnitNumber, fmt='(5(1x,I5),1x,ES9.3,2x,ES9.3)',IOSTAT=IOError) &
      I, CHPARG(I), TPRODG(I), NPROCG(I), RFORMG(I), YIELDG(I), EAYLDG(I)
   if (IOError/=0) then
      Problem = .true.
      return
   end if
end do
end subroutine WriteCommand
end subroutine PRPROD
