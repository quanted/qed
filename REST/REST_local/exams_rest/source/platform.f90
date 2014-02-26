Module Implementation_Control
! file Platform.f90
! 27-Sep-2000: LUN 40-42 reserved for use by Winteracter
! 2005-03-16: added WarnLUN for file of non-fatal Exams warnings
Implicit None
Save
Public :: Detect_File_Codes, Set_File_Sizes, Assign_LUN, Release_Lun, &
          Reserve_Lun
! Reserve_LUN can be called by any routine using this module in order to
! exclude a LUN from use. It is not currently (9/2000) used by Exams.
integer, private :: iload ! local counter for loading data
! Set the boundaries on available Logical Unit Numbers
! The list of legal values is system-dependent:
! System                   Range of Legal Values
! Dec F90 for Intel           0 - 119
! VMS F77                     0 -  99
! DEC OSF-1 (Digital Unix)    0 -  (2**31 - 1)
! Low numbers (0-10) are skipped to avoid the most probable system conflicts
integer, private, parameter :: Min_LUN = 10
integer, private, parameter :: Max_LUN = 99
! LUN 40,41,42 are reserved for use by Winteracter
logical, public             :: LUN_is_Free(Min_LUN:Max_LUN) = &
            (/(.true.,iload=Min_LUN,39),(.false.,iload=40,42),&
            (.true.,iload=43,Max_LUN)/)
integer, public, parameter  :: Max_File = 255
! Max_File is the maximum length for fully-qualified file names
! per Microsoft for Windows/DOS
!
! Logical Unit Numbers for keyboard input, screen output, errors, printing
integer, public, parameter :: stdin  = 5 ! for interactive I/O
integer, public, parameter :: stdout = 6 ! for interactive I/O
integer, public, parameter :: stderr = 0 ! for interactive I/O
integer, public, parameter :: printr = 7 ! for the Print command
! ----------------------------------------------------------------------------
! Standard "preconnected" I/O Units; some systems expect a lineprinter LUN
! System Identification    MACHIN code  StdIN  StdOUT  StdERR  PRINTR Max_File
! =====================    ===========  =====  ======  ======  ====== ========
! Linux NAG Compiler         LNX          5      6        0
! Lahey F90 4.5 - DOS        DOS          5      6        0              93
! Lahey F95 (WIN API)                     5      6        0             255
! DEC Digital Unix           DEC          5      6        0
! DEC VMS-F77                DEC          5      6        0             147
! DEC PDP-11/70              PDP          5      5                6
! SunOS                      SUN          5      6        0
! SGI Irix 6.4               SGI          5      6        0
! SGI Irix 6.4 (alternative)            100    101      102
! IBM Mainframe TSO          IBM          5      6                        7
! Siemens 2000 Unix          SMN          1      2                6      41
! Definicon Systems          DSI          0      0
! ----------------------------------------------------------------------------

integer, public, parameter  :: Key_Buffer = 127
! This input buffer matches the DOS keyboard buffer (dings at the right time).
! Lets the length of the input line accommodate the full DOS keyboard buffer;
! character 128 is reserved for <enter>.
character(len=Key_Buffer) :: INPUT  = ' '
! INPUT is the command line to be processed.
character(len=Max_File), dimension(2) :: FILNAM = (/' ',' '/)
! FILNAM holds names of files; two are required so that command files can read
! and write external files.
character(len=Max_File) :: DAFile_Name = 'exams.daf'
! DAFile_Name is the name for Exams' direct access file. If the file is
! not in the default directory, or has been renamed, the new name is
! held for the duration of the interactive session and then discarded.
character(len=Max_File) :: OzFile_Name = 'ozone.daf'
! OzFile_Name is the name for the TOMS direct access file. If the file is
! not in the default directory, or has been renamed, the new name is
! held for the duration of the interactive session and then discarded.
!character(len=3), public, parameter :: MACHIN = 'DOS'
! The variable "MACHIN" is used to identify groups of machines or operating
! systems according to manufacturer or class of operating system in order to
! cope with various eccentricities in their Fortran implementations...
!  Value           Description
!  ------    ----------------------------------------------
!   DOS      Intel 80x86 machines running MS-DOS or PC-DOS
!   DEC      Minicomputers from DEC (PDP and VAX series)
!   IBM      TSO Mainframe environment from IBM
!   OS2      PS/2 and compatibles running OS/2
!   SMN      Siemens Corp. computers

!  MACHNO  is the number of the machine for this version
!          Machines supported are listed below with "Name"
!integer, parameter :: MACHNO = 6
! The number of this implementation is held in MACHNO for selecting LUNs.

!  MACHNO     Name               Description
!  ------    ------      ------------------------------------------------
!    1       VAXATH      VAX at EPA-ORD Athens ERL
!    2       VAXRTP      VAX at EPA National Computer Center at RTP, NC
!    3       VAXSTD      Standard VAX
!    4       PDP-11      DEC PDP11/70 computers
!    5       MS-DOS      Standard MS-DOS pc operating system
!    6       LAHEY       Lahey compiler under MS-DOS
!    7       RMCFAR      Ryan-McFarland compiler under MS-DOS
!    8       SIEMNS      Siemens 2000 series computers
!    9       IBMTSO      Time Sharing Option (TSO) on IBM mainframes
!   10       IBMOS2      IBM System/2 pc operating system OS2
!   11       DSI780      Definicon Systems processor board
!   12       VAXSTA      DEC VAXStation
!   13-16    RESERV      reserved for future expansion

! list of values in use or at least partially implemented...
! SYSTEM            MACHIN   MACHNO
! ----------------  ------   ------
!  DSI                DOS      11
!  Athens-ERL VAX     DEC       1
!  RMF                DOS       7
!  RTP-Castor VAX     DEC       2
!  FOR                DOS       5
!  F7L-Lahey Fortran  DOS       6
!  VAXstation 3100    DEC      12


integer :: AUDLUN=-99
!  AUDLUN  While the AUDIT directive is in effect a copy of
!          user inputs and responses is written to file AUDOUT.
!          AUDLUN also is used in Utility to read file TYPE.
integer :: BASSLUN=-99
!  BASSLUN LUN for writing to BASS transfer file
integer :: DOLUN=-99
!  DOLUN   LUN for reading command files named in FILNAM(1).
!          Also used by Utility program to read file HELPVAR.
integer :: ENVLUN=-99
!  ENVLUN  LUN to read environmental data files--
!          file ENCANON in the Utility program,
!          user-specified file FILNAM(2) in the READ command.
integer :: FG1LUN=-99
integer :: FG2LUN=-99
!  FGnLUN  LUNs for output to FGETS data transfer files
integer :: HWIRLUN=-99
!  HWIRLUN LUN for exposure data transfer to HWIR output file
integer :: KINLUN=-99
!  KINLUN  LUN for writing and reading results of numerical
!          integration in kinetics plotting file KINOUT;
!          also used to access file SPECS in Utility program.
integer :: Oz_UNT=-99
!  Oz_UNT  LUN for the TOMS file support.  Ozone.daf is a
!          direct access file for retrieving total column ozone
!          data derived from the TOMS (Total Ozone Mapping
!          Spectrometer) instrument flown on the Nimbus7 spacecraft.
integer :: PLTLUN=-99
!  PLTLUN  LUN for use by plotting routines to access files
!          SSOUT and KINOUT.
integer :: PRZLUN=-99
!  PRZLUN  LUN for acquiring input from PRZM
integer :: RANUNT=-99
!  RANUNT  LUN for the EXAMDAF file support.  EXAMDAF is a
!          direct access file for retrieving and storing chemical
!          and environmental parameters, for supporting the on-
!          line assistance facility, and for supporting the
!          System Parameters operations (show, describe, etc.)
integer :: RPTLUN=-99
!  RPTLUN  LUN for data written to tabular REPORT file.
integer :: RWLUN=-99
!  RWLUN   LUN for use by WRITE commands to file FILNAM(2),
!          and in Utility program to read file HELPFIL.
integer :: SSLUN=-99
!  SSLUN   LUN for data written to plotting file containing
!          EXAMS' steady-state or time-slice concentrations.
integer :: WRKLUN=-99
!  WRKLUN  LUN for working space file WORKDAF.
!
integer :: ToxCLUN=-99   ! Compartment EcoTox exposure file 
integer :: RskCLUN=-99   ! Compartment EcoRisk file (extrema)
integer :: ToxRLUN=-99   ! Reach-oriented EcoTox exposure file 
integer :: RskRLUN=-99   ! Reach-oriented EcoRisk file (extrema)
integer :: FULLUN =-99   ! Full compartment concentration outputs
integer :: TmpLun1=-99   ! LUN for file CptRisk.tmp scratch file
integer :: TmpLun2=-99   ! LUN for file RchRisk.tmp scratch file
integer :: WarnLUN=-99   ! LUN for warnings file
!
! set print target for hardware (F) or file (T) by indicating whether
! operation of EXAMS is from a "remote" location...
!logical, dimension(16), parameter :: REMOTE = (/.false.,.true.,.false.,&
!   .false.,.false.,.false.,.false.,.false.,.false.,.false.,.false.,.false.,&
!   .false.,.false.,.false.,.false./)
!  REMOTE  Logical variable to indicate that prints should be
!          routed to an intermediate file rather than to hardware, i.e.,
!          .true. means that EXAMS is being run from a remote location.
!
! Variables to store (implementation-dependent) numbers
! returned on end-of-file, end-of-record, and attempt to read past eof.
  Integer, Public :: IOeor    ! end of record
  Integer, Public :: IOeof    ! end of file
  Integer, Public :: IOrpeof  ! attempt to read past end of file
! Examples:
!            end of   end of   reading
! Compiler   record    file    past eof
! -------------------------------------
! SGI        -4006    -4001    -4003
! Digital       -2       -1       -1
! Sun        -1006    -1001    -1003
! Lahey         -2       -1       -1
!
! SGI: MIPSpro Compilers: Version 7.20 (f90)
! Sun: WorkShop Compilers 4.2 10/22/96 FORTRAN 90 1.2
! Digital: DIGITAL Fortran 90 V5.0-492
! Lahey: Lahey Fortran 90 Compiler Release 4.50e

! Storage for file structure parameters
  Integer, Public :: VARCEC, VARIEC, VARREC, VARDEC
  Integer, Public, Parameter  :: LENREC = 8192
! 8192 is LF95 default blocksize
! 512 selected for some Exams implementations because the DOS I/O buffer is 512 bytes.


contains

Subroutine Detect_File_Codes ! Detect numbers returned on end-of-file etc.
Implicit None
Character (Len=1) :: One_char
      ! single character for testing I/O errors
Integer :: stat     ! for acquisition of no-error file I/O status
Integer :: Unit_Number

!    To determine the "end of file" and "end of record" status numbers
!    we create a file with one character, rewind the file, and execute
!    four non-advancing "reads" of one character each, recording the
!    "iostat" variable after each read:
!
!    "Read"    iostat
!    number    value
!    ------    ------
!      1         0        no errors (by F90/F95 standard)
!      2       IOeor      "end of record"
!      3       IOeof      "end of file"
!      4       IOrpeof    "reading past end of file"

call Assign_LUN (Unit_Number)
Open (unit = Unit_Number, status = 'scratch', &
         position = 'rewind', action = 'readwrite')
Write (unit = Unit_Number, fmt = '(a1)') '!'; Rewind (unit=Unit_Number)

Read (unit=Unit_Number, fmt='(a1)', iostat=stat,    advance='no') One_char
Read (unit=Unit_Number, fmt='(a1)', iostat=IOeor,   advance='no') One_char
Read (unit=Unit_Number, fmt='(a1)', iostat=IOeof,   advance='no') One_char
Read (unit=Unit_Number, fmt='(a1)', iostat=IOrpeof, advance='no') One_char

Close (unit = Unit_Number, status = 'delete') 
call Release_LUN(Unit_Number)
return
end Subroutine Detect_File_Codes

! In general, best efficiency can be achieved by matching the record length
! to the default buffer size. However, much of this is controlled by the
! system manager and can't be easily ascertained. Thus, we leave recl at 512
! and work out storage using the Inquire function.
!
! Lahey Fortran90 (v. 4.5) had a 16,348 byte "block size" default
!     in the compiler. Setting LENREC=16348 resulted, however, in excess
!     storage in exams.daf.
! The record length specifier (RECL) of Fortran gives the length of each
!  record for direct access files, or the maximum length of a record in a file
!  connected for sequential access, in "processor-dependent" units.
! In the DEC implementation, RECL is in "longwords," i.e., the
!   record length is given as the number of 4-byte units per record, when
!   the file is connected for unformatted access. For formatted data transfer,
!   RECL is expressed in bytes.
! Could set LENREC to 128 to maintain the same file storage setup
!   as found in 512-byte buffer implementations, i.e., still get
!   integer, parameter :: VARCEC=512,VARIEC=128,VARREC=128,VARDEC=64
!   but use the long-word version of the statement given below to set values:
!   parameter statements-longword specification of direct access record length
!   require setting the number of variables per record via:
!   integer, parameter ::
!               VARCEC=LENREC*4,VARIEC=LENREC,VARREC=LENREC,VARDEC=LENREC/2
! Could set LENREC to 32 (4-byte units) in order to use the default features
!   of the PDP 11/70 linker operating under IAS, thus decreasing overhead.
!   (also evaluate to (VARCEC=128,VARIEC=32,VARREC=32,VARDEC=16))
!   (The default I/O buffer was 132 bytes maximum; setting LENREC
!   to 32 gives 128-byte transfers and thus avoids the added
!   overhead needed if the default value is exceeded.)
! For byte-oriented machines (many microcomputers, UNIX, IBM,
!   Siemens 2000 series) LENREC must be set to 128 to achieve
!   a file architecture equivalent to the DEC design/PDP default;
!   this is desirable IFF the default I/O buffer is <= 128 bytes.
! Under MS-DOS, I/O buffers are 512 bytes long.
! Under CP/M,   I/O buffers are 128 bytes long.
! VARCEC is the number of Characters stored per record.
! VARIEC is the number of integer variables stored per record.
! VARREC is the number of real    variables stored per record.
! VARDEC is the number of real (kind (0D0)) variables per record.
! The length of the file information and data transfer buffers
! are best set to reflect the I/O buffer size of the operating
! system, or the buffer size chosen during site implementation of
! the EXAMS code. These variables are used in dimension statements
! to set up the buffers. I/O interacts with the site implementations
! of the Fortran Numerical Storage Unit and Character Storage Unit.
! For DEC Fortran, the Length of the Numeric Storage Unit (LoNSU)
! is 4 bytes (LoNSU=4), and character storage requires 1 byte per
! character, giving LoCSU=1. For example, the default maximum buffer
! size on the PDP 11/70 is 132. Using the more convenient CP/M
! standard of 128 byte I/O buffers, combined with a LoNSU of four bytes
! (aka a "longword"), gives
!   (VARCEC=128,VARIEC=32,VARREC=32,VARDEC=16), as mentioned above.
! For machines with 2-byte integers (e.g., DEC PDP-11) VARIEC
! could be set at 64 integers per record.
! Example parameter statements for byte-oriented platforms with 4-byte NSU
! integer, parameter :: VARCEC=LENREC,&
!                      VARIEC=LENREC/4,VARREC=LENREC/4,VARDEC=LENREC/8
!

Subroutine Set_File_Sizes ()
! This code attempts to circumvent problems of cross-platform variation
! in the length of the Numeric Storage Unit, Character Storage Unit, short
! integers, etc.
  Implicit None
  Integer, Parameter  :: idim = 16
! the number "16" is an arbitrary choice for "idim" that is assumed to be 
! large enough to encompass the full range of RECL units.
  Integer, Dimension (idim) :: jtemp = 1
  Real, Dimension (idim)    :: rtemp = 1.0e+00
  Real (Kind (0D0)), Dimension (idim) :: dtemp = 1.0d+00
  Character (Len=idim) :: ctemp = 'a'

  Integer :: Length_of_character_idim
  Integer :: Length_of_integer_idim
  Integer :: Length_of_real_idim
  Integer :: Length_of_double_precision_idim

! VARCEC - Characters per record
  Inquire (iolength=Length_of_character_idim) ctemp
  VARCEC = LENREC / Length_of_character_idim * idim

! VARIEC - integers per record
  Inquire (iolength=Length_of_integer_idim) jtemp
  VARIEC = LENREC / Length_of_integer_idim * idim

! VARREC - reals varibles per record
  Inquire (iolength=Length_of_real_idim) rtemp
  VARREC = LENREC / Length_of_real_idim * idim

! VARDEC - double precision variables per record
  Inquire (iolength=Length_of_double_precision_idim) dtemp
  VARDEC = LENREC / Length_of_double_precision_idim * idim

end Subroutine Set_File_Sizes


Subroutine Assign_LUN (LUN)

! Subroutine to assign an available Fortran Logical Unit Number
Implicit None
  integer, intent (out) :: LUN ! the outcome of the discovery process
  integer :: Error_Check
  logical :: LUN_in_use
  do lun = Min_LUN, Max_LUN
    if (LUN_is_Free(LUN)) then ! LUN is marked "free", check to make sure,
                               ! and check the validity of the LUN
      inquire (unit=LUN, Opened=LUN_in_use, iostat = Error_Check)
      if (Error_Check /= 0) LUN_in_use = .true. ! i.e., LUN is unavailable
      LUN_is_Free(LUN) = .false.   ! either already open, invalid, or
                                   ! about to be opened upon return from here
      if (.not. LUN_in_use) return ! with LUN set to the next available value
    end if
  end do

! or...and skip all the calls upon closing files...except then one can't
! reserve certain LUNs, etc., and the inquire function, which may be slow,
! is executed for all the LUNs already open
!do LUN = Min_LUN, Max_LUN
!inquire (unit=LUN, Opened=LUN_in_use, iostat = Error_Check)
!if (Error_Check=0 .and. .not.LUN_in_use) return
!end do

! Arrival at this point signifies catastrophe: no LUN available, but we need
! to open a file in order to continue. This is not recoverable, so
  STOP ' No LUN available for file access! Please notify the author ASAP!'
end Subroutine Assign_LUN

Subroutine Reserve_LUN (LUN)
! This routine allows specific LUNs to be ruled out-of-bounds.
Implicit None
  integer, intent (in) :: LUN
  if (Min_LUN<=LUN .and. LUN<=Max_LUN) LUN_is_free(LUN) = .false.
! Note that requests outside the range Min_LUN to Max_LUN are ignored
! without notification.
end Subroutine Reserve_LUN

Subroutine Release_LUN (LUN)
! This routine marks a LUN as free for use.
! This routine closes the unit if necessary. 
Implicit None
  integer, intent (inout) :: LUN
  integer :: io_error
  logical :: Not_Closed
  inquire (unit=LUN, opened=Not_Closed)
  if (Not_Closed) then
     close (unit=LUN, iostat=io_error)
     if (io_error /= 0) write (stderr,fmt='(/a,I2)')&
          ' Error closing LUN ',LUN 
  end if
  if (Min_LUN<=LUN .and. LUN<=Max_LUN) LUN_is_free(LUN) = .true.
! Note that requests outside the range Min_LUN to Max_LUN are ignored
! without notification.
  LUN = -99 ! LUN is aliased to illegal value for storage
end Subroutine Release_LUN 

!Subroutine Set_Console (Platform)
!Implicit None
!character (len=*), intent(in) :: Platform
!select case (Platform)
! the default values (as set in declarations) are not altered unless known
!  case ("IBM")
!      stdin  =    5  ! keyboard
!      stdout =    6  ! console screen
!  case ("SMN")
!      stdin  =    1  ! keyboard
!      stdout =    2  ! console screen
!      printr =    6  ! line printer
!  case ("PDP")
!      stdin  =    5  ! keyboard
!      stdout =    5  ! console screen
!      printr =    6  ! line printer
!  case ("DSI")
!      stdin  =    0  ! keyboard
!      stdout =    0  ! console screen
!  case default ! most systems...
!      stdin  =     5  ! keyboard
!      stdout =     6  ! console screen
!      printr =     7  ! line printer
!      stderr =     0  ! standard error
!end select
!end Subroutine Set_Console

end module Implementation_Control
