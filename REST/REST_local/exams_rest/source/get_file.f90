subroutine Get_File_Name (Command_Name, File_Name, Success, Action_Request)
! file Get_File.f90
! Purpose--to provide support for opening an external file. The procedure
! -- inputs the file specification information
! -- tests it for syntax
! -- opens the file
! -- if successful, returns the file name to the calling routine
!       to handle input/output operations on the specified file.
! Subroutines required: IMBED, INREC, SKAN, and MATCH
! Developed October 1998 by derivation from older "doit.f90"
! Revisions: 02-Dec-1999 -- add No and Yes as allowed responses to "Replace?"
! Revisions: 08-Feb-2001 -- trap "prn" and "lpt" to forestall access errors
use Implementation_Control
use Input_Output
use MultiScan
! Local variables
Implicit None
character(len=*), intent(in) :: Command_Name
      ! the Exams command that needs a file
character(len=1), dimension(1), parameter :: BLANK=' '
character(len=*), intent (out) :: File_Name

! Max_File is the number of characters allowed for file names.

character(len=*), intent (in) :: Action_Request
! READ if a file must exist (for call from READER)
! WRITE for output files. If the file exists ask for permission to replace it.
! PRINT for output tables to files

logical, intent (out) :: Success ! to register the validity of the name, or
                                 ! permission to proceed with WRITE if
                                 ! file already exists
logical :: DeviceDetected        ! signal that requested file is a device
integer, parameter :: One=1, Two=2, Three=3, Four=4, Five=5, &
      RspSiz=8, RplSiz=20, AppSiz=21

integer :: IMBED,MATCH,IT,I,JSTOP,IL,J, EOF, WHICH
integer, parameter :: MINRES(2)=(/1,1/),       NORESP(2)=(/4,4/)
integer, parameter :: MINRPL(5)=(/1,1,1,1,1/), NORPL(5) =(/4,4,7,2,3/)
integer, parameter :: MINAPP(4)=(/1,1,1,1/),   NOAPP(4) =(/4,4,7,6/)
character(len=1), parameter :: & 
      RESP(RspSiz)=   (/'H','E','L','P',  'Q','U','I','T'/),&
      Replace(RplSiz)=(/'H','E','L','P',  'Q','U','I','T',&
                        'R','E','P','L','A','C','E', 'N','O', 'Y','E','S'/),&
      Append(AppSiz)= (/'H','E','L','P',  'Q','U','I','T',&
                        'R','E','P','L','A','C','E', 'A','P','P','E','N','D'/)

logical :: period_found ! to test for presence of "." in file specification
integer :: IOStatus
File_Name = ' '
Success = .false.

Get_name: do
START = IMBED(INPUT,STOPIT)
if (START == -999) then ! no more non-blank characters in the input buffer
   write (stdout,fmt='(/A,I4,A/A)',advance='NO')&
      ' Enter name of file (no more than',Max_File,' characters)',&
      ' Help, or Quit-> '
   call INREC (EOF,stdin)
      if (EOF == 1) then
          write (stdout,fmt='(/A)')&
             ' "'//trim(Command_Name)//'" command cancelled.'
          Success = .false.
         return
      end if
   STOPIT = 0
   cycle Get_name
end if
call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
if (TYPE == 100) STOPIT = Key_Buffer+1
WHICH = MATCH(TWO,RSPSIZ,NORESP,RESP,MINRES)
select case (WHICH)
case (1) ! Help requested
   write (stdout,fmt='(/,4(/A))')&
      ' "'//trim(Command_Name)//'" requires an external file for processing.',&
      ' In reponse to the prompt, enter a fully-qualified file name.',&
      ' If the file is not in the default directory, include the',&
      ' specifics needed to locate it (e.g., c:\path1\path2\file.ext).'
   write (stdout,fmt='(2(/A)/A,I4/A)')&
      ' An appropriate filename suffix (e.g., ".exa" for command files)',&
      ' will be added if no suffix is present in the name you enter.',&
      ' The maximum length for fully-qualified file names is',Max_File,&
      ' characters; this limit includes the suffix.'
   write (stdout,fmt='(/A,I4,A/A)',advance='NO')&
      ' Enter name of file (no more than',Max_File,' characters)',&
      ' Help, or Quit-> '
   call INREC (EOF,stdin)
      if (EOF == 1) then
         Success = .false.
         write (stdout,fmt='(//A)')&
            ' "'//trim(Command_Name)//'" command cancelled.'
         return
      end if
   STOPIT = 0
   cycle Get_name
case (2) ! Quit requested
   write (stdout,fmt='(/A)') ' "'//trim(Command_Name)//'" command cancelled.'
   Success = .false.
   return
case (0) ! Neither Help nor Quit, thus a presumptive file name
   if (STOPIT-START > Max_File) then ! basic reality check...
      write (stdout,fmt='(/A,I4,A)')&
         ' File names cannot be longer than',Max_File,' characters.'
      cycle Get_name
   else
      exit Get_name
   endif
end select
end do Get_name
                           ! Now decode and test the file specification.
                           ! Code for up to Max_File characters in file
                           ! names, which may include "." and square brackets.
   IT = 0                  ! Pointer to next character in line to be processed
   JSTOP = STOPIT - 1      ! Location of last non-blank character
   IL = 0                  ! Test for closure on [brackets] in specification
   period_found = .false.  ! Test for "." in file (not path) specification

   Find_Period: do I = START, JSTOP
      J = I
      if (INPUT(I:I) == '[') IL = IL+1
      if (INPUT(I:I) == ']') IL = IL-1
      if (INPUT(I:I)=='.' .and. IL == 0 & ! if the brackets are closed, and
      .and. (I>scan(input,"\:/[]",back=.true.))) & ! no more path characters
         then                                   ! (assuming brackets are in
         period_found = .true.                  ! the right order ([])). If
         exit Find_Period                       ! they are not, the error will
      end if                                    ! show up on opening the file.
      ! The tests for brackets allow for VMS account name internals, e.g.,
      ! "[NAME.SUBNAM]filnam.ext". The IL test ensures that the brackets
      ! have been closed. The "\:/[]" test ensures that there are no more 
      ! path specs coming up.
      ! A "." is then taken as the start of a file suffix.
      IT = IT+1
      File_Name(IT:IT) = INPUT(I:I)
   end do Find_Period

   if (period_found .and. J<JSTOP) then ! period followed by non-blank
      do I = J, JSTOP                   ! so load the rest of the user request
         IT = IT+1                      ! which may include ";version_number"
         File_Name(IT:IT) = INPUT(I:I)
      end do
   else  ! either period with trailing blanks, or no period, so
      if (IT+4 < Max_File+1) then ! if there is room, add the suffix
          Add_Suffix: select case (trim(Command_Name))
            case ('DO')
               File_Name(IT+1:IT+4) = '.exa'
            case ('EXAMS')
               File_Name(IT+1:IT+4) = '.daf'
            case ('OZONE')
               File_Name(IT+1:IT+4) = '.daf'
            case ('READ Chemical', 'WRITE Chemical')
               File_Name(IT+1:IT+4) = '.chm'
            case ('READ Environment', 'WRITE Environment')
               File_Name(IT+1:IT+4) = '.env'
            case ('READ Load', 'WRITE Load')
               File_Name(IT+1:IT+4) = '.lod'
            case ('READ PROduct', 'WRITE Product')
               File_Name(IT+1:IT+4) = '.prd'
            case ('Print')
               File_Name(IT+1:IT+4) = '.xms'
            case ('READ Meteorology')
               File_Name(IT+1:IT+4) = '.dvf'
          end select Add_Suffix
          IT = IT + 4
      else                ! If no room for suffix, inform user and cancel
         write (stdout,fmt='(/A/A)')&
            ' File specification does not allow room for suffix.',&
            ' "'//trim(Command_Name)//'" command cancelled.'
         return
      endif
   endif
   if (IT < Max_File) File_Name(IT+1:) = ' ' ! blank out extraneous characters

! Test the validity of the file name
if (Action_Request == 'READ') then
   call CheckForDeviceName(DeviceDetected,Action_Request)
   if (DeviceDetected) return
   inquire (file=trim(File_Name), IOSTAT=IOStatus, Exist=Success)
   if (Success) then ! the file exists, we can proceed
      return ! Calling routines must check that the file is of the right sort
   else ! the file does NOT exist, the logical will be used upon return to
        !  READ to stop processing of the READ command
      write (stdout,fmt='(//A/A)')&
         ' File "'//trim(File_Name)//'" was not found.',&
         ' "'//trim(Command_Name)//'" command cancelled.'
      return
   end if

elseif (Action_Request == 'WRITE') then
   call CheckForDeviceName(DeviceDetected,Action_Request)
   if (DeviceDetected) return
   inquire (file=trim(File_Name), IOSTAT=IOStatus, Exist=Success)
   if (Success) then ! the file already exists, ask the user for instructions
      Instructions: do
      START = IMBED(INPUT,STOPIT)
      if (START == -999) then ! input line is blank
      Success = .false. ! outcome favors protecting existing file
      write (stdout,fmt='(/,3(/A))', advance='NO')&
         ' File "'//trim(File_Name)//'" already exists.',&
         ' May the "'//trim(Command_Name)//'" command replace it?',&
         ' (The old version of "'//trim(File_Name)//'" will be deleted.)'
         write (stdout,fmt='(//A)', advance='NO')&
            ' Enter Replace, Help, or Quit -> '
         call INREC (EOF, stdin)
            if (EOF == 1) then
               write (stdout, fmt= '(/A)')&
               ' "'//trim(Command_Name)//'" command cancelled.'
               Success = .false. ! transfer back to WRITER
               return
            end if
         STOPIT = 0
         cycle Instructions
      end if
      call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
      if (TYPE == 100) STOPIT = Key_Buffer+1
      WHICH = MATCH(Five,RPLSIZ,NORPL,Replace,MINRPL)
      select case (WHICH)
      case (0) ! Neither Help, Quit, nor Replace
         write (stdout,fmt='(/A,I4,A)')&
               ' Response not understood.'
         cycle Instructions
      case (1) ! Help requested
         write (stdout,fmt='(/,5(/A),//A)')&
         ' "'//trim(Command_Name)//'" requires an external file for processing.',&
         ' You have requested that file "'//trim(File_Name)//'" be written.',&
         ' A file of that name already exists. If you want to replace',&
         ' it, respond to the prompt with "Replace." If not, respond with',&
         ' "Quit" and re-enter the "'//trim(Command_Name)//'" command.',&
            ' Enter Replace, Help, or Quit-> '
         call INREC (EOF,stdin)
            if (EOF == 1) then
               Success = .false.
               write (stdout,fmt='(//A)')&
                  ' "'//trim(Command_Name)//'" command cancelled.'
               return
            end if
         STOPIT = 0
         cycle Instructions
      case (2,4) ! Quit requested (or user answered "No")
         write (stdout,fmt='(/A)') &
            ' "'//trim(Command_Name)//'" command cancelled.'
         Success = .false.
         return
      case (3,5) ! Replace requested (or user answered "Yes")
         Success = .true.
         return
      end select
      end do Instructions
   else ! file not present, so Success is .false. Now set the outcome .true.
        ! to indicate to WRITER that it is O.K. to proceed
      Success = .true. ! i.e., O.K. to proceed
      return
   end if
elseif (Action_Request == 'PRINT') then
   call CheckForDeviceName(DeviceDetected,Action_Request)
   if (DeviceDetected) return
   inquire (file=trim(File_Name), IOSTAT=IOStatus, Exist=Success)
   if (Success) then ! the file already exists, ask the user for instructions
      Append_Instructions: do
      START = IMBED(INPUT,STOPIT)
      if (START == -999) then ! input line is blank
      Success = .false.       ! outcome favors protecting existing file
      Append_Lines = .true.
      write (stdout,fmt='(/,4(/A))', advance='NO')&
      ' A file named "'//trim(File_Name)//'"',&
      ' already exists. Should "'//trim(Command_Name)//'" replace it,',&
      ' or do you want to append more outputs to the existing file?',&
      ' (If you choose "replace", the old version of "'&
      //trim(File_Name)//'" will be deleted.)'
         write (stdout,fmt='(//A)', advance='NO')&
            ' Enter Append, Replace, Help, or Quit -> '
         call INREC (EOF, stdin)
            if (EOF == 1) then
               write (stdout, fmt= '(/A)')&
               ' "'//trim(Command_Name)//'" command cancelled.'
               Success = .false. ! transfer back to LIST (operating as Print)
               return
            end if
         STOPIT = 0
         cycle Append_Instructions
      end if
      call SKAN (INPUT,START,STOPIT,TYPE,BLANK)
      if (TYPE == 100) STOPIT = Key_Buffer+1
      WHICH = MATCH(Four,AppSiz,NOAPP,Append,MINAPP)
      select case (WHICH)
      case (0) ! Nor Help, Quit, Replace, Append
         write (stdout,fmt='(/A,I4,A)')&
               ' Response not understood.'
         cycle Append_Instructions
      case (1) ! Help requested
         write (stdout,fmt='(/,8(/A),//A)')&
' "'//trim(Command_Name)//'" will place its output in a file.',&
' You have requested that file "'//trim(File_Name)//'" be used.',&
' A file of that name already exists. If you want to replace',&
' it, respond to the prompt with "Replace" (the existing version',&
' will be deleted and a new file created).If you just want to add',&
' additional outputs to "'//trim(File_Name)//'", respond to the',&
' the prompt with "Append." If you want to create a completely new file',&
' respond with "Quit" and re-enter the "'//trim(Command_Name)//'" command.',&
' Enter Append, Replace, Help, or Quit-> '
         call INREC (EOF,stdin)
            if (EOF == 1) then
               Success = .false.
               write (stdout,fmt='(//A)')&
                  ' "'//trim(Command_Name)//'" command cancelled.'
               return
            end if
         STOPIT = 0
         cycle Append_Instructions
      case (2) ! Quit requested
         write (stdout,fmt='(/A)') &
            ' "'//trim(Command_Name)//'" command cancelled.'
         Success = .false.
         return
      case (3) ! Replace requested
         Success = .true.
         Append_Lines = .false.
         return
      case (4) ! Append requested
         Success = .true.
         Append_Lines = .true.
         return
      end select
      end do Append_Instructions
   else ! file not present, so Success is .false. Now set the outcome .true.
        ! to indicate to WRITER that it is O.K. to proceed
      Success = .true. ! i.e., O.K. to proceed
      Append_Lines = .false.
      return
   end if

end if
return
contains


subroutine CheckForDeviceName(DeviceDetected,CallingCommand)
! To test for user request of a system device.
! Preserve the current values of INPUT, START, and STOPIT for further
! processing, set INPUT to the first three characters of the requested
! file name, alias START and STOPIT to yield device lengths, and test.
! Restore INPUT, START, and STOPIT for further processing in any case.
! If a device name is requested, kill the command and return.
! Anything starting with "prn" or "lpt" is rejected.
logical, intent(out) :: DeviceDetected
! local variables to preserve the state of the user input
! while testing file specifications for device names
character(len=Key_Buffer) :: INPUTSave  = ' '
integer :: STOPITSave,STARTSave
! Parameters for passing to MATCH
integer, parameter :: DeviceSiz=12
integer, parameter :: MINDevice(4)=(/3,3,3,3/), NODevice(4)=(/3,3,3,3/)
character(len=1), parameter :: Device(DeviceSiz) = &
   (/'P','R','N','L','P','T','C','O','N','C','O','M'/)
character (len=*) :: CallingCommand
DeviceDetected=.false.
INPUTSave=INPUT;STOPITSave=STOPIT;STARTSave=START
input=' ';input=File_Name(1:3);stopit=4;start=1
WHICH = MATCH(4,DeviceSiz,NODevice,Device,MINDevice)
INPUT=INPUTSave;STOPIT=STOPITSave;START=STARTSave
select case (WHICH)
   case (0) ! no action required
   case (1,2,3,4) ! possibly attempting to write to a system device...
      write (stderr,fmt='(A/A)')&
         ' PRN, LPT, COM, and CON are reserved names of system devices.',&
         ' They cannot be used as file names. '//CallingCommand//' cancelled.'
      DeviceDetected=.true.
      return
end select

end subroutine CheckForDeviceName
end subroutine Get_File_Name
