module nonInputVariables
!  Written by Dirk F. Young (Virginia, USA).
implicit none 

integer :: num_records            !number of met file records

real(8),allocatable,dimension(:):: wind               !wind speed (m/s) at 10 cm
real(8),allocatable,dimension(:):: temp_avg           !average 30 day previous temperature C, (processed from met file)
real(8),allocatable,dimension(:):: evap               !evaporation (m)
real(8),allocatable,dimension(:):: precip             !precipitation (m)

real(8),allocatable,dimension(:) :: daily_depth       !daily water body depths
real(8),allocatable,dimension(:) :: depth_release     !vector of water releases (m)
real(8),allocatable,dimension(:) :: makeupwater       !daily water body depths
real(8),allocatable,dimension(:) :: overflow          !vector of overflow depths


real(8),allocatable,dimension(:) :: k_aer_aq          !aqueous-phase aerobic rate (per sec)
real(8),allocatable,dimension(:) :: k_anaer_aq        !aqueous-phase anaerobic rate (per sec)
real(8),allocatable,dimension(:) :: k_aer_s           !sorbed-phase aerobic rate (per sec)
real(8),allocatable,dimension(:) :: k_anaer_s         !sorbed-phase anaerobic rate (per sec)

real(8),allocatable,dimension(:) :: k_hydro           !hydrolysis rate (per sec)
real(8),allocatable,dimension(:) :: k_volatile        !first order volatilization rate (per sec)
real(8),allocatable,dimension(:) :: k_photo           !photolysis rate (per sec)
real(8),allocatable,dimension(:) :: k_flow            !array of daily wash out rates (per second)

real(8),allocatable,dimension(:) :: k_leakage         !array of daily leakage rates (per second)

real(8),allocatable,dimension(:) :: plant_factor      !fractional plant growth daily values

real(8), allocatable, dimension(:)  :: gamma_1                  !effective littoral degradation
real(8), allocatable, dimension(:)  :: gamma_2                  !effective benthic degradation

real(8), allocatable, dimension(:)  :: A,E,F,B                   !final coefficients for the 2 simultaneous equations
 
real(8), allocatable, dimension(:)  :: theta                    !solute holding capacity ratio [--]
real(8), allocatable, dimension(:)  :: capacity_1               !solute holding capacity of region 1 [m3]
real(8), allocatable, dimension(:)  :: fw1                      !fraction of region 1 solute in aqueous phase

real(8)                             :: capacity_2               !solute holding capacity of region 2 [m3]
real(8)                             :: fw2                      !fraction of region 2 solute in aqueous phase
real(8), allocatable, dimension(:)  :: v1                       !volume of water column
real(8):: v2

real(8)                             :: omega                    !mass transfer coefficient

real(8), allocatable, dimension(:)  :: lamda                    !Benthic leakage parameter

real(8), allocatable, dimension(:)  :: m1_input,m2_input        !at start of time step: the mass input in litt and benthic

! *******  Chemical Output Arrays ******************************
real(8),allocatable,dimension(:,:) :: m1_store,m2_store           !array of daily peak/avg. mass in littoral and benthic
real(8),allocatable,dimension(:,:) :: mavg1_store, mavg2_store
real(8),allocatable,dimension(:,:) :: release_mass                !vector of daily mass released
real(8),allocatable,dimension(:,:) :: aqconc_avg1 ,aqconc_avg2
real(8),allocatable,dimension(:,:) :: washout_mass               !mass lost due to washout

!***************************************************************

real(8),allocatable,dimension(:) :: aqconc1,aqconc2
real(8),allocatable,dimension(:) :: fractional_removal !vector of fraction of water column removed during drain

integer :: startday 

real(8),allocatable,dimension(:) :: degradateProduced1    !holds the ammount of degradate mass produced during degaradtion of parent in water column
real(8),allocatable,dimension(:) :: degradateProduced2    !holds the ammount of degradate mass produced during degaradtion of parent in benthic
 
real(8),allocatable,dimension(:) ::WashoutHalflife
real(8),allocatable,dimension(:) ::WatercoHalflife
real(8),allocatable,dimension(:) ::Hydrol1Halflife
real(8),allocatable,dimension(:) ::PhotolyHalflife
real(8),allocatable,dimension(:) ::VolatizHalflife
real(8),allocatable,dimension(:) ::LeakageHalflife
real(8),allocatable,dimension(:) ::BenthicHalflife
real(8),allocatable,dimension(:) ::Hydrol2Halflife


end module nonInputVariables