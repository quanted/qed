subroutine PRICL(NYR)
! PRICL prints initial conditions and chemical loadings.
! Revised 25-DEC-1985 (LAB)
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
! dependent cursor control. Converted to Fortran90 2/20/96
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
use Internal_Parameters
Implicit None
! Local variables
real :: OUT(6), TEST, XHOUR
integer :: I,J,K,NYR,NSTART,NSTOP,N1,IMBED
! NSTART and NSTOP control the loop on monthly loadings.
! NYR is the number of the year being processed in DRIVER.
! Local variables for mode 2/3 operations
integer :: IPULS2,IPULS3,N01,NLAST,NPLS,EOF
integer, parameter :: Zero = 0 
! N01 is the first pulse for a month being processed.
! NLAST is the last active pulse for a month being processed.
! NPLS is the number of pulse loads occurring in a given month.
logical :: PRTEST
! In mode 3, loads and pulses are printed at the end of each RUN;
! PRTEST is used to check on the existence of a non-zero load set.
character(len=78) :: OUTLIN
character(len=2), dimension(2) :: KOUT
! KOUT(1) holds the character representation of K; KOUT(2), NDAT.
! CCHAR is carriage control character
character(len=1), dimension(2) :: CCHAR = (/'1','0'/)
IPULS2 = 1             ! Initialize counter for vector of chemical pulse loads
if (BATCH /= 0) then   ! For SHOW entry,
   if (mod(NYR,4)==0 .and. mod(NYR,100)/=0 .or. mod(NYR,400)==0) then
      NDAYS(2) = 29    ! set number of days in Feb. according to YEAR1
   else
      NDAYS(2) = 28
   end if
endif
if (MODEG == 3) then ! Set NDAT loop controls
   NSTART = 1
   NSTOP = 12
elseif (PRSWG == 0) then
   NSTART = 13
   NSTOP = 13
else
   NSTART = MONTHG
   NSTOP = MONTHG
endif
! Skip next sector in Mode 1/2
Mode_three: if (MODEG == 3) then
! In mode 3, begin with summary table (this is the only table
! that includes pulse loads when invoked by SHOW command)
Chemical_loop: do K = 1, KCHEM
   Check_loop: do ! Test for non-zero loads and pulses; if none, skip chemical
      do J = 1, KOUNT
         do NDAT = 1, 12
            TEST = STRLDG(J,K,NDAT)+PCPLDG(J,K,NDAT)+SEELDG(J,K,NDAT)&
               +NPSLDG(J,K,NDAT)+DRFLDG(J,K,NDAT)
         ! Move on to print sequence when a non-zero load occurs
         if (TEST .GreaterThan. 0.0) exit Check_loop
         end do
      end do
      Pulse_loop: do I = 1, MAXMAS ! Test for pulses for this chemical
         ! Skip leap-day loads if not leap year
         if(NDAYS(2)==28 .and. IMONG(I)==2 .and. IDAYG(I)==29)cycle Pulse_loop
         if (ICHEMG(I) == K) exit Check_loop ! found a pulse, leave check area
         ! Pulse loop ends when all pulses checked; or leave early if entered
         ! via the RUN command, because the pulses have been pre-processed and
         ! the first occurrence of a zero ICHEMG signals the end of the data.
         if (ICHEMG(I) == 0 .and. BATCH == 0) exit Pulse_loop
      end do Pulse_loop
      ! No loads or pulses--go to next chemical
      cycle Chemical_loop
   end do Check_loop
   ! This chemical has non-zero allochthonous loads; start print sequence
   ! Page header
   write (RPTLUN,5000) CCHAR(BATCH+1),VERSN,MODEG,trim(ECONAM)
   write (RPTLUN,fmt='(A,I2,A)') ' Chemical:',K,') '//trim(CHEMNA(K))
   write (RPTLUN,5020) ! dashed line
   ! Load character string for transmitting K to table headers
   write (KOUT(1),fmt='(I2)') K
   if (KOUT(1)(1:1) == ' ') KOUT(1)(1:1) = '0'
   ! Table title and column headings
   write (RPTLUN,fmt='(A/A,I4,A)')&
   ' Table 14.'//KOUT(1)//&
      '.13.  Total annual allochthonous chemical loads and',&
      ' pulses (kg) during year ',NYR,'.'
   write (RPTLUN,5020) ! dashed line
   if (BATCH > 0) write (RPTLUN,fmt='(A)')&
       ' Load data--  '//trim(LOADNM)
   write (RPTLUN,5150) ! column headings
   Segment_loop: do J = 1, KOUNT
      OUT = 0.0 ! Zero output vector
      do NDAT = 1, 12                         ! Sum across months
         XHOUR = float(24*NDAYS(NDAT))        ! Multiplication by 24 (hrs/day)
         OUT(1) = OUT(1)+STRLDG(J,K,NDAT)*XHOUR ! and number of days in months
         OUT(2) = OUT(2)+PCPLDG(J,K,NDAT)*XHOUR ! converts kg/hr load input
         OUT(3) = OUT(3)+SEELDG(J,K,NDAT)*XHOUR ! to total kg for the month
         OUT(4) = OUT(4)+NPSLDG(J,K,NDAT)*XHOUR
         OUT(5) = OUT(5)+DRFLDG(J,K,NDAT)*XHOUR
      end do ! End sum on months
      Pulse_inventory: do I = 1, MAXMAS ! Inventory pulse load vector
         ! In RUN mode, the pulses have been pre-processed and the first
         ! zero entry in IMONG signals the end of the data
         if (BATCH==0 .and. IMONG(I)==0) exit Pulse_inventory
         if (ICHEMG(I) /= K .or. ISEGG(I) /= J) cycle Pulse_inventory
         if (NDAYS(2)==28 .and. IDAYG(I)==29 .and. IMONG(I)==2)& ! leap year?
            cycle Pulse_inventory ! if not leap year, skip leap day load
         OUT(6) = OUT(6)+IMASSG(I)
      end do Pulse_inventory
      TEST = sum(OUT)               ! Test for non-zero entry for this segment
      if (TEST .Equals. 0.0) cycle Segment_loop ! skip segments without loads
      write (OUTLIN,fmt='(1X,I3,1PG10.3,5G10.3)')&
         J,(OUT(I),I=1,6)                  ! Write line to internal file
      N1 = 1                               ! Blank out zero entries
      do I = 5, 55, 10
         if (OUT(N1) .Equals. 0.0) OUTLIN(I:I+9) = '          '
         N1 = N1+1
      end do
      write (RPTLUN,fmt='(A)') trim(OUTLIN)
   end do Segment_loop
   write (RPTLUN,5020) ! dashed line
end do Chemical_loop
   if (PRSWG == 0) return  ! If detailed table not requested, exit now
end if Mode_three          ! End of mode 3 summary table

N01 = 1    ! Initialize counters for sweeping
NLAST = 1  ! pulse load vector in mode 3
Data_loop: do NDAT = NSTART, NSTOP ! Start loop on blocks of data
   NPLS = 0             ! Count the number of pulses in the current month IFF
   if (MODEG==3 .and. N01<=MAXMAS .and. BATCH==0) then ! mode 3, & not SHOW
      do K = N01, MAXMAS
         if (IMONG(K) /= NDAT) exit
         NPLS = NPLS+1
      end do
      NLAST = N01+NPLS-1
   end if
   ! When entry is via a SHOW command, query the user before emitting a table
   Show_more: if (BATCH/=0 .and. NSTART/=NSTOP) then
      Show_table: do
         write (stdout,fmt='(A)',advance='NO')&
            ' Do you want to see the '//trim(NAMONG(NDAT))//&
            ' chemical loads? (Yes, No, or Quit)-> '
         call INREC (EOF,stdin)
         if (EOF == 1) return
         START = IMBED(INPUT,Zero)
         if (START == -999) exit Show_table ! treat null input as yes...
         select case (INPUT(START:START))
            case ('Q', 'q'); return
            case ('N', 'n'); cycle Data_loop
            case ('Y', 'y'); exit Show_table
            case default; write (stdout,fmt='(/A)')&
               ' Response was not understood; Please try again.'
                 cycle Show_table
         end select
      end do Show_table
   end if Show_more

   Chemicals: do K = 1, KCHEM
      PRTEST = .false.
      write (KOUT(1),fmt='(I2)') K
      if (KOUT(1)(1:1) == ' ') KOUT(1)(1:1) = '0'
      ! Tabulate loads on system, write to LUN RPTLUN -
      ! Page header
      write (RPTLUN,5000) CCHAR(BATCH+1),VERSN,MODEG,trim(ECONAM)
      write (RPTLUN,fmt='(A,I2,A)')&
         ' Chemical:',K,') '//trim(CHEMNA(K))
      write (RPTLUN,5020) ! dashed line
   
      ! Separate entry via RUN/CONTINUE from entry via SHOW
      RUN_or_SHOW: if (BATCH==0) then ! Entry via RUN/CONTINUE--
         ! separate setup for case MODE=1 and case MODE=2 or higher
         Mode_select: if (MODEG==1) then ! Mode 1 is steady-state analysis
            write (RPTLUN,fmt='(A)')& ! Table title and column headers
              ' Table 14.'//KOUT(1)//&
              '.  Segment allochthonous chemical loadings (kg/hr).'
            write (RPTLUN,5020)  ! dashed line
            write (RPTLUN,5110)  ! column headings sans pulses
         else Mode_select ! MODE=2 or more; user control of I.C. or pulse load
            select case (MODEG) ! Mode 2 and 3 have different table headers
               case (2); write (RPTLUN,fmt='(A)')&
                  ' Table 14.'//KOUT(1)//&
                  '.  Allochthonous loads (kg/hr) and pulses (kg).'
               case (3); write (KOUT(2),fmt='(I2)') NDAT
                  if (KOUT(2)(1:1) == ' ') KOUT(2)(1:1) = '0'
                  write (RPTLUN,fmt='(A/A,I4,A)')&
                     ' Table 14.'//KOUT(1)//'.'//KOUT(2)//&
                     '. Allochthonous chemical loads (kg/hr) and',&
                     ' pulses (kg) during '//trim(NAMONG(NDAT))//&
                     ' of year ',NYR,'.'
            end select
            write (RPTLUN,5020) ! dashed line
            write (RPTLUN,5150) ! column headings
         end if Mode_select
      else RUN_or_SHOW   ! Entry via SHOW command
         write (RPTLUN,fmt='(A,I5,A)')&
            ' '//trim(NAMONG(NDAT))//' of year',NYR,&
            ': allochthonous chemical loads (kg/hr).'
         write (RPTLUN,5020) ! dashed line
         write (RPTLUN,fmt='(A)') ' Load data--  '//trim(LOADNM)
         write (RPTLUN,5110) ! column headings sans pulses
      end if RUN_or_SHOW

      Segments: do J = 1, KOUNT
         OUT(1) = STRLDG(J,K,NDAT)
         OUT(2) = PCPLDG(J,K,NDAT)
         OUT(3) = SEELDG(J,K,NDAT)
         OUT(4) = NPSLDG(J,K,NDAT)
         OUT(5) = DRFLDG(J,K,NDAT)
         OUT(6) = 0.0 ! Pulses initialized to zero.
         ! In mode 1 and for the SHOW command, the zero set will prevent
         ! printing of pulses. Processing for Mode 2 & 3 is now conducted
         RUN_or_CONTINUE: if (BATCH == 0) then      ! for the RUN command
            Mode_choose: select case (MODEG) ! choose current operations mode
            case (2) Mode_choose ! Mode 2 pulses : if the current member of
               if (IPULS2<=MAXMAS .and.& ! the pulse vector belongs to current
               ICHEMG(IPULS2)==K .and. ISEGG(IPULS2)==J) then ! print set,
                  OUT(6) = IMASSG(IPULS2) ! load it into the output vector and
                  IPULS2 = IPULS2+1       ! increment the vector counter
               end if
            case (3) Mode_choose  ! Mode 3 processing...check for completed
               ! processing of pulse loads or no pulses for the current month
               if (NPLS > 0) then ! There are pulses for the month;
                  ! only load those for the current chemical and segment
                  do IPULS3 = N01, NLAST
                     if (ICHEMG(IPULS3)/=K .or. ISEGG(IPULS3)/=J) cycle
                     if (NDAT==2 .and. NDAYS(2)==28 .and. IDAYG(IPULS3)==29)&
                        cycle           ! Skip leap day load if not leap year
                     OUT(6) = OUT(6)+IMASSG(IPULS3) ! Load hit
                  end do
               end if
               TEST = sum(OUT)
               if (sum(OUT) .LessThanOrEqual. 0.0) then
                  ! No loads, thus skip line. However,
                  ! if this is the last segment and nothing has been printed,
                  if (J==KOUNT .and. .not.PRTEST)& ! then
                     write (RPTLUN,fmt='(A)')&
                        ' No allochthonous loads or pulses for '&
                        //trim(NAMONG(NDAT))
                  cycle Segments ! in any case, as no loads
               end if
            end select Mode_choose
         end if RUN_or_CONTINUE
         PRTEST = .true.
         write (OUTLIN,fmt='(1X,I3,1PG10.3,5G10.3)')&
            J,(OUT(I),I=1,6)                    ! Write line to internal file
         N1 = 1                                 ! Blank out zero entries
         do I = 5, 55, 10
            if (OUT(N1) .Equals. 0.0) OUTLIN(I:I+9) = '          '
            N1 = N1+1
         end do
         write (RPTLUN,fmt='(A)') trim(OUTLIN) ! Write line to report
      end do Segments
      write (RPTLUN,5020) ! dashed line
   end do Chemicals
   ! Completed processing of current month, update mode 3 pulse load pointer
   N01 = NLAST+1
end do Data_loop ! End of loop on NDAT
5000 format&  ! formats for table headers
(A1,'Exposure Analysis Modeling System -- EXAMS Version ',A,', Mode',I2,&
/' Ecosystem: ',A)
5020  format (1X,77('-'))  ! Dashed line format statement
5110  format&   ! column headings sans pulses
   (' Seg  Streams  Rainfall    Seeps   NPS Loads   Drift',&
   /' --- --------- --------- --------- --------- ---------')
5150 format& ! column headings with pulses
   (' Seg  Streams  Rainfall    Seeps   NPS Loads   Drift    Pulse IC',&
   /' --- --------- --------- --------- --------- --------- ---------')
end subroutine PRICL
