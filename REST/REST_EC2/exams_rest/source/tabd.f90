subroutine TABD
! Created 10 November 1983 (LAB) by disaggregation of PRENV;
! this routine prints/shows the dispersive transport field.
! Revised 25-DEC-1985 (LAB)
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
!    dependent cursor control. Converted to Fortran90 2/20/96
! Revised April 2001 for wider output format and support of dynamic memory
! Revised April 2002 to support optional production of report file
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
use Internal_Parameters
!use Rates_and_Sums
use Table_Variables
Implicit None
! Internal counters
integer :: I, I1, IPAGE, IPASS, ITEST, J, K, KNT, NBLOCL, NUMBLK, EOF
integer :: IMBED
integer, parameter :: Zero = 0
! NUMBLK is number of block of data per page of output.
! Local control variables
character(len=1), dimension(2) :: CCHAR = (/'1',' '/)
call Allocate_Table_Variables

! Separate cases (SHOW (BATCH=1) vs. RUN (BATCH=0) entry)
if (BATCH == 0) then
   ! Entry via RUN order; reset if necessary
   if (PRSWG == 1 .and. MODEG == 3) then
      TAG(1:1) = ' '
      MEAN = .false.
   endif
else ! Entry via SHOW command
   NFIRST = MONTHG
   NLAST = MONTHG
   NBLOCL = MONTHG
   MEAN = .false.
   TAG(1:1) = ' '
   if (MONTHG == 13) TAG(1:1) = '*'
   NMON = NAMONG(MONTHG)
endif

! Begin sequence of output tables
Output_tables: do NBLOCL = NFIRST, NLAST
   if (BATCH==0 .and. RPTFIL)&
       write (RPTLUN,5000) CCHAR(BATCH+1),VERSN,MODEG,trim(ECONAM)
   if (BATCH==1 .or. RPTFIL) write (RPTLUN,5010) ! dashed line
   ! Load NMON as needed--change current value only when printing the
   ! entire series ...
   if (MODEG==3 .and. PRSWG==1 .and. BATCH==0) then
      NMON = NAMONG(NBLOCL)
      ! When printing entire series, the last table is mean value
      if (NBLOCL == 13) then
         MEAN = .true.
         TAG(1:1) = '*'
      end if
   end if
   ! Load character string for transmitting NBLOCL to table headers
   write (KOUT,fmt='(I2.2)') NBLOCL
   if (BATCH==1 .or. RPTFIL) then
      write (RPTLUN,5040) KOUT,NMON
      write (RPTLUN,5010) ! dashed line
   end if
   ! Initialize the transfer vectors
   LOC1 = 0
   LOC2 = 0
   OUT1 = 0.0
   OUT2 = 0.0
   OUT3 = 0.0
   ! Compress the pairings to eliminate inactive pairs, count the
   ! active pairs
   KNT = 0
   Count_specifications: do I = 1, size(JTURBG)
      if (JTURBG(I) == 0 .and. ITURBG(I) == 0) cycle Count_specifications
      KNT = KNT+1
      LOC1(KNT) = JTURBG(I)
      LOC2(KNT) = ITURBG(I)
      OUT1(KNT) = XSTURG(I)
      OUT2(KNT) = CHARLG(I)
      if (MEAN) then ! Compute average value of DSPG
         OUT3(KNT) = 0.0
         do I1 = 1, 12
            OUT3(KNT) = OUT3(KNT)+DSPG(I,I1)
         end do
         OUT3(KNT) = OUT3(KNT)/12.0
         DSPG(I,13) = OUT3(KNT)  ! Load average value in sector 13 of DSPG
      end if
      OUT3(KNT) = DSPG(I,NBLOCL)
   end do Count_specifications
   No_data: if (KNT == 0) then
      if (BATCH == 0 .and. RPTFIL) then
         write (RPTLUN,fmt='(A)')&
            ' No dispersive transport field specified.'
      else ! interactive, so write empty table with variable names
         write (RPTLUN,5080)
         write (RPTLUN,5090)
         write (RPTLUN,5100)
         write (RPTLUN,5110)
         write (RPTLUN,5120)
         write (RPTLUN,5070)
      endif
      return
   end if No_data
   ! Transfer compressed vectors to database variables
   do I = 1, size(JTURBG)
      JTURBG(I) = LOC1(I)
      ITURBG(I) = LOC2(I)
      XSTURG(I) = OUT1(I)
      CHARLG(I) = OUT2(I)
      DSPG(I,NBLOCL) = OUT3(I)
   end do

   ReportData: if (BATCH==1 .or. RPTFIL) then
   ! Set number of blocks of data per page of output
   if (BATCH > 0) then
      NUMBLK = 2 ! interactive
   else
      NUMBLK = 3 ! printed page (still must fit on screen)
   endif
   ! Begin print sequence
   J = KNT
   K = 1
   IPASS = 1
   IPAGE = 0
   if (KNT > 6) J = 6
   Print_pages: do
      write (RPTLUN,5080) (LOC1(I),I=K,J)
      write (RPTLUN,5090) (LOC2(I),I=K,J)
      write (RPTLUN,5100) (OUT1(I),I=K,J)
      write (RPTLUN,5110) (OUT2(I),I=K,J)
      write (RPTLUN,5120) TAG(1:1),(OUT3(I),I=K,J)
      ! write pathway numbers if interactive database call
      if (BATCH > 0) write (RPTLUN,5070) (I,I=K,J)
      KNT = KNT-6
      if (KNT <= 0) cycle Output_tables
      IPASS = IPASS+1
      IPAGE = IPAGE+1
      New_page: if (IPAGE == NUMBLK) then
         Interactive: if (BATCH /= 0) then
            write (RPTLUN,5010) ! dashed line
            if (TAG(1:1) == '*') write (RPTLUN,5020) TAG(1:1)
            Query: do
               write (stdout,fmt='(A/A)',advance='NO')&
                  ' Do you want to see additional specifications?',&
                  ' Enter Yes, No, or Quit-> '
               call INREC (EOF,stdin)
               if (EOF == 1) return
               START = IMBED(INPUT,Zero)
               ! Assume yes answer if nothing on line...
               if (START == -999) exit Query
               select case (INPUT(START:START))
               case ('Q','q','N','n'); return
               case ('Y','y'); exit Query
               case default
                  write (stdout,fmt='(/A)')&
                     ' Response was not understood; please try again.'
               end select
            end do Query
         end if Interactive
         write (RPTLUN,5000) CCHAR(BATCH+1),VERSN,MODEG,trim(ECONAM)
         write (RPTLUN,5010) ! dashed line
         write (RPTLUN,5040) KOUT,NMON
         IPAGE = 0
      end if New_page
      K = 6*IPASS-5
      J = J+KNT
      ITEST = IPASS*6
      if (J > ITEST) J = ITEST
   end do Print_pages
   end if ReportData
end do Output_tables
if (BATCH==1 .or. RPTFIL) then
   write (RPTLUN,5010) ! dashed line
   if (TAG(1:1) == '*') write (RPTLUN,5020) TAG(1:1)
end if
return
5000 format (A1,'Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2/' Ecosystem: ',A)
5010 format (1X,77('-'))  ! dashed line
5020 format (1X,A1,' Average of 12 monthly mean values.')! mean value footnote
5040 format (' Table 10.',A2,'.  ',A4,' dispersive transport field.')
5070 format ('  Path No.:',2X,6(I6,5X))
5080 format (/' J TURB    ',2X,6(I6,5X))
5090 format (' I TURB    ',2X,6(I6,5X))
5100 format (' XS TUR m2 ',2X,1PG10.3,5(1X,G10.3))
5110 format (' CHARL m   ',2X,1PG10.3,5(1X,G10.3))
5120 format (' DSP m2/hr',A1,2X,1PG10.3,5(1X,G10.3))
end Subroutine TABD
