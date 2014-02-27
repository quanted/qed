subroutine CHEMIN(CHEM1,CHELUN)
! CHEMIN reads the chemical input data from the sequential file
! ("CHEMDAT" in batch mode) attached to LUN CHELUN.
! Revised 21-DEC-1985 (LAB) to accomodate IBM file structures.
! Revised 10/21/1988 to convert machine dependencies to run-time solutions
! Revised 12-10-1999 to suppress deprecate negative values in the input stream
! Revised 2004-05-18 to include biolysis study temperatures
use Implementation_Control
use Global_Variables ! EXAMS' input data
use Local_Working_Space
Implicit None
! Local variables in this subroutine
integer :: I, J, K, KSTART, KSTOP, Eof_check, ioerror
integer :: CHELUN
! CHELUN is logical unit number for reading data files
! I, J, and K are loop counters
! KSTART and KSTOP are limits of K loop on chemicals
character(len=3), intent(in) :: CHEM1(*)
character(len=3):: CHEM2(KCHEM)
! CHEM1 and CHEM2 are 3-letter codes for chemical names,
! used to search data files for proper section.
! Separate batch mode file processing from interactive READ
if (CHEM1(1) == 'QQQ') then ! single chemical read from interactive
                            ! file input (READ command)
  KSTART = MCHEMG
  KSTOP = MCHEMG
else                 ! reading from Utility program
  KSTART = 1
  KSTOP = KCHEM
endif
if (CHEM1(1) /= 'QQQ') then ! Utility mode, so
   ! Find appropriate section of chemical data base
   call Assign_LUN (CHELUN)
   open (unit=CHELUN,file='chemdat.dat',status='OLD',position='REWIND')
end if ! Utility program

Chemicals: do K = KSTART, KSTOP
   if (CHEM1(1) /= 'QQQ') then ! Utility program -- find data in flat file
      do
         read (CHELUN,fmt='(A3)',iostat=Eof_check) CHEM2(K)
         if (Eof_check == IOeof) then ! Chemical data base not found in file,
            ! so write error message, set abort flag (IFLAG) to 8, and return
            write (stdout,fmt='(A/A/A)')&
               ' Error in chemical identifier--',&
               ' No data found for compound '//CHEM1(K),&
               ' -- execution terminated.'
            go to 6020 ! set IFLAG = 8 and bail out
         end if
         if (CHEM2(K) == CHEM1(K)) exit
      end do
   end if

   ! Proper section of data base found or interactive READ
   read (CHELUN,fmt='(A50)') CHEMNA(K) !  read name of chemical
   ! Read in the data as needed. First, read which species occur
   read (CHELUN,fmt='(7(I1,1X))') (SPFLGG(I,K),I=1,7)
   ! Check for bogus value
   do I=1,7
      if (SPFLGG(I,K) /= 0 .and. SPFLGG(I,K) /=1) then
         write (stderr, fmt = '(A/5x,A/A,I1,A,I1,A)' ) &
         ' Error in chemical data for ',trim(CHEMNA(K)),&
         ' SPFLG(',I,') is "',SPFLGG(I,K),&
         '." Exams expects either "1" or "0".'
         go to 6020
      end if
   end do
   ! Seven species can occur. SPFLGG flags the chemical species present
   ! SPFLGG  Species
   ! ------  -------
   !   1      SH3      neutral
   !   2      SH4+     singly charged cation
   !   3      SH5++    doubly charged cation
   !   4      SH6+++   triply charged cation
   !   5      SH2-     singly charged anion
   !   6      SH=      doubly charged anion
   !   7      S(3-)    triply charged anion
   !-----------------------------------------------------------------------
   ! Chemical input data is read in via a loop, with loop increments
   ! controlled by SPFLGG. In this way, the input data can be loaded
   ! in blocks that contain data only for those species that actually
   ! exist; non-existent species do not require blocks of null data.

   ! Read in required basic data
   read (CHELUN,5020,err=6000,end=6010) MWTG(K),KOCG(K),KOWG(K)
   ! Check for bogus value
      if (MWTG(K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,ES10.2E3)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' Molecular weight is ',MWTG(K)
         go to 6020
      elseif (KOCG(K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,ES10.2E3)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' Koc is ',KOCG(K)
         go to 6020
      elseif (KOWG(K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,ES10.2E3)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' Kow is ',KOWG(K)
         go to 6020
      end if
   read (CHELUN,5020,err=6000,end=6010) &
         MPG(K),HENRYG(K),EHENG(K),VAPRG(K),EVPRG(K)
   ! Check for bogus value
      if (MPG(K) < -273.15) then
         write (stderr,fmt='(A/5x,A/A,ES10.2E3,A)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' Melting point is ',MPG(K),' C.'
         go to 6020
      elseif (HENRYG(K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,ES10.2E3,A)')&
         ' Error in chemical data for',CHEMNA(K),&
         " The Henry's Law Constant is ",HENRYG(K),' atmosphere-m3/mole.'
         go to 6020
      elseif (EHENG(K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,ES10.2E3)')&
         ' Error in chemical data for',CHEMNA(K),&
         " Henry's Law enthalpy term is ",EHENG(K)
         go to 6020
      elseif (VAPRG(K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,ES10.2E3,A)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' Vapor pressure is ',VAPRG(K),' Torr.'
         go to 6020
      elseif (EVPRG(K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,ES10.2E3,A)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' Molar heat of vaporization is ',EVPRG(K),' kcal/mole.'
         go to 6020
      end if

   ! Now start loop on all species
   species: do J = 1, 7
      if (SPFLGG(J,K) /= 1) cycle species
      read (CHELUN,5020,err=6000,end=6010)&
        SOLG(J,K),ESOLG(J,K),KPSG(J,K),KPBG(J,K),KPDOCG(J,K)
      if (J > 1) read (CHELUN,5020,err=6000,end=6010)&
        PKG(J-1,K),EPKG(J-1,K),KIECG(J-1,K)
      read (CHELUN,5020,err=6000,end=6010) (QYield(I,J,K),I=1,3)
      do I=1,3
      if (QYield(I,J,K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
         ' Error in photochemical data for',CHEMNA(K),&
         ' QYield(',I,',',J,',',K,') is negative.'
         go to 6020
      elseif (QYield(I,J,K) > 1.00000) then
         write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
         ' Error in photochemical data for',CHEMNA(K),&
         ' QYield(',I,',',J,',',K,') is greater than 1.0.'
         go to 6020
      end if
      end do
      read (CHELUN,5020,err=6000,end=6010) (ABSORG(I,J,K),I=1,46)
      do I=1,46
      if (ABSORG(I,J,K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
         ' Error in light absorption data for',CHEMNA(K),&
         ' ABSOR(',I,',',J,',',K,') is ',ABSORG(I,J,K)
         go to 6020
      end if
      end do

      read (CHELUN,5020,err=6000,end=6010) &
         KDPG(J,K),RFLATG(J,K),LAMAXG(J,K)
      read (CHELUN,5020,err=6000,end=6010) (KAHG(I,J,K),I=1,3)
      do I=1,3
      if (KAHG(I,J,K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' KAH(',I,',',J,',',K,') is ',KAHG(I,J,K)
         go to 6020
      end if
      end do
      read (CHELUN,5020,err=6000,end=6010) (EAHG(I,J,K),I=1,3)
      read (CHELUN,5020,err=6000,end=6010) (KNHG(I,J,K),I=1,3)
      do I=1,3
      if (KNHG(I,J,K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' KNH(',I,',',J,',',K,') is ',KNHG(I,J,K)
         go to 6020
      end if
      end do
      read (CHELUN,5020,err=6000,end=6010) (ENHG(I,J,K),I=1,3)
      read (CHELUN,5020,err=6000,end=6010) (KBHG(I,J,K),I=1,3)
      do I=1,3
      if (KBHG(I,J,K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' KBH(',I,',',J,',',K,') is ',KBHG(I,J,K)
         go to 6020
      end if
      end do

      read (CHELUN,5020,err=6000,end=6010) (EBHG(I,J,K),I=1,3)
      read (CHELUN,5020,err=6000,end=6010) (KOXG(I,J,K),I=1,3)
      do I=1,3
      if (KOXG(I,J,K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' KOX(',I,',',J,',',K,') is ',KOXG(I,J,K)
         go to 6020
      end if
      end do
      read (CHELUN,5020,err=6000,end=6010) (EOXG(I,J,K),I=1,3)
      read (CHELUN,5020,err=6000,end=6010) (K1O2G(I,J,K),I=1,3)
      do I=1,3
      if (K1O2G(I,J,K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' K1O2(',I,',',J,',',K,') is ',K1O2G(I,J,K)
         go to 6020
      end if
      end do
      read (CHELUN,5020,err=6000,end=6010) (EK1O2G(I,J,K),I=1,3)
      read (CHELUN,5020,err=6000,end=6010) (KREDG(I,J,K),I=1,3)
      do I=1,3
      if (KREDG(I,J,K) < 0.0) then
         write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
         ' Error in chemical data for',CHEMNA(K),&
         ' KRED(',I,',',J,',',K,') is ',KREDG(I,J,K)
         go to 6020
      end if
      end do
      read (CHELUN,5020,err=6000,end=6010) (EREDG(I,J,K),I=1,3)
      read (CHELUN,5020,err=6000,end=6010) (KBACWG(I,J,K),I=1,4)
      do I=1,4
         if (KBACWG(I,J,K) < 0.0) then
            write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
            ' Error in chemical data for',CHEMNA(K),&
            ' KBACW(',I,',',J,',',K,') is ',KBACWG(I,J,K)
            go to 6020
         end if
      end do
      read (CHELUN,5020,err=6000,end=6010) (QTBAWG(I,J,K),I=1,4)
      read (CHELUN,5020,err=6000,end=6010) (KBACSG(I,J,K),I=1,4)
      do I=1,4
         if (KBACSG(I,J,K) < 0.0) then
            write (stderr,fmt='(A/5x,A/A,I3,A,I3,A,I3,A,ES10.2E3)')&
            ' Error in chemical data for',CHEMNA(K),&
            ' KBACS(',I,',',J,',',K,') is ',KBACSG(I,J,K)
            go to 6020
         end if
      end do
      read (CHELUN,5020,err=6000,end=6010) (QTBASG(I,J,K),I=1,4)
      read (CHELUN,5020,err=6000,end=6010) (QTBTWG(I,J,K),I=1,4)
      read (CHELUN,5020,err=6000,end=6010) (QTBTSG(I,J,K),I=1,4)
      do I=1,4 ! Default value for metabolic studies is 25 C
               ! Values outside 0-100C are presumably errors
         if (QTBTWG(I,J,K)<=0.0 .or. QTBTWG(I,J,K)>100.0) QTBTWG(I,J,K) = 25.0
         if (QTBTSG(I,J,K)<=0.0 .or. QTBTSG(I,J,K)>100.0) QTBTSG(I,J,K) = 25.0
      end do
   end do species
   ! Aquatic aerobic and anaerobic metabolism half-lives (days) are the last
   ! element in the file. If these data are missing, they are set to zero.
   read (CHELUN,5020,err=6000,iostat=Eof_check) AerMet(K), AnaerM(K)
   if (Eof_check == IOeof) then
     AerMet(K) = 0.0; AnaerM(K) = 0.0
   end if
   if (KSTART /= KSTOP) rewind CHELUN ! Utility searches file for next code
end do Chemicals
return

5020 format (8F10.0)
! Various error returns...
6000 write (stderr,fmt='(A)')&
 ' An error occurred while reading the chemical data file.',&
 ' This file must be repaired before the data can be read by Exams.'
go to 6020

6010 write (stderr,fmt='(A)')&
 ' The chemical data file is incomplete.',&
 ' Exams cannot read a partial data file.'

6020 IFLAG=8
return
end subroutine CHEMIN
