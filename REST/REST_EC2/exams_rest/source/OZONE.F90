Subroutine Ozone(Lat,Lon,OzoneData,Print,PrintLUN,DAFUnit,Zonals)
! This subroutine accepts as input the latitude and longitude of any location,
! finds its position within a 1 degree latitude by 1.25 longitude grid of the
! surface of the Earth, and returns total column ozone in the 13-element array
! OzoneData, consisting of 12 monthly values and the annual mean.
! Input latitude and longitude are decimal values, with South to North
! ranging from -90.0 (South Pole) to +90.0 (North Pole). Longitudes
! range from the International Date Line (-180.0) eastward through the
! prime meridian (0.0) to the International Date Line (+180.0).
! South latitude is negative, North latitude is positive.
! West longitude is negative, East longitude is positive.

! OzoneData are returned as cm Ozone at NTP (Normal Temperature and Pressure).
! The logical "Print" requests a table of the data for the input Lat/Lon.
! The table is emitted to Logical Unit Number "PrintLUN".
! The data are read on Logical Unit Number "DAFUnit". 
! By setting "Zonals" .true., zonal means from the locations' 5-degree
! zonal average will be returned
! The calling routine must have opened the data file using LUN DAFUnit.
! The file is called "Ozone.daf" for Exams/Piranha. Example open statement:
! open (DafUnit,access='direct',recl=1152,file='d:\dir\ozone.daf',&
!    status='old',action='read',form='unformatted')
! To illustrate:
      ! Program Get_Ozone_Data
      ! real :: OzoneG(13)
      ! open (13,access='direct',recl=1152,file='d:\ozone\ozone.daf',&
      !       status='old',action='read',form='unformatted')
      ! call Ozone(33.94,-83.32,OzoneG,.true.,6,13,.false.)
      ! write(*,*)' Ozone for Athens, GA'
      ! close (13)
      ! end Program Get_Ozone_Data

! The dataset was derived from a 2 CD-ROM set containing the latest version
! (version 7) of ozone data from the TOMS (Total Ozone Mapping Spectrometer)
! instrument flown onboard the Nimbus 7 spacecraft. Data covering the entire
! Nimbus 7 TOMS lifetime (November 1, 1978 through May 6, 1993) are given
! as monthly averages.
! ****************************************************************************
! CD-ROM Title: "TOMS Version7-May 22, 1996 -- Gridded O3 Data: 1978-1993"
! (Text adapted from TOMS "readme.1st" file.)
! Overview of the source CD-ROMs: The first CD-ROM, designated OPT_004A,
! contains monthly gridded data for the period November 1978 through 1987.
! The second CD-ROM, designated OPT_004B, contains similar data for 1988
! through May 1993, along with monthly zonal means. The data are described
! in more detail in the "Data Files" section.
! 
! The Ozone Measurement
! ---------------------
! The Nimbus 7 spacecraft was in a south-to-north, sun-synchronous
! polar orbit so that it was always close to local noon/midnight below
! the spacecraft. Thus, ozone measurements were taken for the entire
! world every 24 hours. TOMS directly measured the ultraviolet
! sunlight scattered by the Earth's atmosphere. Total column ozone was
! inferred from the differential absorption of scattered sunlight in the
! ultraviolet range. Ozone was calculated by taking the ratio of two
! wavelengths (312 nm and 331 nm, for example), where one
! wavelength is strongly absorbed by ozone while the other is absorbed
! only weakly. The instrument had a 50 kilometer square field of view
! at the sub-satellite point. TOMS collected 35 measurements every 8
! seconds as it scanned right to left, producing approximately 200,000
! ozone measurements daily. These individual measurements varied
! typically between 100 and 650 Dobson Units (DU) and averaged about
! 300 DU. This is equivalent to an 0.3 cm (about a 10th of an inch) thick
! layer of pure ozone gas at NTP (Normal Temperature and Pressure).
! 
! The Data Files
! --------------
! Gridded Monthly Average: For each month, the individual TOMS measurements
! were averaged into grid cells covering 1 degree of latitude by 1.25
! degrees of longitude. The 180x288 ASCII data array contains data from 90S
! to 90N, from 180W to 180E. Each ozone value is a 3 digit integer (see
! sample). For each grid cell, at least 20 days of data in any given month
! and year were required to be good for the monthly average to have been
! computed. Both CDs example: \y79\gm7903.n7t. For Piranha, these files were
! averaged to provide grand mean monthly values for the period of record.
! 
! Sample Data (from \y82\gm8201.n7t)
!-------------
!Month:   January 1982 Production V70 NIMBUS-7/TOMS OZONE                     
!Longitudes:  288 bins centered on 179.375 W to 179.375 E  (1.25 degree steps)
!Latitudes :  180 bins centered on  89.5   S to  89.5   N  (1.00 degree steps)
!307307307307308308308308307307307307306306306306306306306306306306306306306
!306306306306306306306306306306306306306306306306306306306306306306306307307
!307307307307307307306306306306307307307307306306306306307307307307306306306
!306306306306306306306306306306306306306306306306306305305305305305305305305
!307307307307306306306306306306306306306306306306306306306306306306306306306
!306306306306306306306307307307307307307307307307307307307307307307307308308
!308308308308308308308308308308307307307307308308308308308308308308308308308
!308308308308308308308308308308308308308308308308308308308308308308308308308
!308308308308309309309309309309309309308308308308307307307307308308308308309
!309309309309309309309309309309309309309309309308308308308309309309309309309
!309309309309309309309309309309308308308308309309309309309309309309309309309
!309309309309309308308308308308308308308   lat =  -89.5  
!----------------------------------------------------------------------------- 
!
! Zonal Means
! -----------
! Monthly zonal means in the file \zonalavg\zonalmon.n7t on the 2nd CD.
! The averages are for 5 degree latitude zones, area weighted. At least
! 75% of possible data in a given zone was required to be present for the
! mean to be calculated. In 1978 and 1979 there were missing days when
! the TOMS instrument was turned off to conserve power. In the later years
! there are at least some data every day. The units of measurement for the
! zonal means are Dobson Units.
! 
! Problems with the data
! ----------------------
! Polar Night: TOMS measured ozone using scattered sunlight; it is not
! possible to measure ozone when there is no sun (in the polar regions
! in winter). Consequently, for example, the Antarctic polar regions for
! August and September always have areas of missing data due to polar night.
! These gaps were filled by the expedient of averaging the monthly zonal
! means across all available years, interpolating from polar dusk to polar
! dawn during periods of continuous darkness, and then substituting these
! values for zeros remaining in the Piranha monthly gridded dataset after
! incorporating all available monthly gridded data.
! 
! Missing Data: During 1978/1979 the TOMS instrument was turned
! off periodically to conserve power, including a 5 day period
! (6/14-6/18) in June 1979. On many days, data were lost due to
! missing orbits or other problems. The sample size among grid cells
! is thus not identical. The variance (2 S.E.) in the ozone data
! over the 14-year lifetime of the instrument is, however, only 1.5%.
! 
! High Terrain: The ozone reported is total column ozone to the ground. Over
! high mountains (the Himalayas, the Andes) low ozone will be noticed relative
! to surrounding low terrain. This is not an error.
! ****************************************************************************

real, intent(inout) :: Lat,Lon
! Inout because bogus values (|lat| > 90, |lon| > 180) are altered to the
! poles or to the International Date Line
real, intent(out) :: OzoneData(13)
integer, intent(in) :: PrintLUN, DAFUnit
! PrintLUN - Logical Unit Number for reporting outcome
! DAFUnit  - Logical Unit Number for opening the datafile
logical, intent(in) :: Print, Zonals
! Print to request immediate reporting of the data
! Zonals to request zonal mean data rather than a database fetch
! Internal data stuctures
real :: LatLine(288)
integer :: LatBin, LonBin, recnum, Month
character (len=1) :: NS ! to identify Northern/Southern hemisphere in output
character (len=1) :: EW ! to identify Eastern/Western hemisphere in output
character (len=28) :: JJ = 'Jan  Feb  Mar  Apr  May  Jun'
character (len=28) :: JD = 'Jul  Aug  Sep  Oct  Nov  Dec'
! Zonal means from Nimbus 7 v.7 TOMS data (processed by zonebar.f90)
real, dimension (36,12) :: ZonalData = reshape ( (/ &
300.8,304.2,306.5,311.9,319.1,325.7,328.0,323.2,312.6,300.3,289.9,281.1,&
273.5,268.1,265.3,262.4,258.6,253.9,249.6,245.3,243.5,245.6,252.8,266.8,&
289.3,319.2,346.0,364.9,376.7,380.4,378.7,384.0,379.0,385.6,375.4,382.5,&
285.0,289.8,292.8,299.5,309.1,314.4,314.3,308.4,299.4,290.7,283.1,275.6,&
268.6,264.0,262.2,260.9,258.2,254.7,250.8,246.5,245.5,250.2,260.4,276.2,&
301.4,334.5,364.7,387.2,399.9,405.7,406.9,410.5,406.8,409.5,397.5,400.0,&
274.6,287.6,291.2,297.0,302.5,305.3,303.8,298.1,290.2,283.9,279.1,273.5,&
267.2,262.4,260.9,260.5,259.8,258.3,256.4,254.0,254.9,261.0,272.2,288.7,&
313.0,342.8,370.3,392.4,407.6,418.4,427.7,434.6,434.6,433.5,419.6,417.5,&
264.2,277.1,280.3,288.3,299.7,305.6,306.5,301.7,292.8,284.1,277.6,273.2,&
267.8,262.4,259.3,259.3,260.1,260.7,261.1,262.2,265.9,273.8,285.6,301.1,&
320.4,343.8,366.8,385.0,398.7,409.7,420.1,431.3,438.5,442.0,441.8,435.0,&
253.9,266.6,269.5,279.6,297.4,307.3,311.4,311.1,306.5,297.9,287.1,277.1,&
269.0,262.6,258.0,256.3,257.4,259.5,262.2,267.2,272.5,280.3,292.1,305.9,&
321.1,340.0,359.5,374.8,385.3,392.8,397.5,402.6,406.5,404.9,402.5,399.5,&
243.5,256.0,258.6,270.9,295.0,309.6,318.1,318.2,316.5,311.1,300.3,286.7,&
273.6,264.2,257.4,254.1,255.6,260.1,265.2,271.3,275.5,281.1,289.0,297.2,&
307.0,322.2,342.0,357.4,365.0,365.1,360.1,357.3,361.8,365.5,367.7,366.5,&
233.1,245.5,247.7,262.2,292.7,312.0,325.2,327.3,328.7,325.8,315.4,299.3,&
282.5,270.3,261.9,257.3,258.0,263.3,269.2,275.3,278.5,281.3,286.6,292.6,&
298.7,307.8,321.7,334.8,343.1,343.1,336.1,328.2,325.6,326.0,327.8,326.9,&
222.8,235.0,236.9,253.6,290.3,314.3,333.6,343.4,345.5,341.7,329.6,310.8,&
291.0,276.0,266.4,261.3,261.8,266.9,271.9,277.1,279.0,279.5,282.8,288.0,&
293.4,299.5,308.3,317.2,323.5,324.4,319.5,311.8,304.7,300.7,298.3,295.1,&
212.4,224.5,226.0,244.9,278.2,319.4,350.1,360.6,359.8,352.3,338.4,319.9,&
300.9,285.9,274.7,268.4,267.4,270.2,272.6,275.7,276.4,275.3,276.6,280.5,&
285.2,291.1,298.8,306.5,311.8,312.8,308.9,302.5,295.5,289.6,286.9,312.6,&
202.0,213.9,233.8,266.1,308.2,346.5,368.2,370.7,362.8,350.9,336.1,319.3,&
302.7,289.2,278.2,270.4,267.3,266.5,266.1,267.3,266.8,265.8,267.7,271.6,&
276.1,282.2,291.8,301.9,309.7,312.6,310.4,304.4,295.7,313.6,309.0,330.1,&
285.3,292.7,304.3,324.1,346.3,360.4,363.0,355.5,343.1,330.2,318.1,306.1,&
294.4,284.1,275.4,268.8,264.4,260.7,258.3,257.6,255.7,255.3,258.3,263.3,&
271.2,283.8,299.6,312.8,321.3,324.6,322.3,330.9,323.5,337.6,331.1,347.6,&
325.8,328.3,330.5,334.8,340.0,342.2,341.1,334.6,323.3,310.9,300.0,291.3,&
282.9,275.5,270.2,265.5,260.7,256.1,252.5,249.6,247.2,247.9,253.0,262.7,&
278.5,299.9,321.2,337.3,346.7,350.3,350.5,357.4,351.3,361.6,353.3,365.0/),&
(/36,12/) )
! End of data for mapping latitude to zonal means

! Note: transformation from position to bins fails on endpoints
! (i.e., the poles and the international date line), so these values
! are trapped and set to the endpoint bins, as are out-of-range values.
OzoneData = 0.0
LatBin = 1+Nint(Lat+89.5)
LonBin = 1+Nint((Lon+179.375)/1.25)
if     (Lat <= -90.0) then; Lat = -90.0; LatBin =      1
elseif (Lat >=  90.0) then; Lat =  90.0; LatBin =    180; endif
if     (Lon <= -180.0) then; Lon = -180.0; LonBin =    1
elseif (Lon >=  180.0) then; Lon =  180.0; LonBin =  288; end if
if (Lat < 0) then; NS = 'S'; else; NS = 'N'; end if
if (Lon < 0) then; EW = 'W'; else; EW = 'E'; end if
Datasource: if (Zonals) then
   ! Locate the proper latitude bin and load the Ozone data from the
   ! zonal averages (i.e., no longitude resolution)
   OzoneData(1:12) = ZonalData(ceiling(real(LatBin)/5.01),1:12)
   OzoneData(13) = sum(OzoneData(1:12))/12.0
   if (Print) then
      write (PrintLUN,fmt='(//1x,a,f4.1,a/a/)')&
         ' Monthly mean total column ozone (DU) for Latitude ',abs(Lat),&
         ' '//NS//' (zonal means).',&
         ' Data from Nimbus7 Total Ozone Mapping Spectrometer '//&
         '(TOMS) Nov 1978 - Apr 1993.'
      write (PrintLUN,fmt='(4x,a)') JJ//'  '//JD//'   Mean'
      write (PrintLUN,fmt='(4x,12(i3,2x),1x,i3/)') nint(OzoneData)
   end if
else
   RecNum=LatBin
   do Month = 1,12
      read (DafUnit, rec=recnum) LatLine(1:288)
      OzoneData(Month) = LatLine(LonBin)
      RecNum = RecNum + 180
   end do
   OzoneData(13) = sum(OzoneData(1:12))/12.0
   if (Print) then
      write (PrintLUN,fmt='(//1x,a,f4.1,a,f5.1,a/a/)')&
         ' Monthly mean total column ozone (DU) for Latitude ',abs(Lat),&
         ' '//NS//', Longitude ', abs(Lon), ' '//EW//'.',&
         ' Data from Nimbus7 Total Ozone Mapping Spectrometer '//&
         '(TOMS) Nov 1978 - Apr 1993.'
      write (PrintLUN,fmt='(4x,a)') JJ//'  '//JD//'   Mean'
      write (PrintLUN,fmt='(4x,12(i3,2x),1x,i3/)') nint(OzoneData)
   end if
end if Datasource
! Transform data from Dobson Units (DU) to cm NTP
OzoneData = OzoneData * 0.001
return
end Subroutine Ozone
   