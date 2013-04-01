      ! include file pparm.inc

      ! NCMPTS - number of przm compartments
      ! the dimension for 'NCMPTS' must be at least one number larger
      ! than the number of compartments that are being simulated.

      ! 11/11/96 by jmc
      ! if 'NCMPTS' is increased, NPII must also increase. the new
      ! value of NPII should be set equal to NCMPTS*NUM. NUM is defined
      ! in SUBROUTINE INITL in RSINP2.FOR at line 2633 (line 558 of INITL).
      ! NUM is currently set equal to 4.
      !
      ! note if NPII value is changed, write statements in lines 106-123
      ! of subroutine RSTPT1 and read statements in lines 120-138 of
      ! subroutine RSTGT1 for variable CC need to be modified accordingly.

      INTEGER , PARAMETER :: NCMPTS = 500

      ! NAPP - number of pesticides applications
      INTEGER , PARAMETER :: NAPP = 800

      ! NC - number of crops
      INTEGER , PARAMETER :: NC = 5

      ! NPII - number of points for moc algorithm.
      INTEGER , PARAMETER :: NPII = 2000

      INTEGER , PARAMETER :: NCMPP2 = NCMPTS + 2

      ! maximum number of cropping periods
      ! Nominally, NC crops for 30 years (1961-1990)
      INTEGER , PARAMETER :: MXCPD = 150

