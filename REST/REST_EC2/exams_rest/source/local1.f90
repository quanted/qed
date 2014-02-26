module Internal_Parameters
! file LOCAL1.f90
! Revised 06 March 1984 (LAB) for scratch file operations.
! Revised 22 April 1997 (LAB) to add 60- and 90- day event variables.
! Revised 10 November 1998 (LAB) to allocate computational storage as needed
! Revised 30 March 1999 (LAB) to add Stiff_Start
! Revised 18 April 2001 (LAB) to add local version of 2nd-order biolysis
! Revised 24 July 2001 to add DaysInYear, a counter of the days in the
!   the year(s) of the current Mode 3 simulation. Used for annual averages.
! Revised 2002-04-12 for user-specified-duration annual maximum event tracking
Implicit None
Save

Real (Kind (0D0)), Allocatable :: CONLDL(:,:), INTINL(:,:,:),&
                     TOTKL(:,:), YIELDL(:,:,:)
Real (Kind (0E0)), Allocatable :: &
      ALPHA(:,:,:), BIOLKL(:,:), BIOTOL(:),&
      EXPOKL(:,:), HYDRKL(:,:), OXIDKL(:,:),&
      PHOTKL(:,:), REDKL(:,:),  S1O2KL(:,:),&
      SEDCOL(:), SEDMSL(:), VOLKL(:,:), WATVOL(:),&
      YSATL(:,:,:)
! WATVOL is volume of water in segment, in Liters
! SEDCOL is sediment to water ratio in segment, kg sediment per Liter of water
! SEDMSL is mass of sediment solids in segment, in kg
! BIOTOL is biomass (total plankton or benthos): kg Dry Wt per Liter of water

real, allocatable :: TOTLDL(:,:), YSUM(:,:)
integer :: FRSTYR=1, KEQN=1, LASREC=0
! FRSTYR is the starting point of the loop on the number of
! years requested for (mode 3) simulation via NYEARG.
! LASREC points to the next available record in the scratch pad.
!
! accumulators and analysis variables
real :: FLUXCT=0.0
real, allocatable :: YBIOS(:), YBIOW(:), YEXPO(:),&
        YGWAT(:), YHYDR(:), YOXID(:), YPHOT(:),&
        YRED(:),  YS1O2(:), YSUMS(:,:,:),&
        YTOT(:,:,:), YVOLK(:)

! working storage vector
real, allocatable, dimension(:,:) :: Calc_Vector

!**************************************************************************
! Variables for FGETS transfer file -- for whole system
real :: Plankton_FW=0.0
! plankton fresh weight in food chain, converted from Exams' dry weight

!**************************************************************************
! Variables for reach summaries and BASS transfer file. Current version
! of BASS requires system-wide averaging for transfer file.
real, allocatable, dimension(:) :: Reach_Depth
! Reach_Depth is the total depth of each reach
real, allocatable, dimension(:) :: Reach_Limnetic_Volume
real, allocatable, dimension(:) :: Reach_Benthic_Volume
real, allocatable, dimension(:) :: Reach_Benthos_Volume
!
! The number of benthic and water column compartments in each reach
! (Note that the number of "benthos" compartments is usually one (1), 
! because the surficial layer is the layer populated by macrobenthos.)
integer, allocatable, dimension(:) :: Benthic_Count
integer, allocatable, dimension(:) :: Benthos_Count
integer, allocatable, dimension(:) :: Limnion_Count
integer, allocatable, dimension(:) :: Reach_ID
! Reach_ID attaches a reach number to each compartmnet
!
logical, allocatable, dimension(:) :: Benthic   ! to tag compartments...
logical, allocatable, dimension(:) :: Limnetic  ! to tag compartments...
logical, allocatable, dimension(:) :: Benthos   ! to tag compartments...
! Reach standing stocks
real, allocatable, dimension(:) :: Bacterioplankton  ! cfu/ml
real, allocatable, dimension(:) :: Phytoplankton     ! mgDW/L
real, allocatable, dimension(:) :: Zooplankton       ! mgDW/L
real, allocatable, dimension(:) :: Plankton_Biomass  ! mgDW/L
! HWIR-specific output variables
! TSS (total suspended solids) -- sum of SUSEDG and PLMASG
real, allocatable, dimension(:) :: Reach_TSS         ! mgDW/L
real, allocatable, dimension(:) :: focbenthic        ! dimensionless
! benthic invertebrates
real, allocatable, dimension(:) :: Benthos_Biomass   ! mgDW/m^2
! incidental terrestrial insects
real, allocatable, dimension(:) :: Insects           ! mgDW/m^2
! periphyton or grazable algae
real, allocatable, dimension(:) :: Periphyton        ! mgDW/m^2
real, allocatable, dimension(:) :: Water_Temperature ! Celsius
! Chemical contaminant variables
real, allocatable, dimension(:,:) :: Reach_cwtot       ! mg/L in Limnetic Zone
real, allocatable, dimension(:,:) :: Reach_Cwater      ! mg/L diss in Limn Z
real, allocatable, dimension(:,:) :: Reach_Cplankton   ! mg/kg FW  in Limn Z
real, allocatable, dimension(:,:) :: Reach_Cbtot       ! mg/kg DW in Benthic Z
real, allocatable, dimension(:,:) :: Reach_Cbdiss      ! mg/L pore water
real, allocatable, dimension(:,:) :: Reach_Cbnths      ! mg/kg dw for BASS,
                                                       ! mg/kg fw for FGETS
! System-wide averages
real :: Mean_Water_Depth=0.0            ! water depth, meters
real :: Mean_Bacterioplankton=0.0
real :: Mean_Phytoplankton=0.0
real :: Mean_Zooplankton=0.0
real :: Mean_Benthos=0.0
real :: Mean_Insects=0.0
real :: Mean_Periphyton=0.0
real :: Mean_Water_Temperature=0.0
real :: Total_Limnetic_Volume=0.0
real :: Total_Benthic_Volume=0.0
real :: Total_Benthos_Volume=0.0
real :: Mean_Plankton_Biomass=0.0
integer :: Reaches_in_System=0 ! counter to convert compartment structure
! Chemical averages -- allocated KCHEM in code
real, allocatable, dimension(:) :: Mean_Cwater
real, allocatable, dimension(:) :: Mean_Cplankton
real, allocatable, dimension(:) :: Mean_Cbtot
real, allocatable, dimension(:) :: Mean_Cbdiss
real, allocatable, dimension(:) :: Mean_Cbnths
real, allocatable, dimension(:) :: Mean_Cinsct
real, allocatable, dimension(:) :: Mean_Cphytn
real, allocatable, dimension(:) :: Mean_Cpplnk
real, allocatable, dimension(:) :: Mean_Czplnk
!**************************************************************************
real :: WLAML(46)=0.0, ACCUM1(52)=0.0
! accum1 for documenting mean values of environmental parameters.

! Variables for use in DISTRB -- these will be allocated as
real, allocatable :: KPDOCL(:,:), KOCL(:), KOWL(:), KPBL(:,:)

logical :: Stiff_Start=.false.
! Stiff_Start signals that the problem was initially diagnosed as stiff,
! so the Gear's method integrator should print the initial conditions.
! When the problem solution is initiated with Adam and then transferred
! to Gear, printing of the I.C. is skipped (see STFINT)

!**************************************************************************
! internal versions of biolysis rate constants
! If the input chemical properties include rate constants, they are
! transferred to local versions. If not, but aquatic half-lives are
! supplied, the aerobic half-life is used to generate KBACW and the
! anaerobic half-life is used to generate KBACS

real, allocatable :: KBACWL(:,:,:), KBACSL(:,:,:)

!**************************************************************************
! Gas constant factor for Arrhenius functions (the 4.58 in the manual)
real, parameter :: R_Gas = 1.98588E-03 ! Kcal/deg.mole Gas Constant R
real :: R_Factor ! R_Factor = R_Gas/log10(exp(1.0))
!**************************************************************************

end module Internal_Parameters
