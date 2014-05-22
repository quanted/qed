subroutine PLOTX(FIXFIL,MCHEMG,KOUNT)
! Purpose: to determine what type of plot requested.
! Note: The plotting area is controlled by the following
!    XWIDTH  - width of the plotting area
!    MINBAR  - minimum width of a bar
!    AREA must be dimensioned (21)*XWIDTH
! Reals for transfer of values from files --
! YW for water column segments, YB for benthic segments.
! Revised 28-NOV-1985 (LAB) to accomodate IBM file structures.
! Revisions 10/21/88--run-time implementation of machine dependencies
use Floating_Point_Comparisons ! Revisions 09-Feb-1999
use Implementation_Control
use Input_Output
Implicit None
integer, intent(in) :: KOUNT
real :: Y(KOUNT+2),YW(KOUNT),YB(KOUNT),YLEN=4.0,RESULT,YMIN,YMAX,RANGE,YPRT
integer, parameter :: One = 1
integer :: XWIDTH=61,MINBAR=3,FIXFIL,MCHEMG,EOF,MAXPRM,I0,IT,KIN
integer :: WIDTH=11,WIDN,N,N1,N2,MAXY=21,Y1,Y2,XCOOD,XOFF,UP,XLOC
integer :: VLEN,ISTRT,INC,K,IZON, File_Check
integer, dimension(5) :: VTXTLN=(/10,14,18,10,9/), VALSTR=(/1,12,26,44,54/)
integer :: I,I1,I2,I3,I4,NC,IOPT,IDAT,IVAL,IMBED,IERR
! Integers for transfer of segment numbers
integer, dimension(KOUNT) :: NOTE, NOTE1, NOTE3
character(len=1) :: CCHAR, UNDER = '_'
! Characters for transfer of segment types
character(len=1), dimension(KOUNT) :: NOTE2, NOTE4, NOTEE
character(len=1), dimension(4) :: VALEND = (/'L',' ','K','G'/)
character(len=1), dimension(62) :: VALTXT = &
   (/'T','o','t','a','l',' ','m','g','/','L',' ','D','i',&
   's','s','o','l','v','e','d',' ','m','g','/','L','P','a',&
   'r','t','i','c','u','l','a','t','e','s',' ','m','g','/',&
   'k','g','B','i','o','t','a',' ','u','g','/','g','M','a',&
   's','s',' ','g','/','m','2'/)
character(len=61), dimension(21) :: AREA
character(len=1), dimension(28)  :: BLABEL = &
   (/'W','a','t','e','r',' ','C','o','l','u','m','n',&
     'B','o','t','t','o','m',' ','S','e','d','i','m','e','n','t','s'/)
character(len=1), dimension(21) :: CONC = (/(' ',i=1,4),&
   'C','o','n','c','e','n','t','r','a','t','i','o','n',(' ',i=18,21)/)
character(len=1), dimension (21,4) :: POLABL = reshape ((/ &
   (' ',i=01,07),'A','v','e','r','a','g','e',(' ',i=15,21),&
   (' ',i=22,28),'M','a','x','i','m','u','m',(' ',i=36,42),&
   (' ',i=43,49),'M','i','n','i','m','u','m',(' ',i=57,63),&
   (' ',i=64,70),'M','i','n','m','a','x',(' ',i=77,84)/),(/21,4/))

character(len=1), dimension(21,5) :: PRLABL = reshape ((/ &
   (' ',i=1,5),'T','o','t','a','l',' ','m','g','/','L',(' ',i=16,21),&
   (' ',i=22,25),'D','i','s','s','o','l','v','e','d',' ',&
                 'm','g','/','L',' ',' ',' ',&
   ' ','P','a','r','t','i','c','u','l','a','t','e','s',' ',&
                 'm','g','/','k','g',' ',' ',&
   (' ',i=64,69),'B','i','o','t','a',' ','u','g','/','g',(' ',i=80,84),&
   (' ',i=85,90),'M','a','s','s',' ','g','m','2',(' ',i=99,105)/),(/21,5/))

AREA = ' '  ! blank the array
NC = MCHEMG
! determine type of plotting option, POINT, PROFILE, or KINETIC
call TYPOPT (IOPT)
select case (IOPT)
case (-1,4) ! end-of-file or QUIT request
   write (stdout, fmt='(/A)') ' PLOT cancelled.'
   return
case (5) ! Kinetic plot
   call KINOPT (KIN)
   if (KIN == -1 .or. KIN == 4) then ! end-of-file or QUIT request
      write (stdout, fmt='(/A)') ' PLOT cancelled.'
      return
   end if
   call Assign_LUN (PLTLUN)
   open (unit=PLTLUN, status='OLD', access='SEQUENTIAL',&
         form='UNFORMATTED', position='REWIND', file='kinout.plt',&
         action='read', iostat=File_Check)
   if (File_Check /= 0 ) then ! error opening file
      write (stdout,fmt='(A/A)')&
         ' Error opening results file "kinout.plt"',&
         ' PLOT command cancelled.'
      call Release_LUN (PLTLUN)
      return
   end if
   call KINET (KIN,MCHEMG,KOUNT)
   close (unit=PLTLUN,iostat=File_Check)
   call Release_LUN (PLTLUN)
   return
end select
! open the file for Point and Profile plots
call Assign_LUN (PLTLUN)
open (unit=PLTLUN, status='OLD', access='SEQUENTIAL',&
      form='UNFORMATTED', position='REWIND', file='ssout.plt',&
      action='read', iostat=File_Check)
if (File_Check /= 0 ) then ! error opening file
   write (stdout,fmt='(A/A)')&
      ' Error opening results file "ssout.plt"',&
      ' PLOT command cancelled.'
   call Release_LUN (PLTLUN)
   return
end if
call DATOPT (IDAT)               ! now get the concentration type
if (IDAT == -1 .or. IDAT == 7) then  ! end-of-file or QUIT request
   write (stdout, fmt='(/A)') ' PLOT cancelled.'
   close (unit=PLTLUN,iostat=File_Check)
   call Release_LUN (PLTLUN)
   return
end if

Plot_type: select case (IOPT) ! 1 for POINT, 2 for PROFILE
case (1) ! POINT plot
   call STAOPT (IVAL)        ! get the statistical type for the 'POINT' plot
   if (IVAL == -1 .or. IVAL == 5) then  ! end-of-file or QUIT request
      write (stdout, fmt='(/A)') ' PLOT cancelled.'
      close (unit=PLTLUN,iostat=File_Check)
      call Release_LUN (PLTLUN)
      return
   end if

! undocumented/incomplete feature...put chemical number at end of command
   ! More input? if so, interpret as the number of the chemical
   START = IMBED(INPUT,STOPIT)
   if (START /= -999) then
      NC = MCHEMG
      call GETNUM (IERR,RESULT)
      if (IERR == 0) then
         NC = int(RESULT)
      else
         write (stdout,5010) IERR
         5010 format (//' Error converting chemical number. Error',I4)
      endif
   endif

   ! do a "POINT" plot
   call SHOPLO (FIXFIL,1,I1,I2,I3,IERR,PLTLUN,stdout)
   if (IERR /= 0) then
      call Error_check
      return
   end if
   ! get the IVAL record of the IZON type
   N = 2
   WIDTH = 11
   WIDN = WIDTH+1
   XOFF = WIDTH/2
   if (mod(WIDTH,2) == 0) XOFF = XOFF+1
   if (NC<1 .or. NC>I1) then
      write (stdout,fmt='(//A,I3,A/A)')& ! Chemical out-of-range
         ' No chemical numbered ',NC,' is present in the file.',&
         ' Please review the following and try again.'
      call SHOPLO (FIXFIL,0,I1,I2,I3,IERR,PLTLUN,stdout)
      close (unit=PLTLUN,iostat=File_Check)
      call Release_LUN (PLTLUN)
      return
   end if
   do I = 1, NC
      call PRODAT (EOF,YW,YB,N1,N2,NOTE1,NOTE2,NOTE3,NOTE4,IDAT)
      if (EOF == 1) then
         write (stdout,fmt='(A)') ' PLOT cancelled.'
         close (unit=PLTLUN,iostat=File_Check)
         call Release_LUN (PLTLUN)
         return
      end if
      call PONDAT (EOF,NOTE,NOTEE,Y,IVAL,IDAT)
      if (EOF == 1) then
         write (stdout,fmt='(A)') ' PLOT cancelled.'
         close (unit=PLTLUN,iostat=File_Check)
         call Release_LUN (PLTLUN)
         return
      end if
   end do
   ! plot it--put in underscores
   N1 = N*WIDN
   do I = 1, N1
      AREA(MAXY)(I:I) = UNDER
   end do
   ! map data to axes and compute plotting factors
   call SKALE (Y,YLEN,N,1,KOUNT+2)
   YMIN = Y(N+1)
   YMAX = YMIN+YLEN*Y(N+2)
   RANGE = YMAX-YMIN
   if (RANGE .LessThanOrEqual. 0.0) RANGE = 1.0
   do I = 1, N ! fill in area with plotting information
      ! compute location of the lower left coordinate of the current bar
      XCOOD = WIDN*(I-1)+2
      ! compute the height of the bar
      Y1 = (Y(I)-YMIN)/RANGE*MAXY+0.5
      call XBAR (XCOOD,Y1,WIDTH,MAXY,AREA,NOTE(I),NOTEE(I))
      ! Get the length of the vertical label
      VLEN = VTXTLN(IDAT)
      if (IDAT == 1) then ! Move units to the label area
         if (I == 2) then
            VALTXT(10) = VALEND(3)
            VALTXT(11) = VALEND(4)
            VLEN = 11
         else
            VALTXT(10) = VALEND(1)
            VALTXT(11) = VALEND(2)
            VLEN = 10
         endif
      end if
      ! Get starting location of the string
      ISTRT = VALSTR(IDAT)
      ! Move label to plotting area
      XLOC = XCOOD+XOFF
      Y2 = MAXY-VLEN-1
      do I4 = 1, VLEN
         AREA(Y2+I4)(XLOC:XLOC) = VALTXT(ISTRT+I4-1)
      end do
   end do
   INC = 0
   ! Transfer the plot to the output device
   CCHAR = 'I'
   write (stdout,fmt='(///)')
   do I = 1, MAXY
      if (I == MAXY) CCHAR = '+'
      ! Determine the location of the last non-blank character in this row
      K = max(1,len_trim(AREA(I)))
      UP = K
      if (mod(I,5) == 1) then ! Place a label every 5 lines
         INC = INC+1
         YPRT = YMAX-(INC-1)*Y(N+2)
         write (stdout,5030) &
            POLABL(I,IVAL),CONC(I),YPRT,CCHAR,AREA(I)(1:UP)
      else
         write (stdout,5040) &
            POLABL(I,IVAL),CONC(I),CCHAR,AREA(I)(1:UP)
      endif
   end do
   write (stdout,fmt="(20X,' Water Col',4X,'Benthic')")
case (2) ! PROFILE plots
   call ZONOPT (IZON) ! Get the 'ZONE' or 'ENVIRONMENT'
   if (IZON==-1 .or. IZON==4) then  ! end-of-file or QUIT request
      write (stdout, fmt='(/A)') ' PLOT cancelled.'
      close (unit=PLTLUN,iostat=File_Check)
      call Release_LUN (PLTLUN)
      return
   end if

   ! Undocumented feature...can add chemical number on end of command
   ! More input?
   START = IMBED(INPUT,STOPIT)
   if (START /= -999) then
      NC = MCHEMG
      call GETNUM (IERR,RESULT)
      if (IERR == 0) then
         NC = int(RESULT)
      else
         write (stdout,5010) IERR
      end if
   end if
   ! do the 'PROFILE' plot
   call SHOPLO (FIXFIL,1,I1,I2,I3,IERR,PLTLUN,stdout)
   if (IERR /= 0) then
      call Error_check
      return
   end if
   if (NC<1 .or. NC>I1) then
      write (stdout,fmt='(//A,I3,A/A)')& ! Chemical out-of-range
         ' No chemical numbered ',NC,' is present in the file.',&
         ' Please review the following and try again.'
      call SHOPLO (FIXFIL,0,I1,I2,I3,IERR,PLTLUN,stdout)
      close (unit=PLTLUN,iostat=File_Check)
      call Release_LUN (PLTLUN)
      return
   end if
   do I = 1, NC
      call PRODAT (EOF,YW,YB,N1,N2,NOTE1,NOTE2,NOTE3,NOTE4,IDAT)
      if (EOF == 1) then
         write (stdout,fmt='(A)') ' PLOT cancelled.'
         close (unit=PLTLUN,iostat=File_Check)
         call Release_LUN (PLTLUN)
         return
      end if
      if (I /= NC) call PONDAT (EOF,NOTE,NOTEE,Y,One,One)
      if (EOF == 1) then
         write (stdout,fmt='(A)') ' PLOT cancelled.'
         close (unit=PLTLUN,iostat=File_Check)
         call Release_LUN (PLTLUN)
         return
      end if
   end do
   ! set up array for plotting
   if (IZON == 1) then  ! do water column
      do I = 1, N1
         Y(I) = YW(I)
         NOTE(I) = NOTE1(I)
         NOTEE(I) = NOTE2(I)
      end do
   else                 ! do the sediments
      do I = 1, N2
         Y(I) = YB(I)
         NOTE(I) = NOTE3(I)
         NOTEE(I) = NOTE4(I)
      end do
   endif
   N = N1
   if (IZON == 2) N = N2
   if (N == 0) then
      write (stdout,fmt='(//A/)')&
         ' No data available. PLOT cancelled.'
      close (unit=PLTLUN,iostat=File_Check)
      call Release_LUN (PLTLUN)
      return
   endif
   ! there are "N" parameters to be plotted
   MAXPRM = (XWIDTH-1)/(1+MINBAR)
   if (N > MAXPRM) then
      write (stdout,fmt='(//1X,I5,A,I3,A/A/A,I5,A/)') N, &
         ' exceeds the maximum number (',MAXPRM,')',&
         ' of parameters that can be plotted.',&
         ' Only the first ',MAXPRM,' parameters will be plotted.'
      N = MAXPRM
   endif
   WIDTH = (XWIDTH-1)/N-1
   if (WIDTH > 11) WIDTH = 11
   ! underscore
   WIDN = WIDTH+1
   N1 = N*WIDN
   do I = 1, N1
      AREA(MAXY)(I:I) = UNDER
   end do
   call SKALE (Y,YLEN,N,One,KOUNT+2)
   YMIN = Y(N+1)
   YMAX = YMIN+YLEN*Y(N+2)
   RANGE = YMAX-YMIN
   if (RANGE .LessThanOrEqual. 0.0) RANGE = 1.0
   do I = 1, N
      XCOOD = WIDN*(I-1)+2
      Y1 = (Y(I)-YMIN)/RANGE*MAXY+0.5
      call XBAR (XCOOD,Y1,WIDTH,MAXY,AREA,NOTE(I),NOTEE(I))
   end do
   INC = 0
   CCHAR = 'I'
   write (stdout,fmt='(///)')
   ! test for nonstandard label, i.e., TOTAL
   if (IZON == 2) then
      PRLABL(15,1) = 'K'
      PRLABL(16,1) = 'G'
   else
      PRLABL(15,1) = 'L'
      PRLABL(16,1) = ' '
   endif
   do I = 1, MAXY
      if (I == MAXY) CCHAR = '+'
      K = max(1,len_trim(AREA(I)))
      UP = K
      if (mod(I,5) == 1) then    ! enter values every fifth row
         INC = INC+1
         YPRT = YMAX-(INC-1)*Y(N+2)
         write (stdout,5030)&
            PRLABL(I,IDAT),CONC(I),YPRT,CCHAR,AREA(I)(1:UP)
      else
         write (stdout,5040)&
            PRLABL(I,IDAT),CONC(I),CCHAR,AREA(I)(1:UP)
      endif
   end do
   if (IZON == 1) then
      I0 = 0
      IT = 12
   else
      I0 = 12
      IT = 16
   endif
   AREA(1) = ' '
   VLEN = (1+(1+WIDTH)*N)/2
   VLEN = VLEN-IT/2-1
   if (VLEN < 0) VLEN = 0
   do I = 1, IT
      I0 = I0+1
      AREA(1)(VLEN+I:VLEN+I) = BLABEL(I0)
   end do
   write (stdout,fmt='(10X,A)') AREA(1)
end select Plot_type

close (unit=PLTLUN,iostat=File_Check)
call Release_LUN (PLTLUN)
return
5030 format (1X,A1,1X,A1,1X,1PE9.2,3X,'-',A1,A)
5040 format (1X,A1,1X,A1,14X,A1,A)
contains
Subroutine Error_check
select case (IERR)
case (1) ! FIXFIL = 0, results not available
   write (stdout,fmt='(3(A/))')&
      ' FIXFIL indicates results are not available.',&
      ' Enter "HELP FIXFIL" for assistance.',&
      ' PLOT command cannot be executed.'
   close (unit=PLTLUN,iostat=File_Check)
   call Release_LUN (PLTLUN)
   return
case (2) ! end-of-file reading plot file
   write (stdout,fmt='(2(A/))')&
      ' The plot file ended unexpectedly.',&
      ' PLOT cancelled.'
   close (unit=PLTLUN,iostat=File_Check)
   call Release_LUN (PLTLUN)
   return
case (3) ! error reading plot file
   write (stdout,fmt='(2(A/))')&
      ' Error encountered reading the plot file.',&
      ' PLOT cancelled.'
   close (unit=PLTLUN,iostat=File_Check)
   call Release_LUN (PLTLUN)
   return
end select
end Subroutine Error_check
end subroutine PLOTX
