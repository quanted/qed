module allocations
!Written by Dirk F. Young (Virginia, USA)
implicit none


contains
    subroutine allocation1
    
        use nonInputVariables
        use variables, ONLY: nchem
        integer :: status   !integer :: status           !array allocation status,  0=success
        
        allocate (wind(num_records), STAT=status)
        allocate (temp_avg(num_records), STAT=status)  
        allocate (evap(num_records), STAT=status)
        allocate (precip(num_records), STAT=status)

        allocate (daily_depth(num_records), STAT=status)
        allocate (depth_release(num_records), STAT=status)
        allocate (makeupwater(num_records), STAT=status)

        allocate (overflow(num_records), STAT=status)

        allocate (k_aer_aq(num_records), STAT=status)           
        allocate (k_anaer_aq(num_records), STAT=status)         
        allocate (k_aer_s(num_records), STAT=status)            
        allocate (k_anaer_s(num_records), STAT=status)

        allocate (k_hydro(num_records), STAT=status)   
        allocate (k_flow(num_records), STAT=status)

        allocate (k_volatile(num_records), STAT=status)
        allocate (k_photo(num_records), STAT=status)
        allocate (k_leakage(num_records), STAT=status)
   
        allocate (gamma_1(num_records), STAT=status)
        allocate (gamma_2(num_records), STAT=status)
        
        allocate (lamda(num_records), STAT=status)
        
        allocate (A(num_records), STAT=status)
        allocate (B(num_records), STAT=status)
        allocate (E(num_records), STAT=status)
        allocate (F(num_records), STAT=status)
        
        allocate (theta(num_records), STAT=status)
        allocate (capacity_1(num_records), STAT=status)
        allocate (fw1(num_records), STAT=status)
        allocate (v1(num_records), STAT=status)
        
        allocate (m1_input(num_records), STAT=status)
        allocate (m2_input(num_records), STAT=status)  
        !***************************************************
        allocate (m1_store(num_records,nchem), STAT=status)
        allocate (m2_store(num_records,nchem), STAT=status)
        allocate (mavg1_store(num_records,nchem), STAT=status)
        allocate (mavg2_store(num_records,nchem), STAT=status)
        allocate (release_mass(num_records,nchem), STAT=status)
        allocate (aqconc_avg1(num_records,nchem), STAT=status) 
        allocate (aqconc_avg2(num_records,nchem), STAT=status) 
        
        allocate (washout_mass(num_records,nchem), STAT=status)
           
        
        !*******************************************************
        allocate (plant_factor(num_records), STAT=status)   
        allocate (fractional_removal(num_records), STAT=status) 
        allocate (aqconc1(num_records), STAT=status) 
        allocate (aqconc2(num_records), STAT=status)      
        allocate (degradateProduced1(num_records), STAT=status)
        allocate (degradateProduced2(num_records), STAT=status)     
        
        allocate (WashoutHalflife(nchem), STAT=status)
        allocate (WatercoHalflife(nchem), STAT=status)
        allocate (Hydrol1Halflife(nchem), STAT=status)
        allocate (PhotolyHalflife(nchem), STAT=status)
        allocate (VolatizHalflife(nchem), STAT=status)
        allocate (LeakageHalflife(nchem), STAT=status)
        allocate (BenthicHalflife(nchem), STAT=status)
        allocate (Hydrol2Halflife(nchem), STAT=status)
        
        
    end subroutine allocation1

   !**********************************************************************
    subroutine initializations
        use nonInputVariables
        implicit none
        mavg1_store = 0.
        mavg2_store = 0.
        aqconc_avg1= 0.
        aqconc_avg2= 0.
        release_mass =0.
        m1_store =0.
        m2_store = 0. 
        
        degradateProduced1 = 0.
        degradateProduced2 = 0.
        washout_mass= 0.
        
    end subroutine initializations
    !**********************************************************************

end module allocations