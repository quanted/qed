module metfileprocessing
!  Written by Dirk F. Young (Virginia, USA).
contains
!******************************************************************
      subroutine count_met(ierror)
            !read met file and count records for array allocation, returns n
            use variables, ONLY: metfilename
            use nonInputVariables, ONLY: num_records
            
            implicit none
            integer, intent(out):: ierror               !open file error 0=success
            integer :: ieof             !signal for no more records '/=0' = no record 
            integer dummy

           open (UNIT=17, FILE=metfilename,STATUS='OLD',ACTION='read',IOSTAT=ierror)
            
            if (ierror ==0) then   !count records if file exists
                num_records=0
                do
                    read (17,*, IOSTAT=IEOF) dummy
                    if (ieof /= 0)exit
                    num_records=num_records+1
              end do
            end if
            close(UNIT=17)

      end subroutine count_met
  !****************************************************************************
  
  !****************************************************************************
      subroutine read_metfile(eof)
          !This subroutine reads the metfile and returns the 
          !average previous 30 day temperature,precip, evap, daily wind speed, and startday
          use utilities_module
          use variables, ONLY: metfilename !name of metfile
          use nonInputVariables, ONLY: num_records, & !number of metfile records, used for array allocation
                                       wind, &      !array of output wind speed (m/s) [read as cm/sec from file and converted]
                                       temp_avg,&   !output: average of previous 30 day temperature
                                       precip, &    !output: daily precipitation (m) 
                                       evap,   &    !output: daily evaporation (m)
                                       startday     !OUTPUT reference day to 1/1/1900
          implicit none
          
          real(8) :: temp30(30)     !array to hold previous 30 days of temperature 
          real(8) :: tempsum            !sum of 30 day temperature values
          real(8) :: temp               !temp as read from met file (C)
          integer :: i,j                !do loop counters
          integer :: DUMMY !yr,mon,day
          integer :: ierror
          integer :: firstyear ,firstmon ,firstday 
          integer :: firstdate
                
          integer,intent(out) ::  eof                   !end of file flag
           
   
          
          eof=0 
          ierror=0
         
          !*******check if met file exists*************************
          open (UNIT=19, FILE=metfilename,STATUS='old',ACTION='read',IOSTAT=ierror)
          if (ierror /=0) then 
            write(11,*) 'no met file'
            return
          end if
          
          !********************!Get the first date from the metfile********************************************
          read(19,*, IOSTAT = eof) firstdate
          firstmon = firstdate/10000
          firstday = (firstdate - firstmon*10000)/100
          firstyear = firstdate - firstday*100 -firstmon*10000 +1900



          rewind (19)  !reset to position to read entire file
          
          do i=1,num_records

            !********** read temp and wind speeds ***********************
            read (19,*, IOSTAT=eof) DUMMY ,precip(i), evap(i),temp,wind(i)  !wind is used directly, temp is processed later

        !   100 format(1X,I2,I2,I2,5F10.0)  !see PRZM manual for definitions in met file p.4-2

            if (eof /=0) then           !met file read error check
                write (11,*) 'met file out of whack'
                return
            end if

            !********  read temperature *******************
            if (i==1) then !initially fill array with temperature of first array
                temp30=temp 
                tempsum=30.*temp
            end if

            tempsum = tempsum +temp-temp30(1)   !calculate new average termperature
            temp_avg(i)=tempsum/30.             !calculate new average termperature

            do j=1, 29                  !update new array
                temp30(j)= temp30(j+1)
            end do
            temp30(30) = temp
            !***********************************************

          end do
          
          !Calculate the 
          
          !reference day to 1/1/1900
          startday = jd (firstyear,firstmon,firstday)
          

          wind=wind/100.        !whole array operation convert to m/s
          evap = evap/100.  !whole array operation convert to m
          precip = precip/100. !whole array operation convert to m
          
          close (UNIT=19)
      end subroutine read_metfile
   
end module metfileprocessing
  