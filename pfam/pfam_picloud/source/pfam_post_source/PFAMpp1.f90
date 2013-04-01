!  PFAMpp1.f90 
!  Written by Dirk F. Young (Virginia, USA).
!  Console Application
!
!****************************************************************************
!  Program: PFAMpp1.f90
!  
!  This is a post processor for PFAM.
!  Data is taken from the text file output from the main model
!  and processed here. The intent is that when this is compiled
!  program can be easily change out according to user needs as it
!  is completely independent from the main program.
!
!****************************************************************************

program PFAMpp1
use utilities_pp1
implicit none


! VARIABLES TO BE READ IN FROM FILE:
integer :: startday
integer :: num_records
real(8) benthic_depth, area
real(8):: minimum_depth 
integer :: nchem

real(8),allocatable,dimension(:):: daily_depth
real(8),allocatable,dimension(:):: depth_release     !vector of water releases (m)
real(8),allocatable,dimension(:):: makeupwater
real(8),allocatable,dimension(:):: overflow

real(8),allocatable,dimension(:):: m1_store
real(8),allocatable,dimension(:):: m2_store

real(8),allocatable,dimension(:,:):: mavg1_store
real(8),allocatable,dimension(:,:):: mavg2_store
real(8),allocatable,dimension(:,:):: release_mass
real(8),allocatable,dimension(:,:):: washout_mass 
real(8),allocatable,dimension(:,:):: conc1
real(8),allocatable,dimension(:,:):: conc2

!LOCAL VARIABLES
integer :: outfilelength

integer :: i, j,n

integer :: year, month, day
real(8) :: volume1, volume2

!variables for processing command line argumants
integer:: length, status,ierror
character(len=256):: PPfilename
character(len=256) :: outputfilename    !file name with data to be read
character(len= 30):: dummy
character(len=256) :: processed_outputfile

real(8),allocatable,dimension(:,:)::  released_conc





!****************Get output file information from command line ******************
call get_command_argument(1,outputfilename,length)! outputfilename, the full path and name of file to be read (intermediate output from PFAM)


!This is the full path and file name for the post processed file
!PPfilename = trim(outputfilename)//".pp1"  
processed_outputfile  = outputfilename(1:len_trim(outputfilename)-4) // "_ProcessedOutput.txt"



open (UNIT = 32, FILE =processed_outputfile, STATUS = 'unknown', IOSTAT = ierror)
if (ierror /= 0) then
    write(11,*) "There is a problem creating the post proccessed output file."
end if

!************************************************************************************

!*************************************************************************************
!Get Data from Intermediate Output File (the one produded by the main model)
open (UNIT = 31, FILE =outputfilename, STATUS = 'OLD', ACTION = 'READ', IOSTAT = ierror) 

if (ierror /= 0) then
    write(11,*) "No intermediate output file"
    stop
end if


do i=1,19   ! skip lines to get to data
    read (31,*)
end do

read (31,*) startday
read (31,*) num_records  
read (31,*) area
read (31,*) benthic_depth
read (31,*) minimum_depth
read (31,*) nchem
read (31,*)  !watershed area
read (31,*)  !watershed curve number
read (31,*)  !width
read (31,*)  !depth
read (31,*)  !length
read (31,*)  !base flow




!skip 2 more lines
read (31,*)
read (31,*)

allocate(daily_depth(num_records), STAT= status)
allocate(depth_release(num_records), STAT= status) 
allocate(makeupwater(num_records), STAT= status)
allocate(overflow(num_records), STAT= status)

allocate(m1_store(num_records), STAT= status)
allocate(m2_store(num_records), STAT= status)

allocate(mavg1_store(num_records,nchem), STAT= status)
allocate(mavg2_store(num_records,nchem), STAT= status)

allocate(release_mass(num_records,nchem), STAT= status)
allocate(washout_mass(num_records,nchem), STAT= status)

allocate(conc1(num_records,nchem), STAT= status)
allocate(conc2(num_records,nchem), STAT= status)

allocate(released_conc(num_records,nchem), STAT= status)

do i=1,num_records
          !      1              2                3           4             5            6             7                   8             9                 10                        11             12       
 read (31,*) daily_depth(i),depth_release(i),makeupwater(i),overflow(i), m1_store(i),m2_store(i), &
             (mavg1_store(i,n),mavg2_store(i,n), release_mass(i,n),washout_mass(i,n), conc1(i,n), conc2(i,n), n=1,nchem)
end do

!********************************************************************************************
!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   
!XXXXXXXX                         PROCESS OUTPUT                                   XXXXXXXXXX
!XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   

    call get_date (STARTDAY, YEAR,MONTH,DAY)    
    WRITE(32,*) 'Contents:'   
    WRITE(32,*) 'Part 1: Record of Water and Mass Releases'
    WRITE(32,*) 'Part 2: Record of Water and Soil/Benthic Concentration'
    WRITE(32,*)
    WRITE(32,*) '*******************************************************************************'
    WRITE(32,*) 'Part 1: Record of Water and Mass Releases'
    WRITE(32,*) '*******************************************************************************'
    WRITE(32,*) 'Records for all events in which pesticide mass was released whether from'
    WRITE(32,*) 'manual releases or from spill over from precipitation.'
    WRITE(32,*) '*******************************************************************************'
    
  !  WRITE(32,'(a11, 21x,3i12))') 'chemical id',  (n, n=1,nchem)
    WRITE(32,2500) 'Event#','Date','Release', 'Released' ,   ('Released    ', n=1,nchem)
    WRITE(32,3000) 'Type          Volume(m3)', ('Conc',n,'(ug/L) ', n=1,nchem)
    
    2500    Format(a6,2x,a4,10x,a7,4x ,4(4x,a8) )
    3000    Format(23x,a24,2x,  3(a4,i1,a7) )
    
    j=0  
    do i=1,num_records
        if (depth_release(i)> 0.) then
           call get_date (startday+i-1, YEAR,MONTH,DAY)
                j=j+1
                released_conc(j,:) = release_mass(i,:)/ (depth_release(i)*area) *1000000.
     
             WRITE(32,5000)  j, month,day,year, " manual release ",   depth_release(i)*area,  (released_conc(j,n),  n=1,nchem) !  ,
        end if
        if (overflow(i)> 0.) then
             call get_date (startday+i, YEAR,MONTH,DAY)
             j=j+1          
             released_conc(j,:) = washout_mass(i,:)/(overflow(i)*area)*1000000.
      
             if (daily_depth(i)<=minimum_depth)then
                  WRITE(32,5000)  j, month,day,year,"dry field runoff", overflow(i)*area , (released_conc(j,n),  n=1,nchem)  !
             else
                  WRITE(32,5000)  j, month,day,year,"     overflow   " ,overflow(i)*area, (released_conc(j,n),  n=1,nchem)  ! 
             end if     
        end if   
    end do

    5000    Format(I5, 1x,I2,'/'I2,'/'I4,1x,a16,3x, E10.3,10(2x,E10.3) )

    WRITE(32,*)
    write(32,'("Maximum released concentration = ",  5E10.3, " ppb")')   (maxval(released_conc(:,n)),  n=1,nchem)
    write(32,'("Index for max released concen. = ",  5I10)')   (maxloc(released_conc(:,n)),  n=1,nchem)
    WRITE(32,*)


    !***************************************************************************************************************
    !***********    Write daily concentrations of water body *********************************
    WRITE(32,*) '*******************************************************************************'
    WRITE(32,*) 'Part 2: Record of Water and Soil/Benthic Concentrations' 
    WRITE(32,*)   
    WRITE(32,*) 'Irrig is the amount of water added to maintain weir requirements.'

    WRITE(32,*) 

    WRITE(32,'(A75,3a48)') '****************************  DAILY RECORD  **********************************', &
                          ('************************************************', n=1,nchem-1)
    WRITE(32,'(A26,2x,4a48)')  '                    Irrig.' ,('Water       Benthic     Benthic  Benthic Areal ', n=1,nchem   )
    WRITE(32,'(A26,2x,4a48))') 'Date      Depth(m)  H2O(m)', ('Total(ug/L) Total(ug/L) Pore(ug/L) M2/A(kg/m2)  ', n=1,nchem   )
    WRITE(32,'(a11, 9x,20i12))') 'chemical id',  (n,n,n,n, n=1,nchem)
    WRITE(32,'(A75,3a48)') '******************************************************************************', &
                          ('************************************************', n=1,nchem-1)
    Volume2 = benthic_depth*area

    do i= 1, num_records
       call get_date (startday+i-1, YEAR,MONTH,DAY)    
       volume1 = daily_depth(i)*area
       if (daily_depth(i)<=minimum_depth) then  
          WRITE(32,7000) MONTH, Day, YEAR, daily_depth(i), makeupwater(i), &
          ("---------", mavg2_store(i,n)/Volume2*1000000., conc2(i,n), mavg2_store(i,n)/area, n=1,nchem)
       else
          WRITE(32,6000) MONTH,Day, YEAR, daily_depth(i),makeupwater(i), &
          (mavg1_store(i,n)/volume1*1000000., mavg2_store(i,n)/Volume2*1000000., conc2(i,n), mavg2_store(i,n)/area, n=1,nchem)
       end if
    end do
    
    WRITE(32,*) '*******************************************************************************'
!    WRITE(32,*) 'Part 3: Record of Water and Soil/Benthic Concentrations'
!    WRITE(32,'(A93)') '****************************  DAILY RECORD   ***********************************************'
!    WRITE(32,'(A51)') '  Date       C1avg(ug/L)  C2avg(ug/L)  M2/A(kg/m2)'
!    WRITE(32,'(A93)') '********************************************************************************************'
!    
!    
!    
!    
!        do i= 1, num_records
!           call get_date (startday+i-1, YEAR,MONTH,DAY)         
!           WRITE(32,8000) MONTH,Day, YEAR, conc1(i)*1000000.,  conc2(i)*1000000.,  mavg2_store(i)/area           
!       end do
!    
!    
!!!Write(34,*) '****************** Water Level for Graphing *************************'
!!!
!!!do i = 1, num_records
!!!   call get_date (startday+i-1, YEAR,MONTH,DAY) 
!!!   
!!!   if (depthforgraphing(i) >0.) then 
!!!      WRITE(32,6000) MONTH,Day, YEAR,depthforgraphing(i)
!!!   endif    
!!!   
!!!   WRITE(32,6000) MONTH,Day, YEAR, daily_depth(i)
!!
!!end do

   

    6000    Format(I2,'/'I2,'/'I4,1x, F7.4,1x, F7.4,  20(1x,E11.3))   
    7000    Format(I2,'/'I2,'/'I4,1x, F7.4,1x, F7.4,  20(A12,1x,E11.3,1x,E11.3,1x,E11.3)) 
    8000    Format(I2,'/'I2,'/'I4,1x, E12.3,1x, E12.3,1x, E12.3)
   
    !*****************************************************
close(31)
close(32)


end program PFAMpp1