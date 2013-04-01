
Module IoSubs

   Use General_Vars
   Implicit None
   Private

   !-- The list of legal logical unit numbers is system-dependent.
   !-- We avoid low-numbered luns to minimize likely system conflicts.
   Integer, Parameter :: Min_Lun =  10
   Integer, Parameter :: Max_Lun = 499

   ! Units 40, 41, and 42 are reserved for Winteracter
   ! Units 15, 16, and 17 are reserved for Dislin
   Integer, Private :: iw
   Logical, Save :: Lun_is_Free(Min_Lun:Max_Lun) = &
      (/ (.True.,  iw = Min_Lun, 14), &
         (.False., iw = 15, 17), &
         (.True.,  iw = 18, 39), &
         (.False., iw = 40, 42), &
         (.True.,  iw = 43, Max_Lun) /)

   !-- Public procedures.
   Public :: Assign_Lun, Release_Lun, Reserve_Lun
   Public :: IORead, IOWrite, IOClose
   Public :: DetermineIoNumbers
   Public :: Display_LUNs
   Public :: Flush_LUNs

   !-- Global variables.
   Integer, Public, Save :: IOeor    ! End of record
   Integer, Public, Save :: IOeof    ! End of file
   Integer, Public, Save :: IOrpeof  ! Reading past end of file

   ! For testing purposes.
   Logical :: qDebug = .False.

Contains

   Subroutine DetermineIoNumbers()

      ! Determine the end of file and end of record status numbers.
      ! Adapted from Redwine.
      !
      !            end of   end of   reading
      ! Compiler   record   file     past EOF
      ! --------------------------------------
      ! Digital    -2       -1       -1
      ! Lahey      -2       -1       -1
      ! SGI        -4006    -4001    -4003
      ! Sun        -1006    -1001    -1003
      !
      ! Digital: DIGITAL Fortran 90 V5.0-492
      ! Lahey: Lahey Fortran 90 Compiler Release 4.50e
      ! SGI: MIPSpro Compilers: Version 7.20 (f90)
      ! Sun: WorkShop Compilers 4.2 10/22/96 FORTRAN 90 1.2

      Implicit None

      Character(Len=1) :: One_char
      Integer          :: uu, stat

      Call Assign_Lun(uu)
      Open (Unit=uu, Status='scratch', &
            Position='rewind', Action='readwrite')

      ! Algorithm:
      !    To determine the "end of file" and "end of record" status numbers
      !    create a file with one character, rewind the file and perform
      !    four non-advancing "reads" of one character, recording the "iostat"
      !    variable after each read:
      !
      !    "Read"    iostat
      !    number    value
      !    ------    ------
      !      1         0 : no errors
      !      2         "end of record"
      !      3         "end of file"
      !      4         "reading past end of file"

      Write(Unit=uu, Fmt='(a1)') '!'
      Rewind(Unit=uu)

      Read(Unit=uu, Fmt='(a1)', Iostat=stat,    Advance='no') One_char
      Read(Unit=uu, Fmt='(a1)', Iostat=IOeor,   Advance='no') One_char
      Read(Unit=uu, Fmt='(a1)', Iostat=IOeof,   Advance='no') One_char
      Read(Unit=uu, Fmt='(a1)', Iostat=IOrpeof, Advance='no') One_char

      Call IOClose(uu)

   End Subroutine DetermineIoNumbers


   Subroutine Assign_Lun(Lun)

      !-- Assign an available Fortran logical unit number.
      !-- Aborts if no Lun can be assigned; there are no error returns.

      Implicit None
      Integer, Intent(Out) :: Lun  !-- Logical unit number.

      Integer :: jstatus
      Logical :: used

      Do Lun = Min_Lun , Max_Lun
         If (Lun_is_Free(Lun)) Then
            Inquire(Unit=Lun, Opened=used, Iostat=jstatus)
            If (jstatus /= 0) used = .True.
            Lun_is_Free(Lun) = .False.
            If (.Not. used) Then
               If (qDebug) Write(6,*) '>>>>> Assign_Lun = ', Lun
               Return
            End If
         End If
      End Do
      Call Display_LUNs(6)
      Stop '?? Assign_Lun: No luns available.'
   End Subroutine Assign_Lun


   Subroutine Reserve_Lun(Lun)

      !-- Reserve a specific Fortran logical unit number.

      Implicit None
      Integer, Intent(In) :: Lun
      !-- Logical unit number.  Illegal values are silently ignored.

      If (Min_Lun<=Lun .And. Lun<=Max_Lun) Lun_is_Free(Lun) = .False.
      If (qDebug) Write(6,*) '>>>>> Reserve_Lun = ', Lun
   End Subroutine Reserve_Lun


   Subroutine Release_Lun(Lun)

      !-- Release a Fortran logical unit number for reuse.
      !-- No checking is done to see that the Lun is actually closed;
      !-- Assign_Lun will check that before re-assigning it.

      Implicit None
      Integer, Intent(In) :: Lun
      !-- Logical unit number.  Illegal values are silently ignored.

      If (Min_Lun<=Lun .And. Lun<=Max_Lun) Lun_is_Free(Lun) = .True.
      If (qDebug) Write(6,*) '>>>>> Release_Lun = ', Lun
   End Subroutine Release_Lun


   Subroutine IORead(Lun, Fname, Ierror, Ok)

      ! Purpose:
      !    - Attach a file to a unit (read access).
      !
      ! Input:
      !    Fname  - name of the file to be attached to Lun.
      !
      ! Output:
      !    Lun    - > 0 : unit logical unit number that was opened.
      !             == -Huge(0) : error detected
      !    Ierror == 0 : File successfully attached to Lun.
      !           /= 0 : error detected
      !           If Ierror is not present, an error message will be
      !           issued to "*"
      !
      !    Ok : Truth of "No errors detected"
      !
      ! [Keywords]  : i/o and file primitives
      !
      ! history:
      ! = [lsr] Thu Jan 14 11:45:00 1999
      !   . ported to f90
      ! = [lsr] Wed Sep 27 09:00:25 1995
      !   . ported to osf/1
      ! = processed by SPAG 3.14A  at 14:44 on 26 Oct 1992

      Implicit None
      Integer,           Intent(Out) :: Lun
      Character(Len=*),  Intent(In)  :: Fname
      Integer, Optional, Intent(Out) :: Ierror
      Logical, Optional, Intent(Out) :: Ok

      Integer :: ios, jer
      Logical :: have_file, issue_error

      ! Errors will be issued if "Ierror" is not present.
      issue_error = (.Not. Present(Ierror))

      jer = 0
      Inquire (file = Fname, exist = have_file)
      If (have_file) Then
         Call Assign_Lun(Lun)
         Open (Unit = Lun, File = Fname, Status = 'old', Position = 'rewind', &
            Action = 'read', Pad = 'yes', Iostat = ios)
         If (ios /= 0) Then
            Call Release_Lun(Lun)
            jer = ios       ! Some system error
            Lun = -Huge(0)
            If (issue_error) Then
               Write (*, '(3a,i0)') ' ?? IORead: Error While trying to Open ', &
                  Trim(Fname), '; error number = ', ios
            End If
         End If
      Else
         jer = -1           ! File not found
         Lun = -Huge(0)
         If (issue_error) Then
            Write (*, '(2a)') ' ?? IORead: Could not find file ', Trim(Fname)
         End If
      End If

      If (Present(Ierror)) Ierror = jer
      If (Present(Ok)) Ok = (jer == 0)

   End Subroutine IORead


   Subroutine IOWrite(Lun, Fname, Ierror, Ok)

      ! Purpose:
      ! - attach a file to a unit (write access; may destroy
      !   a previous version).
      !
      ! input:
      !    Fname  - name of the file to be attached to Lun.
      !
      ! output:
      !    Lun    - > 0 : unit logical unit number that was opened.
      !             == -Huge(0) : error detected
      !    Ierror == 0 : File successfully attached to Lun.
      !           /= 0 : error detected
      !           If Ierror is not present, an error message will be
      !           issued to "*"
      !
      !    Ok : Truth of "No errors detected"
      !
      ! keywords: i/o and file primitives
      !
      ! history:
      ! = [lsr] Thu Jan 14 12:16:01 1999
      !   . ported to f90
      ! = [lsr] Tue Oct  3 10:30:02 1995
      !   . ported to osf/1
      ! = update:   tue 09:43 10-nov-1992.

      Implicit None
      Integer,           Intent(Out) :: Lun
      Character(Len=*),  Intent(In)  :: Fname
      Integer, Optional, Intent(Out) :: Ierror
      Logical, Optional, Intent(Out) :: Ok

      Integer :: ios, jer

      jer = 0
      Call Assign_Lun(Lun)
      Open (Unit = Lun, File = Fname, Status = 'replace',  &
         Position = 'rewind', Action = 'readwrite', Iostat = ios)

      If (ios == 0) Then
         jer = 0
      Else
         Call Release_Lun(Lun)
         jer = ios       ! Some error
         Lun = -Huge(0)
         If (.Not. Present(Ierror)) Then
            Write (*, '(3a,i0)') ' ?? IOWrite: Error while trying to open ', &
               Trim(Fname), '; error number = ', ios
         End If
      End If

      If (Present(Ierror)) Ierror = jer
      If (Present(Ok)) Ok = (jer == 0)

   End Subroutine IOWrite


   Subroutine IOClose(Lun, Fname, Ierror, Xstatus)

      ! purpose:
      !    - close a file and release the Lun.
      !
      ! input:
      !    Lun    - unit logical unit number to be closed.
      !    Fname  - name of the file attached to Lun.
      !
      ! output:
      !    Ierror - 0: always
      !
      ! keywords: i/o and file primitives
      !
      ! history:
      ! = [lsr] Wed 14 Nov 2001 11:42 am
      !   . added optional argument Xstatus
      ! = [lsr] Thu Jan 14 12:16:01 1999
      !   . ported to f90
      ! = [lsr] Wed Sep 27 09:01:35 1995
      !   . ported to osf/1
      ! = processed by SPAG 3.14A  at 14:44 on 26 Oct 1992

      Implicit None
      Integer,                    Intent(In)  :: Lun
      Character(Len=*), Optional, Intent(In)  :: Fname
      Integer,          Optional, Intent(Out) :: Ierror
      Character(Len=*), Optional, Intent(In)  :: Xstatus

      Integer :: ios
      Character(Len=20) :: tstatus

      If (Present(Xstatus)) Then
         tstatus = Xstatus
      Else
         tstatus = 'Keep'
      End If

      Close (Unit = Lun, Iostat = ios, Status = tstatus)
      Call Release_Lun(Lun)
      If (Present(Ierror)) Ierror = ios

   End Subroutine IOClose


   Subroutine Display_LUNs(Jout)

      !-- Display file names attached to units
      !-- Free of charge, will display units 1 to Max_Lun

      Implicit None
      Integer, Intent(In) :: Jout

      Integer :: Lun, jstatus
      Logical :: used
      Character(MaxFileNameLen) :: Fname

      Do Lun = 1, Max_Lun
         Inquire(Unit=Lun, Opened=used, Iostat=jstatus, Name=Fname)
         If (jstatus /= 0) Then
            ! Some error
            Write(Jout, 9230) Lun, jstatus
            9230 Format(1x, '?? IoSubs unit ', i0, ': Error status = ', i0)
         Else If (used) Then
            Write(Jout, 9250) Lun, Trim(Fname)
            9250 Format(1x, '   IoSubs unit ', i0, ' attached to "', a, '"')
         End If
      End Do
   End Subroutine Display_LUNs


   Subroutine Flush_LUNs()

      !-- Flush units. 15 Apr 2002  4:44 pm
      !-- Free of charge, will flush units 1 to Max_Lun

      Implicit None

      Integer :: Lun, jstatus
      Logical :: used

      Do Lun = 1, Max_Lun
         Inquire(Unit=Lun, Opened=used, Iostat=jstatus)
         If (jstatus /= 0) Then
            ! Some error
         Else If (used) Then
            Call FLush(Lun)
         End If
      End Do
   End Subroutine Flush_LUNs

End Module IoSubs
