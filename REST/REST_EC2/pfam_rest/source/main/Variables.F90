module variables
!  Written by Dirk F. Young (Virginia, USA).
!Only variables that are imported in from the User Interface are kept in this module.  This rule is 
!intended to facilititate changing outthe interface, as only and all the parameters in this module need to be populated.
!Common variables that are calculated and used internally between routines are transported as arguments.

    implicit none
    save
    !**********System Parameters ****************************************************************
    integer, parameter :: max_apps = 30
    !**********Hydrologic Parameters ************************************************************
    real(8),parameter :: minimum_depth = 0.00001  !(m) minimum depth of pond for numerical purposes
    real(8),parameter :: Time_int=86400.  !simulation  TIME INTERVAL IS ONE DAY (units are in sceonds, consistent with SI)
    !**********************************************************
    character(len=256) :: metfilename    !met file name
    character(len=256) :: outputfilename !output file name
    real(8) :: LAT               !scenario latitude
    integer :: nchem             !number of chemicals, at least 1 for parent, currrenly can do two straight chain degradates
    !***********chemical inputs*****************************
    real(8) :: aer_aq(3)         !input aqueous-phase aerobic halflife (days) delivered from window interface
    real(8) :: anae_aq(3)        !anaerobic aquatic
    real(8) :: drysoil(3)        !soil degradation half life (days)
    real(8) :: photo(3)          !near-surface photolysis half life (days
    real(8) :: hydro(3)          !input hydrolysis half life (days)
    real(8) :: koc(3)            !Koc value (ml/g)
    real(8) :: RFLAT(3)          !input latitude for photolysis study

    real(8) :: MWT(3)            !molecular wt (g/mol)
    real(8) :: VAPR(3)           !vapor pressure (torr)
    real(8) :: SOL(3)            !solubility (mg/L)    
    
    real(8) :: temp_ref_aer(3)   !temp at which aerobic study conducted
    real(8) :: temp_ref_anae(3)  !temp at which anaerobic study conducted
    real(8) :: temp_ref_dry(3)   !temp at which soil degradation study was conducted
    real(8) :: temp_ref_henry(3) !temp at which henrys constant (or solublity and vp) were measured (C)
    real(8) :: heat_henry(3)     !enthalpy of solution to gas phase change (J/mol)
    
    real(8) :: xAerobic(3)
    real(8) :: xBenthic(3)
    real(8) :: xUnflood(3)
    real(8) :: xPhoto(3)
    real(8) :: xHydro(3)
      
    !***********Planting******************************
    integer :: PlantZero_day
    integer :: PlantZero_month
    integer :: PlantFull 
    integer :: PlantRemove
    real(8) :: CanopyMax
    
    !***********Event Mode
    integer :: EventMode
        
    !*******Flood Control Variables **************
    integer :: numberFloodEvents  
    
    integer :: event0_day      !day and month of reference start day for flood control
    integer :: event0_month
   ! real(8) event0_weir     !the weir ht on the reference day

    integer :: eventDay(11)  !each event  day is number of days from reference day, event 1 day is always zero
    real(8) :: eventFill(11)
    real(8) :: eventWeir(11)
    real(8) :: eventWashout(11)
    real(8) :: eventMinimum(11)
        
    !******** Pesicide Applications ******************
    integer :: num_apps 
    real(8) :: applicationMass(max_apps)
    integer :: applicationMonth(max_apps)
    integer :: applicationDay(max_apps)
    
    real(8) :: slowRelease(max_apps)  !the first-order rate of dissolution of the pesticide application

    !degradate(1) = TRUE means that parent produces a degradate
    !degradate(2) = TRUE means that degradate produces another degradate,  etc
    
    !************PHYSICAL INPUTS ****************
    real(8):: depth_0
    real(8):: benthic_depth  !meters
    real(8):: porosity      !volume water/total volume
    real(8):: bulk_density  !dry mass/total volume  g/ml
    real(8):: FROC1
    real(8):: FROC2
    real(8):: SUSED
    real(8):: CHL
    real(8):: DOC1 
    real(8):: DOC2
    real(8):: PLMAS
    real(8):: BNMAS
    real(8):: QT           !EXAMS Q10 values eq. 2-133
    real(8):: DFAC
    real(8):: area  !water body area (m2)
    real(8):: D_over_dx
    real(8):: leakage
    real(8),parameter :: CLOUD = 0.
    
    real(8) :: watershed_area
    real(8) :: watershed_cn
    real(8) :: widthMixingCell
    real(8) :: depthMixingCell
    real(8) :: lengthMixingCell
    real(8) :: baseflow  
    
    
end module variables



!********** Parameters *******************
! FOR reference here are the values for the EPA standard pond as defined in EXAMS:
!real(8),parameter :: PCTWA=137.
!real(8),parameter :: BULKD=1.85
!real(8),parameter :: FROC1=0.04
!real(8),parameter :: FROC2=0.04
!real(8),parameter :: DSP= 0.00003
!real(8),parameter :: SUSED=30.
!real(8),parameter :: CHL =0.005
!real(8),parameter :: DOC1= 5. 
!real(8),parameter :: DOC2= 5. 
!real(8),parameter :: PLMAS =0.4
!real(8),parameter :: BNMAS = 0.006 
!real(8),parameter :: QT=2.
!real(8),parameter :: benthic_depth= .02 !meters
!real(8),parameter :: CLOUD = 0.
!real(8),parameter :: DFAC= 1.19
