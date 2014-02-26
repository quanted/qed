subroutine INITL(SECTOR)
! Created August 1979 by L.A. Burns
! Revised 18 March 1985 for F77 character processing
! Revised 29-May-1986 to add "SECTOR" to call
! Revised 09/13/91 to support PRZM data transfer and initializing
! loadings and product chemistries
! Converted to Fortran90 2/13/96
! Revised 2004-05-17 (LAB) to specify the temperature of biolysis studies
! Initialization of state variables eliminated 01/29/2001
! Freundlich flag initialized .false.
use Implementation_Control
use Input_Output
! This routine initializes (in most cases, sets to zero)
! global (under user control) variables
! Parameter statements defining the size of the version
use Global_Variables
use Local_Working_Space
Implicit None
integer, intent(in) :: SECTOR
! SECTOR lets the READ command locate the data to be reset...
! INITL is called by DATAIN in the Utility program, with SECTOR set to
! 2:5 to zero ALL input data. READER calls INITL with SECTOR set to values
! > 1 to zero the portion of the data structure to be replaced by a file
! read from some external ascii file. Specifically,
! SECTOR=2 initializes chemical data (of the current value of MCHEMG)
! SECTOR=3 initializes environmental data
! SECTOR=4 initializes loadings
! SECTOR=5 initializes product chemistry
select case (SECTOR)
case (1)
! reserved for future expansion
! ----------------------------------------------------------------------
case (2) ! start of chemical data initialization
   MWTG(mchemg) = 0.0
   KOCG(mchemg) = 0.0
   Freundlich(mchemg) = .false.
   KOWG(mchemg) = 0.0
   MPG(mchemg) = -99.0
   HENRYG(mchemg) = 0.0
   EHENG(mchemg) = 0.0
   VAPRG(mchemg) = 0.0
   EVPRG(mchemg) = 0.0
   PKG(:,mchemg) = 0.0
   EPKG(:,mchemg) = 0.0
   KIECG(:,mchemg) = 0.0
   CHEMNA(mchemg) = ' '
   RPASS(1) = 'GLOBAL'
   WPASS(1) = 'GLOBAL'
   SPFLGG(:,mchemg) = 0
   LAMAXG(:,mchemg) = 0.0
   SOLG(:,mchemg) = 0.0
   ESOLG(:,mchemg) = 0.0
   KPSG(:,mchemg) = 0.0
   KPDOCG(:,mchemg) = 0.0
   KPBG(:,mchemg) = 0.0
   KDPG(:,mchemg) = 0.0
   RFLATG(:,mchemg) = 40.0
   QYield(:,:,mchemg) = 0.0
   KAHG(:,:,mchemg) = 0.0
   EAHG(:,:,mchemg) = 0.0
   KNHG(:,:,mchemg) = 0.0
   ENHG(:,:,mchemg) = 0.0
   KBHG(:,:,mchemg) = 0.0
   EBHG(:,:,mchemg) = 0.0
   KOXG(:,:,mchemg) = 0.0
   EOXG(:,:,mchemg) = 0.0
   K1O2G(:,:,mchemg) = 0.0
   EK1O2G(:,:,mchemg) = 0.0
   KREDG(:,:,mchemg) = 0.0
   EREDG(:,:,mchemg) = 0.0
   KBACWG(:,:,mchemg) = 0.0
   QTBAWG(:,:,mchemg) = 2.0
   KBACSG(:,:,mchemg) = 0.0
   QTBASG(:,:,mchemg) = 2.0
!  Subpart N USA study guidelines for pesticides specify 25 C
   QTBTWG(:,:,mchemg) = 25.0
   QTBTSG(:,:,mchemg) = 25.0
   AerMet(mchemg)   = 0.0
   AnaerM(mchemg) = 0.0
   ! light absorption by chemical
   ABSORG(:,:,mchemg) = 0.0
! end of chemical section
! ----------------------------------------------------------------------
case (3) ! start of environmental section
   ! pre-zero environmental variables
   RPASS(2)='GLOBAL'
   WPASS(2)='GLOBAL'
   LATG = 34.95
   LONGG = 83.
   ELEVG = 200.0
   ECONAM = ' '
   RAING = 0.0
   CLOUDG = 0.0
   OXRADG = 0.0
   OZONEG = 0.30
   ATURBG = 2.0
   RHUMG = 0.0
   AIRTYG = ' '
   JFRADG = 0
   ITOADG = 0
   ADVPRG = 0.0
   JTURBG = 0
   ITURBG = 0
   XSTURG = 0.0
   CHARLG = 0.0
   DSPG = 0.0
   TYPEG = ' '
   VOLG = 0.0
   AREAG = 0.0
   DEPTHG = 0.0
   XSAG = 0.0
   LENGG = 0.0
   WIDTHG = 0.0
   EVAPG = 0.0
   WINDG = 0.0
   SUSEDG = 0.0
   BULKDG = 0.0
   PCTWAG = 0.0
   FROCG = 0.0
   CECG = 0.0
   AECG = 0.0
   TCELG = 20.0
   PHG = 7.0
   POHG = 7.0
   BACPLG = 0.0
   BNBACG = 0.0
   PLMASG = 0.0
   BNMASG = 0.0
   KO2G = 0.0
   DISO2G = 5.0
   DOCG = 0.0
   CHLG = 0.0
   DFACG = 1.2
   STFLOG = 0.0
   STSEDG = 0.0
   NPSFLG = 0.0
   NPSEDG = 0.0
   SEEPSG = 0.0
   REDAGG = 0.0
! end of environmental section
! ----------------------------------------------------------------------
case (4) ! start of loadings initialization section
   RPASS(3)='GLOBAL'
   WPASS(3)='GLOBAL'
   LOADNM = ' '
   ! zero the loads, first pulses
   ISEGG =0
   ICHEMG=0
   IMONG =0
   IDAYG =0
   IYEARG=0
   IMASSG=0.0
   ! and then the continuous loads
   STRLDG = 0.0
   NPSLDG = 0.0
   PCPLDG = 0.0
   DRFLDG = 0.0
   SEELDG = 0.0
! end of loadings section
!-----------------------------------------------------------------------
case (5) ! start of product chemistry section
   RPASS(4)='GLOBAL'
   WPASS(4)='GLOBAL'
   PRODNM = ' '
   YIELDG=0.0
   EAYLDG=0.0
   CHPARG=0
   TPRODG=0
   NPROCG=0
   RFORMG=0
! end of product chemistry section
end select
return
end subroutine INITL
