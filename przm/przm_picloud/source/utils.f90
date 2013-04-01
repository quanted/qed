Module m_utils

   Implicit None
   Private
   Public :: GetArgs, get_int

Contains

   Subroutine GetArgs (RunFilePath)

      ! Read arguments from the PRZM execution line
      ! Arg-1: Path of input file 'przm3.run'

      ! RunFilePath: Path of input file 'przm3.run'.
      !           On output:
      !           * Either blank (if no argument was present)
      !           * Or contains a trailing delimiter (":" or "\").

      Use General_Vars
      Use F2kCLI
      Implicit None
      Character(Len=*), Intent(Out) :: RunFilePath

      Integer :: nargs, j0, j1, flen
      Character(Len=MaxFileNameLen) :: xarg

      RunFilePath = ''

      ! nargs contains the number of arguments present in the
      ! command line. No arguments -- exit.
      nargs = Command_Argument_Count()
      If (nargs <= 0) Return

      ! The first argument contains the input file path.
      ! * Remove balanced double quotes, if present
      ! * If the path looks like "x:", i.e., a drive
      !   letter followed by a colon, Do no more.
      ! * Otherwise make sure the path has a trailing backslash "\".
      Call Get_Command_Argument(1, xarg)
      j1 = Len_trim(xarg)
      j0 = 1
      If (xarg(j0:j0) == '"') Then
         If (xarg(j1:j1) == '"') Then
            j0 = j0 + 1
            j1 = j1 - 1
         End If
      End If

      flen = Len(RunFilePath)
      If ((j1-j0+1) > flen) Then
         ! This is ugly: the path is too long to store in the user's variable,
         ! and the log file has not been open yet. Issue a message to the screen
         ! and abort.
         Stop 'Increase the length of "RunFilePath"'
      End If
      RunFilePath = xarg(j0:j1)
      j1 = Len_trim(RunFilePath)

      ! Empty string -- exit.
      If (j1 <= 0) Return

      ! Add trailing directory delimiter?
      Select Case (RunFilePath(j1:j1))
      Case (':', '\', '/')
         ! Last characters is a trailing directory delimiter: Leave things as they are.
      Case Default
         ! anything else, append trailing backslash
         ! 7-18-11: change to forward slash for Unix (eca)
         j1 = j1 + 1
!eca     RunFilePath(j1:j1) = '\'
         RunFilePath(j1:j1) = '/'
      End Select

   End Subroutine GetArgs



   Subroutine CutToSize(Xin, OutLength, Xout)

      ! Given a string Xin, of length greater than
      ! OutLength, remove characters from the center
      ! of the string and replace them with "...", so
      ! that the final length of the string is OutLength.
      ! The modified string is returned in Xout.
      !
      ! If the length of Xin is less than or equal to OutLength,
      ! no characters are deleted -- Xout is set equal to Xin.
      !
      ! Example
      ! Xin = "1:/4 678/01234/67 9/1234/67 9/123456 89/file.ext"
      ! OutLength = 40
      ! ==> Xout = "1:/4 678/01234/...7 9/123456 89/file.ext"
      Implicit None
      Character(Len=*),  Intent(In) :: Xin
      Integer,           Intent(In) :: OutLength
      Character(Len=*), Intent(Out) :: Xout

      Integer :: ilen, m1, m2, adjustedLength, maxc
      Integer :: ir, ia, ib, To_remove
      Character(Len=*), Parameter :: ReplacementChars = '...'
      Integer, Parameter :: rlen = Len(ReplacementChars)

      ilen = Len_Trim(Xin)
      If (ilen <= OutLength) Then
         Xout = Xin
         Return
      End If

      ! ilen > OutLength
      ! Try to keep the drive letter and the name of
      !     the file complete.

      m1 = Index(Xin(1:ilen), '\:/')
      If (m1 == 0) m1 = 1
      m2 = Index(Xin(1:ilen), '\:/', Back=.True.)
      If (m2 == 0) m2 = ilen

      ! If the length of Drive letter + file name too long
      ! then process the whole string.
      If (m1 + m2 > OutLength) Then
         m1 = 1
         m2 = ilen
      End If

      ! To_remove -- number of characters from which to remove
      To_remove = m2 - m1 - 1    ! "- 1" is correct.

      ! ia (i.e., ia - 1 + 1) is the number of characters to be
      !     kept from the leading edge of the string
      ! (ilen - ib + 1) is the number of characters to be
      !     kept from the trailing edge of the string
      ! adjustedLength is the lenght of the final string without
      !     the replacement characters.
      !
      ! Therefore:
      !     ia + (ilen - ib + 1) == adjustedLength
      ! ==> ib = 1 - adjustedLength + ia + ilen

      adjustedLength = OutLength - rlen
      ir = (ilen - adjustedLength) / 2    ! half of characters to remove
      ia = To_remove/2 - ir + m1
      ib = 1 + ilen - adjustedLength + ia

      Xout = Xin(1:ia) // ReplacementChars // Xin(ib:ilen)


   End Subroutine CutToSize
   
   subroutine get_int(xbuffer, was_present, xerror, ivalue)
   
   ! get an integer in xbuffer.
   ! xbuffer - should contain an integer value or blanks
   ! was_present - truth of "xbuffer contained a value"
   ! xerror - truth of "error while trying to decode the number)
   ! ivalue -- value found.
   
   Character(Len=*), Intent(In) :: xbuffer
   Logical, Intent(Out) :: was_present, xerror
   Integer, Intent(Out) :: ivalue
   
   Integer :: ilen, iostatus
   character(Len=Len(xbuffer)) :: xcopy
   character(len=20) int_format
   
   
   xerror = .False.
   xcopy = adjustL(xbuffer)
   ilen = len_Trim(xcopy)
   Write(int_format, 9100) ilen
9100  format('(i', i0, ')')   
   
  
   If (ilen == 0) Then
      ! xcopy contains only blanks
      was_present = .False.
      xerror = .False.
      
   Else
	! Sun Apr 16 18:58:53 EDT 2006 
   	! [lsr] after putzing around for 2 hrs. tring to get the fmt=* to work, and failing,
	! i got the read statement with fmt=int_... to work, then went back
	! to the fmt=*.... Now it works! I am leaving both statements here just in case
	! weirdness reappears. 	
      !Read(xcopy(1:ilen), fmt=int_format, iostat = iostatus) ivalue
      Read(xcopy(1:ilen), fmt=*, iostat = iostatus) ivalue
      xerror = (iostatus /= 0)
      was_present = (.Not. xerror)
   End if
   
   ! if not present give ivalue a bogus value.
   if (.Not. was_present) ivalue = -Huge(ivalue)
   
   end subroutine get_int
 
End Module m_utils

