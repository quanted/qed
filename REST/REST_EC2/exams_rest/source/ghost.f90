subroutine GHOST(Y,IT)
! GHOST is primarily a program control module. It performs few computations
! aside from preserving intermediate variables and initializing run-control
! parameters. GHOST writes information to the output files for identifying
! the run, calls subroutines, and checks for error flags that may be set by
! the subroutines.
! Created August 1979 by L.A. Burns.
! Revised 08 May 1984 (LAB) -- command language modifications.
! Revisions 10/22/1988--run-time implementation of machine dependencies.
! Revisions 03/02/2000 for base flow augmentation in event of water deficit
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
use Floating_Point_Comparisons ! Revision 09-Feb-1999
Implicit None
! Y is chemical concentration referred to aqueous phase of system.
real (kind (0D0)) :: Y(KOUNT,KCHEM)
! Set up data handler for scratch file...VARIEC is a Fortran parameter
integer :: IBUFF(VARIEC), IT
! Local counters
integer :: K, NFIRST, NLAST, ISAVE
logical :: Problem ! to detect problem status in PRPROD
! If entry is via the interactive SHOW command, the RUN sector is skipped
Batch_control: if (BATCH == 0) then ! Simulation sector
   if (RPTFIL) then ! if a report file is requested...
      call PRCHEM ! Document input characteristics of compound
    else ! do the MWT check here instead of in PRCHEM
       ! molecular weight is required for checking loadings, etc.
       ! If it has not been specified, set error flag and notify user
       do K=1,KCHEM; if (MWTG(K) .LessThanOrEqual. 0.0) then
          IFLAG = 8
          write (stderr,fmt='(A,I2,A,1PG8.1/1X,A/A)')&
          ' Molecular weight of Chemical in ADB #',K,' = ',&
          MWTG(K),trim(CHEMNA(K)),&
          ' Molecular weight must be specified to RUN an analysis.'
       end if; end do
   end if
   if (IFLAG == 8) return
   if (RPTFIL) call PRPROD(RPTLUN,Problem) ! Print the product chemistry
   call CKPULS ! Call routine to check pulse loadings and print if needed
   call PRENV  ! Check TYPE; document input data describing the environment
   if (IFLAG >= 8) return ! Cancel run if input data no good
   ! Set loop boundaries
   if (PRSWG==0 .or. MODEG==3) then
      NFIRST = 1
      NLAST = 12
   else
      NFIRST = MONTHG
      NLAST = MONTHG
   endif
   ACCUM1 = 0.0 ! Zero accumulators for mean values of environmental data
   ACCUM2 = 0.0
   ACCUM3 = 0.0
   ACCUM4 = 0.0

! Preserve the "unaugmented" or user-supplied base flow into the system
   STFLOG_saved(1,:)=STFLOG(1,:)
   STSEDG_saved(1,:)=STSEDG(1,:)
   
   Data_blocks: do NDAT = NFIRST, NLAST ! Enter loop for (monthly) data blocks
      call DISTRB ! Compute distribution of chemical among species & forms
      call FLOWS  ! Convert input environmental data to program quantities
      if (IFLAG >= 8) return ! Abort system if necessary
      call CKLOAD ! Evaluate plausibility of loadings to system
      ! On return from CKLOAD, external loadings lacking carrier flows have
      ! been eliminated; other loads have been checked for supersaturation.
      ! Steady-state simulations need not be run if no non-zero loads remain.
      ! In addition, elimination of all loads raises the possibility of severe
      ! errors in the input loads,
      ! so the simulation will not be automatically continued.
      if (IFLAG >= 8) return
      call SOLAR ! Compute sunlight intensity and print globals (if desired)
      call FIRORD ! Compute first-order rate coefficients for processes
                  ! and evaluate input data
      ! Transfer computational variables to scratch pad
      if (MODEG<3 .and. PRSWG>0) cycle Data_blocks
      call PACSCR (IBUFF)
   end do Data_blocks
   call TABA
   
   ! Restore original (i.e., unaugmented) values of base flow into system
   STFLOG(1,:)=STFLOG_saved(1,:)
   STSEDG(1,:)=STSEDG_saved(1,:)
   
   ! In mode 1/2, when PRSWG=0 call routine to develop mean values
   ! of computational variables from scratch file:
   if (MODEG<3 .and. PRSWG==0) call M12BAR
   if (MODEG==2) call CKICM2(Y)
   ! CKICM2 sets initial conditions and checks for initial supersaturation or
   ! inappropriate bounds on integration
   if (IFLAG >= 8) return
   ! Steady-state computations executed in mode 1, not otherwise
   if (MODEG==1) then ! Compute steady-state concentrations in system elements
      call STEADY (Y)
      ! Problems with drift loads may be encountered in steady-state routine
      if (IFLAG >= 8) return
   endif
   
   ! Print final loads and Initial Conditions if in MODE 1 or 2:
   Mode_1_or_2: if (MODEG == 1 .or. MODEG == 2) then
      ! Call routine to print final values of chemical loads and
      ! initial conditions:
      if (RPTFIL) call PRICL(1) ! Call argument is NYR, the number of the year
      ! being processed during modes>2 -- included here solely as dummy value
      Mode_1_only: if (MODEG==1) then
         ! Report on general distribution and fate of chemicals
         if (RPTFIL .or. PLTFIL) call AVEOUT(Y)
         if (IFLAG >= 8) return
         call FLXOUT (Y)   ! Analyze and report mass flux ratios
         ! Steady-state analysis complete. Time frame for decay simulation
         ! computed from steady-state properties.
         ! Prepare to run decay simulation:
         do K = 1, KCHEM             ! Save steady-state pollutant masses
            QWSAV(K) = Z(5,K)        ! Pollutant mass in water column
            QSSAV(K) = Z(6,K)        ! Mass in sediments
            QTSAV(K) = Z(5,K)+Z(6,K) ! Total pollutant mass in system
         end do
      end if Mode_1_only
   end if Mode_1_or_2
   ! Allow for non-mode 1 runs with single segments:
   if (KOUNTW .Equals. 0.0) KOUNTW = 1.0
   if (KOUNTS .Equals. 0.0) KOUNTS = 1.0
   return
   
else Batch_control ! Sector purpose: to call subroutines for the SHOW command
   ! Subroutines referenced TABC, TABD, SOLAR, CKPULS, PRPROD,
   !                        PRCHEM, PRICL
   ! IT      DESCRIPTION
   ! ==      ===========
   !
   !  1      SHOW ADVECTION
   !  2      SHOW TURBULENCE, i.e., dispersive flow field
   !  3      SHOW GLOBALS
   !  4      SHOW PULSE LOADS
   !  5      SHOW PRODUCTS
   !  6      SHOW CHEMISTRY
   !  7      SHOW LOADS
   ! Set output unit for terminal output
   ISAVE = RPTLUN
   RPTLUN = stdout
   Show_what: select case (IT)
   case (1) Show_what ! Process the 'SHOW ADVECTION'
      BATCH = 1
      call TABC
   case (2) Show_what ! Process the 'SHOW TURBULENCE' option
      BATCH = 1
      call TABD
   case (3) Show_what ! Process the 'SHOW GLOBALS' option
      BATCH = 1
      call SOLAR
   case (4) Show_what ! Process the 'SHOW PULSE LOADS' option
      BATCH = 1
      call CKPULS
   case (5) Show_what ! Process the 'SHOW PRODUCTS' option
      BATCH = 1
      call PRPROD(RPTLUN,Problem)
   case (6) Show_what ! Process the 'SHOW CHEMISTRY' option
      BATCH = 1
      call PRCHEM
   case (7) Show_what ! process the 'SHOW LOADS' option
   BATCH = 1
   call PRICL (YEAR1G)
   end select Show_what
   BATCH = 0
   RPTLUN = ISAVE
end if Batch_control
return
end Subroutine GHOST
