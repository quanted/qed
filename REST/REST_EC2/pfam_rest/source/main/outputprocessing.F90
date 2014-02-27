module outputprocessing
!Written by Dirk F. Young (Virginia, USA).
!Contains Post Processing an writing of output to text file

contains   

    subroutine process_output
        use variables, ONLY: outputfilename, area, benthic_depth, minimum_depth,nchem, &
        watershed_area,watershed_cn,baseflow, widthMixingCell,depthMixingCell, lengthMixingCell 
                
        use nonInputVariables, ONLY: num_records,daily_depth,depth_release,makeupwater,overflow,k_flow, &
        mavg1_store,mavg2_store,m1_store, m2_store,release_mass,washout_mass,startday,k_leakage,aqconc_avg1, aqconc_avg2, &
        WashoutHalflife,WatercoHalflife,Hydrol1Halflife,PhotolyHalflife,VolatizHalflife,LeakageHalflife,BenthicHalflife, &
        Hydrol2Halflife 
        
        use utilities_module
        implicit none
        integer :: ierror, i, j   
        character(len=256) ::  halflife_outputfile 
        
        
        forall(i=1:nchem)  washout_mass(:,i) = mavg1_store(:,i)  *(k_flow(:)*86400.) !washout mass 

        open (UNIT = 34, FILE =outputfilename, STATUS = 'unknown',RECL = 500, IOSTAT = ierror) 


        write(34,*) "col 1:  depth after precip, evaporation and weir control (m)"   ![daily_depth]
        write(34,*) "col 2:  Intentionally released water  (m)"                      ![depth_release]       
        write(34,*) "col 3:  water manually added to satisfy depth requirements (m)" ![makeupwater]    
        write(34,*) "col 4:  Overflow (m)"                                           ![overflow]     
        write(34,*) "col 5:  Parent mass in water (predegradation) (kg)"             ![m1_store]
        write(34,*) "col 6:  Parent mass in benthic (predegradation)(kg)"            ![m2_store]      
        
        write(34,*) "col 7:  Parent average mass in water column for day (kg)"       ![mavg1_store(:,1)] 
        write(34,*) "col 8:  Parent average mass in benthic region for day (kg)"     ![mavg2_store(:,1)]
        write(34,*) "col 9:  Parent mass intentionally released (kg)"                ![release_mass(:,1)]
        write(34,*) "col 10: Parent mass lost to overflow (kg)"                       ![washout_mass(:,1)] 
        write(34,*) "col 11: Parent aq-phase water column concentration (kg/m3)"     ![aqconc_avg1(:,1)]
        write(34,*) "col 12: Parent benthic pore water concentration (kg/m3)"        ![aqconc_avg2(:,1)]
        
        write(34,*) "col 13, 19: Degradate #1 and #2 respectively, avg mass water column (kg)"      ![mavg1_store(:,2)]
        write(34,*) "col 14, 20: Degradate #1 and #2 respectively, avg mass benthic (kg)"           ![mavg2_store(:,2)]
        write(34,*) "col 15, 21: Degradate #1 and #2 respectively, mass released (kg)"                           ![release_mass(:,2)]    
        write(34,*) "col 16, 22: Degradate #1 and #2 respectively, mass lost to overflow (kg)"                       ![washout_mass(:,2)]                                                                                       
        write(34,*) "col 17, 23: Degradate #1 and #2 respectively, Aq-phase water column concentration (kg/m3)"  ![aqconc_avg1(:,2)]
        write(34,*) "col 18, 24: Degradate #1 and #2 respectively, benthic pore water concentration (kg/m3)"     ![aqconc_avg2(:,2)]

        write(34,*) "**************Additional Simulation Info**********************"
        write (34,*) STARTDAY   , "= Start day relative to 1900"
        write (34,*) num_records, "= Number of Records"
        write (34,*) area , "= Area (m2)"
        write (34,*) benthic_depth, "= Benthic depth (m)"
        write (34,'(E12.4,a60)') minimum_depth, "= Depth model uses to approximate zero depth in water (m)"
        write (34,*) nchem, "= Number of chemicals (parent plus degradates) in output"
        write (34,*) watershed_area, "= area of surrounding watershed (for use w/ additional VVWM post processor"
        write (34,*) watershed_cn, "= curve number of surrounding watershed (for use w/ additional VVWM post processor"
        
        
        write (34,*) widthMixingCell, "= Width of Mixing Cell Receiving Water Body (m)"
        write (34,*) depthMixingCell, "= Depth of Mixing Cell Receiving Water Body (m)"
        write (34,*) lengthMixingCell, "= Length off Receiving Water Body (m)"
        write (34,*) baseflow, "= Base Flow into Receiving Water Body (m3/day)"  
                
                
        write(34,*) "*************************************************************"
 
        write(34, '(5x,30(a3,1x,i2,6x))')("col",j,j=1,6)  ,("col",j,j=7,6+nchem*6)
     
        
        do i=1, num_records
            write (34,7000) daily_depth(i),depth_release(i), makeupwater(i),overflow(i), m1_store(i,1), m2_store(i,1),&
            (mavg1_store(i,j),mavg2_store(i,j),release_mass(i,j),washout_mass(i,j),aqconc_avg1(i,j),aqconc_avg2(i,j),j=1,nchem)
        end do

        write(34,*) "END OF DATA"
        call WriteInputsWithDescriptors(34)

       7000    Format(40(E11.4, 1x))


    !*************************************************************************************
    !The following prints some useful degradation information to a *Effective_HalfLife.txt file 
    !Gives a summary of effective degradation rates so that emphasis on input 
    ! refinements can be placed where they would be most effective.
    !**************************************************************************************
    halflife_outputfile  = outputfilename(1:len_trim(outputfilename)-4) // "_Effective_HalfLives.txt"
    

        open (UNIT = 35, FILE =halflife_outputfile, STATUS = 'unknown', IOSTAT = ierror) 
        write (35,*) "Effective compartment halflives averaged over simulation duration:"
        write (35,*)

        do i=1, nchem
           write(35,*) "----Chemical ", i
           write(35,*) "Washout halflife            = ",WashoutHalflife(i)
           write(35,*) "Aerobic halflife            = ",WatercoHalflife(i)
           write(35,*) "Hydrolysis halflife         = ",Hydrol1Halflife(i)
           write(35,*) "Photolysis halflife         = ",PhotolyHalflife(i)
           write(35,*) "Volatilization halflife     = ",VolatizHalflife(i)
           write(35,*) "Leakage halflife(water col) = ",LeakageHalflife(i)
           write(35,*) "Benthic Metabolism halflife = ",BenthicHalflife(i)
           write(35,*) "Benthic Hydrolysis halflife = ",Hydrol2Halflife(i)
        end do

        close(35)
        close(34)
     !********************************************************************************************     
     
    end subroutine process_output


end module outputprocessing
