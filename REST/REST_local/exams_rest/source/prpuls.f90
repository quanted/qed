subroutine PRPULS
! PRPULS records the input data describing pulse loadings.
! Created 31 August 1983 by L.A. Burns. Revised 12/25/1985.
! Revised 10/20/1988 - run-time formats for
!    implementation-dependent cursor control.
! Help format revisions 10/24/1988. Converted to Fortran90 2/20/1996.
! Minor output format revision 02/29/2000.
! Revision 02/12/2001: in Mode 1, pulse loads are set to zero
! Revision 04/07/2001 -- updated format for large number of chemicals or segs
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
Implicit None
! Local variables for this subroutine
integer :: I, J, K, KNT, IPAGE, ITEST, IPASS, NUMBLK, IMBED, Zero=0, EOF
! NUMBLK is number of blocks of data per page of output.
character(len=1), dimension(2) :: CCHAR = (/'1',' '/)

call Headers

if (NPULSE < 1 .or. MODEG == 1) then
   ! No pulses; blank the data structure, write blank table and return.
   IMONG=0
   IDAYG=0
   IYEARG=0
   ISEGG=0
   ICHEMG=0
   IMASSG=0.0
   write (RPTLUN,fmt='(A)')&
   ' Pulse chemical loadings not used in this analysis.'
   write (RPTLUN, 5020) ! dashed line
   return
end if

KNT = NPULSE
! Set number of blocks of data per page; start output sequence
NUMBLK = 4
if (MODEG == 3) NUMBLK = 3
if (BATCH > 0) NUMBLK = NUMBLK-1
J = KNT
K = 1
IPASS = 1
IPAGE = 0
if (KNT > 5) J = 5
Output_loop: do
   write (RPTLUN,fmt='()') ! skip line
   if (MODEG == 3) then
      write (RPTLUN,fmt='(A,5(3X,I3,4X))')&
         ' IMONth    ', (IMONG(I),I=K,J)
      write (RPTLUN,fmt='(A,5(3X,I3,4X))')&
         ' IDAY      ', (IDAYG(I),I=K,J)
   endif
   write (RPTLUN,fmt='(A,5(I6,4X))')&
      ' ICHEM-ADB#', (ICHEMG(I),I=K,J)
   write (RPTLUN,fmt='(A,5(I7,3X))')&
      ' ISEGment ', (ISEGG(I),I=K,J)
   write (RPTLUN,fmt='(A,1PG10.3,4G10.3)')&
      ' IMASS (kg)', (IMASSG(I),I=K,J)
   if (BATCH > 0) then
      write (RPTLUN,fmt='(A,I3,4X,4(3X,I3,4X))')&
         ' Event Number ', (I,I=K,J)
      write (RPTLUN,fmt='()') ! skip line
   end if
   KNT = KNT-5
   if (KNT <= 0) exit Output_loop
   IPASS = IPASS+1
   IPAGE = IPAGE+1
   End_page: if (IPAGE == NUMBLK) then
      write (RPTLUN,5020) ! dashed line
      write (RPTLUN,5030)
      if (BATCH /= 0) then ! interactive mode, ask user for instructions
         Query: do
            write (stdout,fmt='(A/A)',advance='NO')&
               ' There are more; do you want to see them?',&
               ' Please enter Yes, No, or Quit-> '
            call INREC (EOF,stdin)
            if (EOF == 1) return
            START = IMBED(INPUT,Zero)
            if (START == -999) exit Query ! treat null input as yes...
            if (INPUT(START:START)=='Q'.or.INPUT(START:START)=='q'.or. &
                INPUT(START:START)=='N'.or.INPUT(START:START)=='n') return
            if (INPUT(START:START)=='Y'.or.INPUT(START:START)=='y') exit Query
            write (stdout,fmt='(/A)')&
               ' Response was not understood; please try again.'
         end do Query
      end if
      call Headers ! write Table headers
      IPAGE = 0
   end if End_page
   K = 5*IPASS-4
   J = J+KNT
   ITEST = IPASS*5
   if (J > ITEST) J = ITEST
end do Output_loop
write (RPTLUN,5020) ! dashed line
write (RPTLUN,5030)
5020 format (1X,77('-')) ! dashed line
5030 format (& ! table footnote
    ' * N.B.: Input data only; may be revised during simulation.')
return

contains
subroutine Headers
! write Table headers
write (RPTLUN,5000) CCHAR(BATCH+1),VERSN,MODEG,trim(ECONAM)
do K = 1, KCHEM
   write (RPTLUN,5010) K,trim(CHEMNA(K))
end do
write (RPTLUN,5020) ! dashed line
write (RPTLUN,fmt='(A)')&
   ' Table 3.  Chemical input data: pulse loadings.*'
write (RPTLUN,5020) ! dashed line
if (BATCH > 0) write (RPTLUN,5050) trim(LOADNM)
! end write Table headers
5000 format (A1,'Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2/' Ecosystem: ',A)
5010 format (' Chemical: ',I0,') ',A)
5020 format (1X,77('-')) ! dashed line
5050 format (' Load Entry--',A)
end subroutine Headers

end subroutine PRPULS
