module Global_Variables
! 2002-04-12 added user-selectable event durations for annual maximum series
! 2002-04-26 revisions to support user-selectable output files
! Revised 2004-05-17 (LAB) to specify the temperature of biolysis studies
! Revised 2005-02-17 (LAB) to force production of report.xms
use Initial_Sizes
use Implementation_Control
Implicit None
save
!_____________________________________________________________________________
! Recognized names...placed here to allow for convenient expansion without
! extensive code revisions
character (len=*), parameter :: Permitted_Compartment_Types = 'LlEeHhBb'
!character (len=*), parameter :: Permitted_Limnos_Types = 'LlEeHh'
!character (len=*), parameter :: Permitted_Benthos_Types = 'Bb'
!character (len=*), parameter :: Permitted_Epilimnetic_Types = 'LlEe'
character (len=*), parameter :: Permitted_Air_Mass_Types = 'MmRrTtUu'
!_____________________________________________________________________________
! Program control parameters
real (kind(0E0)), parameter :: Stiff_threshold = 4.0

logical :: Restart_PRZM, Zonal_Data
logical, allocatable :: Freundlich(:)
! Zonal_Data signals that the TOMS file is missing, so
!    zonal mean total column ozone data is used instead.
! Freundlich is used to signal that a Freundlich isotherm is in use
!_____________________________________________________________________________
! Parameter Group NAMEG - 6 study identifiers
character (len=50), allocatable :: CHEMNA(:)
character (len=50) :: ECONAM=' ',LOADNM=' ',PRODNM=' '
character (len=1), allocatable :: TYPEG(:)
character (len=1) :: AIRTYG(MAXDAT)
!_____________________________________________________________________________
! CONTRG -- 17 control variables the user can manipulate
integer ::  FIXFIL=0, IUNITG=0, MCHEMG=1, KCHEM=1, MODEG=3, PRSWG=1,&
          & MONTHG=13, NYEARG=1, YEAR1G=2000, TCODEG=1
real (kind(0D0)) :: CINTG=2.0D+00, TENDG=24.0d+00, TINITG=0.0
real (kind(0E0)) :: ABSERG=1.0E-13, RELERG=1.0E-09
! User selectable intervals for annual maximum event analysis
integer, dimension(5) :: EventD=0
character (len=1), dimension(10) :: OutFil = &
      (/'Y','N','N','N','N','N','N','N','N','N'/)
! to control output file production -- Yes or No to each file type
! When setting up, match these to the file production logicals in local.f90
! 1: Standard report file (report.xms, Logical RPFIL, LUN=RPTLUN)
!   As of 2005-02-17, production of this file is forced, because much of the
!   error control file handling keys off it 
! 2: Standard (tty-style) plotting files (ssout.plt (LUN=SSLUN),
!      kinout.plt (LUN=KINLUN), Logical PLTFIL)
! 3: BASS data transfer file (bassexp.xms, BASFIL, LUN=BASSLUN)
! 4: FGETS data transfer files (fgetscmd.xms (LUN=FG2LUN),
!    fgetsexp.xms (LUN=FG1LUN), Logical FGTFIL)
! 5: HWIR data transfer file (HWIRExp.xms, Logical HWRFIL, LUN=HWIRLUN )
! 6: Compartment-oriented Ecotox exposure file
!     (EcoToxC.xms, Logical TOXFILC, LUN=TOXCLUN)
! 7: Compartment-oriented annual maximum series analysis and report file
!     (EcoRiskC.xms, Logical RSKFILC LUN=RSKCLUN)
! 8: Reach-oriented Ecotox exposure file
!     (EcoToxR.xms, Logical TOXFILR, LUN=TOXRLUN)
! 9: Reach-oriented annual maximum series analysis and report file
!     (EcoRiskR.xms, Logical RSKFILR, LUN=RSKRLUN)
! 10: Complete compartment-oriented concentration file
!     (FullOut.xms, Logical FULFIL, LUN=FULLUN)
!_____________________________________________________________________________
! PCHEMG -- 6 physical chemistry parameters
real (kind(0E0)), allocatable :: MWTG(:),SOLG(:,:),ESOLG(:,:),&
   PKG(:,:),EPKG(:,:)
integer, allocatable :: SPFLGG(:,:)
!_____________________________________________________________________________
! PARTG -- 6 partitioning and sorption parameters
real (kind(0E0)), allocatable :: KOCG(:),KOWG(:),KPBG(:,:),KPDOCG(:,:),&
   KPSG(:,:),KIECG(:,:)
!_____________________________________________________________________________
! VOLATG -- 5 volatilization parameters
real (kind(0E0)), allocatable :: MPG(:),HENRYG(:),EHENG(:),VAPRG(:),EVPRG(:)
!_____________________________________________________________________________
! DPHOTG -- 5 direct photolysis parameters
! QUAntg altered to QYield 05/12/99 to resolve help conflict with QUAlity
real (kind(0E0)), allocatable :: QYield(:,:,:),KDPG(:,:),RFLATG(:,:),&
   ABSORG(:,:,:),LAMAXG(:,:)
!_____________________________________________________________________________
! HYDROG -- 6 hydrolysis parameters
real (kind(0E0)), allocatable :: KAHG(:,:,:),EAHG(:,:,:),&
   KNHG(:,:,:),ENHG(:,:,:),KBHG(:,:,:),EBHG(:,:,:)
!_____________________________________________________________________________
! REDOXG -- 6 redox chemistry parameters
real (kind(0E0)), allocatable :: KOXG(:,:,:), EOXG(:,:,:),&
   K1O2G(:,:,:), EK1O2G(:,:,:), KREDG(:,:,:), EREDG(:,:,:)
!_____________________________________________________________________________
! BIOLYG -- 8 biolysis parameters
real (kind(0E0)), allocatable :: KBACWG(:,:,:), QTBAWG(:,:,:),&
                                 KBACSG(:,:,:), QTBASG(:,:,:),&
                                 QTBTWG(:,:,:), QTBTSG(:,:,:)
real (kind(0E0)), allocatable :: AerMet(:),AnaerM(:)
!_____________________________________________________________________________
! TRPORT -- 9 transport and system connectivity parameters
integer :: KOUNT=1
integer, allocatable :: JFRADG(:),ITOADG(:),JTURBG(:),ITURBG(:)
real (kind(0E0)), allocatable :: ADVPRG(:),XSTURG(:),CHARLG(:),DSPG(:,:)
!_____________________________________________________________________________
! SEDMG -- 6 sediment properties
real (kind(0E0)), allocatable :: SUSEDG(:,:),BULKDG(:,:),&
      FROCG(:,:),CECG(:,:),AECG(:,:),PCTWAG(:,:)
!_____________________________________________________________________________
! QUALG -- 10 water quality parameters
real (kind(0E0)), allocatable :: TCELG(:,:),PHG(:,:),POHG(:,:),&
      OXRADG(:),REDAGG(:,:),BACPLG(:,:),BNBACG(:,:),PLMASG(:,:),&
      BNMASG(:,:),KO2G(:,:)
!_____________________________________________________________________________
! PHOTOG -- 6 parameters of photolytic light fields
real (kind (0E0)) :: CLOUDG(MAXDAT),OZONEG(MAXDAT)
real (kind (0E0)), allocatable :: DOCG(:,:),CHLG(:,:),DFACG(:,:),DISO2G(:,:)
!_____________________________________________________________________________
! GEOMT -- 6 water body geometry paramters
real (kind (0E0)), allocatable :: &
      VOLG(:),AREAG(:),DEPTHG(:),XSAG(:),LENGG(:),WIDTHG(:)
!_____________________________________________________________________________
! CLIMG -- 8 climate parameters
real (kind (0E0)) :: RAING(MAXDAT), LATG, LONGG, ELEVG, &
      RHUMG(MAXDAT),ATURBG(MAXDAT)
real (kind (0E0)), allocatable :: EVAPG(:,:),WINDG(:,:)
!_____________________________________________________________________________
! FLOWG -- hydrology; 5 parameters for input flows of water and solids
real (kind (0E0)), allocatable :: STFLOG(:,:), STSEDG(:,:),&
      NPSFLG(:,:), NPSEDG(:,:), SEEPSG(:,:)
!_____________________________________________________________________________
! LOADSG -- 13 external chemical loads
real (kind (0E0)), allocatable :: STRLDG(:,:,:), NPSLDG(:,:,:),&
   PCPLDG(:,:,:), DRFLDG(:,:,:), SEELDG(:,:,:)
real (kind(0E0)) :: IMASSG(MAXMAS), PRBENG=0.5
integer :: ISEGG(MAXMAS), ICHEMG(MAXMAS), IMONG(MAXMAS),&
           IDAYG(MAXMAS), IYEARG(MAXMAS)
real (kind (0E0)) :: SPRAYG = 10.0
!_____________________________________________________________________________
! SPECTR -- 6 product chemistry parameters
real (kind (0E0)) :: YIELDG(NTRAN),EAYLDG(NTRAN)
integer :: CHPARG(NTRAN),TPRODG(NTRAN),NPROCG(NTRAN),RFORMG(NTRAN)
!_____________________________________________________________________________
contains

Subroutine Allocate_Storage (area,new_env,new_chem)
! Set up global variable storage in response to a recall, a read, or a
! change in KOUNT or KCHEM. Note that this routine assumes that the
! storage is already allocated and requires re-allocation.

integer, intent(in) :: area ! number of chemicals, number of segments
integer, intent(in) :: new_env,new_chem ! the new value of KOUNT, KCHEM

select case (area)

case (1) ! alteration in number of chemicals
   deallocate (CHEMNA)
   deallocate (MWTG,SOLG,MPG,ESOLG,PKG,EPKG,SPFLGG)  ! physical chemistry
   deallocate (KOCG,KOWG,KPBG,KPDOCG,KPSG,KIECG)     ! partitioning & sorption
   deallocate (Freundlich)
   deallocate (HENRYG,EHENG,VAPRG,EVPRG)             ! volatilization
   deallocate (QYield,KDPG,RFLATG,ABSORG,LAMAXG)     ! direct photolysis
   deallocate (KAHG,EAHG,KNHG,ENHG,KBHG,EBHG)        ! hydrolysis
   deallocate (KOXG,EOXG,K1O2G,EK1O2G,KREDG,EREDG)   ! redox chemistry
   deallocate (KBACWG,QTBAWG,KBACSG,QTBASG)          ! biolysis
   deallocate (QTBTWG,QTBTSG,AerMet,AnaerM)          ! biolysis
   allocate (CHEMNA(new_chem))
   ! physical chemistry
   allocate (MWTG(new_chem),SOLG(7,new_chem),MPG(new_chem),ESOLG(7,new_chem),&
      PKG(6,new_chem),EPKG(6,new_chem),SPFLGG(7,new_chem))
   ! partitioning and sorption
   allocate (KOCG(new_chem),KOWG(new_chem),KPBG(7,new_chem),&
      KPDOCG(7,new_chem),KPSG(7,new_chem),KIECG(6,new_chem),&
      Freundlich(new_chem))
   ! volatilization
   allocate (HENRYG(new_chem),EHENG(new_chem),VAPRG(new_chem),EVPRG(new_chem))
   ! direct photolysis
   allocate (QYield(3,7,new_chem),KDPG(7,new_chem),RFLATG(7,new_chem),&
      ABSORG(46,7,new_chem),LAMAXG(7,new_chem))
   ! hydrolysis
   allocate (KAHG(3,7,new_chem),EAHG(3,7,new_chem),&
      KNHG(3,7,new_chem),ENHG(3,7,new_chem),KBHG(3,7,new_chem),&
      EBHG(3,7,new_chem))
   ! redox chemistry
   allocate (KOXG(3,7,new_chem),EOXG(3,7,new_chem),&
      K1O2G(3,7,new_chem),EK1O2G(3,7,new_chem),KREDG(3,7,new_chem),&
      EREDG(3,7,new_chem))
   ! biolysis
   allocate (KBACWG(4,7,new_chem),QTBAWG(4,7,new_chem),&
      KBACSG(4,7,new_chem),QTBASG(4,7,new_chem),&
      QTBTWG(4,7,new_chem),QTBTSG(4,7,new_chem))
   allocate (AerMet(new_chem),AnaerM(new_chem))
   call Allocate_Loads

case (2) ! alteration in number of environmental segments
   deallocate (SUSEDG, BULKDG, FROCG, CECG, AECG, PCTWAG)
   deallocate (TCELG,PHG,POHG,OXRADG,REDAGG,BACPLG,BNBACG,PLMASG,BNMASG,KO2G)
   deallocate (DOCG,CHLG,DFACG,DISO2G)
   deallocate (VOLG,AREAG,DEPTHG,XSAG,LENGG,WIDTHG)
   deallocate (EVAPG,WINDG)
   deallocate (STFLOG,STSEDG,NPSFLG,NPSEDG,SEEPSG)
   deallocate (TYPEG)
   deallocate (JFRADG,ITOADG,JTURBG,ITURBG,ADVPRG,XSTURG,CHARLG,DSPG)


   ! transport field
   allocate (JFRADG(new_env*KountMult), ITOADG(new_env*KountMult),&
             JTURBG(new_env*KountMult), ITURBG(new_env*KountMult))
   allocate (ADVPRG(new_env*KountMult), XSTURG(new_env*KountMult),&
             CHARLG(new_env*KountMult), DSPG(new_env*KountMult,MAXDAT))
   JFRADG=0; ITOADG=0; JTURBG=0; ITURBG=0
   ADVPRG=0.0; XSTURG=0.0; CHARLG=0.0; DSPG=0.0
   ! sediment descriptors
   allocate (SUSEDG(new_env,MAXDAT)); SUSEDG=0.0
   allocate (BULKDG(new_env,MAXDAT)); BULKDG=0.0
   allocate (FROCG(new_env,MAXDAT),CECG(new_env,MAXDAT)); FROCG=0.0;CECG=0.0
   allocate (AECG(new_env,MAXDAT),PCTWAG(new_env,MAXDAT)); AECG=0.0;PCTWAG=0.0
   ! water quality descriptors
   allocate (TCELG(new_env,MAXDAT),PHG(new_env,MAXDAT),POHG(new_env,MAXDAT),&
   OXRADG(MAXDAT),REDAGG(new_env,MAXDAT),BACPLG(new_env,MAXDAT),&
   BNBACG(new_env,MAXDAT),PLMASG(new_env,MAXDAT),BNMASG(new_env,MAXDAT),&
   KO2G(new_env,MAXDAT))
   TCELG=20.0;PHG=7.0;POHG=7.0;OXRADG=0.0;REDAGG=0.0;BACPLG=0.0;BNBACG=0.0
   PLMASG=0.0;BNMASG=0.0;KO2G=0.0
   ! solar light field
   allocate (DOCG(new_env,MAXDAT),CHLG(new_env,MAXDAT));DOCG=0.0;CHLG=0.0
   allocate (DFACG(new_env,MAXDAT),DISO2G(new_env,MAXDAT))
   DFACG=1.2;DISO2G=5.0
   ! geometry
   allocate (VOLG(new_env),AREAG(new_env),DEPTHG(new_env),&
      XSAG(new_env),LENGG(new_env),WIDTHG(new_env))
   VOLG=0.0;AREAG=0.0;DEPTHG=0.0;XSAG=0.0;LENGG=0.0;WIDTHG=0.0
   ! climate
   allocate (EVAPG(new_env,MAXDAT),WINDG(new_env,MAXDAT));EVAPG=0.0;WINDG=0.0
   ! hydrology
   allocate (STFLOG(new_env,MAXDAT),STSEDG(new_env,MAXDAT),&
   NPSFLG(new_env,MAXDAT),NPSEDG(new_env,MAXDAT),SEEPSG(new_env,MAXDAT))
   STFLOG=0.0;STSEDG=0.0;NPSFLG=0.0;NPSEDG=0.0;SEEPSG=0.0
   ! structural segment types
   allocate (TYPEG(new_env));TYPEG=' ';TYPEG(1)='L';ECONAM=' '

   call Allocate_Loads

case default
   stop ' Software fault: environment memory allocation failure.'
end select

contains
Subroutine Allocate_Loads
! monthly loads must be reallocated upon a change in chemicals or segments
deallocate (STRLDG,NPSLDG,PCPLDG,DRFLDG,SEELDG)
allocate (STRLDG(new_env,new_chem,MAXDAT),NPSLDG(new_env,new_chem,MAXDAT),&
   PCPLDG(new_env,new_chem,MAXDAT),DRFLDG(new_env,new_chem,MAXDAT),&
   SEELDG(new_env,new_chem,MAXDAT))
! Initialize new structure
STRLDG=0.0; NPSLDG=0.0; PCPLDG=0.0; DRFLDG=0.0; SEELDG=0.0
end Subroutine Allocate_Loads
end Subroutine Allocate_Storage

end module Global_Variables
