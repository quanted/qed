Module SetValue ! facilities to set the values of variables
use Alias_Transfer
use Floating_Point_Comparisons
use Global_Variables
use Implementation_Control
use Initial_Sizes
use Input_Output
use Internal_Parameters
use Local_Working_Space
use Model_Parameters
use MultiScan
use getarg_mod
character(len=1), dimension(1), parameter :: BLANK=' '
integer :: File_Check ! for testing for I/O errors
integer :: LoadLUN, ChemStop
integer :: CHELUN
logical :: All_Done, Problem
! "All_Done" halts processing when data will actually come from
!   an external file (e.g., TOMS ozone data)
! "Problem" signals problems with file I/O in other routines
contains
Subroutine MODIFY(IT,Y)
! Purpose--to provide a means of dynamically modifying variables in EXAMS.
! If the expression is not found on the current line, a prompt is presented.
! Revised 27-DEC-85 (LAB)
! Revised 10/20/88 (LAB)--run-time formats for implementation-
! dependent cursor control.
! Revision of help text 10/24/88
! Revision of interface to XVALUE 1/22/96
! Converted to Fortran90 2/20/96 et seq.
! Revisions for dynamic memory allocation February 2001
! Revised 07/23/2001 to control values of abser and reler
! Revised 2004-05-17 to add QTBTWG and QTBTSG
! Error returns
! -3 * common group not found
! -2 * invalid name
! -1 * E-O-F (end of file)
!  0 * O.K.
!  1 * null input
!  2 * imbedded blank, system error
!  3 * subscript out-of-range
!  4 * invalid number of arguments
!  5 * invalid subscript
!  6 * common name specified
!  7 * scalars cannot have arguments
!  8 * null argument
!  9 * no "TO" specified
! 10 * invalid quantity to right of = mark
Implicit None
real (kind(0D0)) :: Y(:,:) ! Y(KOUNT,KCHEM)
real :: ARGS(10), VAL
integer :: LOW1, LOW2, LOW3, UP1, UP2, UP3, NULL, EOF,&
   LOWUP(6), NARGS, K, I, INDX, MATCH, ITM1, ITDTD
integer, intent (out) :: IT
character(len=1) :: TEMP
character(len=1), dimension(3), parameter :: DELIM = (/' ' , '(' , '='/)
logical :: NOTNUM
All_Done = .false.
NARGS = 0
call READSP ! Get system parameter information
NULL = 0
IT = 0
START = STOPIT+1
Query_one: do
   Tab_out: do ! convert horizontal tabs in the input line to blanks
     K = index(INPUT,achar(09))
     if (K==0) exit
     INPUT(K:K) = " "
   end do Tab_out
               K=index(INPUT(START:),' TO ') ! Allow for alternative syntax of
   if (K == 0) K=index(INPUT(START:),' to ') ! the modify/change/set command,
   if (K == 0) K=index(INPUT(START:),' To ') ! i.e., either "SET PH(*)=7.2"
   if (K == 0) K=index(INPUT(START:),' tO ') !       or     "SET PH(*) TO 7.2"
   if (K /= 0) then                            ! Alter " TO " (etc.) to "=   "
     I = START+K-1; INPUT(I:I+3) = '=   '
   end if
   K = START-1
   Blank_out: do I = START, len(INPUT) ! Remove all blanks from the input line
      TEMP = INPUT(I:I)
      if (TEMP == ' ') cycle Blank_out
      K = K+1
      INPUT(K:K) = INPUT(I:I)
   end do Blank_out
   if (K == len(INPUT)) exit Query_one
   if (K /= START-1) then ! additional input present
      K = K+1
      INPUT(K:) = ' ' ! blank remainder of line
      exit Query_one
   end if
   NULL = NULL+1 ! Null input, count number of occurrences
   IT = 1
   if (NULL > 1) return
   ! Prompt for input
   write (stderr,fmt='(/A/A/A)',advance='NO')&
      ' Sytax is "CHANGE <name of variable> TO <new value>"',&
      '       or    "SET <name of variable>  = <new value>"',&
      ' Enter name=value command-> '
   call INREC (EOF,stdin)
   IT = -1
   if (EOF == 1) return
   START = 1
end do Query_one
! Ready to decipher, search for variable name.
! Valid delimiters are blank, '(', and '='.
call SKAN (INPUT,START,STOPIT,TYPE,DELIM)
! If a blank was encountered, input is insufficient to process
IT = 2
if (TYPE == 1) return
! See if a valid name of variable.
INDX = MATCH(NOMOD,LNMODS,MODLEN,MODS,MODMIN)
IT = -2
! If name not identified, quit
if (INDX == 0) return
! See if 'LABELED COMMON NAME' specified
IT = 6
if (TD(INDX) == 0) return
! '=' ?
if (TYPE /= 3) then ! '(' encountered.
   ! determine if the "variable name" has been defined to be a scalar.
   IT = 7
   if (TS(INDX) == 1) return
   ! No, a '(', so get any and all arguments
   ITM1 = TS(INDX)-1
   call GETARG (NARGS,ARGS,IT,ITM1)
   if (IT /= 0) return
   START = STOPIT+1
   IT = 9
   if (INPUT(START:START) /= DELIM(3)) return
   STOPIT = START
end if
! Test for a subscripted variable w/o specified subscripts
IT = 4
if (TS(INDX)-1 /= NARGS) return
START = STOPIT+1
Query_two: do
   IT = 0
   call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
   if (TYPE == 0) STOPIT = Key_Buffer+1
   if (START /= STOPIT) exit Query_two
   ! no input, prompt
   write (stderr,fmt='(A)',advance='NO') '  Enter value-> '
   call INREC (EOF,stdin)
   IT = -1
   if (EOF == 1) return
   START = 1
end do Query_two
VAL = 0.0
if(TD(INDX) /= 5) call XVALUE(INPUT(START:(STOPIT-1)),STOPIT-START,VAL,NOTNUM)
! Valid numeric quantity?
IT = 10
if (NOTNUM) return
call CHKSUB (ARGS,INDX,LOWUP,IT) ! Validate subscript ranges
if (IT /= 0) return
LOW1 = LOWUP(1)
LOW2 = LOWUP(2)
LOW3 = LOWUP(3)
UP1 = LOWUP(4)
UP2 = LOWUP(5)
UP3 = LOWUP(6)
RDWR = 0
ITDTD = TD(INDX)
Data_put: do ICL1 = LOW1, UP1; do ICL2 = LOW2, UP2; do ICL3 = LOW3, UP3
   Data_Type: select case (ITDTD)
   case (1) Data_Type !-complex
      write (stderr,fmt='(/A)')&
         ' Complex data indicated. Not implemented.'
      exit Data_put
   case (2) Data_Type !-high precision or real (kind (0D0)) (real*8)
      R8 = VAL; call PUTVAR(Y); if (All_Done) exit Data_put
   case (3) Data_Type !-real
      R4 = VAL; call PUTVAR(Y); if (All_Done) exit Data_put
   case (4) Data_Type !-integer
      I2 = VAL; call PUTVAR(Y); if (All_Done) exit Data_put
   case (5) Data_Type !-character
      L1 = trim(INPUT(START:)); call PUTVAR(Y)
   end select Data_Type
end do; end do; end do Data_put
return
end Subroutine MODIFY

subroutine PUTVAR(Y)
! 03-MAY-1985 -- L.A. Burns
! Revised 21/08/1985, 25/08/87 (LAB)
! Revised 10/21/88--run-time implementation of machine dependencies
! Revised 12/13/1988 to default TCODE to 2 when MODE is set to 3
! Revised 03/13/91 to trap bad values of CLOUDiness
! Revised 08/03/91 to trap bad values of MONTHG
! Revised 08/05/91 to trap bad values of MODEG
! Revised 09/14/91 to add PRBENG
! Revised 11/24/98 to correct concentrations when compartment geometry altered
! Revised 2002-04-19 to process EventD and OutFil
Implicit None
real (kind(0D0)) :: Y(KOUNT,KCHEM)
integer :: Check_value, Letter_Case, I
logical :: Found_It ! to check on existence of files
character (len=3) :: ChemCode(KCHEM)
do i=1,kchem
   ChemCode(I)='QQQ'
end do
Groups: select case (ICOM)
case (1) Groups ! Parameter Group: NAMEG
   select case (IVAR)
      case (1); CHEMNA(ICL1) = L1
      case (2); ECONAM = L1
      case (3); LOADNM = L1
      case (4); PRODNM = L1
      case (5) ! set a compartment type; modification to basic geometry
        IRUN = 0 ! prevent "continue" until "run" has been executed
        Check_Value = scan (trim(L1), Permitted_Compartment_Types)
        if (Check_Value == 0) then
          write (stderr, fmt='(/A,I0,/A/A)')&
          ' Error: Compartment number ',ICL1, &
          ' was coded as TYPE "'//trim(L1)//&
          '".',' Enter "Help TYPE" for assistance.'
       else ! proper compartment type, if necessary convert to upper case
         TYPEG(ICL1) = trim(L1)
         Letter_Case = iachar(TYPEG(ICL1))
         if (Letter_Case > 96 .and. Letter_Case < 123) & ! lower case letter,
         TYPEG(ICL1) = achar (Letter_Case - 32)          ! convert to capital
       end if
      case (6)
        Check_Value = scan (trim(L1), Permitted_Air_Mass_Types)
        if (Check_Value == 0) then
          write (stderr, fmt='(/A,I0,/A)')&
          ' Error: Air Mass Type for month ',ICL1,&
          ' was coded as "'//trim(L1)//&
          '". Enter "Help AIRTY" for assistance.'
       else ! proper Air Mass type, if necessary convert to upper case
         AIRTYG(ICL1) = trim(L1)
         Letter_Case = iachar(AIRTYG(ICL1))
         if (Letter_Case > 96 .and. Letter_Case < 123) & ! lower case letter,
         AIRTYG(ICL1) = achar (Letter_Case - 32)          ! convert to capital
       end if
   end select
case (2) Groups ! Parameter Group: CONTRG
   select case (IVAR)
      case (1)
         FIXFIL = I2
!         if (FIXFIL /= 0) then ! restore values from files
!            ! First make sure results files exist
!                          Inquire (File = 'report.xms',   exist = Found_It)
!            if (Found_It) Inquire (File = 'ssout.plt',    exist = Found_It)
!            if (Found_It) Inquire (File = 'kinout.plt',   exist = Found_It)
!            if (Found_It) Inquire (File = 'fgetscmd.xms', exist = Found_It)
!            if (Found_It) Inquire (File = 'fgetsexp.xms', exist = Found_It)
!            if (Found_It) Inquire (File = 'bassexp.xms',  exist = Found_It)
!            if (.not. Found_it) then
!               write (stderr, fmt='(2(/A))')&
!               ' One or more of the results files is missing.',&
!               ' Exams must be RUN before results can be displayed.'
!               FIXFIL = 0
!               return
!            end if
!            call Assign_LUN (PLTLUN)
!            open (unit=PLTLUN, status='OLD', access='SEQUENTIAL', form=&
!                  'UNFORMATTED', position='rewind', file='ssout.plt',&
!                  action='read', iostat=Check_value)
!            if (Check_value /= 0) then
!               write (stderr, fmt='(A)')&
!                  ' Error opening results file.',&
!                  ' You must RUN Exams before results can be accessed.'
!               FIXFIL = 0
!            else
!               read (PLTLUN,iostat=Check_value) KCHEM, MODEG, KOUNT
!               if (Check_value == 0) then
!                  if (echo) write (stdout,fmt='(/,3(/,A,I0),/)')&
!                     ' Number of chemicals: ',KCHEM,&
!                     ' Simulation Mode:     ',MODEG,&
!                     ' Number of segments:  ',KOUNT
!                  FIXFIL = 1; if (MODEG == 3) TCODEG = 2
!                  close (Unit=PLTLUN,iostat=File_Check)
!               else ! problem reading plot file
!                  write (stderr, fmt='(A)')&
!                     ' Error reading results file.',&
!                     ' You must RUN Exams before results can be accessed.'
!                  FIXFIL = 0
!               end if
!            end if
!            call Release_LUN (PLTLUN)
!         end if
      case (2); IUNITG = I2
      case (3)
         if (I2 < 1 .or. I2 > KCHEM) then
            write (stderr,fmt='(/A/A,I0,A/A,I0,A,I0,A)')&
               ' MCHEM cannot be negative, zero or greater than the',&
               ' current value of KCHEM (now set at ',KCHEM,'). MCHEM',&
               ' has not been set to ',I2,'; it is still = ',MCHEMG,'.'
         else
            MCHEMG = I2
         endif
      case (4) ! changing the number of chemicals; 
               ! needs new allocate for Y and for chemical data spaces
         if (KCHEM==I2) then ! no action required
            if (ECHO) write (stdout,fmt='(A,I0,A)') &
               ' KCHEM is already ',KCHEM,'.'
            return
         elseif (KCHEM <= 0) then
            write (stderr,fmt='(A,I0,A)')&
              ' KCHEM must be a positive integer, not ',I2,'.'
            return
         end if
         ! Save the current chemical data. If the number of chemicals
         ! is being increased, all the data are stored and then recovered.
         ! If the number of chemicals is being decreased, only the data
         ! needed for the new structure is transferred.
         ! First, establish logical unit number and file name for
         ! save/restore of current chemical data
         if (I2> KCHEM) then ! increase in number of chemicals, save all
            ChemStop=KCHEM
         else ! decrease in number of chemicals, only save those needed
            ChemStop=I2
         end if
         ! store current chemical data for restoration to new structure
         call Assign_LUN (CHELUN)
         open (unit=CHELUN, status='SCRATCH', access='SEQUENTIAL',&
            action='readwrite', form='FORMATTED', position='rewind',&
            iostat=File_Check)
         if (File_Check /= 0) then
            write (stderr,fmt='(/A)')&
            ' Error opening data transfer file; KCHEM was not altered.'
            return
            endif
         do MCHEMG = 1, ChemStop
            call CHMOUT(CHELUN)
         end do
         ! Save the loadings
         call Assign_LUN (LoadLUN)
         open (unit=LoadLUN, status='SCRATCH', access='SEQUENTIAL',&
            action='readwrite', form='FORMATTED', position='rewind',&
            iostat=File_Check)
         if (File_Check /= 0) then
            write (stderr,fmt='(/A)')&
            ' Error opening disk file; KCHEM was not altered.'
            return
         endif
         call LOADOUT(LoadLUN,Problem,KOUNT,ChemStop)
         if (Problem) then
            write (stderr,fmt='(/A)')&
               ' Error processing disk file; KCHEM was not altered.'
            return
         end if

         call Allocate_Storage(1,KOUNT,I2) ! rework chemical data storage

         KCHEM = I2
         ! Initialize the new load struture
         call initl(4)
         ! Recall the load data into the new structure
         Rewind LoadLUN
         call LOADIN(LoadLUN,Problem,KOUNT,ChemStop)
         if (Problem) then
            call INITL(4) ! to zero the loads
            write (stderr,fmt='(A/A)') ' Warning: Loads were reset',&
            &' because the prior loads could not be recovered.'
         end if
         close (LoadLUN)
         call Release_LUN(LoadLUN)

         ! Initialize the new chemical structure
         do MCHEMG=1,KCHEM
            call initl(2)
         end do
         ! retrieve the current chemical data into the new structure
         Rewind CHELUN
         do MCHEMG = 1, ChemStop
            call CHEMIN(ChemCode(1),CHELUN)
         end do
         ! Close the file and release the LUN
         close (unit=CHELUN,iostat=Check_value)
         call Release_LUN (CHELUN)
         MCHEMG=1   ! safety measure
         IRUN = 0   ! prevent "continue" until "run" has been executed
         FIXFIL = 0 ! prevent invocation of plot routines
         if (echo) write (stdout,fmt='(/A,I0,A)')&
            ' Number of chemicals is now ',KCHEM,'.'
      case (5) ! setting operation mode
         if (I2  > 0 .and. I2  <=  3) then
            MODEG = I2
            IRUN =  0         ! Prevent CONTINUE until a new RUN
            IFLAG = 0
            TINITG = 0.0D+00  ! Set default values for time
            TENDG  = 1.0D+00
            CINTG  = 1.0D+00
            if (MODEG == 3) then
               PRSWG = 0  ! Mode 3 produces daily output, which is by default
               TCODEG = 2 ! numbered sequentially by days, thus...
               YEAR1G = 2000
               NYEARG = 1
            else
               PRSWG = 1
               MONTHG=13
            endif
         else
            write (stderr,fmt='(4(/A),//A)')&
               ' EXAMS has three operational modes--',&
               '    Mode 1 -- steady-state analyses',&
               '    Mode 2 -- initial value problems',&
               '    Mode 3 -- dynamics over annual cycles',&
               ' MODE has not been altered.'
         endif
      case (6)
         PRSWG = I2
      case (7) ! set the "month" to be used
         if (I2  > 0 .and. I2  <=  13) then
            MONTHG = I2
         else
            write (stderr,fmt='(A/A)')&
            ' Set "month" to a number between 1 and 12 for calendar months,',&
            ' or to 13 for average values. "Month" has not been altered.'
         endif
      case (8)
            if (I2<1 .or. I2>6999) then
               NYEARG = 1
               write (stderr,fmt='(/A/A/)')&
                  ' Error: NYEAR must not be <1 or >6999.',&
                  ' NYEAR has been reset to 1.'
            else
               NYEARG = I2
            end if
      case (9)
         YEAR1G = I2
         if (MODEG == 3) then  ! Because YEAR1 is used in timer computations,
            IRUN = 0           ! prevent CONTINUE until a new RUN...
            IFLAG = 0
         endif
      case (10)
         if (0 < I2 .and. I2 < 5) then
            TCODEG = I2
            ! In mode 3, output is daily, encoded in days ONLY to simplify
            ! post-processing routines.  Thus, prevent alteration by user...
            if (MODEG == 3) then
               TCODEG=2
               write (stderr,fmt='(/A)') &
                  ' TCODE cannot be changed in Mode 3.',&
                  ' The output interval is fixed as Days',&
                  " for use by Exams' data analysis subroutines."
            end if
            IRUN = 0
            IFLAG = 0
         else
            write (stderr,fmt='(/A)')&
               ' TCODE must be 1, 2, 3, or 4. Command cancelled.'
         endif
      case (11) ! Communications interval
         if (R4 .LessThanOrEqual. 0.0) then
            write(stderr,fmt='(A)')&
            ' Error: CINT must be a positive integer and not zero.'
         elseif (R4 .GreaterThan. 6999.0) then
            CINTG = 1.0D+00
            write(stderr,fmt='(/A/A/)')&
            ' Error: CINT must be less than 7,000.',&
            ' CINT has been reset to 1.'
         else
            CINTG = dble(ceiling(R4))
            if ((mod(R4,1.0)) .NotEqual. (0.0)) then
               write(stderr,fmt='(A,I0)')&
                  ' Error: CINT must be a positive integer; CINT now = ',&
                  ceiling(R4)
            end if
         end if
      case (12)
         if (R4 .LessThanOrEqual. 0.0) then
            write(stderr,fmt='(A)')&
            ' Error: TEND must be a positive integer and not zero.'
         elseif (R4 .GreaterThan. 999999.0) then
            write(stderr,fmt='(/A/A/)')&
            ' Error: TEND must be less than 1,000,000.',&
            ' TEND has not been changed.'
            if (TCODEG<4) write (stderr,fmt='(/A/A/)')&
            ' Consider changing the time frame of the analysis',&
            ' by increasing the value of TCODE.'
         else
            TENDG = dble(ceiling(R4))
            if ((mod(R4,1.0)) .NotEqual. (0.0)) then
               write(stderr,fmt='(A,I0)')&
                  ' Error: TEND must be a positive integer; TEND now = ',&
                  ceiling(R4)
            end if
            IRUN = 0
            IFLAG = 0
         end if
      case (13)
         if (R4 .LessThan. 0.0) then
            TINITG=0.0D+00
            write(stderr,fmt='(/A/A/)')&
            ' Error: TINIT must be a positive integer or zero.',&
            ' TINIT has been reset to 0.'
         elseif (R4 .GreaterThan. 999998.0) then
            TINITG = 0.0D+00
            write(stderr,fmt='(/A/A/)')&
            ' Error: TINIT must be less than 999,998.',&
            ' TINIT has been reset to 0.'
         else
            TINITG = dble(floor(R4))
            if ((mod(R4,1.0)) .NotEqual. (0.0)) then
               write(stderr,fmt='(A,I0)')&
               ' Error: TINIT must be a positive integer; TINIT now = ',&
                  int(TINITG)
            end if
         ! Preserve value for restoration between RUN/CONTINUE commands
         TINITL = TINITG
         end if
      case (14)
         if (R4 .LessThanOrEqual. 0.0) then
            write (stderr,fmt='(a/a)')&
            ' Error controls cannot be zero or negative.',&
            '  ABSER was not altered.'
         elseif (R4 .LessThan. (max(FOURU, 1.e-15))) then
            write (stderr,fmt='(a,es10.3,/a)')&
            ' ABSER cannot be less than',max(FOURU, 1.e-15),&
            '  ABSER was not altered.'
         else
            ABSERG = R4
         end if
      case (15)
         if (R4 .LessThanOrEqual. 0.0) then
            write (stderr,fmt='(a/a)')&
            ' Error controls cannot be zero or negative.',&
            '  RELER was not altered.'
         elseif (R4 .LessThan. (max(FOURU, 1.e-11))) then
            write (stderr,fmt='(a,es10.3,/a)')&
            ' RELER cannot be less than',max(FOURU, 1.e-11),&
            '  RELER was not altered.'
         else
            RELERG = R4
         end if
      case (16) ! user-selectable event durations
         IRUN = 0 ! prevent "continue" until "run" has been executed
                  ! (otherwise the output gets hopelessly scrambled)
         if (I2 == 0) then
            if (echo) write (stdout,fmt='(/A,I0,A)')&
            ' Event Duration Number ', ICL1,' has been disabled.'
            EventD(ICL1) = 0
         elseif (I2<1 .or. I2>364) then
            write (stderr,fmt='(/A/A,I0,A/A,I0,A)')&
            ' Event durations must be between 1 and 364 days.',&
            ' The request for ',I2,' has not been executed.',&
            ' Event Duration Number ', ICL1,' has been disabled.'
            EventD(ICL1) = 0
         else
            EventD(ICL1) = I2
            if (echo) write (stdout,fmt='(/A,I0,A,I0,A)')&
            ' Event Duration Number ',ICL1,' has been set to ',I2,' days.'
         end if
      case (17)  ! user-selection of output files
         ! Convert input to upper case (to maintain consistent view in SHOW)
         Letter_Case = iachar(L1(1:1))
         if (Letter_Case > 96 .and. Letter_Case < 123) & ! lower case letter,
         L1(1:1) = achar (Letter_Case - 32)              ! convert to capital
         Check_Value = scan ("YN", L1(1:1))
         WhichFile: select case (Check_Value)
           case default ! neither yes nor no...
              write (stderr,fmt='(A/A,I0,A)')&
                   ' Files are selected by SETting OutFil to "Yes" or "No."'&
                  ,' OutFil(',ICL1,') was not altered.'
              return
           case (1) ! Yes, produce the file
             OutFil(ICL1) = L1
             Produce: Select case (ICL1)
               case (1);  RPTFIL = .true.  ! produce report.xms
               case (2);  PLTFIL = .true.  ! produce ssout.plt; kinout.plt
               case (3);  BASFIL = .true.  ! produce bassexp.xms
               case (4);  FGTFIL = .true.  ! produce fgetscmd.xms;fgetsexp.xms
               case (5);  HWRFIL = .true.  ! produce HWIREx.xms
               case (6);  TOXFILC = .true. ! produce EcoToxC.xms
               case (7);  RSKFILC = .true. ! produce EcoRiskC.xms
               case (8);  TOXFILR = .true. ! produce EcoToxR.xms
               case (9);  RSKFILR = .true. ! produce EcoRiskR.xms
               case (10); FULFIL = .true.  ! produce FullOut.xms
               case default 
             end select Produce
           case (2) ! No, do not produce the file
             OutFil(ICL1) = L1
             NoProduct: Select case (ICL1)
!              case (1);  RPTFIL  = .false. ! do not make report.xms
               case (1);  RPTFIL  = .true.  ! prevent-needed for error control
               case (2);  PLTFIL  = .false. ! do not make ssout & kinout
               case (3);  BASFIL  = .false. ! do not make bassexp.xms
               case (4);  FGTFIL  = .false. ! do not make fgetscmd & fgetsexp
               case (5);  HWRFIL  = .false. ! do not make HWIREx.xms
               case (6);  TOXFILC = .false. ! do not make EcoToxC.xms
               case (7);  RSKFILC = .false. ! do not make EcoRiskC.xms
               case (8);  TOXFILR = .false. ! do not make EcoToxR.xms
               case (9);  RSKFILR = .false. ! do not make EcoRiskR.xms
               case (10); FULFIL  = .false. ! do not make FullOut.xms
             end select Noproduct
         end select WhichFile
      end select
case (3) Groups ! Parameter Group: PCHEMG
   IRUN = 0 ! prevent "continue" command from executing
   select case (IVAR)
      case (1)
         if (I2 /= 0 .and. I2 /= 1) then
          write (stderr,fmt='(/A/A)')&
          ' SPFLGs can only be set to "1" (exists) or "0" (does not exist).',&
          ' The request has not been executed.'
         else
            SPFLGG(ICL1,ICL2) = I2
         end if
      case (2); MWTG(ICL1) = R4
      case (3); SOLG(ICL1,ICL2) = R4
      case (4); ESOLG(ICL1,ICL2) = R4
      case (5); PKG(ICL1,ICL2) = R4
      case (6); EPKG(ICL1,ICL2) = R4
   end select
case (4) Groups ! Parameter Group: PARTG
   IRUN = 0 ! prevent "continue" command from executing
   select case (IVAR)
      case (1); KOCG(ICL1) = R4
      case (2); KOWG(ICL1) = R4
      case (3); KPBG(ICL1,ICL2) = R4
      case (4); KPDOCG(ICL1,ICL2) = R4
      case (5); KPSG(ICL1,ICL2) = R4
      case (6); KIECG(ICL1,ICL2) = R4
   end select
case (5) Groups ! Parameter Group: VOLATG
   IRUN = 0 ! prevent "continue" command from executing
   select case (IVAR)
      case (1)
         if (R4 .GreaterThanOrEqual. -273.15) then
            MPG(ICL1) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2,A)') &
               ' Error in data specification: MP below absolute zero.',&
               ' Melting Point remains ', MPG(ICL1),' degrees C.'
         end if
      case (2)
         if (R4 .GreaterThanOrEqual. 0.0) then
            HENRYG(ICL1) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2,A)') &
               ' Error in data specification: HENRY cannot be negative.',&
               " Henry's Law constant remains ", HENRYG(ICL1),' atm-m3/mole.'
         end if
      case (3)
         if (R4 .GreaterThanOrEqual. 0.0) then
            EHENG(ICL1) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2,A)') &
               ' Error in data specification: EHEN cannot be negative.',&
               " Henry's Law enthalpy remains ", EHENG(ICL1),' kcal/mol.'
         end if
      case (4)
         if (R4 .GreaterThanOrEqual. 0.0) then
            VAPRG(ICL1) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2,A)') &
               ' Error in data specification: VAPR cannot be negative.',&
               ' Vapor pressure remains ', VAPRG(ICL1),' Torr.'
         end if
      case (5)
         if (R4 .GreaterThanOrEqual. 0.0) then
            EVPRG(ICL1) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2,A)') &
              ' Error in data specification: EVPR cannot be negative. Molar',&
              ' heat of vaporization remains', EVPRG(ICL1),' kcal/mole.'
         end if
   end select
case (6) Groups ! Parameter Group: DPHOTG
   IRUN = 0 ! prevent "continue" command from executing
   select case (IVAR)
      case (1) ! photochemical quantum yield
         if (R4 .LessThan. 0.0) then
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: Qyield cannot be negative.',&
               ' Qyield remains ', Qyield(ICL1,ICL2,ICL3)
         else
            Qyield(ICL1,ICL2,ICL3) = R4
         end if
      case (2) ! lumped photochemical rate constant
         if (R4 .LessThan. 0.0) then
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: KDP cannot be negative.',&
               ' KDP remains ', KDPG(ICL1,ICL2)
         else
            KDPG(ICL1,ICL2) = R4
         end if
      case (3); RFLATG(ICL1,ICL2) = R4
      case (4); ABSORG(ICL1,ICL2,ICL3) = R4
      case (5); LAMAXG(ICL1,ICL2) = R4
   end select
case (7) Groups ! Parameter Group: HYDROG
   IRUN = 0 ! prevent "continue" command from executing
   select case (IVAR)
      case (1) ! Specific-acid-catalyzed hydrolysis
         if (R4 .LessThan. 0.0) then
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: KAH cannot be negative.',&
               ' KAH remains ', KAHG(ICL1,ICL2,ICL3)
         else
            KAHG(ICL1,ICL2,ICL3) = R4
         end if
      case (2); EAHG(ICL1,ICL2,ICL3) = R4
      case (3) ! Neutral hydrolysis (first order as water is 55M)
         if (R4 .LessThan. 0.0) then
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: KNH cannot be negative.',&
               ' KNH remains ', KNHG(ICL1,ICL2,ICL3)
         else
            KNHG(ICL1,ICL2,ICL3) = R4
         end if
      case (4); ENHG(ICL1,ICL2,ICL3) = R4
      case (5) ! specific-base-catalyzed hydrolysis
         if (R4 .LessThan. 0.0) then
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: KBH cannot be negative.',&
               ' KBH remains ', KBHG(ICL1,ICL2,ICL3)
         else
            KBHG(ICL1,ICL2,ICL3) = R4
         end if
      case (6); EBHG(ICL1,ICL2,ICL3) = R4
   end select
case (8) Groups ! Parameter Group: REDOXG
   IRUN = 0 ! prevent "continue" command from executing
   select case (IVAR)
      case (1) ! oxidation
         if (R4 .LessThan. 0.0) then
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: KOX cannot be negative.',&
               ' KOX remains ', KOXG(ICL1,ICL2,ICL3)
         else
            KOXG(ICL1,ICL2,ICL3) = R4
         end if
      case (2); EOXG(ICL1,ICL2,ICL3) = R4
      case (3) ! singlet oxygen
         if (R4 .LessThan. 0.0) then
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: K1O2 cannot be negative.',&
               ' K1O2 remains ', K1O2G(ICL1,ICL2,ICL3)
         else
            K1O2G(ICL1,ICL2,ICL3) = R4
         end if
      case (4); EK1O2G(ICL1,ICL2,ICL3) = R4
      case (5) ! reduction
         if (R4 .LessThan. 0.0) then
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: KRED cannot be negative.',&
               ' KRED remains ', KREDG(ICL1,ICL2,ICL3)
         else
            KREDG(ICL1,ICL2,ICL3) = R4
         end if
      case (6); EREDG(ICL1,ICL2,ICL3) = R4
   end select
case (9) Groups ! Parameter Group: BIOLYG
   IRUN = 0 ! prevent "continue" command from executing
   select case (IVAR)
      case (1)
         if (R4 .GreaterThanOrEqual. 0.0) then
            KBACWG(ICL1,ICL2,ICL3) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: KBACW cannot be negative.',&
               ' KBACW remains ', KBACWG(ICL1,ICL2,ICL3)
         end if
      case (2)
         if (R4 .GreaterThanOrEqual. 0.0) then
            QTBAWG(ICL1,ICL2,ICL3) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: QTBAW cannot be negative.',&
               ' QTBAW remains ', QTBAWG(ICL1,ICL2,ICL3)
         end if
      case (3)
         if (R4 .GreaterThanOrEqual. 0.0) then
            KBACSG(ICL1,ICL2,ICL3) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: KBACS cannot be negative.',&
               ' KBACS remains ', KBACSG(ICL1,ICL2,ICL3)
         end if
      case (4)
         if (R4 .GreaterThanOrEqual. 0.0) then
            QTBASG(ICL1,ICL2,ICL3) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: QTBAS cannot be negative.',&
               ' QTBAS remains ', QTBASG(ICL1,ICL2,ICL3)
         end if
      case (5)
         if ((R4 .GreaterThan. 0.0) .and. (R4 .LessThan. 100.0) ) then
            QTBTWG(ICL1,ICL2,ICL3) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: QTBTW must be between',&
               ' 0 and 100 C. QTBTW remains ', QTBTWG(ICL1,ICL2,ICL3)
         end if
      case (6)
         if ((R4 .GreaterThan. 0.0) .and. (R4 .LessThan. 100.0) ) then
            QTBTSG(ICL1,ICL2,ICL3) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: QTBTS must be between.',&
               ' 0 and 100C. QTBTS remains ', QTBTSG(ICL1,ICL2,ICL3)
         end if
      case (7)
         if (R4 .GreaterThanOrEqual. 0.0) then
            AerMet(ICL1) = R4
         else
            write (stderr,fmt='(/A/A/A,ES10.3E2)') &
               ' Error in data specification: aquatic aerobic metabolism',&
               ' halflife "AerMet" (days) cannot be negative.',&
               ' AerMet remains ', AerMet(ICL1)
         end if
      case (8)
         if (R4 .GreaterThanOrEqual. 0.0) then
            AnaerM(ICL1) = R4
         else
            write (stderr,fmt='(/A/A/A,ES10.3E2)') &
               ' Error in data specification: aquatic anaerobic metabolism',&
               ' halflife "AnaerM" (days) cannot be negative.',&
               ' AnaerM remains ', AnaerM(ICL1)
         end if
   end select
case (10) Groups ! Parameter Group: TRPORT
if (I2 < 0) then
   write (stderr,fmt='(/A/A)')&
      ' Negative entries have no meaning here.',&
      ' No changes have been made.'
else
   select case (IVAR)
      case (1) ! changing structure of environment (KOUNT)
               ! needs new allocate for "Y" and for environmental data spaces
         if (KOUNT==I2) then ! no action required
            if (echo) write (stdout,fmt='(A,I0,A)')&
                 ' KOUNT is already ',KOUNT,'.'
            return
         elseif (I2 <= 0) then
            write (stderr,fmt='(A,I0,A)')&
              ' KOUNT must be a positive integer, not ',I2,'.'
            return
         end if
         ! Save the current environmental data. If the number of segments
         ! is being increased, all the data are stored and then recovered.
         ! If the number of segments is being decreased, only the data
         ! needed for the new structure is stored.
         call Assign_LUN (ENVLUN)
         open (unit=ENVLUN, status='SCRATCH', access='SEQUENTIAL',&
         action='readwrite', form='FORMATTED', position='rewind',&
         iostat=File_Check)
         if (File_Check /= 0) then
            write (stderr,fmt='(/A)')&
            ' Error opening disk file; KOUNT was not altered.'
            return
         endif
         call Assign_LUN (LoadLUN)
         open (unit=LoadLUN, status='SCRATCH', access='SEQUENTIAL',&
         action='readwrite', form='FORMATTED', position='rewind',&
         iostat=File_Check)
         if (File_Check /= 0) then
            write (stderr,fmt='(/A)')&
            ' Error opening disk file; KOUNT was not altered.'
            return
         endif
         if (I2>KOUNT) then ! increase in segments, write out all the data
            call ENVOUT(ENVLUN,KOUNT,.true.)
            ! .true. signals ENVOUT a SET command is in progress
            call LOADOUT(LoadLUN,Problem,KOUNT,KCHEM)
            if (Problem) then
               write (stderr,fmt='(/A)')&
                  ' Error processing disk file; KOUNT was not altered.'
               return
            end if
         else ! decrease in segments, only write the data needed
            call ENVOUT(ENVLUN,I2,.true.)
            ! .true. signals ENVOUT a SET command is in progress
            call LOADOUT(LoadLUN,Problem,I2,KCHEM)
            if (Problem) then
               write (stderr,fmt='(/A)')&
                  ' Error processing disk file; KOUNT was not altered.'
               return
            end if
         end if
         call Allocate_Storage(2,I2,KCHEM) ! rework environment storage
         ! Initialize the new data structures
         call initl(3)
         call initl(4)
         ! retrieve the current environmental/load data into the new structure
         Rewind ENVLUN
         Rewind LoadLUN
         if (I2>KOUNT) then ! only read the available data; the rest is zero
            call ENVIN('QQQ',.true.)! .true. to signal SET command seqence
            call LOADIN(LoadLUN,Problem,KOUNT,KCHEM)
            if (Problem) then
               call INITL(4) ! to zero the loads
               write (stderr,fmt='(A)') ' Warning: Loads were reset.'
            end if
            KOUNT=I2
         else ! set KOUNT to the new (smaller) value and then read
            KOUNT = I2
            call ENVIN('QQQ',.true.)
            call LOADIN(LoadLUN,Problem,KOUNT,KCHEM)
            if (Problem) then
               call INITL(4) ! to zero the loads
               write (stderr,fmt='(A)') ' Warning: Loads were reset.'
            end if
         end if
         ! ENVIN closes the environmental file and releases the LUN
         close (LoadLUN)
         call Release_LUN(LoadLUN)
         IRUN = 0   ! prevent "continue" until "run" has been executed
         FIXFIL = 0 ! prevent invocation of plot routines
         if (echo) write (stdout,fmt='(/A,I0,A)')&
            ' Number of segments in model is now ',KOUNT,'.'
      case (2)
         if (I2==0 .and. ITOADG(ICL1) /= 0) then
            write (stderr,fmt='(/A/A/A)') ' *** WARNING ***',&
            ' Do not build influent flows through the advective flow field.',&
            ' Use stream flow (STFLO), non-point-source flow (NPSFL), etc.'
            ! Hoever, clear out bad values...
            if (JFRADG(ICL1)>KOUNT) JFRADG(ICL1)=0
            if (ITOADG(ICL1)>KOUNT) ITOADG(ICL1)=0
         elseif (I2 <= KOUNT) then
            JFRADG(ICL1) = I2
         else
            write (stderr,fmt='(/A,I0,A/A,I0,A)')&
          ' Current model is defined using ',KOUNT,' segments.',&
          ' The transport fields cannot include a segment value of ',I2,'.'
         endif
      case (3)
         if (I2 <= KOUNT) then
            ITOADG(ICL1) = I2
         else
            write (stderr,fmt='(/A,I0,A/A,I0,A)')&
          ' Current model is defined using ',KOUNT,' segments.',&
          ' The transport fields cannot include a segment value of ',I2,'.'
         endif
      case (4); ADVPRG(ICL1) = R4
      case (5)
         if (I2 <= KOUNT) then
            JTURBG(ICL1) = I2
         else
            write (stderr,fmt='(/A,I0,A/A,I0,A)')&
          ' Current model is defined using ',KOUNT,' segments.',&
          ' The transport fields cannot include a segment value of ',I2,'.'
         endif
      case (6)
         if (I2 <= KOUNT) then
            ITURBG(ICL1) = I2
         else
            write (stderr,fmt='(/A,I0,A/A,I0,A)')&
          ' Current model is defined using ',KOUNT,' segments.',&
          ' The transport fields cannot include a segment value of ',I2,'.'
         endif
      case (7); XSTURG(ICL1) = R4
      case (8); CHARLG(ICL1) = R4
      case (9)  ! dispersion coefficient DSPG
         ! Check for bad values. First, determine the type of exchange
         ! (although this can't be exhaustive, it catches some typographical
         ! (errors during data entry);
         ! 1. benthic boundary layer or sediment internal
         ! 2. vertical water column
         ! 3. horizontal water column
         ! Skip exchanges across the system boundary and inputs where
         ! the segments haven't yet been selected...
         if (JTURBG(ICL1)==0 .or. ITURBG(ICL1)==0) then
            DSPG(ICL1,ICL2) = R4
         elseif (TYPEG(JTURBG(ICL1))=='B' .or. TYPEG(ITURBG(ICL1))=='B') then
              ! benthic exchange -- screen for patent error
            if (R4 .LessThan. 1.0E-03) then
               DSPG(ICL1,ICL2) = R4
            else ! patent error...issue warning message
               DSPG(ICL1,ICL2) = 1.0E-05
               write (stderr, fmt='(A/A)')&
               ' Sediment dispersivity cannot be greater than',&
               ' 1.0E-03 m2/hr. Input defaulted to 1.0E-05.'
            end if
         else ! water column exchange -- screen for patent error
            if (R4 .GreaterThanOrEqual. 1.0E-03) then
               DSPG(ICL1,ICL2) = R4
            else ! patent error...issue warning message
               write (stderr, fmt='(A)')&
             ' Water column dispersivity cannot be less than 1.0E-03 m2/hr.'
               if (abs(JTURBG(ICL1)-ITURBG(ICL1))==1) then
                  write (stderr, fmt='(A/A)')&
                  ' This appears to be a vertical transport path;',&
                  ' it has been set to 1.0E-02 m2/hr.'
                  DSPG(ICL1,ICL2)=1.0E-02
               else
                  write (stderr, fmt='(A/A)')&
                  ' This appears to be a horizontal transport path;',&
                  ' it has been set to 1.0E+03 m2/hr.'
                  DSPG(ICL1,ICL2)=1.0E+03
               end if
            end if
         end if
   end select
end if
case (11) Groups ! Parameter Group: SEDMG -- sediment properties
   select case (IVAR)
      case (1)
         if (R4 .GreaterThanOrEqual. 0.0) then
            SUSEDG(ICL1,ICL2) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2,A)') &
               ' Error in data specification: SUSED cannot be negative.',&
               ' Suspended sediment remains ', SUSEDG(ICL1,ICL2), ' mg/L.'
         end if
      case (2)
         if (R4 .GreaterThanOrEqual. 0.0) then
            BULKDG(ICL1,ICL2) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2,A)') &
               ' Error in data specification: BULKD cannot be negative.',&
               ' Bulk density remains ', BULKDG(ICL1,ICL2), ' g/cc.'
         end if
      case (3)
         if ((R4 .GreaterThanOrEqual. 0.0) .and. (R4 .LessThanOrEqual. 1.0)) then
            FROCG(ICL1,ICL2) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2)') &
               ' Error in data specification: FROC must be between 0 and 1.',&
               ' Fraction organic carbon remains ', FROCG(ICL1,ICL2)
         end if
      case (4)
         if (R4 .GreaterThanOrEqual. 0.0) then
            CECG(ICL1,ICL2) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2,A)') &
            ' Error in data specification: CEC cannot be negative.',&
            ' Cation exchange capacity remains', CECG(ICL1,ICL2), ' meq/100g.'
         end if
      case (5)
         if (R4 .GreaterThanOrEqual. 0.0) then
            AECG(ICL1,ICL2) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2,A)') &
            ' Error in data specification: AEC cannot be negative.',&
            ' Anion exchange capacity remains ', AECG(ICL1,ICL2), ' meq/100g.'
         end if
      case (6)
         if (R4 .GreaterThanOrEqual. 100.0) then
            PCTWAG(ICL1,ICL2) = R4
         else
            write (stderr,fmt='(/A/A,ES10.3E2,A)') &
               ' Error in data specification: PCTWA cannot be < 100.',&
               ' Water content remains ', PCTWAG(ICL1,ICL2)
         end if
   end select
case (12) Groups ! Parameter Group: QUALG
   select case (IVAR)
      case (1); TCELG(ICL1,ICL2) = R4
      case (2); PHG(ICL1,ICL2) = R4
      case (3); POHG(ICL1,ICL2) = R4
      case (4); OXRADG(ICL1) = R4
      case (5); REDAGG(ICL1,ICL2) = R4
      case (6); BACPLG(ICL1,ICL2) = R4
      case (7); BNBACG(ICL1,ICL2) = R4
      case (8); PLMASG(ICL1,ICL2) = R4
      case (9); BNMASG(ICL1,ICL2) = R4
      case (10); KO2G(ICL1,ICL2) = R4
   end select
case (13) Groups ! Parameter Group: PHOTOG
   select case (IVAR)
      case (1)
         if (TYPEG(ICL1)=='B' .and. R4<10.0) then
            R4=10.0 ! minimum for benthic zone
         elseif (R4<1.0) then
            R4=1.0  ! minimum for water column
         end if
         DOCG(ICL1,ICL2) = R4
      case (2); CHLG(ICL1,ICL2) = R4
      case (3)
         if ((R4.GreaterThanOrEqual.0.0).and.(R4.LessThanOrEqual.10.0)) then
            CLOUDG(ICL1) = R4
         else
            write (stderr,fmt='(3(/A))')&
              ' Cloudiness must be entered in tenths of sky covered;',&
              ' Exams does not accept values outside the range 0.0 to 10.0.',&
              ' CLOUD has not been changed.'
         endif
      case (4)
         if ((R4.GreaterThanOrEqual.1.0).and.(R4.LessThanOrEqual.2.0)) then
            DFACG(ICL1,ICL2) = R4
         else
            write (stderr,fmt='(A/A)')&
               ' DFAC only takes values between 1.0 (for a beam) and 2.0',&
               ' (fully diffused light field). Parameter not altered.'
         endif
      case (5); DISO2G(ICL1,ICL2) = R4
      case (6) ! older: set a value ... OZONEG(ICL1) = R4
            if (echo) write (stdout,fmt='(/A/A)')&
               ' Total column ozone is read from the TOMS database.',&
               ' Given the current latitude and longitude, the values are'
            call ozone(latg,longg,ozoneg,.true.,stdout,Oz_UNT,Zonal_Data)
            All_Done = .true.
  end select
case (14) Groups ! Parameter Group: GEOMT
   select case (IVAR)
      case (1) ! Direct alteration of segment volume
         if (R4 .GreaterThan. 0.0) then
            if (IRUN==0) then
               VOLG(ICL1) = R4
            else ! A run has been executed, so modify the concentration
                 ! so that a Continue will have the right starting values.
                 ! Y is constituent concentration (mg/L) referred to
                 ! aqueous volume. VOLG is the environmental volume, so the
                 ! concentration generally has to be adjusted for the
                 ! sediment/water ratio. Here, however, only the overall
                 ! volume is changing (and not the properties), so the
                 ! environmetal volume ratio can be used for the adjustment.
               if (ICL1<=KOUNT) then
                  do I=1,kchem
                     Y(ICL1,I) = Y(ICL1,I)*VOLG(ICL1)/R4
                  end do
                  ! Adjust reach volume and total volume
                  if (TYPEG(ICL1)=='B') then ! Benthic compartment
                     Reach_Benthic_Volume(Reach_ID(ICL1))=&
                     Reach_Benthic_Volume(Reach_ID(ICL1))-VOLG(ICL1)+R4
                     Total_Benthic_Volume=Total_Benthic_Volume-VOLG(ICL1)+R4
                     Reach_Benthos_Volume(Reach_ID(ICL1))=&
                     Reach_Benthos_Volume(Reach_ID(ICL1))-VOLG(ICL1)+R4
                     Total_Benthos_Volume=Total_Benthos_Volume-VOLG(ICL1)+R4
                  else ! water column compartment
                     Reach_Limnetic_Volume(Reach_ID(ICL1))=&
                     Reach_Limnetic_Volume(Reach_ID(ICL1))-VOLG(ICL1)+R4
                     Total_Limnetic_Volume=Total_Limnetic_Volume-VOLG(ICL1)+R4
                  end if
               end if
               VOLG(ICL1) = R4
            end if
         else ! negative entry
         write (stderr,fmt='(/A/A)') ' Negative volumes not appropriate.',&
            ' Volume was not altered.'
         end if
      case (2); AREAG(ICL1) = R4
      case (3); DEPTHG(ICL1) = R4
      case (4); XSAG(ICL1) = R4; IRUN=0
      case (5)
         LENGG(ICL1) = R4
         IRUN=0 ! basic geometry change, so prevent continue
      case (6); WIDTHG(ICL1) = R4; IRUN=0
   end select
case (15) Groups ! Parameter Group: CLIMG
   select case (IVAR)
      case (1); RAING(ICL1) = R4
      case (2); EVAPG(ICL1,ICL2) = R4
      case (3); LATG = R4; IRUN=0 ! prevent continue - need new ozone data
      case (4); LONGG = R4;IRUN=0 ! prevent continue - need new ozone data
      case (5); WINDG(ICL1,ICL2) = R4
      case (6); ELEVG = R4
      case (7); RHUMG(ICL1) = R4
      case (8); ATURBG(ICL1) = R4
   end select
case (16) Groups ! Parameter Group: FLOWG
   select case (IVAR)
      case (1); STFLOG(ICL1,ICL2) = R4
      case (2); STSEDG(ICL1,ICL2) = R4
      case (3); NPSFLG(ICL1,ICL2) = R4
      case (4); NPSEDG(ICL1,ICL2) = R4
      case (5); SEEPSG(ICL1,ICL2) = R4
   end select
case (17) Groups ! Parameter Group: LOADSG
   select case (IVAR)
      case (1); STRLDG(ICL1,ICL2,ICL3) = R4
      case (2); NPSLDG(ICL1,ICL2,ICL3) = R4
      case (3); PCPLDG(ICL1,ICL2,ICL3) = R4
      case (4); DRFLDG(ICL1,ICL2,ICL3) = R4
      case (5)
         if ((R4.GreaterThanOrEqual.0.0).and.(R4.LessThanOrEqual.1.0)) then
            PRBENG=R4
         else
            write (stderr,fmt='(/A)')&
             ' PRBEN must be between 0.0 and 1.0--its value was not altered.'
         endif
      case (6); SEELDG(ICL1,ICL2,ICL3) = R4
      case (7); IMASSG(ICL1) = R4
      case (8); ISEGG(ICL1) = I2
      case (9); ICHEMG(ICL1) = I2
      case (10); IMONG(ICL1) = I2
      case (11); IDAYG(ICL1) = I2
      case (12); IYEARG(ICL1) = I2
      case (13)
         if (R4 .GreaterThanOrEqual. 0.0) then
            SPRAYG = R4
         else
            write (stderr,fmt='(/A)')&
               ' SPRAY drift cannot be negative; it has been reset to 10%.'
            SPRAYG = 10.0
         end if
   end select
case (18) Groups ! Parameter Group: SPECTR
   select case (IVAR)
      case (1); CHPARG(ICL1) = I2
      case (2); TPRODG(ICL1) = I2
      case (3); NPROCG(ICL1) = I2
      case (4); RFORMG(ICL1) = I2
      case (5); YIELDG(ICL1) = R4
      case (6); EAYLDG(ICL1) = R4
   end select
end select Groups
end Subroutine PUTVAR

end Module SetValue
