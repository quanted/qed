module chemicaltransformation
!Written by Dirk F. Young (Virginia, USA)
contains

    subroutine transformation(j)
               
    use nonInputVariables, ONLY: num_records, mavg1_store, mavg2_store,fractional_removal,m1_input,m2_input,  &
              release_mass,m1_store,m2_store, A,B,E,F,fw1,fw2,daily_depth, aqconc1,aqconc2, aqconc_avg1 ,aqconc_avg2, &
              degradateProduced1,degradateProduced2
                  
    use variables, ONLY: time_int, benthic_depth,Area,porosity ,nchem    
    use degradation
    use solute_capacity
    use coreCalculations
    use mass_inputs    
          
    implicit none
    integer, intent(in) :: j  !j=1 means parent, subsequent values are degradates
 
   !***** Local Parameters *****************************  
    real(8) :: m1,m2            !daily peak
    real(8) :: mn1, mn2         !mass at end of time step
    real(8) :: new_aqconc1
    real(8) :: new_aqconc2
    integer :: day_count        !number of days total, used to refernce met file data (e.g., day #1= 1)

    !***************************************************************
    call solute_holding_capacity(j)
    call hydrolysis (j)
    call photolysis(j)
    call metabolism(j)
    call volatilization(j)
    call leak
    call gamma_one
    call gamma_two

    !******* Add the Pesticide at start of days ******
    if (j==1) then                 !j=1 is the parent.  The following call is for the manual pesticide applications.    
       call ParentMass2
    else                           !degradate mass input is  calculated already when the parent degradation was calculated (further down)
      m1_input = degradateProduced1   
      m2_input = degradateProduced2
    end if
    !************************************************ 
    

    call reducer2
    !***** Daily Loop Calculations ************************
    m1  =0.
    m2  =0.
    mn1 =0.
    mn2 =0.
    aqconc1 = 0.
    aqconc2 = 0.     
   
    do day_count = 1,num_records

       m1 = mn1 + m1_input(day_count)  !daily peak mass 
       m2 = mn2 + m2_input(day_count)
                   
       !removed mass due to release of water
       release_mass(day_count,j) = fractional_removal(day_count)*m1   
     
       m1 = m1-release_mass(day_count,j)
       m1_store(day_count,j)=  m1
       m2_store(day_count,j)=  m2
        
       !convert masses to concentrations prio to sending in to solver
       !July 4 2010, created wrapper to deal with concentrations instead of masses
       aqconc1(day_count) = m1*fw1(day_count)/daily_depth(day_count)/Area
       aqconc2(day_count) = m2*fw2/(benthic_depth*Area*porosity )
        
       call simuldiff2 (A(day_count),B(day_count),E(day_count),F(day_count),aqconc1(day_count),aqconc2(day_count), &
       Time_int,new_aqconc1,new_aqconc2,aqconc_avg1(day_count,j), aqconc_avg2(day_count,j))
        
       !unconvert to masses
       mn1 = new_aqconc1/fw1(day_count)*daily_depth(day_count)*Area
       mn2 = new_aqconc2/fw2*benthic_depth*Area*porosity 
        
       mavg1_store(day_count,j) = aqconc_avg1(day_count,j)/fw1(day_count)*daily_depth(day_count)*Area
       mavg2_store(day_count,j) = aqconc_avg2(day_count,j)/fw2*benthic_depth*Area*porosity            
    end do 

    if (nchem > j) then
        call DegradateProduction(j)  !Calculate the vector of daily degradate production
    end if


     call degradationSummary(j)


    end subroutine transformation

end module chemicaltransformation