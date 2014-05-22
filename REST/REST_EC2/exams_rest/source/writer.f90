Subroutine WRITER
! Created 16-MAY-1985 to download EXAMS ADB to disk file
! Revised 27-DEC-85 (LAB)
! Revised 10/20/88 (LAB) -- run-time formats for implementation-
! dependent cursor control. Converted to Fortran90 2/20/96
! Revised 10/26/88 to unify command abort style to "quit"
! Subroutines required: SKAN, IMBED, MATCH
use Implementation_Control
use Input_Output
use Global_Variables
use Local_Working_Space
use MultiScan
Implicit None
integer :: IMBED, MATCH
integer :: EOF, WHICH, err_check

integer, parameter :: Zero=0, Six=6, RSPSIZ=42
!integer, parameter :: LENANS=8
! RSPSIZ is total number of characters in responses
! LENANS is total number of characters in answers (i.e., help + quit = 8)

!integer, dimension(2) :: NUMANS = (/4,4/),          MINANS = (/1,1/)
! NUMber of characters in each ANSwer, and the MINimum characters for each

integer, dimension(6) :: NORESP = (/8,11,8,7,4,4/), MNRESP = (/1,1,1,1,1,1/)
! NO. of characters in each response, and their minimum unique characters

logical :: Chemical, Environment, Product, Load, Proceed, Problem
character(len=1), dimension(1), parameter :: Blank = ' '
character(len=1), dimension(RSPSIZ) :: RESP= (/'C','H','E','M','I','C','A','L',&
   'E','N','V','I','R','O','N','M','E','N','T',&
   'L','O','A','D','I','N','G','S',&
   'P','R','O','D','U','C','T',  'H','E','L','P',  'Q','U','I','T'/)
!character(len=1), dimension(LENANS) :: ANSWER = &
!   (/'H','E','L','P',  'Q','U','I','T'/)
Chemical        = .false. ! Initialize command options
Environment     = .false.
Product         = .false.
Load            = .false.

! More information in input record? (START = location of next
! non-blank, non-tab character, or -999 if there is none such.)
START = IMBED(INPUT,STOPIT)
Inquiry: do
   Need_input: if (START == -999) then    ! no non-blank or non-tab character
      write (stdout,fmt='(/A)',advance='NO')& ! so prompt for it
         ' Enter Chemical, Environment, Load, Product, Help, or Quit-> '
      call INREC (EOF,stdin)
      if (EOF == 1) then
         write (stdout,fmt='(/A)')&
            ' End-of-file marker--WRITE command cancelled. '
         return
      endif
      START = IMBED(INPUT,Zero)
      if (START == -999) cycle Inquiry
   end if Need_input
! Locate the next blank in the input:
   call SKAN (INPUT,START,STOPIT,TYPE,Blank)
   if (TYPE == 100) STOPIT = Key_Buffer+1
   ! WHICH - 0 = no MATCH
   ! WHICH - 1 = Chemical
   ! WHICH - 2 = Environment
   ! WHICH - 3 = Load
   ! WHICH - 4 = Product Chemistry
   ! WHICH - 5 = Help
   ! WHICH - 6 = Quit
   WHICH = MATCH(Six,RSPSIZ,NORESP,RESP,MNRESP)
   File_type: select case (WHICH)
   case (0) File_type ! no match
      write (stdout,fmt='(/A)')&
         ' Response not recognized, please try again:'
      INPUT = ' '
      START = -999
      cycle Inquiry
   case (1) File_type
      Chemical = .true.; exit Inquiry
   case (2) File_type
      Environment = .true.; exit Inquiry
   case (3) File_type
      Load = .true.; exit Inquiry
   case (4) File_type
      Product = .true.; exit Inquiry
   case (5) File_type ! Help requested
      write (stdout,fmt='(8(/A))')&
      ' The WRITE command is used to download the Activity Data Base (ADB)',&
      ' to a separate datafile on disk. In response to the prompt, indicate',&
      ' your choice of',&
      '           C to download Chemical data,',&
      '           E to download Environmental data,',&
      '           L to download Loadings data,',&
      '           P to download Product chemistry,',&
      '        or Quit to return to the EXAMS prompt.'
      INPUT = ' '
      START = -999
      cycle Inquiry
   case (6) File_type ! Quit requested
      write (stdout,fmt='(A)') ' WRITE cancelled.'
      return
   end select File_type
end do Inquiry

if (Chemical) then
   call Get_File_Name ('WRITE Chemical', FILNAM(2), Proceed, 'WRITE')
         ! Acquire the file name. If file exists and user wishes, quit now.
   if (.not.Proceed) Return 
   call Assign_LUN (RWLUN)
   open (unit=RWLUN, status='REPLACE', access='SEQUENTIAL',&
   action='write', form='FORMATTED', position='rewind',&
      iostat=Err_check, file=trim(FILNAM(2)))
   if (Err_check /= 0) then
      write (stdout,fmt='(/A)')&
         ' Error opening disk file. "WRITE Chemical" command cancelled.',&
         ' Possibly directory does not exist or device is not connected.'
   else
      call CHMOUT(RWLUN)
      write (stdout,fmt='(/A)')&
     ' Chemical data written to file "'//trim(FILNAM(2))//'".'
   end if

elseif (Environment) then
   call Get_File_Name ('WRITE Environment', FILNAM(2), Proceed, 'WRITE')
         ! Acquire the file name. If file exists and user wishes, quit now.
   if (.not.Proceed) Return 
   call Assign_LUN (RWLUN)
   open (unit=RWLUN, status='REPLACE', access='SEQUENTIAL',&
      action='write', form='FORMATTED', position='rewind',&
      iostat=Err_check, file=trim(FILNAM(2)))
   if (Err_check /= 0) then
      write (stdout,fmt='(/A)')&
         ' Error opening disk file. "WRITE Environment" command cancelled.',&
         ' Possibly directory does not exist or device is not connected.'
   else
      call ENVOUT(RWLUN,KOUNT,.false.)
      ! .false. signals SET command NOT underway, write all data
      write (stdout,fmt='(/A)')&
         ' Environmental data written to file "'//trim(FILNAM(2))//'".'
   endif
elseif (Load) then
   call Get_File_Name ('WRITE Load', FILNAM(2), Proceed, 'WRITE')
         ! Get the file name. If the file exists and user wishes, quit now.
   if (.not.Proceed) Return 
   call Assign_LUN (RWLUN)
   open (unit=RWLUN, status='REPLACE', access='SEQUENTIAL',&
         action='write', form='FORMATTED', position='rewind',&
         iostat=Err_check,file=trim(FILNAM(2)))
   if (Err_check /= 0) then
      write (stdout,fmt='(/A)')&
         ' Error opening disk file. "WRITE Load" command cancelled.',&
         ' Possibly directory does not exist or device is not connected.'
   else
      call LoadOut (RWLUN, Problem, KOUNT, KCHEM)
       if (.not.Problem) write (stdout,fmt='(/A)')&
          ' Loadings data written to file "'//trim(FILNAM(2))//'".'
   endif

elseif (Product) then
   call Get_File_Name ('WRITE Product', FILNAM(2), Proceed, 'WRITE')
         ! Get the file name. If file exists and user wishes, quit now.
   if (.not.Proceed) Return 
   call Assign_LUN (RWLUN)
   open (unit=RWLUN, status='REPLACE', access='SEQUENTIAL',&
         action='write', form='FORMATTED', position='rewind',&
         iostat=Err_check, file=trim(FILNAM(2)))
   if (Err_check /= 0) then
      write (stdout,fmt='(/A)')&
    ' Error opening disk file. "WRITE Product" chemistry command cancelled.',&
    ' Possibly directory does not exist or device is not connected.'
   else
      BATCH=2
      call PRPROD(RWLUN, Problem)
      if (.not.Problem) write (stdout,fmt='(/A)')&
         ' Product chemistry written to file "'//trim(FILNAM(2))//'".'
   endif
else
   write (stdout,fmt='(A)') ' WRITE command failed.'
endif

close (unit=RWLUN,iostat=err_check)
call Release_LUN (RWLUN)

return

end Subroutine WRITER
