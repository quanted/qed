module utilities_module
!Written by Dirk F. Young (Virginia, USA).
contains

   !*****************************************************************************
   pure elemental integer function jd (YEAR,MONTH,DAY)
     !calculate the days since 1/1/1900 given year,month, day, from Fliegel and van Flandern (1968)
    !Fliegel, H. F. and van Flandern, T. C. (1968). Communications of the ACM, Vol. 11, No. 10 (October, 1968). 

     implicit none
     integer, intent(in) :: year,month,day

      JD= day-32075+1461*(year+4800+(month-14)/12)/4+367*(month-2-(month-14)/12*12) /12-3*((year+4900+(month-14)/12)/100)/4 -2415021

    end function jd
   !*****************************************************************************
 

   !******************************************************************************
 pure subroutine get_date (date1900, YEAR,MONTH,DAY)
 !computes THE GREGORIAN CALENDAR DATE (YEAR,MONTH,DAY) given days since 1900
   implicit none

   integer,intent(out) :: YEAR,MONTH,DAY

   integer,intent(in) :: date1900  !days since 1900
   integer :: L,n,i,j

   L= 2483590 + date1900

   n= 4*L/146097

   L= L-(146097*n+3)/4
   I= 4000*(L+1)/1461001
   L= L-1461*I/4+31
   J= 80*L/2447

   day= L-2447*J/80
   L= J/11
   month = J+2-12*L
   year = 100*(N-49)+I+L

 !   YEAR= I
 !  MONTH= J
 !  DAY= K

   end subroutine get_date
   !******************************************************************************
   
   
   
   subroutine WriteInputsWithDescriptors(unitnumber)
   !This routine prints out the inputs along with a description ofthe terms
   !Time and Date stamped also
    use variables
    implicit none
    integer, intent(in) :: unitnumber
     integer :: i
    integer ::date_time(8)
    call date_and_time(VALUES = date_time)
    write(unitnumber,*) 
    write(unitnumber,*)  '*******************************************'
    write(unitnumber,'("Performed on: ", i2,"/",i2,"/",i4,2x,"at " ,i2,":",i2) ') date_time(2),date_time(3),date_time(1), &
    date_time(5),date_time(6)
    write(unitnumber,*)  '**************** Inputs *******************'
    write(unitnumber,*)
    write(unitnumber,*) aer_aq(1)       , 'Aerobic Aquatic Halflife =   '
    write(unitnumber,*) anae_aq(1)      , 'Anaerobic Aquatic Halflife = '
    write(unitnumber,*) drysoil(1)      , 'Dry Soil Halflife =          '
    
    write(unitnumber,*) photo(1)        , 'Photolysis Halflife =        ' 
    write(unitnumber,*) hydro(1)        , 'Hydrolysis Halflife =        '
    write(unitnumber,*) MWT(1)          , 'Molecular Wieght =           '
    write(unitnumber,*) VAPR(1)         , 'Vapor Pressure =             '
    write(unitnumber,*) SOL(1)          , 'Solubility =                 '
    write(unitnumber,*) koc(1)          , 'Koc =                        '
    write(unitnumber,*) temp_ref_aer(1) , 'Aerobic Reference Temper =   '
    write(unitnumber,*) temp_ref_anae(1), 'Anaerobic Reference Temper = '   
    write(unitnumber,*) temp_ref_dry(1) , 'Dry Soil Reference Temper=  '
    write(unitnumber,*) RFLAT(1)        , 'Reference Latitude =         '

    write(unitnumber,*) heat_henry(1)   , 'Enthalpy of Henry =          '
    write(unitnumber,*) temp_ref_henry(1),'Henry Reference Temperature  '

    write (unitnumber,*)  num_apps          ,'Number of Applications and then day, month, mass'
    write (unitnumber,'(30(I2,1x))')  (applicationDay(i), i=1,num_apps)
    write (unitnumber,'(30(I2,1x))')  (applicationMonth(i), i=1,num_apps)
    write (unitnumber,'(30(F6.3,1X))')  (applicationMass(i), i=1,num_apps)
 
    write(unitnumber,*)  metfilename(1:len_trim(metfilename))      
    write(unitnumber,*)  LAT
    
    write(unitnumber,*) NumberFloodEvents    
    write(unitnumber,*) event0_day  , 'Flood Reference Day Zero =    '
    write(unitnumber,*) event0_month, 'Flood Reference  Month Zero = '

    write(unitnumber,*)  eventDay(1),'Flood Event Days #1 =        '
    write(unitnumber,*)  eventDay(2),'Flood Event Days #2 =        '
    write(unitnumber,*)  eventDay(3),'Flood Event Days #3 =        '
    write(unitnumber,*)  eventDay(4),'Flood Event Days #4 =        '
    write(unitnumber,*)  eventDay(5),'Flood Event Days #5 =        '
    write(unitnumber,*)  eventDay(6),'Flood Event Days #6 =        '
    write(unitnumber,*)  eventDay(7),'Flood Event Days #7 =        '
    write(unitnumber,*)  eventDay(8),'Flood Event Days #8 =        '
    write(unitnumber,*)  eventDay(9),'Flood Event Days #9 =        '
    write(unitnumber,*)  eventDay(10),'Flood Event Days #10 =        '
    write(unitnumber,*)  eventDay(11),'Flood Event Days #11 =        '      

    write(unitnumber,*)eventFill(1),'Flood Event Fill #1 =      '
    write(unitnumber,*)eventFill(2),'Flood Event Fill #2 =      '
    write(unitnumber,*)eventFill(3),'Flood Event Fill #3 =      '
    write(unitnumber,*)eventFill(4),'Flood Event Fill #4 =      '
    write(unitnumber,*)eventFill(5),'Flood Event Fill #5 =      '
    write(unitnumber,*)eventFill(6),'Flood Event Fill #6 =      '
    write(unitnumber,*)eventFill(7),'Flood Event Fill #7 =      '
    write(unitnumber,*)eventFill(8),'Flood Event Fill #8 =      '
    write(unitnumber,*)eventFill(9),'Flood Event Fill #9 =      '
    write(unitnumber,*)eventFill(10),'Flood Event Fill #10 =      '
    write(unitnumber,*)eventFill(11),'Flood Event Fill #11 =      '

    write(unitnumber,*) eventWeir(1),'Flood Event Weir Ht #1 =      '
    write(unitnumber,*) eventWeir(2),'Flood Event Weir Ht #2 =      '
    write(unitnumber,*) eventWeir(3),'Flood Event Weir Ht #3 =      '
    write(unitnumber,*) eventWeir(4),'Flood Event Weir Ht #4 =      '
    write(unitnumber,*) eventWeir(5),'Flood Event Weir Ht #5 =      '
    write(unitnumber,*) eventWeir(6),'Flood Event Weir Ht #6 =      '
    write(unitnumber,*) eventWeir(7),'Flood Event Weir Ht #7 =      '
    write(unitnumber,*) eventWeir(8),'Flood Event Weir Ht #8 =      '
    write(unitnumber,*) eventWeir(9),'Flood Event Weir Ht #9 =      '
    write(unitnumber,*) eventWeir(10),'Flood Event Weir Ht #10 =      '
    write(unitnumber,*) eventWeir(11),'Flood Event Weir Ht #11 =      '   
      
    write(unitnumber,*) eventMinimum(1),'Flood Event Minimum #1 =    '
    write(unitnumber,*) eventMinimum(2),'Flood Event Minimum #2 =    '
    write(unitnumber,*) eventMinimum(3),'Flood Event Minimum #3 =    '
    write(unitnumber,*) eventMinimum(4),'Flood Event Minimum #4 =    '
    write(unitnumber,*) eventMinimum(5),'Flood Event Minimum #5 =    '
    write(unitnumber,*) eventMinimum(6),'Flood Event Minimum #6 =    '
    write(unitnumber,*) eventMinimum(7),'Flood Event Minimum #7 =    '
    write(unitnumber,*) eventMinimum(8),'Flood Event Minimum #8 =    '
    write(unitnumber,*) eventMinimum(9),'Flood Event Minimum #9 =    '
    write(unitnumber,*) eventMinimum(10),'Flood Event Minimum #10 =    '
    write(unitnumber,*) eventMinimum(11),'Flood Event Minimum #11 =    '

    write(unitnumber,*)eventWashout(1),'Flood Event Washout #1 =      '
    write(unitnumber,*)eventWashout(2),'Flood Event Washout #2 =      '
    write(unitnumber,*)eventWashout(3),'Flood Event Washout #3 =      '
    write(unitnumber,*)eventWashout(4),'Flood Event Washout #4 =      '
    write(unitnumber,*)eventWashout(5),'Flood Event Washout #5 =      '
    write(unitnumber,*)eventWashout(6),'Flood Event Washout #6 =      '
    write(unitnumber,*)eventWashout(7),'Flood Event Washout #7 =      '
    write(unitnumber,*)eventWashout(8),'Flood Event Washout #8 =      '
    write(unitnumber,*)eventWashout(9),'Flood Event Washout #9 =      '
    write(unitnumber,*)eventWashout(10),'Flood Event Washout #10 =      '
    write(unitnumber,*)eventWashout(11),'Flood Event Washout #11 =      '

    write(unitnumber,*)PlantZero_day,  'Reference Plant Day =         ' 
    write(unitnumber,*)PlantZero_month,'Reference Plant Month =       ' 
    write(unitnumber,*)PlantFull    ,  'Days to Full Ht. =            ' 
    write(unitnumber,*)PlantRemove  ,  'Days to Plant Removal =   ' 
    write(unitnumber,*)CanopyMax    ,  'Maximum Canopy Coverage =    ' 

!****Physical Inputs ***************

    write(unitnumber,*) D_over_dx         ,   'Mass Transfer Coefficient =  '
    write(unitnumber,*) depth_0           ,   'Reference Depth =            '
    write(unitnumber,*) benthic_depth     ,   'Benthic Depth =              '
    write(unitnumber,*) porosity          ,   'Porosity =                   '
    write(unitnumber,*) bulk_density      ,   'Bulk Density =               '
    write(unitnumber,*) FROC1             ,   'FOC 1  =                     '
    write(unitnumber,*) FROC2             ,   'FOC 2 =                      '

    write(unitnumber,*)  SUSED            ,   'SS =                         '
    write(unitnumber,*)  CHL              ,   'Chlorophyll =                '
    write(unitnumber,*)  DOC1             ,   'DOC1 =                       '
    write(unitnumber,*)  DOC2             ,   'DOC2 =                       '
    write(unitnumber,*)  PLMAS            ,   'Water Column Biomass =       '
    write(unitnumber,*)  BNMAS            ,   'Benthic Biomass =            '
    write(unitnumber,*)  QT               ,   'Q10 =                        '
    write(unitnumber,*)  DFAC             ,   'DFAC =                       '
    write(unitnumber,*)  AREA             ,   'Area =                       '
    write(unitnumber,*)  leakage          ,   'Leakage (m/d)  =             '
    
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    write(unitnumber,*) outputfilename (1:len_trim(outputfilename)) 
    write(unitnumber,*) nchem, 'number of chemicals (parent = 1)'
    
   write(unitnumber,*) aer_aq(2) , 'Degradate #1 Chemical Info'
   write(unitnumber,*) anae_aq(2)
   write(unitnumber,*) drysoil(2)   
   write(unitnumber,*) photo(2)         
   write(unitnumber,*) hydro(2)         
   write(unitnumber,*) MWT(2)           
   write(unitnumber,*) VAPR(2)          
   write(unitnumber,*) SOL(2)           
   write(unitnumber,*) koc(2)           
   write(unitnumber,*) temp_ref_aer(2)  
   write(unitnumber,*) temp_ref_anae(2) 
   write(unitnumber,*) temp_ref_dry(2)
   write(unitnumber,*) RFLAT(2)  
   write(unitnumber,*) heat_henry(2)
   write(unitnumber,*) temp_ref_henry(2)   

   write(unitnumber,*) xAerobic(1), 'Aerobic Molar transformation Fraction, Deg #1'  ! transforms are associated with the parent, because calcs are performed at parent time
   write(unitnumber,*) xBenthic(1), 'Benthic Molar transformation Fraction, Deg #1'  ! hence, "i-1" is used here
   write(unitnumber,*) xUnflood(1), 'Dry Soil Molar transformation Fraction, Deg #1'
   write(unitnumber,*) xPhoto(1),   'Photo Molar transformation Fraction, Deg #1'
   write(unitnumber,*) xHydro(1),   'Hydroly Molar transformation Fraction, Deg #1'

   write(unitnumber,*) aer_aq(3) , 'Degradate #2 Chemical Info'
   write(unitnumber,*) anae_aq(3)
   write(unitnumber,*) drysoil(3)   
   write(unitnumber,*) photo(3)         
   write(unitnumber,*) hydro(3)         
   write(unitnumber,*) MWT(3)           
   write(unitnumber,*) VAPR(3)          
   write(unitnumber,*) SOL(3)           
   write(unitnumber,*) koc(3)           
   write(unitnumber,*) temp_ref_aer(3)  
   write(unitnumber,*) temp_ref_anae(3) 
   write(unitnumber,*) temp_ref_dry(3)
   write(unitnumber,*) RFLAT(3)  
   write(unitnumber,*) heat_henry(3)
   write(unitnumber,*) temp_ref_henry(3)   

   write(unitnumber,*) xAerobic(2),  'Aerobic Molar transformation Fraction, Deg #2' ! transforms are associated with the parent, because calcs are performed at parent time
   write(unitnumber,*) xBenthic(2),  'Benthic Molar transformation Fraction, Deg #2' ! hence, "i-1" is used here
   write(unitnumber,*) xUnflood(2),  'Dry Soil Molar transformation Fraction, Deg #2'
   write(unitnumber,*) xPhoto(2),    'Photo Molar transformation Fraction, Deg #2'
   write(unitnumber,*) xHydro(2),    'Hydroly Molar transformation Fraction, Deg #2'
 

    write(unitnumber,*)  '************** End of Run *****************'
    

   end subroutine   WriteInputsWithDescriptors
   
   
   
   
   

end module utilities_module