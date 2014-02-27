subroutine TABC
! Created 10 November 1983 (LAB) by disaggregation of PRENV;
! this routine prints/shows the advective transport field.
! Revised 25-DEC-1985 (LAB)
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
! dependent cursor control.
! Converted to Fortran90 2/20/96, 6/1/96
! Revised April 2001 for wider output format; dynamic memory allocation
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Table_Variables

Implicit None

integer :: EOF, IMBED
integer, parameter :: Zero = 0
! EOF indicates End-of-File in the SHOW command.
integer :: I, IPAGE, IPASS, ITEST, J, K, KNT, NUMBLK
! NUMBLK is the number of blocks of data per page of output.
! Footnote variables
character(len=1), dimension(2) :: CCHAR = (/'1',' '/)
! CCHAR is carriage control character for page/nopage on output.
call Allocate_Table_Variables
! BATCH is 0 for run/continue, 1 for "show" command
if (BATCH==0 .and. RPTFIL) &
   write (RPTLUN,5000) CCHAR(BATCH+1),VERSN,MODEG,trim(ECONAM)
if (BATCH==1 .or. RPTFIL) then
   write (RPTLUN,5010) ! dashed line
   write (RPTLUN,5020) ! Table 9 title
   write (RPTLUN,5010) ! dashed line
end if
! Initialize the output vector
LOC1 = 0
LOC2 = 0
OUT1 = 0.0
! Compress the pairings to eliminate inactive pairs, count the active pairs
KNT = 0
do I = 1, size(JFRADG)
if (JFRADG(I) == 0 .and. ITOADG(I) == 0) cycle
   KNT = KNT+1
   LOC1(KNT) = JFRADG(I)
   LOC2(KNT) = ITOADG(I)
   OUT1(KNT) = ADVPRG(I)
end do
No_advection: if (KNT == 0) then
   if (BATCH==0 .and. RPTFIL) then
      write (RPTLUN,fmt='(A)')&
         ' No advective transport field specified.'
      write (RPTLUN,5010) ! dashed line
   else ! Interactive, so write dummy table to show variable names
      write (RPTLUN,5040)
      write (RPTLUN,5050)
      write (RPTLUN,5060)
      write (RPTLUN,5030)
      write (RPTLUN,5010) ! dashed line
   endif
   return
end if No_advection

! Transfer the compressed data to the database variables
JFRADG = LOC1
ITOADG = LOC2
ADVPRG = OUT1

ReportData: if (BATCH==1 .or. RPTFIL) then
! Set the number of data blocks per page
if (BATCH > 0) then
   NUMBLK = 4 ! interactive output
else
   NUMBLK = 5 ! printed page output
end if

! Print the active pairings, 6 per line
J = KNT
K = 1
IPASS = 1
IPAGE = 0
if (KNT > 6) J = 6
Print_loop: do
   write (RPTLUN,5040) (LOC1(I),I=K,J)
   write (RPTLUN,5050) (LOC2(I),I=K,J)
   write (RPTLUN,5060) (OUT1(I),I=K,J)
   ! WRITE out pathway numbers for an interactive database call
   if (BATCH > 0) write (RPTLUN,5030) (I,I=K,J)
   KNT = KNT-6
   if (KNT <= 0) exit Print_loop
   IPASS = IPASS+1
   IPAGE = IPAGE+1
   New_page: if (IPAGE == NUMBLK) then
      Interactive: if (BATCH > 0) then
         Query_loop: do ! Code for interactive version
            write (stdout,fmt='(A/A)',advance='NO')&
               ' Do you want to see additional specifications?',&
               ' Enter Yes, No, or Quit-> '
            call INREC(EOF,stdin)
            if (EOF == 1) return
            START = IMBED(INPUT,Zero)
            ! treat null input as yes...
            if (START == -999) exit Query_loop
            select case (INPUT(START:START))
            case ('Q','q','N','n'); return
            case ('Y','y'); exit Query_loop
            case default
            write (stdout,fmt='(/A)')&
               ' Response not understood.'
            end select
         end do Query_loop
      end if Interactive
      write (RPTLUN,5000) CCHAR(BATCH+1),VERSN,MODEG,trim(ECONAM)
      write (RPTLUN,5010) ! dashed line
      write (RPTLUN,5020)
      IPAGE = 0
   end if New_page
   K = 6*IPASS-5
   J = J+KNT
   ITEST = IPASS*6
   if (J > ITEST) J = ITEST
end do Print_loop
write (RPTLUN,5010) ! dashed line
end if ReportData
return
5000 format (A1,'Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2/' Ecosystem: ',A)
5010 format (1X,77('-')) ! dashed line
5020 format (' Table 9.  Input specifications -- advective transport field.')
5030 format ('  Path No.:',6(I6,4X))
5040 format (/' J FR AD   ',6(I6,4X))
5050 format (' I TO AD   ',6(I6,4X))
5060 format (' ADV PR    ',1PG10.3,5G10.3)
end subroutine TABC
