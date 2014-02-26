Subroutine Parameter_Summary (Monthly) ! file ParSum.f90
! Nov 1998.
! Routine to summarize system parameters needed for transfer to
! collaborating programs. These are not state variables, but may
! vary according to user specifications. They are calculated only
! when they change, thus minimizing the work needed in other output
! routines. If fatal problems arise, IFLAG can be set to 8 to
! signal the calling routine.
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
Implicit None

! local counters
integer :: I, J, J1, K
integer, intent (in) :: Monthly
!IFLAG = 1 ! Reset error flag?
!write (*,*) ' Computational month = ', Monthly

! Initialize reach varibles
! Group 1: not currently available
Phytoplankton = 0.0E+00
Zooplankton   = 0.0E+00
Periphyton    = 0.0E+00
Insects       = 0.0E+00

! Group 2: currently available
Plankton_Biomass  = 0.0E+00
Bacterioplankton  = 0.0E+00
Water_Temperature = 0.0E+00
Reach_TSS         = 0.0E+00
focbenthic        = 0.0E+00
Benthos_Biomass   = 0.0E+00

! Initialize averages
Mean_Bacterioplankton  = 0.0E+00
Mean_Phytoplankton     = 0.0E+00
Mean_Zooplankton       = 0.0E+00
Mean_Plankton_Biomass  = 0.0E+00
Mean_Benthos           = 0.0E+00
Mean_Insects           = 0.0E+00
Mean_Periphyton        = 0.0E+00
Mean_Water_Temperature = 0.0E+00


Calc_vector = 0.0E+00

! Use structure to calculate limnetic properties
do I=1, Reaches_in_System
   where (Reach_ID==I .and. .not.benthic)
      Calc_Vector(:,1) = VOLG(1:KOUNT)*&
                    (SUSEDG(1:KOUNT,Monthly)+PLMASG(1:KOUNT,Monthly))
   elsewhere
      Calc_Vector(:,1) = 0.0E+00
   end where
!write (*,*) ' TSS seg vector = ', Calc_Vector
   Reach_TSS(I) = sum(Calc_Vector(:,1))/Reach_Limnetic_Volume(I)
end do
!write (*,*) ' reach TSS vector = ', reach_tss


! Use structure to calculate benthic properties
do I=1, Reaches_in_System
   where (Reach_ID==I .and. benthos)
      Calc_Vector(:,1) = VOLG(1:KOUNT)*FROCG(1:KOUNT,Monthly)
   elsewhere
      Calc_Vector(:,1) = 0.0E+00
   end where
   focbenthic(I) = sum(Calc_Vector(:,1))/Reach_Benthos_Volume(I)
end do
!write (*,*) ' Reach benthic foc vector = ',focbenthic

! BASS calculations
K = 1         ! Used to update starting point for compartment summing
Reach: do I = 1, Reaches_in_System
  Column: do J = K, KOUNT-1
!    Phytoplankton(I) = Phytoplankton(I) + ...(J)
!    (function of CHL)
!    Zooplankton(I) = Zooplankton(I) + ...(J)
!    (Total - phytoplankton ... will need control against zero values)
!    Bacterioplankton(I) = Bacterioplankton(I) + BACPLG(J,Monthly)*VOLG(J)
     Plankton_Biomass(I) = Plankton_Biomass(I) + PLMASG(J,Monthly)*VOLG(J)
     Water_Temperature(I)= Water_Temperature(I)+ TCELG(J,Monthly)*VOLG(J)
     if (TYPEG(J+1) == 'B') then ! end of water column, so
                                 ! locate the next water column for restart
        K=(J+2)                  ! if only 1 B, it starts here
        do J1 = K, KOUNT         ! but if not, find where it starts
                                 ! Note that J1 could be beyond the end of
                                 ! KOUNT, except that K > KOUNT so the loop
                                 ! will not execute
           if (TYPEG(J1) == 'B') then ! continuing benthic zone, so
             K = K+1
           else                       ! found start of next water column, so
             exit Column              ! exit water column loop, do next reach
           end if
        end do
     end if
  end do Column


! Accumulate for system-wide averages
!Mean_Bacterioplankton = Mean_Bacterioplankton + Bacterioplankton(I)
Mean_Water_Temperature = Mean_Water_Temperature + Water_Temperature(I)
Mean_Plankton_Biomass  = Mean_Plankton_Biomass  + Plankton_Biomass(I)
! Calculate average values for the reach water column
!Phytoplankton(I) = Phytoplankton(I)/Com_Count
!Zooplankton(I) = Zooplankton(I)/Com_Count
!Bacterioplankton(I) = Bacterioplankton(I)/Reach_Limnetic_Volume(I)
Water_Temperature(I)= Water_Temperature(I)/Reach_Limnetic_Volume(I)
Plankton_Biomass(I) = Plankton_Biomass(I)/Reach_Limnetic_Volume(I)

end do Reach

! Calculate whole-system values
!Mean_Bacterioplankton  = Mean_Bacterioplankton  /Total_Limnetic_Volume
Mean_Water_Temperature = Mean_Water_Temperature /Total_Limnetic_Volume
Mean_Plankton_Biomass  = Mean_Plankton_Biomass  /Total_Limnetic_Volume



! Use structure to calculate benthic properties
do I=1, Reaches_in_System
   where (Reach_ID==I .and. benthos)
      Calc_Vector(:,1) = VOLG(1:KOUNT)*BNMASG(1:KOUNT,Monthly)
   elsewhere
      Calc_Vector(:,1) = 0.0E+00
   end where
   Benthos_Biomass(I) = sum(Calc_Vector(:,1))/Reach_Benthos_Volume(I)
end do
! Output unit for BASS is mg/m^2
Mean_Benthos = 1.0E+03*sum(Benthos_Biomass*Reach_Benthos_Volume)&
               /Total_Benthos_Volume

! FGETS wants fresh weight. Here we assume dw is 10% of fw.
Plankton_FW = Mean_Plankton_Biomass/0.10

! Alias for BASS variables not yet available:
! Group 1: not currently available
Mean_Phytoplankton = -999.00
Mean_Zooplankton   = -999.00
Mean_Periphyton    = -999.00
Mean_Insects       = -999.00

!write (*,*) ' Bactpl = ', Mean_Bacterioplankton
!write (*,*) ' mean TCEL   = ', Mean_Water_Temperature

return
end Subroutine Parameter_Summary
