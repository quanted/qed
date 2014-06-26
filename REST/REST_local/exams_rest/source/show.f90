subroutine SHOW(IT,IS)
! Purpose of this routine is to determine the show sub-command.
! It may be on the input record; if it is not, prompt for it and read records
! until a sub-command is found.
! Revised 28-NOV-1985 (LAB) to accomodate IBM file structures.
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
! dependent cursor control.
! Revised 10/28/88 to add IMBED to INTEGER declaration
! Revised 12/13/88 to print TCODE in mode 3 SH TI FR
! Converted to Fortran90 2/20/96 et seq.
! Revisions April 2001 due to dynamic memory allocation
use Implementation_Control
use Input_Output
use Alias_Transfer
! Local variable identification
! HOW     sub-command table index
! MINSHO  minimum show command lengths
! NOSHOW  number of sub-commands
! SHOLEN  vector of sub-command lengths
! SHONAM  vector of sub-commands
use Global_Variables
use Local_Working_Space
use Model_Parameters
Implicit None
integer :: HOW,EOF,IT,IS,IFIND,I,ITEMP,I1,I3,IPASS,IP1,IMBED,File_Check
integer, parameter :: Zero = 0, Two = 2, NAMLEN = 94, NAMLN2 = 9, NOSHOW = 14
integer, dimension(2),  parameter :: LENS2 = (/5,4/), MINS2 = (/1,1/)
integer, dimension(14), parameter :: MINSHO = (/1,2,1,1,3,2,1,1,1,3,2,2,2,1/)
integer, dimension(14), parameter :: SHOLEN = (/9,8,9,10,7,7,5,4,4,4,5,8,5,9/)
character(len=50) :: NAMECO, NAMEEC
character(len=7), dimension(4) :: TUNIT =  (/ &
   ' Hours ',' Days  ',' Months',' Years '/)
character(len=9), dimension(13) :: MONAM = (/ &
   'January  ','February ','March    ','April    ',&
   'May      ','June     ','July     ','August   ',&
   'September','October  ','November ','December ','Average  '/)
character(len=1), dimension(94) :: SHONAM = (/ &
   'C','H','E','M','I','S','T','R','Y',&
   'G','E','O','M','E','T','R','Y',&
   'A','D','V','E','C','T','I','O','N',&
   'D','I','S','P','E','R','S','I','O','N',&
   'Q','U','A','L','I','T','Y',&
   'G','L','O','B','A','L','S',&
   'L','O','A','D','S',&
   'T','I','M','E',&
   'H','E','L','P',&
   'Q','U','I','T',&
   'P','U','L','S','E',&
   'P','R','O','D','U','C','T','S',&
   'P','L','O','T','S',&
   'V','A','R','I','A','B','L','E','S'/)
character(len=1), dimension(9) :: NAME2 = &
   (/'F','R','A','M','E',  'Q','U','I','T'/)

!  IT      DESCRIPTION
!  ==     =====================
!  0      SHOW SATISIFIED
!  1      SHOW ADVECTION
!  2      SHOW DISPERSION
!  3      SHOW GLOBALS
!  4      SHOW PULSE LOADS
!  5      SHOW PRODUCTS
!  6      SHOW CHEMISTRY
!  7      SHOW LOADS
!  8      ERROR - Plot file not available
!
! Load the names etc. of the input data from disk
call READSP
IT = 0
IS = 0
Subcommands_loop: do ! go get a subcommand
HOW = IFIND(NOSHOW,NAMLEN,SHOLEN,SHONAM,MINSHO) + 3
Subcommands: select case (HOW)
case (11) Subcommands ! Process the 'HELP TIME' option
   Time_loop: do
      I = IFIND(Two,NAMLN2,LENS2,NAME2,MINS2) + 3
      Time_case: select case (I)
      case (1) Time_case ! HELP
         write (stdout,fmt='(//A//A/A/A)',advance='NO')&
         ' The following options are available:',&
         '           Frame - list current integration time parameters, or',&
         '           Quit  - return to command mode without any action.',&
         ' Option-> '
         call INREC (EOF,stdin)
         if (EOF == 1) then
            write (stdout,fmt='(/A)') ' SHOW cancelled.'
            return
         end if
         STOPIT = 0
      case (2) Time_case
         write (stdout,fmt='(/A)')&
            ' E-O-F encountered. SHOW terminated.'
         return
      case (3) Time_case
         write (stdout,fmt='(/A)') ' Option not identified.'
         return
      case (4) Time_case ! "SHOW TIME FRAME" option selected
         Mode_select: select case (MODEG)
         case (1) Mode_select
            write (stdout,fmt='(/A/A/)')&
               ' Currently in steady-state mode;',&
               ' time parameters not required.'
            return
         case (2) Mode_select
            write (stdout,fmt='(//A,I0,A,I0,A/A,I0,A/)') &
             ' A RUN will integrate from ',int(TINITL),' to ',&
               int(TENDG),TUNIT(TCODEG),&
             ' with output at intervals of ',int(CINTG),&
               trim(TUNIT(TCODEG))//'.'
            if (IFLAG == 2) write (stdout,fmt='(A,I0,A/)')&
               ' A CONTINUE will commence at ',int(TENDG),&
                 trim(TUNIT(TCODEG))//'.'
            write (stdout,fmt='(A,I0,A,I0/A,I0,A,I0)')&
             ' CINT = ',int(CINTG),', TINIT = ',int(TINITL),&
             ' TEND = ',int(TENDG),', TCODE =    ',TCODEG
            return
         case (3) Mode_select
            if (NYEARG<1 .or. NYEARG>999999) then
               NYEARG = 1
               write (stderr,fmt='(/A/A/)')&
                  ' Error: NYEAR must not be <1 or >999,999.',&
                  ' NYEAR has been reset to 1.'
            end if
            ITEMP = YEAR1G+NYEARG-1
            write (stdout,fmt='(//A,I0/A,I0/A/A,I0,A,I0,A,I0,A)')&
          ' A RUN will integrate from 1 January ',YEAR1G,&
          '                 through 31 December ',ITEMP,&
          ' with daily output encoded in'//TUNIT(TCODEG),&
          ' (YEAR1 = ',YEAR1G,', NYEAR = ',NYEARG,', and TCODE = ',TCODEG,').'
            if (IFLAG == 2) then
               ITEMP = LASTYR+NYEARG
               write (stdout,fmt='(/A,I0/A,I0,A)') &
                  ' CONTinuation will proceed through 31 December ',ITEMP,&
                  ' (NYEAR = ',NYEARG,'.)'
            elseif (IFLAG > 2) then; write (stdout,fmt='(/A,I0)')&
                  ' CONTinuation will proceed through 31 December ',LASTYR
            endif
            return
         case default Mode_select
            write (stdout,fmt='(/A/)')&
               ' MODE is not in allowable range (1, 2, or 3 only).'
            return
         end select Mode_select
      case (5) Time_case
         return
      end select Time_case
   end do Time_loop
case (14) Subcommands ! Process the 'SHOW PULSE LOADS' command
   IT = 4
   return
case (15) Subcommands ! process the 'SHOW PRODUCTS' command.
   IT = 5
   return
case (16) Subcommands ! process the "SHOW PLOTS" command
   call Assign_LUN (PLTLUN)
   open (unit=PLTLUN,status='OLD',access='SEQUENTIAL',action='read',&
   form='UNFORMATTED',position='REWIND',file='ssout.plt',err=200)
   if (FIXFIL == 0) then
      IT = 8
   else
      read (PLTLUN,end=210,err=200) I1,I2,I3
      write (stdout,fmt='(//A,I0/A,I0/A,I0//)')&
         ' Number of chemicals-- ',I1,&
         ' Simulation Mode--     ',I2,&
         ' Number of segments--  ',I3
      do I = 1, I1
         read (PLTLUN,end=210,err=200) NAMECO
         write (stdout,fmt='(A,I0,A)')&
            ' Chemical: ',I, ') '//trim(NAMECO)
      end do
      read (PLTLUN,end=210,err=200) NAMEEC
      write (stdout,fmt='(A)') ' Environment: '//trim(NAMEEC)
   end if
   go to 220
   200 continue
      write (stdout,fmt='(//A)') ' Error reading the plot file.'
   go to 220
   210 continue
      write (stdout,fmt='(//A)')&
      ' End-of-file enountered while reading the plot file.'
   220   continue
   close (unit=PLTLUN,iostat=File_Check)
   call Release_LUN (PLTLUN)
   230 return
case (1, 12) Subcommands !  SHOW HELP
   write (stdout,fmt='(/A/4(/A))',advance='NO') &
      ' The following options are available ',&
      ' Advection,  Chemistry,   Dispersion,   GEometry,',&
      ' GLobals,    Loads,       PLot,         PUlse Loads,',&
      ' PRoducts,   QUAlity,     Time Frame,   Variables,',&
      ' Help, or    QUIt-> '
   call INREC (EOF,stdin)
   if (EOF == 1) then
      write (stdout, fmt='(/A)') ' SHOW cancelled.'
      return
   end if
   STOPIT = 0
   cycle Subcommands_loop
case (4) Subcommands ! Show chemistry--set flag to call Subroutine PRCHEM
   IT = 6
   return
case (5) Subcommands ! Process 'SHOW GEOMETRY'
   IPASS = 0
   call HEDSHO(KOUNT) ! list the segments and their Types first
   Geometry_segments: do I = 1, KOUNT
      if (IPASS == 0) then
         write (stdout,fmt='(/A,I0,A)')&
            ' Segment No. ',I,&
            ',  Type--'//TYPEG(I)//',  Month--'//MONAM(MONTHG)
         write(stdout,fmt='(/A,1PG11.4,A,G11.4,4(/A,G11.4,A,G11.4))')&
            ' VOL    = ', VOLG(I),          '   XSA    = ', XSAG(I),&
            ' AREA   = ', AREAG(I),         '   LENGth = ', LENGG(I),&
            ' DEPTH  = ', DEPTHG(I),        '   WIDTH  = ', WIDTHG(I),&
            ' STFLO  = ', STFLOG(I,MONTHG), '   STSED  = ', STSEDG(I,MONTHG),&
            ' NPSFL  = ', NPSFLG(I,MONTHG), '   NPSED  = ', NPSEDG(I,MONTHG)
         if (TYPEG(I) /= 'B') then ! water column segment
            write (stdout,fmt='(A,1PG11.4,A,G11.4)')&
            ' SEEPS  = ', SEEPSG(I,MONTHG), '   SUSED  = ', SUSEDG(I,MONTHG)
            if (I == 1 .or. (I>1 .and. TYPEG(I-1)=='B'))&
               write (stdout,fmt='(A,1PG11.4,A,G11.4/)')&
               ' WIND   = ', WINDG(I,MONTHG), '   EVAP   = ', EVAPG(I,MONTHG)
         else ! benthic segment
            write (stdout,fmt='(/A,1PG11.4,A,G11.4,/A,G11.4)')&
            ' SEEPS  = ',SEEPSG(I,MONTHG), '   BULKD  = ', BULKDG(I,MONTHG),&
            ' Percent water (PCTWA) = ', PCTWAG(I,MONTHG)
         endif
      end if
      IPASS = 0
      if (I < KOUNT) then
         IP1 = I+1
         Segmnt_query: do
            write (stdout,fmt='(/A,I0,A/A)',advance='NO')&
               ' Do you want to see Segment # ',IP1,'?',&
               ' (Enter Yes, No, or Quit)-> '
            call INREC (EOF,stdin)
            if (EOF == 1) then
               write (stdout,fmt='(/A)') ' SHOW cancelled.'
               return
            end if
            START = IMBED(INPUT,Zero)
            if (START == -999) exit Segmnt_query ! treat null input as yes...
            if (INPUT(START:START) == 'Q'.or.INPUT(START:START) == 'q') return
            if (INPUT(START:START) == 'Y'.or.INPUT(START:START) == 'y')&
               exit Segmnt_query
            if (INPUT(START:START) == 'N'.or.INPUT(START:START) == 'n') then
               IPASS = 1
               exit Segmnt_query
            end if
            write (stdout,fmt='(/A)')&
               ' Response not understood, please try again.'
         end do Segmnt_query
      end if
   end do Geometry_segments
   return
case (6) Subcommands ! Process 'SHOW ADVECTION'
   call HEDSHO(KOUNT)
   IT = 1            ! Set flag to call table subroutine
   return
case (7) Subcommands ! Process 'SHOW DISPERSION'
   call HEDSHO(KOUNT)
   IT = 2
   return
case (8) Subcommands ! Process 'SHOW QUALITY'
   IPASS = 0
   call HEDSHO(KOUNT) ! list the segments and their Types first
   Quality_segments: do I = 1, KOUNT
      if (IPASS == 0) then
         write (stdout,fmt='(/A,I0,A)')&
            ' Segment No. ',I,&
            ',  Type--'//TYPEG(I)//',  Month--'//MONAM(MONTHG)
         write(stdout,fmt='(/A,1PG11.4,A,G11.4,3(/A,G11.4,A,G11.4))')&
            ' AEC   = ',AECG(I,MONTHG),   '   CEC    = ',CECG(I,MONTHG),&
            ' REDAG = ',REDAGG(I,MONTHG), '   FROC   = ',FROCG(I,MONTHG),&
            ' PH    = ',PHG(I,MONTHG),    '   POH    = ',POHG(I,MONTHG),&
            ' TCEL  = ',TCELG(I,MONTHG),  '   DOC    = ',DOCG(I,MONTHG)
         if (TYPEG(I) /= 'B') then; write(stdout,&
            fmt='(A,1PG11.4,A,G11.4,2(/A,G11.4,A,G11.4)/)')&
            ' BACPL = ',BACPLG(I,MONTHG), '   PLMAS  = ',PLMASG(I,MONTHG),&
            ' KO2   = ',KO2G(I,MONTHG),   '   DISO2  = ',DISO2G(I,MONTHG),&
            ' CHL   = ',CHLG(I,MONTHG),   '   DFAC   = ', DFACG(I,MONTHG)
         else; write (stdout,fmt='(A,1PG11.4,A,G11.4)')&
            ' BNBAC = ', BNBACG(I,MONTHG), '   BNMAS  = ', BNMASG(I,MONTHG)
         endif
      end if
      IPASS = 0
      if (I < KOUNT) then
         IP1 = I+1
         Segment_query: do
            write (stdout,fmt='(/A,I0,A/A)',advance='NO')&
               ' Do you want to see Segment # ',IP1,'?',&
               ' (Enter Yes, No, or Quit)-> '
            call INREC (EOF,stdin)
            if (EOF == 1) then
               write (stdout,fmt='(/A)') ' SHOW cancelled.'
               return
            end if
            START = IMBED(INPUT,Zero)
            if (START == -999) exit Segment_query ! treat null input as yes
            if (INPUT(START:START) == 'Q'.or.INPUT(START:START) == 'q') return
            if (INPUT(START:START) == 'Y'.or.INPUT(START:START) == 'y')&
               exit Segment_query
            if (INPUT(START:START) == 'N'.or.INPUT(START:START) == 'n') then
               IPASS = 1
               exit Segment_query
            end if
            write (stdout,fmt='(A)') ' Response not understood.'
         end do Segment_query
      end if
   end do Quality_segments
   return
case (9) Subcommands    ! Process the 'SHOW GLOBALS' command
   call HEDSHO(KOUNT)
   IT = 3               ! Set flag to call PRENV/GLOBALS
   ! Acquire total column ozone from TOMS dataset
   call Ozone(latg,longg,ozoneg,.false.,stdout,Oz_UNT,Zonal_Data)
   return
case (10) Subcommands   ! Process the 'SHOW LOADS' command
   call HEDSHO(KOUNT)
   IT = 7               ! Set flag to call PRICL
   return
case (17) Subcommands    ! Process the 'SHOW VARIABLES' command
   call SHOVAR
   return
case (13) Subcommands
   return
case (2) Subcommands
   write (stdout,fmt='(/A)')&
      ' E-O-F encountered. SHOW terminated.'
   return
case default Subcommands
   write (stdout,fmt='(/A)') ' Option not identified.'
   return
case (3) Subcommands ! The SHOW option was invalid
   ! See if there was a valid variable name given.
   STOPIT = START-1
   call PRTPRM (IS)
   return
end select Subcommands
end do Subcommands_loop
return

contains
subroutine HEDSHO (KNT)
! purpose--to list the name and segments of ecosystem in a header
! revisions 10/21/88--run-time implementation of machine dependencies
! revisions 11/22/88--added NSLINE to control width of output line
! revisions April 2001--revised for up to 99 segments, suppressed if
! KOUNT>99
Implicit None
integer :: I,II,J,K,K2,K1
integer, intent (in) :: KNT
! KNT is the number of segments in the ecosystem, passed value of KOUNT
integer, parameter :: NSLINE = 20
! NSLINE is the Number of Segments per output LINE (60 available spaces,
! using 4 spaces per line to allow up to 9999 segments to be listed.)
write (stdout,fmt='(/A)') ' Name of environment: '//trim(ECONAM)
write (stdout,fmt='(A,I0)') ' Total number of segments (KOUNT) = ',KNT
if (KNT == 0 .or. KNT > 99) return ! suppress output if system too large
K = KNT/NSLINE
J = KNT-NSLINE*K
if (J /= 0) K = K+1
do II = 1, K
   K1 = (II-1)*NSLINE+1
   K2 = K1+NSLINE-1
   if (K2 > KNT) K2 = KNT
   write (stdout,fmt='(A,20(I3))')&
      ' Segment Number:',(I,I=K1,K2)
   write (stdout,fmt='(A,20(2X,A1))')&
      ' Segment "TYPE":',(TYPEG(I),I=K1,K2)
end do
! Formats are explicitly set up for 20 groups, as parameter (e.g., NSLINE)
! can't be used in a format specification. Beyond 99 compartments the output
! would start to run together, but this is unlikely to pose a real problem
! because in any case interactive SHOW commands will be impractical for
! so complex an environmental scenario. Thus, this feature is suppressed
! when KOUNT>99.
return
end subroutine HEDSHO
end Subroutine SHOW
