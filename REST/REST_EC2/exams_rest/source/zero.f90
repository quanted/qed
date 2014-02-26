subroutine ZERO(Y,IS,Silent)
! Revised 25-Dec-85 (LAB)
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
! dependent cursor control. Converted to Fortran90 2/20/96
! Revised 10/26/88 to unify command abort style to "quit"
! Fortran90 revisions 12-Feb-96, 15-Apr-96
! Revised 12/26/2000 to suppress superfluous message issued
! during start-up, as it bothers some users (addition of "Silent" logical)
use Implementation_Control
use Input_Output
use Global_Variables
Implicit None
real (kind (0D0)) :: Y(KOUNT,KCHEM)
integer :: EOF,IT,IFIND
integer, intent(in) :: IS
integer :: THREE=3, FIVE=5 ,NAMLN1=27, NAMLN2=13
logical, intent(in) :: Silent ! to suppress message reporting
character(len=1) :: &
NAME1(27)=(/'P','U','L','S','E',  'L','O','A','D','S',&
'R','E','S','I','D','U','A','L','S',  'H','E','L','P',  'Q','U','I','T'/),&
NAME2(13)=(/'L','O','A','D','S',  'H','E','L','P',  'Q','U','I','T'/)
integer :: LENS1(5)= (/5,5,9,4,4/), LENS2(3)= (/5,4,4/),&
           MINNO1(5)=(/1,1,1,1,1/), MINNO2(3)=(/1,1,1/)
if (IS /= 0) then ! command already fully specified
   STRLDG = 0.0
   NPSLDG = 0.0
   PCPLDG = 0.0
   DRFLDG = 0.0
   SEELDG = 0.0
   if (.not.Silent) &
      write (stdout,fmt='(/A/)') ' All allochthonous loads removed.'
   return
endif

Command_loop: do
   IT = IFIND(FIVE,NAMLN1,LENS1,NAME1,MINNO1) + 3
   Commands: select case (IT)
   case (3) Commands ! Process no match on available choices
      write (stdout,fmt='(/A)')&
         ' Option not recognized; ZERO command cancelled.'
      exit Command_loop
   case (4) Commands ! the Pulse option
      Pulse_loop: do
         IT = IFIND(THREE,NAMLN2,LENS2,NAME2,MINNO2) + 3
         Pulses: select case (IT)
         case (3) Pulses ! no match on available choices
            write (stdout,fmt='(/A)')&
            ' Option not recognized; ZERO command cancelled.'
            exit Command_loop
         case (4) Pulses ! Zero the pulse loads
            ISEGG  = 0
            ICHEMG = 0
            IMONG  = 0
            IDAYG  = 0
            IYEARG = 0
            IMASSG = 0.0
            write (stdout,fmt='(/A/)')&
               ' All allochthonous pulse loads removed.'
            exit Command_loop
         case (1,5) Pulses ! Help request or null input
            write (stdout,fmt='(//A//,3(10X,A/))')&
               ' The following options are available:',&
               ' Loads --zero all pulse loads,',&
               ' Help  --this message, or',&
               ' Quit  --return to command mode; no action.'
            write (stdout,fmt='(/A)',Advance='No') ' ZERO-> '
            call INREC (EOF,stdin)
            if (EOF == 1) then
               write (stdout,fmt='(/A)') ' ZERO command cancelled.'
               exit Command_loop
            else
               STOPIT = 0
               cycle Pulse_loop
            endif
         case (6) Pulses ! Quit requested
            write (stdout,fmt='(/A)') ' ZERO command cancelled.'
            exit Command_loop
         end select Pulses
      end do Pulse_loop
   case (5) Commands ! Process 'loads' option, zero all loads
      STRLDG = 0.0
      NPSLDG = 0.0
      PCPLDG = 0.0
      DRFLDG = 0.0
      SEELDG = 0.0
      write (stdout,fmt='(/A/)') ' All allochthonous loads removed.'
      exit Command_loop
   case (6) Commands ! Process 'residuals' option
      Y = 0.0
      write (stdout,fmt='(/A)') ' All chemicals removed.'
      exit Command_loop
   case (1,7) Commands ! Help requested, or null input
      write (stdout,fmt='(/A/,5(/10X,A))')&
         ' The following options are available:',&
         ' Pulse Loads--zero all event loadings,',&
         ' Loads      --zero all continuous loads,',&
         ' Residuals  --zero all current pollutant concentrations,',&
         ' Help       --this message, or',&
         ' Quit       -- return to command mode with no action.'
      write (stdout,fmt='(/A)',advance='NO') " ZERO-> "
      call INREC (EOF,stdin)
      if (EOF == 1) then
         write (stdout,fmt='(/A)') ' ZERO command cancelled.'
         exit Command_loop
      else
         STOPIT = 0
         cycle Command_loop
      end if
   case (8) Commands ! Quit reqested
      write (stdout,fmt='(/A/)') ' ZERO command cancelled.'
      exit Command_loop
   end select Commands
end do Command_loop
return
end subroutine ZERO
