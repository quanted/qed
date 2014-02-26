subroutine LIST(OUTLUN,SPOOL)
! Purpose--to list all or selected portions of the listing file.
! Subroutines required--GETNUM, INREC, SKAN
! Revised 25-DEC-1985, 16-APR-87, 14-MAY-87 (LAB)
! Revised 10/24/88 (LAB) -- run-time formats for implementation-
! dependent cursor control. Converted to Fortran90 2/20/96, 4/18/96
! Revised 10/26/88 to unify command abort style to "quit"
use Implementation_Control
use Input_Output
use MultiScan
Implicit None
real :: XT
integer :: EOF,ERROR,NTABL,OUTLUN,REPEAT,KNT,IMBED,II,IT,MATCH,IS,J
integer, parameter :: Zero=0, Three=3, NAMLEN=11
integer :: IOerror
logical, intent (in) :: Spool ! signals user wants print, not terminal list
! OUTLUN was assigned to stdout if Spool .false.
! OUTLUN was assigned to printr if Spool .true.
character(len=80), dimension(4) :: HOLD
character(len=7) ::  TABID = ' Table '
character(len=8) :: Particle ! to distinguish between "append" and "replace"
character(len=2), dimension(20) :: SUFFIX =&
(/'1.','2.','3.','4.','5.','6.','7.','8.','9.','10',&
  '11','12','13','14','15','16','17','18','19','20'/)
integer :: LENS(3) = (/3,4,4/), MINS(3) = (/1,1,1/)
character(len=1), dimension(11) :: NAME =&
   (/'A','L','L',  'Q','U','I','T',  'H','E','L','P'/)
character(len=1), dimension(1), parameter :: BLANK = ' '
character(len=Max_File) :: Output_File
logical :: Success      ! if get a valid output file for Printing
! Process user input--Update position pointer and evaluate the
! input, skipping the prompt.
START = STOPIT+1
   REPEAT = 0
KNT = 0
Get_request: do
   START = IMBED(INPUT,START-1)
   Need_input: if (START == -999) then ! additional input is required, so
      write (stdout,fmt='(3(/A))',advance='NO')& ! prompt the user
         ' At the prompt, enter a Table number, "Quit,"',&
         ' or "Help" to see a catalog of the output tables.',&
         ' Enter Table Number -> '
      call INREC (EOF,stdin) ! Get user input from keyboard
      if (EOF == 1) then
         write (stdout,fmt='(/A)') ' End of LIST.'
         close (unit=RPTLUN,iostat=IOError); call Release_LUN (RPTLUN); return
      end if
      STOPIT = 0
      START = 1
      cycle Get_request
   end if Need_input
   II = START-1 ! Save position pointer in case no keyword is found
   call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
   ! find next blank; if no more blanks, line is all characters
   if (TYPE == 100) STOPIT = Key_Buffer+1
   IT = MATCH(Three,NAMLEN,LENS,NAME,MINS)
   ! return codes are
   ! 0 - Potential table number (no match on other choices)
   ! 1 - 'ALL', 2 - 'QUIT', 3 - 'HELP'
   Check_request: select case (IT)
   case (0) Check_request     ! Potential table number, so
      STOPIT = II             ! restore the position pointer.
      call GETNUM (ERROR,XT)  ! Return codes are 0, 1, or 2.
      Analysis: select case (ERROR)
      case (0) Analysis ! entry was a valid number
         NTABL = int(XT)
         if (1 <= NTABL .and. NTABL <= 20) then  ! valid table number
            exit Get_request
         else                                    ! not a valid table entry;
                                                 ! inform user and ask again
            write(stdout,fmt='(/A)')&
               ' Exams generates 20 results tables.'
            STOPIT = 0
            START = 1
            INPUT = ' '
            cycle Get_request
         endif
      case (1) Analysis ! null input
         cycle Get_request
      case (2) Analysis ! invalid input (not a number), inform user
         write (stdout,fmt='(/A)')&
            ' Unable to interpret input; please try again.'
         STOPIT = 0
         START = 1
         INPUT = ' '
         cycle Get_request
      end select Analysis
   case (1) Check_request ! request to list ALL tables
      NTABL = 21
      exit Get_request
   case (2) Check_request ! Quit requested
      write (stdout,fmt='(/A)') ' LISTing terminated.'
      return
   case (3) Check_request ! HELP requested
      write (stdout,fmt='(//,20(A/),A)')&
      '   1 Chemical inputs: FATE Data',&
      '   2 Chemical inputs: PRODUCT Chemistry',&
      '   3 PULSE Chemical Loadings',&
      '   4 Environmental Input Data: BIOLOGICAL Parameters',&
      '   5 Environmental Input Data: HYDROLOGIC Parameters',&
      '   6 Environmental Input Data: SEDIMENT Properties',&
      '   7 Environmental Input Data: PHYSICAL GEOMETRY',&
      '   8 MISCellaneous Environmental Input Data: Wind, D.O., etc.',&
      '   9 Input specifications: ADVECTIVE transport field',&
      '  10 Input specifications: DISPERSIVE transport field',&
      '  11 Environmental Input Data: GLOBAL site parameters',&
      '  12 KINETIC PROFILE of Synthetic Chemical',&
      '  13 Chemical REACTIVITY PROFILE of Ecosystem',&
      '  14 Allochthonous Chemical LOADS and Pulses',&
      '  15 DISTRIBUTION of Chemical in Environment',&
      '  16 Chemical SPECIATION of Dissolved Concentrations',&
      '  17 Chemical Concentration MEANS, Maxima, and Minima',&
      '  18 Sensitivity Analysis of Chemical FATE',&
      '  19 Summary TIME-TRACE of Chemical Concentrations',&
      '  20 Exposure Analysis SUMMARY',&
      '  ALL Entire Report'
      STOPIT = 0 ! to force request for additional input
      START = 1
      INPUT = ' '
      cycle Get_request
   end select Check_request
end do Get_request

! User specifications are valid; list the data if it is available
call Assign_LUN (RPTLUN)
open (unit=RPTLUN,status='OLD', access='SEQUENTIAL', form='FORMATTED',&
      action='read', position='rewind', file='report.xms',iostat=IOerror)
if (IOerror /= 0) then  ! REPORT file has problems
   write (stdout,fmt='(/A)')&
      ' Error opening file "report.xms"; LIST command cancelled.'
   close (Unit=RPTLUN, iostat=IOerror)
   call Release_Lun (RPTLUN)
   return
endif
! If the PRINT command is being processed (SPOOL true), attachment to LUN
! "printr" was done in the EXAMS main program by assigning OUTLUN to PRINTR.
! Conversely, if the LIST command is being processed, OUTLUN has been
! assigned to "stdout".
if (Spool) then ! get the output file name from the user
   call Get_File_Name ('Print', Output_File, Success, 'PRINT')
   if (success) then
      if (.not. Append_Lines) then ! either user asked that existing file
                                   ! be replaced, or file doesn't exist.
                                   ! Writing to LUN "printr;" can't reassign.
        open (unit=OUTLUN, file=trim(Output_File), action='write',&
        status='REPLACE',access='SEQUENTIAL', form='FORMATTED',iostat=IOerror)
            if (IOerror /= 0 ) then
               write (stdout, fmt='(/A)')&
                  ' Error processing output. Print cancelled.'
               close (Unit=OUTLUN, iostat=IOerror)
               close (unit=RPTLUN, iostat=IOerror)
               call Release_LUN (RPTLUN)
               return
            end if
        ! test device integrity
        write (OUTLUN, fmt='(a1)', iostat=IOerror) ' '
            if (IOerror /= 0 ) then
               write (stdout, fmt='(/A)')&
                  ' Error processing output. Print cancelled.'
               close (Unit=OUTLUN, iostat=IOerror)
               close (unit=RPTLUN, iostat=IOerror)
               call Release_LUN (RPTLUN)
               return
            end if
      else
        open (unit=OUTLUN, file=trim(Output_File), action='write',&
              status='OLD',access='SEQUENTIAL', form='FORMATTED',&
              position='APPEND',iostat=IOerror)
            if (IOerror /= 0 ) then
               write (stderr, fmt='(/A)')&
                  ' Error opening output file. Print cancelled.'
               close (Unit=OUTLUN, iostat=IOerror)
               close (unit=RPTLUN, iostat=IOerror)
               call Release_LUN (RPTLUN)
               return
            else   ! write form feed
               write (OUTLUN, fmt='(a1)', iostat=IOerror) achar(12)
                  if (IOerror /= 0 ) then
                  write (stderr, fmt='(/A)')&
                  ' Error processing output. Print cancelled.'
                  close (Unit=OUTLUN, iostat=IOerror)
                  close (unit=RPTLUN, iostat=IOerror)
                  call Release_LUN (RPTLUN)
                  return
                  end if
            end if
      end if
   else
      return
   end if
endif

IS = 0

Wants_it_all: if (NTABL == 21) then ! list entire file
   All_tables: do
      call INREC (EOF,RPTLUN)
      if (EOF == 1) then ! all tables (whole file) written
         call Closer; return
      end if
      KNT = KNT+1
      if (len_trim(INPUT) == 0) then ! write blank line
         write (OUTLUN,fmt=*)
      else
         write (OUTLUN,fmt='(A)') ' '//trim(INPUT(2:))
      endif
   end do All_tables
endif Wants_it_all

! A single table was requested. Always save the last 4 records that are input.
! These are the header records to be listed if the specified table is found.
call INREC (EOF,RPTLUN)
   if (EOF == 1) then; call Closer; return; end if

KNT = KNT+1

One_table: Do
   IS = IS+1 ! save the record
   if (IS == 5) IS = 1
   HOLD(IS) = INPUT
   if (INPUT(2:7) /= TABID(2:7) .or. INPUT(8:9) /= SUFFIX(NTABL)) then
      call INREC (EOF,RPTLUN) ! Don't have the table
         if (EOF == 1) then
            call Closer; exit One_table
         endif
      KNT = KNT+1
      cycle One_table
   endif
   ! found it
   More_tables: if (REPEAT /= 0 .and. .not.Spool) then
      Query: do
         write (stdout,fmt='(A)',advance='NO')&
            ' More? (Yes/No/Quit)-> '
         call INREC (EOF,stdin)
            if (EOF == 1) then
               write (stdout,fmt='(/A)') ' LISTing terminated.'
               call Closer; exit One_table
            end if
         START = IMBED(INPUT,Zero)
         if (START == -999) exit Query ! treat null input as yes...
         Response: select case (INPUT(START:START))
         case ('Q', 'q') Response ! Quit requested
            write (stdout,fmt='(/A)') ' LISTing terminated.'
            call Closer; exit One_table
         case ('N', 'n') Response ! go back for a possible additional instance
            call INREC (EOF,RPTLUN)              ! of this table
               if (EOF == 1) then
                  call Closer; exit One_table
               end if
            KNT = KNT+1
            cycle One_table
         case ('Y', 'y') Response
            exit Query
         case default Response
            write (stdout,fmt='(/A)')& ! invalid response
               ' Response was not understood; Please try again.'
            cycle Query
         end select Response
      end do Query
   end if More_tables

   ! List the last few records. Increment the buffer pointer.
   IS = IS+1
   if (IS == 5) IS = 1
   List_4_lines: do J = 1, 4
      INPUT = HOLD(IS)
      if (len_trim(INPUT) == 0) then ! write blank line
         write (OUTLUN,fmt=*)
      else
         write (OUTLUN,fmt='(1X,A)') trim(INPUT(2:))
      endif
      IS = IS+1
      if (IS == 5) IS = 1
   end do List_4_lines

   List_more_lines: do
      call INREC (EOF,RPTLUN)
      if (EOF == 1) then ! all done...
         call Closer
         exit One_table
         end if
      KNT = KNT+1
      if (INPUT(1:1) == '1') then ! found mark for next table
         if (Spool) write (OUTLUN, fmt='(a1)') achar(12)   ! write form feed
         exit List_more_lines
      end if
      if (len_trim(INPUT) == 0) then ! write blank line
         write (OUTLUN,fmt=*)
      else
         write (OUTLUN,fmt='(1X,A)') trim(INPUT(2:))
      endif
   end do List_more_lines

   REPEAT = 1
   IS = 0
end do One_table

return

contains
Subroutine Closer ! processing complete
Implicit None
Results: if (KNT == 0) then ! no results
   write (stdout,fmt='(//A)') ' No records found in the report file.'
else Results                          ! records have been written, so
   Printed: if (Spool) then   ! if processing a print command...
      if (Append_Lines) then
         Particle = 'appended'
      else
         Particle = 'written'
      end if
      write (stdout,fmt='(/A)') ' Requested report has been '&
      //trim(Particle)//' to "'//trim(Output_File)//'".'
      close (unit=OUTLUN,iostat=IOError)
   end if Printed
end if Results

close (unit=RPTLUN,iostat=IOError)
call Release_LUN (RPTLUN)
end Subroutine Closer

end Subroutine LIST
