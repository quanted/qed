
!> Replace 1.0d-30 et al. with Huge, Tiny, etc.
!       Include file CMPLR.PAR (Compiler and hardware specific
!                               parameters).
!------- The following are used in the program supplied functions.
      REAL*8 REALMX , REALMN , EXPMN , EXPMX , EXNMX
      INTEGER*4 MAXINT
      LOGICAL PCASCI , WINDOW , NONPC
      INTEGER*2 MAXREC
!------- Specify maximum and minimum allowable real numbers.
      PARAMETER (REALMX=1.0D30,REALMN=1.0D-30)
!------- Maximum allowable integer and record length.
      PARAMETER (MAXINT=2147483647)
      PARAMETER (MAXREC=512)
!------- Set limits for exponential function.
!     EXP(EXNMX) = 0.0
!     EXP(EXPMN) = 1.0
!     EXP(EXPMX) > REALMX, overflow condition
      PARAMETER (EXNMX=-53.0,EXPMN=REALMN,EXPMX=53.0)
!------- Set WINDOW to TRUE if window ouput is desired (it should).
! From subroutine PZSCRN: display to IBM-PC computers w/ANSI.SYS
!     installed in CONFIG.SYS. If this is not the system
!     being used, set the parameter WINDOW (in PCMPLR.INC) to .FALSE.
!     and the screen display will be replaced with a list-type
!     display (eg. any computer or terminal CRT or printer)
! Windows 2000 & XP Do not support ansi.sys
!     PARAMETER (WINDOW = .TRUE.)
      PARAMETER (WINDOW=.FALSE.)
!------- Set PCASCI to TRUE if PC-compatible is being used.
      PARAMETER (PCASCI=.TRUE.)
!------- Set NONPC to TRUE if NON-PC computer is used.  If PC-compatible
!     computer is being used, PCASCI should equal TRUE and NONPC should
!     equal FALSE. If terminal (non-PC) is being used (i.e. PRIME, VAX)
!     both WINDOW and NONPC should equal TRUE for window output
      PARAMETER (NONPC=.FALSE.)
