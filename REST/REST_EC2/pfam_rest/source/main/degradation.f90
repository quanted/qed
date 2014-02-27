module degradation
!Written by Dirk F. Young (Virginia, USA).

contains
!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subroutine gamma_one
      !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      !This subroutine calculates the Gamma_1 --the overall littoral degradation rate
      !metabloism is coded to accept sorbed phase degradation independently, but 
      !standard water bodies equate sorbed and aqueous metabloism rate
      !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      use nonInputVariables, ONLY: num_records, k_aer_aq, k_aer_s, k_hydro,k_photo,k_flow,k_volatile,k_leakage, fw1,gamma_1
      implicit none
      !real(8),intent(out), dimension(num_records)::gamma_1 !output overall aqueous-phase first-order rate littoral (per sec)

      gamma_1 = k_flow+ (k_photo + k_hydro +k_volatile + k_leakage) *fw1  +k_aer_aq*fw1 + k_aer_s*(1.-fw1)

    end subroutine gamma_one
!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    subroutine gamma_two
       !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       !This subroutine calcualtes the overall rates for given
       !the individual rates for all processes
       !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       use nonInputVariables, ONLY: num_records, k_anaer_aq,k_anaer_s, k_hydro,fw2,gamma_2
       implicit none
       !real(8),intent(out), dimension(num_records)::gamma_2 !output overall sorbed-phase first-order rate benthic (per sec)
          
       gamma_2  = k_anaer_aq*fw2 +k_anaer_s*(1.-fw2)+ k_hydro*fw2
    end subroutine gamma_two
   
!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subroutine photolysis(index)
       !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       !calculates photolysis rate, creates a vector k_photo of daily photolysis rates, Rates vary due to depth only
       !K_photo in per sec
        !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       use variables, ONLY:LAT, canopymax,SUSED,CHL,DOC1,CLOUD,dfac,minimum_depth,RFLAT,photo
       use nonInputVariables, ONLY: num_records,daily_depth,temp_avg , k_photo ,  plant_factor  
       implicit none

       integer, intent(in) :: index
       real(8):: A
       real(8):: KDP    !calculated EXAMS parameter  
       real(8),dimension(num_records) :: term3
       real(8) term1,term2,term4
       real(8) :: reflatitude, photorate
       
       reflatitude = RFLAT(index)
       photorate = photo(index)

       A= 0.141 +101.*CHL+6.25*DOC1 +.34*SUSED   !EXAMS 2.98 section 2.3.3.2.2
        
       term1 = 191700.+87050.*cos(0.0349*LAT)    !latitude correction
       term2 = 191700.+87050.*cos(0.0349*reflatitude)
        
       term3 = (1.-exp(-dfac*daily_depth*A))/dfac/daily_depth/A
       term4 = 1.-0.056*cloud
           
       KDP  = 8.0225368e-6/photorate !KDP  = 0.69314718/photo/24/3600.  !EXAMS parameter (per sec)
         
       !The following condition was placed on the photolysis in order to not
       !perform photolysis on a dry field.  The photolysis routine was written for
       !water bodies, not fields.  Therefore, if photolysis off the field is wanted, then 
       !users should inlude the photolysis rate in the soil degradation input.  May 1, 2009.

        where (daily_depth > minimum_depth*1.001)
           k_photo = KDP*term1/term2*term3*term4 * (1.-CanopyMax *plant_factor ) !effective photolysis rate (per sec)
        elsewhere
           k_photo = 0.
        end where
           
        where (temp_avg <= 0) !eliminate volatilization and photolysis when the pond freezes
           k_photo = 0.
        end where
        
    end subroutine photolysis
    
!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subroutine metabolism(index)
       !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       !This subroutine calculates the first-order metabolic degradation rate, given the 
       ! half life inputs for areobic and anaerobic sorbed and aqueous phases.
       !%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       use variables, ONLY:QT,minimum_depth ,aer_aq,anae_aq,temp_ref_aer , temp_ref_anae,drysoil,temp_ref_dry
       use nonInputVariables, ONLY: num_records, temp_avg, daily_depth,k_aer_aq, k_anaer_aq, k_aer_s,k_anaer_s
         
       implicit none                      
       integer,intent(in):: index                 
       !Unflooded soil can have a different degradation rate than flooded soil
       where (daily_depth > minimum_depth*1.001)
          k_aer_aq = 8.0225368e-6/aer_aq(index)*QT**((temp_avg - temp_ref_aer(index))/10.)    !k_aer_aq  = 0.69314718/aer_aq/86400.
          k_aer_s  = k_aer_aq                                                   !effective solid metab rate (per sec)
         
          k_anaer_aq = 8.0225368e-6/anae_aq(index)*QT**((temp_avg - temp_ref_anae(index))/10.) !effective aq metab rate (per sec)
          k_anaer_s  = k_anaer_aq          !effective sorbed rate        
       elsewhere  !when it is unflooded, everything degrades at the same rate.In essence-one campartment
          k_anaer_aq = 8.0225368e-6/drysoil(index)*QT**((temp_avg - temp_ref_dry(index))/10.)    !unflooded condition soil water rate
          k_anaer_s  = k_anaer_aq          !unflooded condition soil deg rate
                 
          k_aer_aq   = 8.0225368e-6/drysoil(index)*QT**((temp_avg - temp_ref_dry(index))/10.)    !essentially there is no water column here
          k_aer_s    = k_aer_aq           !so approximate the tiny water remaining as soil degradation    
       end where
          
    end subroutine metabolism

!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subroutine hydrolysis (index)        !calculates the hydrolysis rate, given the half life 
          use variables, ONLY:minimum_depth,hydro
          use nonInputVariables, ONLY: num_records, daily_depth, k_hydro
          implicit none

          integer,intent(in) :: index
          
          k_hydro  = 0.69314718/hydro(index)/86400.

          !Since the field is supposed to be unflooded when depth is minimum depth, we will eliminmate hydrolysis since 
          !we are saying that no water exists in the benthic during this period.
          
          where (daily_depth <= minimum_depth*1.001) k_hydro = 0.
               
    end subroutine hydrolysis
!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subroutine volatilization (index)
       !this subroutine calculates the effective first-order volatilization rate
       use variables, ONLY:  area,minimum_depth,MWT,sol,vapr,temp_ref_henry,heat_henry 
       use nonInputVariables, ONLY:  num_records,WIND,temp_avg, daily_depth, k_volatile 
       implicit none
       
       integer, intent(in) :: index
    
      ! real(8), dimension(num_records) :: KO2           !exams parameter, but in m/s
      ! real(8), dimension(num_records) :: VW            !p.36 EXAMS (eq 2.82)
      
       real(8), dimension(num_records) :: RL             !liquid phase resistance
       real(8), dimension(num_records) :: RG             !gas phase resistance      
       real(8), dimension(num_records) :: HENRY     !Henry's constant       
       real(8) :: H_ref     !reference Henry's constant at Temp_ref_henry    
       real(8) :: f2      
       real(8),dimension(num_records) :: U          !wind speed adjusted to 10m above surface
       real(8),dimension(num_records):: v  
       real(8):: wind_height !height of wind measurement (m)
       parameter (wind_height = 6) !met file wind measured at 6 m  
       real(8) :: dHoverR
            
       v = area*daily_depth
      
       H_ref = VAPR(index)/760./(SOL(index)/MWT(index)) !EXAMS p188 version 2.98
       
       dHoverR = heat_henry(index)/8.314472             !R = 8.314472 in Joules/K/mol
       f2= 1./(temp_ref_henry(index)+273.15)
       
       HENRY = H_ref *exp( -dHoverR *(1./(temp_avg+273.15)- f2))
       
       !******calculate liquid resistance*********
       U = 4./log10(wind_height*1000.)*wind  !adjust wind ht to 10m (see paragraph under eqn 2-85)

       where (U < 5.5)                 !default conditions p.36
            RL = 4.19e-6*sqrt(U)           !m/s
       elsewhere (U>=5.5)
            RL = 3.2e-7*U*U                !m/s
       end where

       RL =RL*1.024**(temp_avg-20.)          !temp adjustment p. 36
       RL = 1./RL/sqrt(32./MWT(index))           !(s/m) EXAMS (eq 2-77)

       !******calculate gas resistance*****************************************
       ! wind_10cm = U/2.   !convert to wind speed at 10 cm

        !VW = (0.1857+5.68*U)                      !(m/hr) EXAMS 2-82 optimized
        !RG = R*(temp+273.15)/VW/HENRY/sqrt(18./MWT)     !(hr/m) EXAMS 2-76
        !R= 8.2057e-5  is gas constant (atm m3/mol) for calcs below
        
        RG = (8.2057e-5)*(temp_avg + 273.15)/(0.1857+5.68*U)/HENRY/sqrt(18./MWT(index))     !(hr/m) EXAMS 2-76
        RG = RG*3600.                                   !(s/m)
        !************************************************************************

        ! K_overall = 1./(RL+RG)                           !(m/s)  EXAMS 2-78
        ! see below k_volatile = AREA*K_overall/v                    !per sec

        !The following condition was placed on the volatilization in order to not
        !perform volatilization on a dry field.  The volatilization routine was written for
        !water bodies, not fields.  Therefore, if volatilization off the field is wanted, then 
        !users should inlude the volatilization rate in the soil degradation input.  May 1, 2009.

        where (daily_depth > minimum_depth*1.001)
         !  k_volatile = AREA*K_overall/v 
            k_volatile = AREA/(RL+RG)/v 
        elsewhere
           k_volatile = 0.
        end where 

        where (temp_avg <= 0) !eliminate volatilization and photolysis when the pond freezes
            k_volatile = 0.
        end where


    end subroutine volatilization
!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

subroutine Leak
    use variables, ONLY: leakage,minimum_depth
    use nonInputVariables, ONLY:  num_records, daily_depth, k_leakage, Lamda, fw1,theta
    implicit none
 
    !Note on Leakage approximation:
    !It is possible that on the day prior to reaching the minimum water level during a leakage/evaporation
    !scenario that there could be less water available for leakage than specified.  
    !This is a trivial note with realistic water leakage rates and the coding
    !effort to address this would not be worthwhile and would be confusing.
    
    !leakage is in m/day
   !NOTE that this formulation of k_leakage is the water column equivalent of degradation, it does
   !represent benthic leakage directly, benthic leakage is calculated through lamda
   
    where (daily_depth > minimum_depth*1.001)
           k_leakage = leakage/daily_depth/86400.
    elsewhere       
           k_leakage = 0.0
    end where 
 
    Lamda = k_leakage*fw1/theta


end subroutine Leak

subroutine degradationSummary(j)
   use nonInputVariables, ONLY: num_records,daily_depth,mavg1_store,k_flow,washout_mass,k_aer_aq,k_anaer_aq, &
        k_hydro, k_volatile, k_photo, k_flow,fw1,fw2, k_leakage, &
        WashoutHalflife,WatercoHalflife,Hydrol1Halflife,PhotolyHalflife,VolatizHalflife,LeakageHalflife, &
        BenthicHalflife,Hydrol2Halflife 
       
   use variables, ONLY: nchem,outputfilename, minimum_depth
   implicit none
   integer, intent(in) :: j
   integer numberWetDays
   
   numberWetDays = count(daily_depth > minimum_depth)  
   WashoutHalflife(j) = 0.69314/(sum(k_flow,daily_depth > minimum_depth)/numberWetDays)/86400. ! does not include dry field runoff
   WatercoHalflife(j) = 0.69314/(sum(k_aer_aq,daily_depth > minimum_depth)/num_records)/86400.
   Hydrol1Halflife(j) = 0.69314/(sum(k_hydro*fw1)/num_records)/86400.
   PhotolyHalflife(j) = 0.69314/(sum(k_photo*fw1)/num_records)/86400.
   VolatizHalflife(j) = 0.69314/(sum(k_volatile*fw1)/num_records)/86400.
   LeakageHalflife(j) = 0.69314/(sum(k_leakage*fw1, daily_depth > minimum_depth)/numberWetDays)/86400.
   BenthicHalflife(j) = 0.69314/(sum(k_anaer_aq)/num_records)/86400.
   Hydrol2Halflife(j) = 0.69314/(sum(k_hydro*fw2)/num_records)/86400.


end subroutine degradationSummary

end module degradation