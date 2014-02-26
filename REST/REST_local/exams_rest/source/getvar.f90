subroutine GETVAR ()
! 03-MAY-1985 - L.A. Burns
! Revised 07-April-2001 to add aquatic metabolism to biolysis group
! Revised 2004-05-17 to add study temperature for metabolism
! Subroutines required: none
use Alias_Transfer
use Initial_Sizes
use Global_Variables
use Implementation_Control
Implicit None

Groups: select case (ICOM)
case (1) Groups ! Parameter Group: NAMEG
   select case (IVAR)
      case (1); L1 = CHEMNA(ICL1)
      case (2); L1 = ECONAM
      case (3); L1 = LOADNM
      case (4); L1 = PRODNM
      case (5); L1 = TYPEG(ICL1)
      case (6); L1 = AIRTYG(ICL1)
   end select
case (2) Groups ! Parameter Group: CONTRG
   select case (IVAR)
      case (1); I2 = FIXFIL
      case (2); I2 = IUNITG
      case (3); I2 = MCHEMG
      case (4); I2 = KCHEM
      case (5); I2 = MODEG
      case (6); I2 = PRSWG
      case (7); I2 = MONTHG
      case (8); I2 = NYEARG
      case (9); I2 = YEAR1G
      case (10); I2 = TCODEG
      case (11); R4 = CINTG
      case (12); R4 = TENDG
      case (13); R4 = TINITG
      case (14); R4 = ABSERG
      case (15); R4 = RELERG
      case (16); I2 = EventD(ICL1)
      case (17); L1 = OutFil(ICL1)
   end select
case (3) Groups ! Parameter Group: PCHEMG
   select case (IVAR)
      case (1); I2 = SPFLGG(ICL1,ICL2)
      case (2); R4 = MWTG(ICL1)
      case (3); R4 = SOLG(ICL1,ICL2)
      case (4); R4 = ESOLG(ICL1,ICL2)
      case (5); R4 = PKG(ICL1,ICL2)
      case (6); R4 = EPKG(ICL1,ICL2)
   end select
case (4) Groups ! Parameter Group: PARTG
   select case (IVAR)
      case (1); R4 = KOCG(ICL1)
      case (2); R4 = KOWG(ICL1)
      case (3); R4 = KPBG(ICL1,ICL2)
      case (4); R4 = KPDOCG(ICL1,ICL2)
      case (5); R4 = KPSG(ICL1,ICL2)
      case (6); R4 = KIECG(ICL1,ICL2)
   end select
case (5) Groups ! Parameter Group: VOLATG
   select case (IVAR)
      case (1); R4 = MPG(ICL1)
      case (2); R4 = HENRYG(ICL1)
      case (3); R4 = EHENG(ICL1)
      case (4); R4 = VAPRG(ICL1)
      case (5); R4 = EVPRG(ICL1)
   end select
case (6) Groups ! Parameter Group: DPHOTG
   select case (IVAR)
      case (1); R4 = QYield(ICL1,ICL2,ICL3)
      case (2); R4 = KDPG(ICL1,ICL2)
      case (3); R4 = RFLATG(ICL1,ICL2)
      case (4); R4 = ABSORG(ICL1,ICL2,ICL3)
      case (5); R4 = LAMAXG(ICL1,ICL2)
   end select
case (7) Groups ! Parameter Group: HYDROG
   select case (IVAR)
      case (1); R4 = KAHG(ICL1,ICL2,ICL3)
      case (2); R4 = EAHG(ICL1,ICL2,ICL3)
      case (3); R4 = KNHG(ICL1,ICL2,ICL3)
      case (4); R4 = ENHG(ICL1,ICL2,ICL3)
      case (5); R4 = KBHG(ICL1,ICL2,ICL3)
      case (6); R4 = EBHG(ICL1,ICL2,ICL3)
   end select
case (8) Groups ! Parameter Group: REDOXG
   select case (IVAR)
      case (1); R4 = KOXG(ICL1,ICL2,ICL3)
      case (2); R4 = EOXG(ICL1,ICL2,ICL3)
      case (3); R4 = K1O2G(ICL1,ICL2,ICL3)
      case (4); R4 = EK1O2G(ICL1,ICL2,ICL3)
      case (5); R4 = KREDG(ICL1,ICL2,ICL3)
      case (6); R4 = EREDG(ICL1,ICL2,ICL3)
   end select
case (9) Groups ! Parameter Group: BIOLYG (biolysis parameters)
   select case (IVAR)
      case (1); R4 = KBACWG(ICL1,ICL2,ICL3)
      case (2); R4 = QTBAWG(ICL1,ICL2,ICL3)
      case (3); R4 = KBACSG(ICL1,ICL2,ICL3)
      case (4); R4 = QTBASG(ICL1,ICL2,ICL3)
      case (5); R4 = QTBTWG(ICL1,ICL2,ICL3)
      case (6); R4 = QTBTSG(ICL1,ICL2,ICL3)
      case (7); R4 = AerMet(ICL1)
      case (8); R4 = AnaerM(ICL1)
   end select
case (10) Groups ! Parameter Group: TRPORT
   select case (IVAR)
      case (1); I2 = KOUNT
      case (2); I2 = JFRADG(ICL1)
      case (3); I2 = ITOADG(ICL1)
      case (4); R4 = ADVPRG(ICL1)
      case (5); I2 = JTURBG(ICL1)
      case (6); I2 = ITURBG(ICL1)
      case (7); R4 = XSTURG(ICL1)
      case (8); R4 = CHARLG(ICL1)
      case (9); R4 = DSPG(ICL1,ICL2)
   end select
case (11) Groups ! Parameter Group: SEDMG
   select case (IVAR)
      case (1); R4 = SUSEDG(ICL1,ICL2)
      case (2); R4 = BULKDG(ICL1,ICL2)
      case (3); R4 = FROCG(ICL1,ICL2)
      case (4); R4 = CECG(ICL1,ICL2)
      case (5); R4 = AECG(ICL1,ICL2)
      case (6); R4 = PCTWAG(ICL1,ICL2)
   end select
case (12) Groups ! Parameter Group: QUALG
   select case (IVAR)
      case (1); R4 = TCELG(ICL1,ICL2)
      case (2); R4 = PHG(ICL1,ICL2)
      case (3); R4 = POHG(ICL1,ICL2)
      case (4); R4 = OXRADG(ICL1)
      case (5); R4 = REDAGG(ICL1,ICL2)
      case (6); R4 = BACPLG(ICL1,ICL2)
      case (7); R4 = BNBACG(ICL1,ICL2)
      case (8); R4 = PLMASG(ICL1,ICL2)
      case (9); R4 = BNMASG(ICL1,ICL2)
      case (10); R4 = KO2G(ICL1,ICL2)
   end select
case (13) Groups ! Parameter Group: PHOTOG
   select case (IVAR)
      case (1); R4 = DOCG(ICL1,ICL2)
      case (2); R4 = CHLG(ICL1,ICL2)
      case (3); R4 = CLOUDG(ICL1)
      case (4); R4 = DFACG(ICL1,ICL2)
      case (5); R4 = DISO2G(ICL1,ICL2)
      case (6)  ! Access the TOMS database to get the data...
                call Ozone(LatG,LongG,OzoneG,.false.,stdout,Oz_UNT,Zonal_Data)
                R4 = OZONEG(ICL1)
   end select
case (14) Groups ! Parameter Group: GEOMT
   select case (IVAR)
      case (1); R4 = VOLG(ICL1)
      case (2); R4 = AREAG(ICL1)
      case (3); R4 = DEPTHG(ICL1)
      case (4); R4 = XSAG(ICL1)
      case (5); R4 = LENGG(ICL1)
      case (6); R4 = WIDTHG(ICL1)
   end select
case (15) Groups ! Parameter Group: CLIMG
   select case (IVAR)
      case (1); R4 = RAING(ICL1)
      case (2); R4 = EVAPG(ICL1,ICL2)
      case (3); R4 = LATG
      case (4); R4 = LONGG
      case (5); R4 = WINDG(ICL1,ICL2)
      case (6); R4 = ELEVG
      case (7); R4 = RHUMG(ICL1)
      case (8); R4 = ATURBG(ICL1)
   end select
case (16) Groups ! Parameter Group: FLOWG
   select case (IVAR)
      case (1); R4 = STFLOG(ICL1,ICL2)
      case (2); R4 = STSEDG(ICL1,ICL2)
      case (3); R4 = NPSFLG(ICL1,ICL2)
      case (4); R4 = NPSEDG(ICL1,ICL2)
      case (5); R4 = SEEPSG(ICL1,ICL2)
   end select
case (17) Groups ! Parameter Group: LOADSG
   select case (IVAR)
      case (1); R4 = STRLDG(ICL1,ICL2,ICL3)
      case (2); R4 = NPSLDG(ICL1,ICL2,ICL3)
      case (3); R4 = PCPLDG(ICL1,ICL2,ICL3)
      case (4); R4 = DRFLDG(ICL1,ICL2,ICL3)
      case (5); R4 = PRBENG
      case (6); R4 = SEELDG(ICL1,ICL2,ICL3)
      case (7); R4 = IMASSG(ICL1)
      case (8); I2 = ISEGG(ICL1)
      case (9); I2 = ICHEMG(ICL1)
      case (10); I2 = IMONG(ICL1)
      case (11); I2 = IDAYG(ICL1)
      case (12); I2 = IYEARG(ICL1)
      case (13); R4 = SPRAYG
   end select
case (18) Groups ! Parameter Group: SPECTR
   select case (IVAR)
      case (1); I2 = CHPARG(ICL1)
      case (2); I2 = TPRODG(ICL1)
      case (3); I2 = NPROCG(ICL1)
      case (4); I2 = RFORMG(ICL1)
      case (5); R4 = YIELDG(ICL1)
      case (6); R4 = EAYLDG(ICL1)
   end select
end select Groups
return
end Subroutine GETVAR
