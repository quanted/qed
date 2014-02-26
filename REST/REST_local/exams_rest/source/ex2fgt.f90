subroutine EX2FGT(Y,JFLAG,RTIMER,ITIMER,CurrentDate)
! Subroutine to record time-trace computations in transfer files
! Created 11-SEP-1991; revised 23-JAN-1992 to add modes 1 & 2
! revised November 1998 to improve algorithms and add HWIR reach processing
! revised April 2002 to implement user choice for output file production
! revised April 2002 to implement EcoTox file
use Implementation_Control; use Global_Variables; use Local_Working_Space
use Internal_Parameters; Implicit None
real (kind (0D0)), intent (in) :: Y(KOUNT,KCHEM)
! Y is toxicant concentration in mg/L referred to aqueous phase of segment
real, intent (in) :: RTIMER
integer :: I, K ! loop counters
integer, intent (in) :: JFLAG
integer, intent (in) :: ITIMER
! JFLAG is 1 on initial condition call(?), may be useful...
! RTIMER is time in days during mode 3 simulations
! ITIMER is integer-valued time in Mode 2 simulations
character(len=10) :: CurrentDate

Chemicals: Do K=1,kchem
   Calc_Vector = 0.0E+00
   ! Use reach structure to calculate for limnetic zone
   Limnetic_Zone: do I=1, Reaches_in_System
      where (Reach_ID==I .and. .not.Benthic)
         ! Total concentration in water column (HWIR CWtot)
         Calc_Vector(:,1) = VOLG(1:KOUNT)*dabs(Y(1:KOUNT,K))
         ! Dissolved concentration in limnetic zone (HWIR Cwater)
         Calc_Vector(:,2) = Calc_Vector(:,1)*ALPHA(29,1:KOUNT,K)
         ! Concentration in (fresh weight) plankton (for FGETS)
         Calc_Vector(:,3) = Calc_Vector(:,1)*ALPHA(32,1:KOUNT,K)&
                            /(BIOTOL(1:KOUNT)*10.0)
      elsewhere ! i.e., in benthic segments; other reaches
         Calc_Vector(:,1) = 0.0E+00
         Calc_Vector(:,2) = 0.0E+00
         Calc_Vector(:,3) = 0.0E+00
      end where
      Reach_Cwtot(I,K)     = sum(Calc_Vector(:,1))/Reach_Limnetic_Volume(I)
      Reach_Cwater(I,K)    = sum(Calc_Vector(:,2))/Reach_Limnetic_Volume(I)
      Reach_Cplankton(I,K) = sum(Calc_Vector(:,3))/Reach_Limnetic_Volume(I)
   end do Limnetic_Zone
   Mean_Cwater(K)    = sum(Reach_Cwater(:,K)*Reach_Limnetic_Volume)&
                           /Total_Limnetic_Volume
   Mean_Cplankton(K)  = sum(Reach_Cplankton(:,K)*Reach_Limnetic_Volume)&
                           /Total_Limnetic_Volume

   ! Use reach structure to calculate for macrobenthos in benthic zone
   Benthic_Zone: do I=1, Reaches_in_System
      where (Reach_ID==I .and. benthos)
        Calc_Vector(:,7)=VOLG(1:KOUNT)*dabs(Y(1:KOUNT,K))
        Calc_Vector(:,4)=Calc_Vector(:,7) /SEDCOL(1:KOUNT)
        Calc_Vector(:,5)=Calc_Vector(:,7) * ALPHA(29,1:KOUNT,K)
        Calc_Vector(:,6)=Calc_Vector(:,7) * ALPHA(32,1:KOUNT,K)&
                            /(BIOTOL(1:KOUNT)*10.0)
      elsewhere
        Calc_Vector(:,7) = 0.0E+00
        Calc_Vector(:,4) = 0.0E+00
        Calc_Vector(:,5) = 0.0E+00
        Calc_Vector(:,6) = 0.0E+00
      end where
        Reach_Cbtot(I,K)  = sum(Calc_Vector(:,4))/Reach_Benthos_Volume(I)

        ! Cbdiss is exposure of benthos to dissolved chemical;
        ! 'B' compartments w/o benthos skipped
        Reach_Cbdiss(I,K) = sum(Calc_Vector(:,5))/Reach_Benthos_Volume(I)

        Reach_Cbnths(I,K) = sum(Calc_Vector(:,6))/Reach_Benthos_Volume(I)
   end do Benthic_Zone
   Mean_Cbtot(K) = sum(Reach_Cbtot(:,K)*Reach_Benthos_Volume)&
      /Total_Benthos_Volume
   Mean_Cbdiss(K)= sum(Reach_Cbdiss(:,K)*Reach_Benthos_Volume)&
      /Total_Benthos_Volume
   Mean_Cbnths(K)= sum(Reach_Cbnths(:,K)*Reach_Benthos_Volume)&
      /Total_Benthos_Volume
end do Chemicals

if (HWRFIL) call HWIR_Exposure_Data ! for reach entries of the chemicals
if (FGTFIL) call Fgets_Model_Exposure_Data
if (BASFIL) call Bass_Model_Exposure_Data
if (TOXFILR) call EcoToxReachFile
return

contains
!*****************************************************************************
Subroutine Fgets_Model_Exposure_Data ()
Implicit None
! In mode 3, I am reporting the mean plankton standing crop and limnetic
! water temperature in the current month. In Mode 1/2 I report for
! the "month" being used as the data source.
! N.B. the use of "32767" as last element of format is actually allowing
! for some unknowable chemical outputs.
write (FG1LUN,fmt='(1PE12.5,1X,0PF5.1,1X,1PE9.2,32767(1X,E9.2))')&
   RTIMER,Mean_Water_Temperature,Plankton_FW,&
   (Mean_Cwater(K),K=1,KCHEM), (Mean_Cbnths(K),K=1,KCHEM), &
   (Mean_Cplankton(K),K=1,KCHEM)
end Subroutine Fgets_Model_Exposure_Data
!*****************************************************************************
Subroutine Bass_Model_Exposure_Data () ! Write BASS exposure data
Implicit None
write (BASSLUN, fmt='(1PE12.5,500(1X,E9.2))') &
   RTIMER, Mean_Water_Temperature, Mean_Water_Depth, Mean_Phytoplankton, &
   Mean_Zooplankton, Mean_Periphyton, Mean_Benthos, Mean_Insects, &
   (Mean_Cwater(K), Mean_Cbnths(K)*10.0, & !*10.0 to recover dry weight FGETS
    Mean_Cinsct(K), Mean_Cphytn(K), &
    Mean_Cpplnk(K), Mean_Czplnk(K), K=1,kchem)
! remember to multiply Cbnths by 10 here to get dry weight basis
return
end Subroutine Bass_Model_Exposure_Data
!*****************************************************************************
Subroutine HWIR_Exposure_Data () ! Write HWIR exposure data
Implicit none
write (HWIRLUN, fmt='(1PE12.5,32767(1X,E9.2))') &
 RTIMER, (Reach_TSS(I),focbenthic(I),I=1,Reaches_in_System),&
         ((Reach_Cwtot(I,K), Reach_Cwater(I,K),&
           Reach_Cbtot(I,K), Reach_Cbdiss(I,K), &
          I=1,Reaches_in_System),K=1,KCHEM)
end Subroutine HWIR_Exposure_Data
!*****************************************************************************
Subroutine EcoToxReachFile ()
! EcoTox Reach-Oriented Exposure 
Implicit none
if (MODEG==3) then ! food-chain concentrations are on dry weight basis here
                   ! by virtue of 10x multiplier
   write (TOXRLUN,fmt='(1X,A,32767(1X,ES9.2))') ' '//CurrentDate,&
         (( Reach_Cwater(I,K), Reach_Cbdiss(I,K), &
            10.0*Reach_Cplankton(I,K), 10.0*Reach_Cbnths(I,K), &
          I=1,Reaches_in_System),K=1,KCHEM)
elseif (MODEG==2) then
   write (TOXRLUN, fmt='(1X,I5,32767(1X,ES9.2))') &
   ITIMER, (( Reach_Cwater(I,K), Reach_Cbdiss(I,K), &
              10.0*Reach_Cplankton(I,K), 10.0*Reach_Cbnths(I,K), &
          I=1,Reaches_in_System),K=1,KCHEM)
else ! Should not be here
   write (stderr, fmt='(A)')&
 ' Exams system error F0002 in routine EX2FGT. Notify author.'
   STOP
end if
end Subroutine EcoToxReachFile
!*****************************************************************************
end Subroutine EX2FGT
! Notes
! As gill uptake is a medium to itself, FGETS/BASS want total dissolved
! concentration, hence the use of ALPHA(29) in these computations.
!    For plankton standing stock (wet weight; assume dry weight is 10% of
! fresh weight), calculate KCHEM concentrations in the plankton. BIOTOL
! (computed in DISTRB) is dw biomass as kg/L of segment water, just as Y
! is mg of toxicant per L of segment water. Computation thus has units of
! mg toxicant per kg of tissue mass (*10 to convert dw to fw). FGETS assumes
! density of 1.0 and takes it as mg/L of tissue.
!    In the benthic zone--do concentrations in benthos (for food chain).
! BIOTOL, computed in DISTRB, is kg dry biomass per liter
! of pore water, so computed variable is mg toxicant per kg biomass
! (*10 to get biomass as fresh weight)
