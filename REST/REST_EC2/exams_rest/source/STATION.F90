module StationData
use Global_Variables, only: LATG, LONGG, ELEVG
use Implementation_Control, only: stdout, Max_File
! LATG, LONGG, ELEVG are real numbers
use Local_Working_Space, only : State, Station, LRR, MLRA, StartYear, &
      EndYear, WBANumber, WMOnumber, Note
! StartYear, EndYear are integers. The values herein reflect the 
!    PRZM met file documentation, which is not always accurate. The
!    values reported by Exams when a met file is read (FirstYear, LastYear)
!    are derived from analysis of the data file itself.
! State, LRR, MLRA are character(10)
! MLRA is character(64)
! Station is character(64)
! WBANumber is character(5)
! WMOnumber is character(5)
! WMO from http://meteora.ucsd.edu/weather/cdf/text/weather_station.catalog

implicit none

contains

subroutine LoadStationData (DataFile)
! Data Module for Meteorological Station Identification
implicit none
character (len = *), intent(in) :: DataFile
character (len = Max_File) :: FileName
integer :: Solidus=0

! Detach path from "DataFile" -- test for a DOS or Unix specification
Solidus = scan(DataFile,'/\:',back=.true.)
if (Solidus>0) then ! extract file name from specification
   Solidus=Solidus+1
   FileName = DataFile(Solidus:)
else
   FileName = DataFile
end if

StationData: Select Case (trim(FileName))
case default
   write (stdout,fmt='(A)') ' Station not found.'
   WMOnumber = ' '
   WBANumber = ' '
   Station   = 'Not found'
   State     = 'NA'
   Note      = ' '
   LRR       = ' '
   MLRA      = ' '
   LATG      = 39.      ! somewhere back in Kansas...
   LONGG     = -96.0
   ELEVG     = 270

case ('W26451.DVF')
   WMOnumber = '70273'
   WBANumber = '26451'
   Station   = 'Anchorage'
   State     = 'AK'
   Note      = ' '
   LRR       = 'W'
   MLRA      = '170'
   LATG      = 61.17
   LONGG     = -150.02
   ELEVG     = 35
   StartYear = 1961
   EndYear   = 1990

case ('W25308.DVF')
   WMOnumber = '70398'
   WBANumber = '25308'
   Station   = 'Annette'
   State     = 'AK'
   Note      = ' '
   LRR       = 'W'
   MLRA      = '168'
   LATG      = 55.03
   LONGG     = -131.57
   ELEVG     = 33
   StartYear = 1961
   EndYear   = 1990

case ('W27502.DVF')
   WMOnumber = '70026'
   WBANumber = '27502'
   Station   = 'Barrow'
   State     = 'AK'
   Note      = ' '
   LRR       = 'Y'
   MLRA      = '182'
   LATG      = 71.30
   LONGG     = -156.78
   ELEVG     = 9
   StartYear = 1961
   EndYear   = 1990

case ('W26615.DVF')
   WMOnumber = '70219'
   WBANumber = '26615'
   Station   = 'Bethel'
   State     = 'AK'
   Note      = ' '
   LRR       = 'Y'
   MLRA      = '178'
   LATG      = 60.78
   LONGG     = -161.80
   ELEVG     = 38
   StartYear = 1961
   EndYear   = 1990

case ('W26533.DVF')
   WMOnumber = '70174'
   WBANumber = '26533'
   Station   = 'Bettles'
   State     = 'AK'
   Note      = ' '
   LRR       = 'X'
   MLRA      = '174'
   LATG      = 66.92
   LONGG     = -151.52
   ELEVG     = 196
   StartYear = 1961
   EndYear   = 1990

case ('W26415.DVF')
   WMOnumber = '70267'
   WBANumber = '26415'
   Station   = 'Big Delta'
   State     = 'AK'
   Note      = ' '
   LRR       = 'X'
   MLRA      = '174'
   LATG      = 64.00
   LONGG     = -145.73
   ELEVG     = 386
   StartYear = 1961
   EndYear   = 1990

case ('W25624.DVF')
   WMOnumber = '71485'
   WBANumber = '25624'
   Station   = 'Cold Bay'
   State     = 'AK'
   Note      = ' '
   LRR       = 'W'
   MLRA      = '171'
   LATG      = 55.20
   LONGG     = -162.72
   ELEVG     = 29
   StartYear = 1961
   EndYear   = 1990

case ('W26411.DVF')
   WMOnumber = '70261 '
   WBANumber = '26411'
   Station   = 'Fairbanks'
   State     = 'AK'
   Note      = ' '
   LRR       = 'X'
   MLRA      = '174'
   LATG      = 64.82
   LONGG     = -147.87
   ELEVG     = 133
   StartYear = 1961
   EndYear   = 1990

case ('W26425.DVF')
   WMOnumber = '70271'
   WBANumber = '26425'
   Station   = 'Gulkana'
   State     = 'AK'
   Note      = ' '
   LRR       = 'X'
   MLRA      = '172'
   LATG      = 62.15
   LONGG     = -145.45
   ELEVG     = 478
   StartYear = 1961
   EndYear   = 1990

case ('W25503.DVF')
   WMOnumber = '70326'
   WBANumber = '25503'
   Station   = 'King Salmon'
   State     = 'AK'
   Note      = ' '
   LRR       = 'Y'
   MLRA      = '178'
   LATG      = 58.68
   LONGG     = -156.65
   ELEVG     = 15
   StartYear = 1961
   EndYear   = 1990

case ('W25501.DVF')
   WMOnumber = '70350'
   WBANumber = '25501'
   Station   = 'Kodiak'
   State     = 'AK'
   Note      = ' '
   LRR       = 'W'
   MLRA      = '171'
   LATG      = 57.75
   LONGG     = -152.50
   ELEVG     = 5
   StartYear = 1961
   EndYear   = 1990

case ('W26616.DVF')
   WMOnumber = '70133'
   WBANumber = '26616'
   Station   = 'Kotzebue'
   State     = 'AK'
   Note      = ' '
   LRR       = 'Y'
   MLRA      = '177'
   LATG      = 66.87
   LONGG     = -162.63
   ELEVG     = 3
   StartYear = 1961
   EndYear   = 1990

case ('W26510.DVF')
   WMOnumber = '70231'
   WBANumber = '26510'
   Station   = 'McGrath'
   State     = 'AK'
   Note      = ' '
   LRR       = 'X'
   MLRA      = '174'
   LATG      = 62.97
   LONGG     = -155.62
   ELEVG     = 105
   StartYear = 1961
   EndYear   = 1990

case ('W26617.DVF')
   WMOnumber = '70200'
   WBANumber = '26617'
   Station   = 'Nome'
   State     = 'AK'
   Note      = ' '
   LRR       = 'Y'
   MLRA      = '177'
   LATG      = 64.50
   LONGG     = -165.43
   ELEVG     = 4
   StartYear = 1961
   EndYear   = 1990

case ('W25713.DVF')
   WMOnumber = '70308'
   WBANumber = '25713'
   Station   = 'St. Paul Island'
   State     = 'AK'
   Note      = ' '
   LRR       = 'Y'
   MLRA      = '179'
   LATG      = 57.15
   LONGG     = -170.22
   ELEVG     = 7
   StartYear = 1961
   EndYear   = 1990

case ('W26528.DVF')
   WMOnumber = '70251'
   WBANumber = '26528'
   Station   = 'Talkeetna'
   State     = 'AK'
   Note      = ' '
   LRR       = 'W'
   MLRA      = '170'
   LATG      = 62.30
   LONGG     = -150.10
   ELEVG     = 105
   StartYear = 1961
   EndYear   = 1990

case ('W25339.DVF')
   WMOnumber = '70361'
   WBANumber = '25339'
   Station   = 'Yakutat'
   State     = 'AK'
   Note      = ' '
   LRR       = 'W'
   MLRA      = '169'
   LATG      = 59.52
   LONGG     = -139.67
   ELEVG     = 8
   StartYear = 1961
   EndYear   = 1990

case ('W13876.DVF')
   WMOnumber = '72228'
   WBANumber = '13876'
   Station   = 'Birmingham'
   State     = 'AL'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '128'
   LATG      = 33.57
   LONGG     = -86.75
   ELEVG     = 189
   StartYear = 1961
   EndYear   = 1990

case ('MET129.MET')
   WMOnumber = '72228'
   WBANumber = '13876'
   Station   = 'Birmingham'
   State     = 'AL'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '129'
   LATG      = 33.57
   LONGG     = -86.75
   ELEVG     = 189
   StartYear = 1948
   EndYear   = 1983

case ('W03856.DVF')
   WMOnumber = '72323'
   WBANumber = '03856'
   Station   = 'Huntsville'
   State     = 'AL'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '128'
   LATG      = 34.65
   LONGG     = -86.77
   ELEVG     = 190
   StartYear = 1961
   EndYear   = 1990

case ('W13894.DVF')
   WMOnumber = '72223'
   WBANumber = '13894'
   Station   = 'Mobile'
   State     = 'AL'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '133A'
   LATG      = 30.68
   LONGG     = -88.25
   ELEVG     = 64
   StartYear = 1961
   EndYear   = 1990

case ('MET152A.MET')
   WMOnumber = '72223'
   WBANumber = '13894'
   Station   = 'Mobile'
   State     = 'AL'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '152A'
   LATG      = 30.68
   LONGG     = -88.25
   ELEVG     = 64
   StartYear = 1948
   EndYear   = 1983

case ('W13895.DVF')
   WMOnumber = '72226'
   WBANumber = '13895'
   Station   = 'Montgomery'
   State     = 'AL'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '135'
   LATG      = 32.30
   LONGG     = -86.40
   ELEVG     = 67
   StartYear = 1961
   EndYear   = 1990

case ('MET133A.MET','MET135.MET')
   WMOnumber = '72226'
   WBANumber = '13895'
   Station   = 'Montgomery'
   State     = 'AL'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '133,135'
   LATG      = 32.30
   LONGG     = -86.40
   ELEVG     = 67
   StartYear = 1948
   EndYear   = 1983

case ('W13964.DVF')
   WMOnumber = '72344'
   WBANumber = '13964'
   Station   = 'Fort Smith'
   State     = 'AR'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '118'
   LATG      = 35.33
   LONGG     = -94.37
   ELEVG     = 137
   StartYear = 1961
   EndYear   = 1990

case ('MET117.MET','MET118.MET')
   WMOnumber = '72344'
   WBANumber = '13964'
   Station   = 'Fort Smith'
   State     = 'AR'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '117,118'
   LATG      = 35.33
   LONGG     = -94.37
   ELEVG     = 137
   StartYear = 1948
   EndYear   = 1983

case ('W13963.DVF')
   WMOnumber = ' '
   WBANumber = '13963'
   Station   = 'Little Rock'
   State     = 'AR'
   Note      = 'Adams Field'
   LRR       = 'P'
   MLRA      = '133B'
   LATG      = 34.73
   LONGG     = -92.23
   ELEVG     = 78
   StartYear = 1961
   EndYear   = 1990

case ('MET119.MET')
   WMOnumber = ' '
   WBANumber = '13963'
   Station   = 'Little Rock'
   State     = 'AR'
   Note      = 'Adams Field'
   LRR       = 'N'
   MLRA      = '119'
   LATG      = 34.73
   LONGG     = -92.23
   ELEVG     = 78
   StartYear = 1948
   EndYear   = 1983

case ('W03103.DVF')
   WMOnumber = ' '
   WBANumber = '03103'
   Station   = 'Flagstaff'
   State     = 'AZ'
   Note      = 'Pulliam Airport'
   LRR       = 'D'
   MLRA      = '39'
   LATG      = 35.13
   LONGG     = -111.67
   ELEVG     = 2135
   StartYear = 1961
   EndYear   = 1990

case ('MET39.MET')
   WMOnumber = ' '
   WBANumber = '03103'
   Station   = 'Flagstaff'
   State     = 'AZ'
   Note      = 'Pulliam Airport'
   LRR       = 'D'
   MLRA      = '39'
   LATG      = 35.13
   LONGG     = -111.67
   ELEVG     = 2135
   StartYear = 1950
   EndYear   = 1983

case ('W23183.DVF')
   WMOnumber = '72278'
   WBANumber = '23183'
   Station   = 'Phoenix'
   State     = 'AZ'
   Note      = "Sky Harbor Int'l."
   LRR       = 'D'
   MLRA      = '40'
   LATG      = 33.43
   LONGG     = -112.02
   ELEVG     = 337
   StartYear = 1961
   EndYear   = 1990

case ('MET40.MET')
   WMOnumber = '72278'
   WBANumber = '23183'
   Station   = 'Phoenix'
   State     = 'AZ'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '40'
   LATG      = 33.43
   LONGG     = -112.02
   ELEVG     = 337
   StartYear = 1948
   EndYear   = 1983

case ('W23160.DVF')
   WMOnumber = '72274'
   WBANumber = '23160'
   Station   = 'Tucson'
   State     = 'AZ'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '40'
   LATG      = 32.13
   LONGG     = -110.93
   ELEVG     = 788
   StartYear = 1961
   EndYear   = 1990

case ('MET41.MET')
   WMOnumber = '72274'
   WBANumber = '23160'
   Station   = 'Tucson'
   State     = 'AZ'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '41'
   LATG      = 32.13
   LONGG     = -110.93
   ELEVG     = 788
   StartYear = 1949
   EndYear   = 1983

case ('MET31.MET')
   WMOnumber = '72280'
   WBANumber = '23195'
   Station   = 'Yuma'
   State     = 'AZ'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '31'
   LATG      = 32.66
   LONGG     = -114.60
   ELEVG     = 65.8
   StartYear = 1949
   EndYear   = 1983

case ('MET35.MET')
   WMOnumber = '72374'
   WBANumber = '23194'
   Station   = 'Winslow'
   State     = 'AZ'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '35'
   LATG      = 35.02
   LONGG     = -110.72
   ELEVG     = 1506.0
   StartYear = 1948
   EndYear   = 1983

case ('W24283.DVF')
   WMOnumber = ' '
   WBANumber = '24283'
   Station   = 'Arcata AP/Eureka WSO'
   State     = 'CA'
   Note      = 'Eureka WSO City is WBAN 24213, WMO I.D. 72594'
   LRR       = 'A'
   MLRA      = '4'
   LATG      = 40.98
   LONGG     = -124.10
   ELEVG     = 62
   StartYear = 1961
   EndYear   = 1990

case ('W23155.DVF')
   WMOnumber = '72384'
   WBANumber = '23155'
   Station   = 'Bakersfield'
   State     = 'CA'
   Note      = ' '
   LRR       = 'C'
   MLRA      = '17'
   LATG      = 35.42
   LONGG     = -119.05
   ELEVG     = 151
   StartYear = 1961
   EndYear   = 1990

case ('MET17.MET')
   WMOnumber = '72384'
   WBANumber = '23155'
   Station   = 'Bakersfield'
   State     = 'CA'
   Note      = ' '
   LRR       = 'C'
   MLRA      = '17'
   LATG      = 35.42
   LONGG     = -119.05
   ELEVG     = 151
   StartYear = 1948
   EndYear   = 1983

case ('W23161.DVF')
   WMOnumber = ''
   WBANumber = '23161'
   Station   = 'Daggett'
   State     = 'CA'
   Note      = 'Daggett (Barstow) AP'
   LRR       = 'D'
   MLRA      = '30'
   LATG      = 34.87
   LONGG     = -116.78
   ELEVG     = 586
   StartYear = 1961
   EndYear   = 1990

case ('W93193.DVF')
   WMOnumber = '72389'
   WBANumber = '93193'
   Station   = 'Fresno'
   State     = 'CA'
   Note      = ' '
   LRR       = 'C'
   MLRA      = '17'
   LATG      = 36.78
   LONGG     = -119.72
   ELEVG     = 102
   StartYear = 1961
   EndYear   = 1990

case ('W23129.DVF')
   WMOnumber = '72297'
   WBANumber = '23129'
   Station   = 'Long Beach'
   State     = 'CA'
   Note      = 'Long Beach Daugherty'
   LRR       = 'C'
   MLRA      = '19'
   LATG      = 33.82
   LONGG     = -118.15
   ELEVG     = 8
   StartYear = 1961
   EndYear   = 1990

case ('MET19.MET')
   WMOnumber = '72297'
   WBANumber = '23129'
   Station   = 'Long Beach'
   State     = 'CA'
   Note      = 'Long Beach Daugherty '
   LRR       = 'C'
   MLRA      = '19'
   LATG      = 33.82
   LONGG     = -118.15
   ELEVG     = 8
   StartYear = 1959
   EndYear   = 1983

case ('W23174.DVF')
   WMOnumber = '72295'
   WBANumber = '23174'
   Station   = 'Los Angeles'
   State     = 'CA'
   Note      = ' '
   LRR       = 'C'
   MLRA      = '19'
   LATG      = 33.93
   LONGG     = -118.40
   ELEVG     = 30
   StartYear = 1961
   EndYear   = 1990

case ('MET20.MET')
   WMOnumber = '72295'
   WBANumber = '23174'
   Station   = 'Los Angeles'
   State     = 'CA'
   Note      = ' '
   LRR       = 'C'
   MLRA      = '19'
   LATG      = 33.93
   LONGG     = -118.40
   ELEVG     = 30
   StartYear = 1947
   EndYear   = 1983

case ('W23232.DVF')
   WMOnumber = '72483'
   WBANumber = '23232'
   Station   = 'Sacramento'
   State     = 'CA'
   Note      = 'Executive Airport'
   LRR       = 'C'
   MLRA      = '17'
   LATG      = 38.52
   LONGG     = -121.50
   ELEVG     = 6
   StartYear = 1961
   EndYear   = 1990

case ('MET18.MET')
   WMOnumber = '72483'
   WBANumber = '23232'
   Station   = 'Sacramento'
   State     = 'CA'
   Note      = 'Executive Airport'
   LRR       = 'C'
   MLRA      = '17'
   LATG      = 38.52
   LONGG     = -121.50
   ELEVG     = 6
   StartYear = 1948
   EndYear   = 1983

case ('W23188.DVF')
   WMOnumber = '72290'
   WBANumber = '23188'
   Station   = 'San Diego'
   State     = 'CA'
   Note      = 'Lindbergh Field'
   LRR       = 'C'
   MLRA      = '19'
   LATG      = 32.73
   LONGG     = -117.17
   ELEVG     = 4
   StartYear = 1961
   EndYear   = 1990

case ('W23234.DVF')
   WMOnumber = '72494'
   WBANumber = '23234'
   Station   = 'San Francisco'
   State     = 'CA'
   Note      = ' '
   LRR       = 'C'
   MLRA      = '14'
   LATG      = 37.62
   LONGG     = -122.38
   ELEVG     = 2
   StartYear = 1961
   EndYear   = 1990

case ('MET4.MET','MET14.MET')
   WMOnumber = '72494'
   WBANumber = '23234'
   Station   = 'San Francisco'
   State     = 'CA'
   Note      = ' '
   LRR       = 'C'
   MLRA      = '4,14'
   LATG      = 37.62
   LONGG     = -122.38
   ELEVG     = 2
   StartYear = 1948
   EndYear   = 1983

case ('MET15.MET','MET16.MET')
   WMOnumber = '72493'
   WBANumber = '23230'
   Station   = 'Oakland'
   State     = 'CA'
   Note      = ' '
   LRR       = 'C'
   MLRA      = '15,16'
   LATG      = 37.72
   LONGG     = -122.22
   ELEVG     = 2
   StartYear = 1949
   EndYear   = 1983

case ('W23273.DVF')
   WMOnumber = '72394'
   WBANumber = '23273'
   Station   = 'Santa Maria'
   State     = 'CA'
   Note      = ' '
   LRR       = 'C'
   MLRA      = '15'
   LATG      = 34.90
   LONGG     = -120.45
   ELEVG     = 77
   StartYear = 1961
   EndYear   = 1990

case ('W23061.DVF')
   WMOnumber = '72462'
   WBANumber = '23061'
   Station   = 'Alamosa'
   State     = 'CO'
   Note      = ' '
   LRR       = 'E'
   MLRA      = '51'
   LATG      = 37.45
   LONGG     = -105.87
   ELEVG     = 2298
   StartYear = 1961
   EndYear   = 1990

case ('W94018.DVF')
   WMOnumber = '72469'
   WBANumber = '94018'
   Station   = 'Boulder/Denver(Stapleton AP)'
   State     = 'CO'
   Note      = 'Denver is WBAN 23062; Boulder (sunlight data) is WBAN 94018'
   LRR       = 'G'
   MLRA      = '67'
   LATG      = 39.77
   LONGG     = -104.87
   ELEVG     = 1611
   StartYear = 1961
   EndYear   = 1990

case ('W93037.DVF')
   WMOnumber = '72466'
   WBANumber = '93037'
   Station   = 'Colorado Springs'
   State     = 'CO'
   Note      = ' '
   LRR       = 'E'
   MLRA      = '49'
   LATG      = 38.82
   LONGG     = -104.72
   ELEVG     = 1873
   StartYear = 1961
   EndYear   = 1990

case ('W23063.DVF')
   WMOnumber = ' '
   WBANumber = '23063'
   Station   = 'Eagle'
   State     = 'CO'
   Note      = 'Eagle County AP'
   LRR       = 'E'
   MLRA      = '48A'
   LATG      = 39.65
   LONGG     = -106.92
   ELEVG     = 1980
   StartYear = 1961
   EndYear   = 1988

case ('W23066.DVF')
   WMOnumber = '72476'
   WBANumber = '23066'
   Station   = 'Grand Junction'
   State     = 'CO'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '34'
   LATG      = 39.12
   LONGG     = -108.53
   ELEVG     = 1476
   StartYear = 1961
   EndYear   = 1990

case ('MET34.MET','MET48A.MET','MET48B.MET')
   WMOnumber = '72476'
   WBANumber = '23066'
   Station   = 'Grand Junction'
   State     = 'CO'
   Note      = ' '
   LRR       = 'D,E'
   MLRA      = '34,48A,48B'
   LATG      = 39.12
   LONGG     = -108.53
   ELEVG     = 1480.7
   StartYear = 1948
   EndYear   = 1983

case ('W93058.DVF')
   WMOnumber = '72464'
   WBANumber = '93058'
   Station   = 'Pueblo'
   State     = 'CO'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '69'
   LATG      = 38.28
   LONGG     = -104.50
   ELEVG     = 1428
   StartYear = 1961
   EndYear   = 1990

case ('MET51.MET','MET69.MET')
   WMOnumber = '72464'
   WBANumber = '93058'
   Station   = 'Pueblo'
   State     = 'CO'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '51,69'
   LATG      = 38.28
   LONGG     = -104.50
   ELEVG     = 1428
   StartYear = 1955
   EndYear   = 1981

case ('W94702.DVF')
   WMOnumber = '72504'
   WBANumber = '94702'
   Station   = 'Bridgeport'
   State     = 'CT'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '144A'
   LATG      = 41.17
   LONGG     = -73.13
   ELEVG     = 3
   StartYear = 1961
   EndYear   = 1990

case ('W14740.DVF')
   WMOnumber = ' '
   WBANumber = '14740'
   Station   = 'Hartford'
   State     = 'CT'
   Note      = 'Hartford Bradley AP'
   LRR       = 'R'
   MLRA      = '145'
   LATG      = 41.93
   LONGG     = -72.68
   ELEVG     = 49
   StartYear = 1961
   EndYear   = 1990

case ('W13781.DVF')
   WMOnumber = ' '
   WBANumber = '13781'
   Station   = 'Wilmington'
   State     = 'DE'
   Note      = 'Wilmington New Castle'
   LRR       = 'S'
   MLRA      = '149A'
   LATG      = 39.67
   LONGG     = -75.60
   ELEVG     = 23
   StartYear = 1961
   EndYear   = 1990

case ('MET153C.MET')
   WMOnumber = ' '
   WBANumber = '13781'
   Station   = 'Wilmington'
   State     = 'DE'
   Note      = 'Wilmington New Castle'
   LRR       = 'T'
   MLRA      = '153C'
   LATG      = 39.67
   LONGG     = -75.60
   ELEVG     = 23
   StartYear = 1948
   EndYear   = 1983

case ('W12834.DVF')
   WMOnumber = ' '
   WBANumber = '12834'
   Station   = 'Daytona Beach'
   State     = 'FL'
   Note      = 'Daytona Beach Regional AP'
   LRR       = 'U'
   MLRA      = '155'
   LATG      = 29.18
   LONGG     = -81.05
   ELEVG     = 9
   StartYear = 1961
   EndYear   = 1990

case ('W13889.DVF')
   WMOnumber = '72206'
   WBANumber = '13889'
   Station   = 'Jacksonville'
   State     = 'FL'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '153A'
   LATG      = 30.50
   LONGG     = -81.70
   ELEVG     = 9
   StartYear = 1961
   EndYear   = 1990

case ('W12836.DVF')
   WMOnumber = '72201'
   WBANumber = '12836'
   Station   = 'Key West'
   State     = 'FL'
   Note      = ' '
   LRR       = 'U'
   MLRA      = '156A'
   LATG      = 24.55
   LONGG     = -81.75
   ELEVG     = 1
   StartYear = 1961
   EndYear   = 1990

case ('W12839.DVF')
   WMOnumber = '72202'
   WBANumber = '12839'
   Station   = 'Miami'
   State     = 'FL'
   Note      = ' '
   LRR       = 'U'
   MLRA      = '156A'
   LATG      = 25.80
   LONGG     = -80.30
   ELEVG     = 4
   StartYear = 1961
   EndYear   = 1990

case ('MER156A.MET')
   WMOnumber = '72202'
   WBANumber = '12839'
   Station   = 'Miami'
   State     = 'FL'
   Note      = ' '
   LRR       = 'U'
   MLRA      = '156A'
   LATG      = 25.80
   LONGG     = -80.30
   ELEVG     = 4
   StartYear = 1948
   EndYear   = 1983

case ('W93805.DVF')
   WMOnumber = '72214'
   WBANumber = '93805'
   Station   = 'Tallahassee/Apalachicola'
   State     = 'FL'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '133A'
   LATG      = 30.38
   LONGG     = -84.37
   ELEVG     = 17
   StartYear = 1961
   EndYear   = 1990

case ('MET138.MET')
   WMOnumber = '72214'
   WBANumber = '93805'
   Station   = 'Tallahassee/Apalachicola'
   State     = 'FL'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '138'
   LATG      = 30.38
   LONGG     = -84.37
   ELEVG     = 17
   StartYear = 1948
   EndYear   = 1983

case ('W12842.DVF')
   WMOnumber = '72211'
   WBANumber = '12842'
   Station   = 'Tampa'
   State     = 'FL'
   Note      = ' '
   LRR       = 'U'
   MLRA      = '155'
   LATG      = 27.97
   LONGG     = -82.53
   ELEVG     = 6
   StartYear = 1961
   EndYear   = 1990

case ('W12844.DVF')
   WMOnumber = '72203'
   WBANumber = '12844'
   Station   = 'West Palm Beach'
   State     = 'FL'
   Note      = ' '
   LRR       = 'U'
   MLRA      = '155'
   LATG      = 26.68
   LONGG     = -80.12
   ELEVG     = 6
   StartYear = 1961
   EndYear   = 1990

case ('MET155.MET','MET156B.MET')
   WMOnumber = '72203'
   WBANumber = '12844'
   Station   = 'West Palm Beach'
   State     = 'FL'
   Note      = ' '
   LRR       = 'U'
   MLRA      = '155,156B'
   LATG      = 26.68
   LONGG     = -80.12
   ELEVG     = 6
   StartYear = 1948
   EndYear   = 1983

case ('MET154.MET')
   WMOnumber = ' '
   WBANumber = '12841'
   Station   = 'Orlando'
   State     = 'FL'
   Note      = 'Orlando Herndon AP '
   LRR       = 'U'
   MLRA      = '154'
   LATG      = 28.43
   LONGG     = -81.32
   ELEVG     = 29.3
   StartYear = 1948
   EndYear   = 1973

case ('W13873.DVF')
   WMOnumber = '72311'
   WBANumber = '13873'
   Station   = 'Athens'
   State     = 'GA'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '136'
   LATG      = 33.95
   LONGG     = -83.32
   ELEVG     = 244
   StartYear = 1961
   EndYear   = 1990

case ('MET136.MET')
   WMOnumber = '72311'
   WBANumber = '13873'
   Station   = 'Athens'
   State     = 'GA'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '136'
   LATG      = 33.95
   LONGG     = -83.32
   ELEVG     = 244
   StartYear = 1956
   EndYear   = 1983

case ('W13874.DVF')
   WMOnumber = '72219'
   WBANumber = '13874'
   Station   = 'Atlanta'
   State     = 'GA'
   Note      = 'Hartsfield'
   LRR       = 'P'
   MLRA      = '136'
   LATG      = 33.65
   LONGG     = -84.43
   ELEVG     = 308
   StartYear = 1961
   EndYear   = 1990

case ('W03820.DVF')
   WMOnumber = '72218'
   WBANumber = '03820'
   Station   = 'Augusta'
   State     = 'GA'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '133A'
   LATG      = 33.37
   LONGG     = -81.97
   ELEVG     = 45
   StartYear = 1961
   EndYear   = 1990

case ('MET137.MET')
   WMOnumber = '72218'
   WBANumber = '03820'
   Station   = 'Augusta'
   State     = 'GA'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '137'
   LATG      = 33.37
   LONGG     = -81.97
   ELEVG     = 45
   StartYear = 1950
   EndYear   = 1983

case ('W93842.DVF')
   WMOnumber = ' '
   WBANumber = '93842'
   Station   = 'Columbus'
   State     = 'GA'
   Note      = 'Columbus Metro AP'
   LRR       = 'P'
   MLRA      = '137'
   LATG      = 32.52
   LONGG     = -84.95
   ELEVG     = 137
   StartYear = 1961
   EndYear   = 1990

case ('W03813.DVF')
   WMOnumber = '72217'
   WBANumber = '03813'
   Station   = 'Macon'
   State     = 'GA'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '137'
   LATG      = 32.70
   LONGG     = -83.65
   ELEVG     = 108
   StartYear = 1961
   EndYear   = 1990

case ('W03822.DVF')
   WMOnumber = '72207'
   WBANumber = '03822'
   Station   = 'Savannah'
   State     = 'GA'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '153A'
   LATG      = 32.13
   LONGG     = -81.20
   ELEVG     = 14
   StartYear = 1961
   EndYear   = 1990

case ('W21504.DVF')
   WMOnumber = '91285'
   WBANumber = '21504'
   Station   = 'Hilo'
   State     = 'HI'
   Note      = ' '
   LRR       = 'V'
   MLRA      = '161'
   LATG      = 19.72
   LONGG     = -155.07
   ELEVG     = 8
   StartYear = 1961
   EndYear   = 1990

case ('W22521.DVF')
   WMOnumber = '91182'
   WBANumber = '22521'
   Station   = 'Honolulu'
   State     = 'HI'
   Note      = ' '
   LRR       = 'V'
   MLRA      = '163'
   LATG      = 21.33
   LONGG     = -157.92
   ELEVG     = 2
   StartYear = 1961
   EndYear   = 1990

case ('W22516.DVF')
   WMOnumber = '91190'
   WBANumber = '22516'
   Station   = 'Kahului'
   State     = 'HI'
   Note      = ' '
   LRR       = 'V'
   MLRA      = '158'
   LATG      = 20.90
   LONGG     = -156.43
   ELEVG     = 15
   StartYear = 1961
   EndYear   = 1990

case ('W22536.DVF')
   WMOnumber = '91165'
   WBANumber = '22536'
   Station   = 'Lihue'
   State     = 'HI'
   Note      = ' '
   LRR       = 'V'
   MLRA      = '158'
   LATG      = 21.98
   LONGG     = -159.35
   ELEVG     = 31
   StartYear = 1961
   EndYear   = 1990

case ('W14933.DVF')
   WMOnumber = '72546'
   WBANumber = '14933'
   Station   = 'Des Moines'
   State     = 'IA'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '108'
   LATG      = 41.53
   LONGG     = -93.65
   ELEVG     = 286
   StartYear = 1961
   EndYear   = 1990

case ('MET108.MET','MET109.MET')
   WMOnumber = ' '
   WBANumber = '14931'
   Station   = 'Burlington'
   State     = 'IA'
   Note      = 'Burlington Municipal AP'
   LRR       = 'M'
   MLRA      = '108,109'
   LATG      = 40.78
   LONGG     = -91.12
   ELEVG     = 212.8
   StartYear = 1948
   EndYear   = 1966

case ('MET111.MET')
   WMOnumber = '72429'
   WBANumber = '93815'
   Station   = 'Vandalia'
   State     = 'OH'
   Note      = "Weather station Dayton Int'l. Airport"
   LRR       = 'M'
   MLRA      = '111'
   LATG      = 39.90
   LONGG     = -84.22
   ELEVG     = 307.5
   StartYear = 1948
   EndYear   = 1983

case ('W14940.DVF')
   WMOnumber = ' '
   WBANumber = '14940'
   Station   = 'Mason City'
   State     = 'IA'
   Note      = 'Mason City AP'
   LRR       = 'M'
   MLRA      = '104'
   LATG      = 43.15
   LONGG     = -93.30
   ELEVG     = 364
   StartYear = 1961
   EndYear   = 1990

case ('W14943.DVF')
   WMOnumber = '72557'
   WBANumber = '14943'
   Station   = 'Sioux City'
   State     = 'IA'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '107'
   LATG      = 42.40
   LONGG     = -96.38
   ELEVG     = 334
   StartYear = 1961
   EndYear   = 1990

case ('MET102B.MET')
   WMOnumber = '72557'
   WBANumber = '14943'
   Station   = 'Sioux City'
   State     = 'IA'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '107'
   LATG      = 42.40
   LONGG     = -96.38
   ELEVG     = 334
   StartYear = 1948
   EndYear   = 1983

case ('W94910.DVF')
   WMOnumber = '72548'
   WBANumber = '94910'
   Station   = 'Waterloo'
   State     = 'IA'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '104'
   LATG      = 42.55
   LONGG     = -92.40
   ELEVG     = 265
   StartYear = 1961
   EndYear   = 1990

case ('MET104.MET')
   WMOnumber = '72548'
   WBANumber = '94910'
   Station   = 'Waterloo'
   State     = 'IA'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '104'
   LATG      = 42.55
   LONGG     = -92.40
   ELEVG     = 265
   StartYear = 1961
   EndYear   = 1983

case ('W24131.DVF')
   WMOnumber = '72681'
   WBANumber = '24131'
   Station   = 'Boise'
   State     = 'ID'
   Note      = ' '
   LRR       = 'B'
   MLRA      = '11'
   LATG      = 43.57
   LONGG     = -116.22
   ELEVG     = 865
   StartYear = 1961
   EndYear   = 1990

case ('W24156.DVF')
   WMOnumber = '72578'
   WBANumber = '24156'
   Station   = 'Pocatello'
   State     = 'ID'
   Note      = ' '
   LRR       = 'B'
   MLRA      = '11B'
   LATG      = 42.92
   LONGG     = -112.60
   ELEVG     = 1358
   StartYear = 1961
   EndYear   = 1990

case ('W94846.DVF')
   WMOnumber = '72530'
   WBANumber = '94846'
   Station   = "Chicago O'Hare AP"
   State     = 'IL'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '110'
   LATG      = 42.00
   LONGG     = -87.88
   ELEVG     = 201
   StartYear = 1961
   EndYear   = 1990

case ('MET110.MET')
   WMOnumber = '72534'
   WBANumber = '14819'
   Station   = 'Chicago Midway AP'
   State     = 'IL'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '110'
   LATG      = 41.78
   LONGG     = -87.75
   ELEVG     = 189.0
   StartYear = 1948
   EndYear   = 1979

case ('W14923.DVF')
   WMOnumber = '72544'
   WBANumber = '14923'
   Station   = 'Moline'
   State     = 'IL'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '108'
   LATG      = 41.45
   LONGG     = -90.50
   ELEVG     = 177
   StartYear = 1961
   EndYear   = 1990

case ('W14842.DVF')
   WMOnumber = '72532'
   WBANumber = '14842'
   Station   = 'Peoria'
   State     = 'IL'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '115'
   LATG      = 40.67
   LONGG     = -89.68
   ELEVG     = 198
   StartYear = 1961
   EndYear   = 1990

case ('W94822.DVF')
   WMOnumber = '72543'
   WBANumber = '94822'
   Station   = 'Rockford'
   State     = 'IL'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '95B'
   LATG      = 42.20
   LONGG     = -89.10
   ELEVG     = 221
   StartYear = 1961
   EndYear   = 1990

case ('W93822.DVF')
   WMOnumber = '72439'
   WBANumber = '93822'
   Station   = 'Springfield'
   State     = 'IL'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '115'
   LATG      = 39.85
   LONGG     = -89.68
   ELEVG     = 179
   StartYear = 1961
   EndYear   = 1990

case ('W93817.DVF')
   WMOnumber = '72432'
   WBANumber = '93817'
   Station   = 'Evansville'
   State     = 'IN'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '115'
   LATG      = 38.05
   LONGG     = -87.53
   ELEVG     = 116
   StartYear = 1961
   EndYear   = 1990

case ('MET120.MET')
   WMOnumber = '72432'
   WBANumber = '93817'
   Station   = 'Evansville'
   State     = 'IN'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '120'
   LATG      = 38.05
   LONGG     = -87.53
   ELEVG     = 116
   StartYear = 1962
   EndYear   = 1983

case ('W14827.DVF')
   WMOnumber = '72533'
   WBANumber = '14827'
   Station   = 'Fort Wayne'
   State     = 'IN'
   Note      = 'Baer Field'
   LRR       = 'M'
   MLRA      = '111'
   LATG      = 41.00
   LONGG     = -85.20
   ELEVG     = 241
   StartYear = 1961
   EndYear   = 1990

case ('W93819.DVF')
   WMOnumber = '72438'
   WBANumber = '93819'
   Station   = 'Indianapolis'
   State     = 'IN'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '111'
   LATG      = 39.73
   LONGG     = -86.27
   ELEVG     = 241
   StartYear = 1961
   EndYear   = 1990

case ('W14848.DVF')
   WMOnumber = ' '
   WBANumber = '14848'
   Station   = 'South Bend'
   State     = 'IN'
   Note      = 'South Bend Michiana'
   LRR       = 'L'
   MLRA      = '98'
   LATG      = 41.70
   LONGG     = -86.32
   ELEVG     = 236
   StartYear = 1961
   EndYear   = 1990

case ('MET97.MET')
   WMOnumber = ' '
   WBANumber = '14848'
   Station   = 'South Bend'
   State     = 'IN'
   Note      = 'South Bend Michiana'
   LRR       = 'L'
   MLRA      = '97'
   LATG      = 41.70
   LONGG     = -86.32
   ELEVG     = 236
   StartYear = 1948
   EndYear   = 1983

case ('W13985.DVF')
   WMOnumber = '72451'
   WBANumber = '13985'
   Station   = 'Dodge City'
   State     = 'KS'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '73'
   LATG      = 37.77
   LONGG     = -99.97
   ELEVG     = 787
   StartYear = 1961
   EndYear   = 1990

case ('MET79.MET')
   WMOnumber = '72451'
   WBANumber = '13985'
   Station   = 'Dodge City'
   State     = 'KS'
   Note      = 'Station is in MLRA 73.'
   LRR       = 'H'
   MLRA      = '79'
   LATG      = 37.77
   LONGG     = -99.97
   ELEVG     = 787
   StartYear = 1961
   EndYear   = 1990

case ('W23065.DVF')
   WMOnumber = '72465'
   WBANumber = '23065'
   Station   = 'Goodland'
   State     = 'KS'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '72'
   LATG      = 39.37
   LONGG     = -101.70
   ELEVG     = 1111
   StartYear = 1961
   EndYear   = 1990

case ('MET72.MET','MET73.MET','MET74.MET')
   WMOnumber = '72465'
   WBANumber = '23065'
   Station   = 'Goodland'
   State     = 'KS'
   Note      = 'Station is in MLRA 72.'
   LRR       = 'H'
   MLRA      = '72,73,74'
   LATG      = 39.37
   LONGG     = -101.70
   ELEVG     = 1111
   StartYear = 1948
   EndYear   = 1983

case ('W13996.DVF')
   WMOnumber = '72456'
   WBANumber = '13996'
   Station   = 'Topeka'
   State     = 'KS'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '106'
   LATG      = 39.07
   LONGG     = -95.63
   ELEVG     = 267
   StartYear = 1961
   EndYear   = 1990

case ('W03928.DVF')
   WMOnumber = '72450'
   WBANumber = '03928'
   Station   = 'Wichita'
   State     = 'KS'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '80A'
   LATG      = 37.65
   LONGG     = -97.43
   ELEVG     = 406
   StartYear = 1961
   EndYear   = 1990

case ('MET76.MET')
   WMOnumber = '72450'
   WBANumber = '03928'
   Station   = 'Wichita'
   State     = 'KS'
   Note      = 'Station is in MLRA 80A.'
   LRR       = 'H'
   MLRA      = '76'
   LATG      = 37.65
   LONGG     = -97.43
   ELEVG     = 406
   StartYear = 1948
   EndYear   = 1983

case ('W93814.DVF')
   WMOnumber = '72421'
   WBANumber = '93814'
   Station   = 'Covington (Cincinnati)'
   State     = 'KY'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '121'
   LATG      = 39.05
   LONGG     = -84.67
   ELEVG     = 265
   StartYear = 1961
   EndYear   = 1990

case ('W93820.DVF')
   WMOnumber = '72422'
   WBANumber = '93820'
   Station   = 'Lexington'
   State     = 'KY'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '121'
   LATG      = 38.03
   LONGG     = -84.60
   ELEVG     = 294
   StartYear = 1961
   EndYear   = 1990

case ('MET121.MET','MET125.MET')
   WMOnumber = '72422'
   WBANumber = '93820'
   Station   = 'Lexington'
   State     = 'KY'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '121,125'
   LATG      = 38.03
   LONGG     = -84.60
   ELEVG     = 294
   StartYear = 1948
   EndYear   = 1983

case ('W93821.DVF')
   WMOnumber = '72423'
   WBANumber = '93821'
   Station   = 'Louisville'
   State     = 'KY'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '121'
   LATG      = 38.18
   LONGG     = -85.73
   ELEVG     = 145
   StartYear = 1961
   EndYear   = 1990

case ('MET114.MET')
   WMOnumber = '72423'
   WBANumber = '93821'
   Station   = 'Louisville'
   State     = 'KY'
   Note      = 'Standiford Field '
   LRR       = 'N'
   MLRA      = '121'
   LATG      = 38.18
   LONGG     = -85.73
   ELEVG     = 145
   StartYear = 1948
   EndYear   = 1983

case ('W13970.DVF')
   WMOnumber = ' '
   WBANumber = '13970'
   Station   = 'Baton Rouge'
   State     = 'LA'
   Note      = 'Ryan AP'
   LRR       = 'P'
   MLRA      = '134'
   LATG      = 30.53
   LONGG     = -91.13
   ELEVG     = 20
   StartYear = 1961
   EndYear   = 1990

case ('W03937.DVF')
   WMOnumber = '72240'
   WBANumber = '03937'
   Station   = 'Lake Charles'
   State     = 'LA'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '150A'
   LATG      = 30.12
   LONGG     = -93.22
   ELEVG     = 3
   StartYear = 1961
   EndYear   = 1990

case ('W12916.DVF')
   WMOnumber = '72231'
   WBANumber = '12916'
   Station   = 'New Orleans'
   State     = 'LA'
   Note      = ' '
   LRR       = 'O'
   MLRA      = '131'
   LATG      = 29.98
   LONGG     = -90.25
   ELEVG     = 3
   StartYear = 1961
   EndYear   = 1990

case ('MET151.MET')
   WMOnumber = '72231'
   WBANumber = '12916'
   Station   = 'New Orleans'
   State     = 'LA'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '151'
   LATG      = 29.98
   LONGG     = -90.25
   ELEVG     = 3
   StartYear = 1948
   EndYear   = 1983

case ('W13957.DVF')
   WMOnumber = '72248'
   WBANumber = '13957'
   Station   = 'Shreveport'
   State     = 'LA'
   Note      = ' '
   LRR       = 'O'
   MLRA      = '131'
   LATG      = 32.47
   LONGG     = -93.82
   ELEVG     = 77
   StartYear = 1961
   EndYear   = 1990

case ('MET133B.MET')
   WMOnumber = '72248'
   WBANumber = '13957'
   Station   = 'Shreveport'
   State     = 'LA'
   Note      = ' '
   LRR       = 'O'
   MLRA      = '131'
   LATG      = 32.47
   LONGG     = -93.82
   ELEVG     = 77
   StartYear = 1948
   EndYear   = 1983

case ('W14739.DVF')
   WMOnumber = '72509'
   WBANumber = '14739'
   Station   = 'Boston'
   State     = 'MA'
   Note      = "Logan Int'l."
   LRR       = 'R'
   MLRA      = '144A'
   LATG      = 42.37
   LONGG     = -71.03
   ELEVG     = 6
   StartYear = 1961
   EndYear   = 1990

case ('W94746.DVF')
   WMOnumber = ''
   WBANumber = '94746'
   Station   = 'Worcester'
   State     = 'MA'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '144A'
   LATG      = 42.27
   LONGG     = -71.87
   ELEVG     = 300
   StartYear = 1961
   EndYear   = 1990

case ('MET144A.MET')
   WMOnumber = ' '
   WBANumber = '94746'
   Station   = 'Worcester'
   State     = 'MA'
   Note      = 'Worcester Municipal AP'
   LRR       = 'R'
   MLRA      = '144A'
   LATG      = 42.27
   LONGG     = -71.87
   ELEVG     = 300
   StartYear = 1960
   EndYear   = 1983

case ('W93721.DVF')
   WMOnumber = '72406'
   WBANumber = '93721'
   Station   = 'Baltimore'
   State     = 'MD'
   Note      = ' '
   LRR       = 'S'
   MLRA      = '149A'
   LATG      = 39.18
   LONGG     = -76.67
   ELEVG     = 47
   StartYear = 1961
   EndYear   = 1990

case ('W14607.DVF')
   WMOnumber = '72712'
   WBANumber = '14607'
   Station   = 'Caribou'
   State     = 'ME'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '146'
   LATG      = 46.87
   LONGG     = -68.02
   ELEVG     = 190
   StartYear = 1961
   EndYear   = 1990

case ('W14764.DVF')
   WMOnumber = '72606'
   WBANumber = '14764'
   Station   = 'Portland'
   State     = 'ME'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '144B'
   LATG      = 43.65
   LONGG     = -70.32
   ELEVG     = 14
   StartYear = 1961
   EndYear   = 1990

case ('MET146.MET')
   WMOnumber = '72606'
   WBANumber = '14764'
   Station   = 'Portland'
   State     = 'ME'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '146'
   LATG      = 43.65
   LONGG     = -70.32
   ELEVG     = 14
   StartYear = 1948
   EndYear   = 1983

case ('W94849.DVF')
   WMOnumber = '72639'
   WBANumber = '94849'
   Station   = 'Alpena'
   State     = 'MI'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '94A'
   LATG      = 45.07
   LONGG     = -83.57
   ELEVG     = 210
   StartYear = 1961
   EndYear   = 1990

case ('MET94A.MET')
   WMOnumber = '72639'
   WBANumber = '94849'
   Station   = 'Alpena'
   State     = 'MI'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '94A'
   LATG      = 45.07
   LONGG     = -83.57
   ELEVG     = 210
   StartYear = 1947
   EndYear   = 1983

case ('W94847.DVF')
   WMOnumber = '72537'
   WBANumber = '94847'
   Station   = 'Detroit Metro AP'
   State     = 'MI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '99'
   LATG      = 42.23
   LONGG     = -83.33
   ELEVG     = 193
   StartYear = 1961
   EndYear   = 1990

case ('MET99.MET')
   WMOnumber = '72537'
   WBANumber = '94847'
   Station   = 'Detroit Metro AP'
   State     = 'MI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '99'
   LATG      = 42.23
   LONGG     = -83.33
   ELEVG     = 193
   StartYear = 1959
   EndYear   = 1983

case ('W14826.DVF')
   WMOnumber = '72637'
   WBANumber = '14826'
   Station   = 'Flint'
   State     = 'MI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '98'
   LATG      = 42.97
   LONGG     = -83.75
   ELEVG     = 235
   StartYear = 1961
   EndYear   = 1990

case ('W94860.DVF')
   WMOnumber = '72635'
   WBANumber = '94860'
   Station   = 'Grand Rapids'
   State     = 'MI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '98'
   LATG      = 42.88
   LONGG     = -85.52
   ELEVG     = 239
   StartYear = 1961
   EndYear   = 1990

case ('W94814.DVF')
   WMOnumber = '72638'
   WBANumber = '94814'
   Station   = 'Houghton Lake'
   State     = 'MI'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '94A'
   LATG      = 44.37
   LONGG     = -84.68
   ELEVG     = 350
   StartYear = 1965
   EndYear   = 1990

case ('W14836.DVF')
   WMOnumber = '72539'
   WBANumber = '14836'
   Station   = 'Lansing'
   State     = 'MI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '98'
   LATG      = 42.77
   LONGG     = -84.60
   ELEVG     = 256
   StartYear = 1961
   EndYear   = 1990

case ('MET98.MET')
   WMOnumber = '72539'
   WBANumber = '14836'
   Station   = 'Lansing'
   State     = 'MI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '98'
   LATG      = 42.77
   LONGG     = -84.60
   ELEVG     = 256
   StartYear = 1960
   EndYear   = 1977

case ('W14840.DVF')
   WMOnumber = '72636'
   WBANumber = '14840'
   Station   = 'Muskegon'
   State     = 'MI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '98'
   LATG      = 43.17
   LONGG     = -86.25
   ELEVG     = 190
   StartYear = 1961
   EndYear   = 1990

case ('MET96.MET')
   WMOnumber = '72636'
   WBANumber = '14840'
   Station   = 'Muskegon'
   State     = 'MI'
   Note      = 'Traverse City (WBAN 14850) is a better choice for MLRA 96.'
   LRR       = 'L'
   MLRA      = '96'
   LATG      = 43.17
   LONGG     = -86.25
   ELEVG     = 190
   StartYear = 1948
   EndYear   = 1983

case ('W14847.DVF')
   WMOnumber = '72734'
   WBANumber = '14847'
   Station   = 'Sault Ste. Marie'
   State     = 'MI'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '94B'
   LATG      = 46.47
   LONGG     = -84.35
   ELEVG     = 219
   StartYear = 1961
   EndYear   = 1990

case ('MET94B.MET')
   WMOnumber = '72734'
   WBANumber = '14847'
   Station   = 'Sault Ste. Marie'
   State     = 'MI'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '94B'
   LATG      = 46.47
   LONGG     = -84.35
   ELEVG     = 219
   StartYear = 1960
   EndYear   = 1983

case ('W14850.DVF')
   WMOnumber = ' '
   WBANumber = '14850'
   Station   = 'Traverse City'
   State     = 'MI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '96'
   LATG      = 44.73
   LONGG     = -85.58
   ELEVG     = 188
   StartYear = 1961
   EndYear   = 1990

case ('W14913.DVF')
   WMOnumber = '72745'
   WBANumber = '14913'
   Station   = 'Duluth'
   State     = 'MN'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '93'
   LATG      = 46.83
   LONGG     = -92.18
   ELEVG     = 435
   StartYear = 1961
   EndYear   = 1990

case ('MET92.MET','MET93.MET')
   WMOnumber = '72745'
   WBANumber = '14913'
   Station   = 'Duluth'
   State     = 'MN'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '92,93'
   LATG      = 46.83
   LONGG     = -92.18
   ELEVG     = 435
   StartYear = 1948
   EndYear   = 1983

case ('W14918.DVF')
   WMOnumber = '72747'
   WBANumber = '14918'
   Station   = 'International Falls'
   State     = 'MN'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '88'
   LATG      = 48.57
   LONGG     = -93.38
   ELEVG     = 359
   StartYear = 1961
   EndYear   = 1990

case ('MET88.MET')
   WMOnumber = '72747'
   WBANumber = '14918'
   Station   = 'International Falls'
   State     = 'MN'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '88'
   LATG      = 48.57
   LONGG     = -93.38
   ELEVG     = 359
   StartYear = 1946
   EndYear   = 1983

case ('W14922.DVF')
   WMOnumber = '72658'
   WBANumber = '14922'
   Station   = 'Minneapolis/St. Paul'
   State     = 'MN'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '91'
   LATG      = 44.88
   LONGG     = -93.22
   ELEVG     = 254
   StartYear = 1961
   EndYear   = 1990

case ('MET90.MET','MET91.MET')
   WMOnumber = '72658'
   WBANumber = '14922'
   Station   = 'Minneapolis/St. Paul'
   State     = 'MN'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '90,91'
   LATG      = 44.88
   LONGG     = -93.22
   ELEVG     = 254
   StartYear = 1948
   EndYear   = 1983

case ('W14925.DVF')
   WMOnumber = '72644'
   WBANumber = '14925'
   Station   = 'Rochester'
   State     = 'MN'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '104'
   LATG      = 43.92
   LONGG     = -92.50
   ELEVG     = 395
   StartYear = 1961
   EndYear   = 1990

case ('MET105.MET')
   WMOnumber = '72644'
   WBANumber = '14925'
   Station   = 'Rochester'
   State     = 'MN'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '104'
   LATG      = 43.92
   LONGG     = -92.50
   ELEVG     = 395
   StartYear = 1948
   EndYear   = 1983

case ('W14926.DVF')
   WMOnumber = '72655'
   WBANumber = '14926'
   Station   = 'Saint Cloud'
   State     = 'MN'
   Note      = ' '
   LRR       = 'K'
   MLRA      = '91'
   LATG      = 45.55
   LONGG     = -94.07
   ELEVG     = 313
   StartYear = 1961
   EndYear   = 1990

case ('W03945.DVF')
   WMOnumber = '72445'
   WBANumber = '03945'
   Station   = 'Columbia'
   State     = 'MO'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '113'
   LATG      = 38.82
   LONGG     = -92.22
   ELEVG     = 271
   StartYear = 1970
   EndYear   = 1990

case ('W03947.DVF')
   WMOnumber = '72446'
   WBANumber = '03947'
   Station   = 'Kansas City'
   State     = 'MO'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '107'
   LATG      = 39.32
   LONGG     = -94.72
   ELEVG     = 297
   StartYear = 1973
   EndYear   = 1990

case ('W13995.DVF')
   WMOnumber = '72440'
   WBANumber = '13995'
   Station   = 'Springfield'
   State     = 'MO'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '116B'
   LATG      = 37.23
   LONGG     = -93.38
   ELEVG     = 386
   StartYear = 1961
   EndYear   = 1990

case ('MET116A.MET','MET116B')
   WMOnumber = '72440'
   WBANumber = '13995'
   Station   = 'Springfield'
   State     = 'MO'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '116A,116B'
   LATG      = 37.23
   LONGG     = -93.38
   ELEVG     = 386
   StartYear = 1947
   EndYear   = 1983

case ('W13994.DVF')
   WMOnumber = '72434'
   WBANumber = '13994'
   Station   = 'St. Louis'
   State     = 'MO'
   Note      = "Lambert Int'l."
   LRR       = 'M'
   MLRA      = '115'
   LATG      = 38.75
   LONGG     = -90.37
   ELEVG     = 173
   StartYear = 1961
   EndYear   = 1990

case ('MET113.MET','MET115.MET')
   WMOnumber = '72434 '
   WBANumber = '13994'
   Station   = 'St. Louis'
   State     = 'MO'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '113,115'
   LATG      = 38.75
   LONGG     = -90.37
   ELEVG     = 173
   StartYear = 1950
   EndYear   = 1983

case ('W03940.DVF')
   WMOnumber = '72235'
   WBANumber = '03940'
   Station   = 'Jackson'
   State     = 'MS'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '134'
   LATG      = 32.32
   LONGG     = -90.08
   ELEVG     = 101
   StartYear = 1961
   EndYear   = 1990

case ('MET131.MET','MET134.MET')
   WMOnumber = '72235'
   WBANumber = '03940'
   Station   = 'Jackson'
   State     = 'MS'
   Note      = ' '
   LRR       = 'O'
   MLRA      = '131,134'
   LATG      = 32.32
   LONGG     = -90.08
   ELEVG     = 101
   StartYear = 1964
   EndYear   = 1983

case ('W13865.DVF')
   WMOnumber = '72234'
   WBANumber = '13865'
   Station   = 'Meridian'
   State     = 'MS'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '133A'
   LATG      = 32.33
   LONGG     = -88.75
   ELEVG     = 88
   StartYear = 1961
   EndYear   = 1990

case ('W24033.DVF')
   WMOnumber = '72677'
   WBANumber = '24033'
   Station   = 'Billings'
   State     = 'MT'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '58A'
   LATG      = 45.80
   LONGG     = -108.53
   ELEVG     = 1087
   StartYear = 1961
   EndYear   = 1990

case ('MET58A.MET')
   WMOnumber = '72677'
   WBANumber = '24033'
   Station   = 'Billings'
   State     = 'MT'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '58A'
   LATG      = 45.80
   LONGG     = -108.53
   ELEVG     = 1087
   StartYear = 1948
   EndYear   = 1983

case ('W24137.DVF')
   WMOnumber = ' '
   WBANumber = '24137'
   Station   = 'Cut Bank'
   State     = 'MT'
   Note      = 'Cut Bank Municipal AP'
   LRR       = 'E'
   MLRA      = '46'
   LATG      = 48.60
   LONGG     = -112.37
   ELEVG     = 1170
   StartYear = 1961
   EndYear   = 1988

case ('W94008.DVF')
   WMOnumber = '72768'
   WBANumber = '94008'
   Station   = 'Glasgow'
   State     = 'MT'
   Note      = ' '
   LRR       = 'F'
   MLRA      = '52'
   LATG      = 48.22
   LONGG     = -106.62
   ELEVG     = 696
   StartYear = 1961
   EndYear   = 1990

case ('W24143.DVF')
   WMOnumber = '72775'
   WBANumber = '24143'
   Station   = 'Great Falls'
   State     = 'MT'
   Note      = ' '
   LRR       = 'F'
   MLRA      = '52'
   LATG      = 47.48
   LONGG     = -111.37
   ELEVG     = 1116
   StartYear = 1961
   EndYear   = 1990

case ('MET46.MET','MET52.MET')
   WMOnumber = '72775'
   WBANumber = '24143'
   Station   = 'Great Falls'
   State     = 'MT'
   Note      = ' '
   LRR       = 'E,F'
   MLRA      = 'E-46,F-52'
   LATG      = 47.48
   LONGG     = -111.37
   ELEVG     = 1116
   StartYear = 1948
   EndYear   = 1983

case ('W24144.DVF')
   WMOnumber = '72772'
   WBANumber = '24144'
   Station   = 'Helena'
   State     = 'MT'
   Note      = ' '
   LRR       = 'E'
   MLRA      = '44'
   LATG      = 46.60
   LONGG     = -112.00
   ELEVG     = 1167
   StartYear = 1961
   EndYear   = 1990

case ('MET43.MET')
   WMOnumber = '72772'
   WBANumber = '24144'
   Station   = 'Helena'
   State     = 'MT'
   Note      = ' '
   LRR       = 'E'
   MLRA      = '44'
   LATG      = 46.60
   LONGG     = -112.00
   ELEVG     = 1167
   StartYear = 1948
   EndYear   = 1983

case ('W24146.DVF')
   WMOnumber = '72779'
   WBANumber = '24146'
   Station   = 'Kalispell'
   State     = 'MT'
   Note      = ' '
   LRR       = 'E'
   MLRA      = '44'
   LATG      = 48.30
   LONGG     = -114.27
   ELEVG     = 904
   StartYear = 1961
   EndYear   = 1990

case ('W24036.DVF')
   WMOnumber = ' '
   WBANumber = '24036'
   Station   = 'Lewistown'
   State     = 'MT'
   Note      = 'Lewistown Municipal AP'
   LRR       = 'E'
   MLRA      = '46'
   LATG      = 47.05
   LONGG     = -109.45
   ELEVG     = 1263
   StartYear = 1961
   EndYear   = 1990

case ('W24037.DVF')
   WMOnumber = '74230'
   WBANumber = '24037'
   Station   = 'Miles City'
   State     = 'MT'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '58A'
   LATG      = 46.43
   LONGG     = -105.87
   ELEVG     = 801
   StartYear = 1961
   EndYear   = 1989

case ('W24153.DVF')
   WMOnumber = '72773'
   WBANumber = '24153'
   Station   = 'Missoula'
   State     = 'MT'
   Note      = ' '
   LRR       = 'E'
   MLRA      = '44'
   LATG      = 46.93
   LONGG     = -114.10
   ELEVG     = 974
   StartYear = 1961
   EndYear   = 1990

case ('MET44.MET')
   WMOnumber = '72773'
   WBANumber = '24153'
   Station   = 'Missoula'
   State     = 'MT'
   Note      = ' '
   LRR       = 'E'
   MLRA      = '44'
   LATG      = 46.93
   LONGG     = -114.10
   ELEVG     = 974
   StartYear = 1948
   EndYear   = 1983

case ('W03812.DVF')
   WMOnumber = '72315'
   WBANumber = '03812'
   Station   = 'Asheville'
   State     = 'NC'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '130'
   LATG      = 35.43
   LONGG     = -82.55
   ELEVG     = 652
   StartYear = 1965
   EndYear   = 1990

case ('W93729.DVF')
   WMOnumber = '72304'
   WBANumber = '93729'
   Station   = 'Cape Hatteras'
   State     = 'NC'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '153B'
   LATG      = 35.27
   LONGG     = -75.55
   ELEVG     = 2
   StartYear = 1961
   EndYear   = 1990

case ('W13881.DVF')
   WMOnumber = '72314'
   WBANumber = '13881'
   Station   = 'Charlotte'
   State     = 'NC'
   Note      = 'Charlotte Douglas AP'
   LRR       = 'P'
   MLRA      = '136'
   LATG      = 35.22
   LONGG     = -80.93
   ELEVG     = 220
   StartYear = 1961
   EndYear   = 1990

case ('W13723.DVF')
   WMOnumber = '72317'
   WBANumber = '13723'
   Station   = 'Greensboro'
   State     = 'NC'
   Note      = "Piedmont Triad Int'l."
   LRR       = 'P'
   MLRA      = '136'
   LATG      = 36.08
   LONGG     = -79.95
   ELEVG     = 273
   StartYear = 1961
   EndYear   = 1990

case ('W13722.DVF')
   WMOnumber = '72306'
   WBANumber = '13722'
   Station   = 'Raleigh/Durham'
   State     = 'NC'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '136'
   LATG      = 35.87
   LONGG     = -78.78
   ELEVG     = 127
   StartYear = 1961
   EndYear   = 1990

case ('W13748.DVF')
   WMOnumber = ' '
   WBANumber = '13748'
   Station   = 'Wilmington'
   State     = 'NC'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '153A'
   LATG      = 34.27
   LONGG     = -77.90
   ELEVG     = 9
   StartYear = 1961
   EndYear   = 1990

case ('W24011.DVF')
   WMOnumber = '72764'
   WBANumber = '24011'
   Station   = 'Bismarck'
   State     = 'ND'
   Note      = ' '
   LRR       = 'F'
   MLRA      = '53B'
   LATG      = 46.77
   LONGG     = -100.75
   ELEVG     = 502
   StartYear = 1961
   EndYear   = 1990

case ('MET53B.MET','MET54.MET','MET55A.MET','MET55B.MET')
   WMOnumber = '72764'
   WBANumber = '24011'
   Station   = 'Bismarck'
   State     = 'ND'
   Note      = ' '
   LRR       = 'F'
   MLRA      = '53B,54,55A,55B'
   LATG      = 46.77
   LONGG     = -100.75
   ELEVG     = 502
   StartYear = 1948
   EndYear   = 1983

case ('W14914.DVF')
   WMOnumber = '72753'
   WBANumber = '14914'
   Station   = 'Fargo'
   State     = 'ND'
   Note      = ' '
   LRR       = 'F'
   MLRA      = '56'
   LATG      = 46.90
   LONGG     = -96.80
   ELEVG     = 274
   StartYear = 1961
   EndYear   = 1990

case ('MET56.MET','MET57.MET')
   WMOnumber = '72753'
   WBANumber = '14914'
   Station   = 'Fargo'
   State     = 'ND'
   Note      = ' '
   LRR       = 'F,K'
   MLRA      = '56,57'
   LATG      = 46.90
   LONGG     = -96.80
   ELEVG     = 274
   StartYear = 1948
   EndYear   = 1983

case ('W24013.DVF')
   WMOnumber = ' '
   WBANumber = '24013'
   Station   = 'Minot'
   State     = 'ND'
   Note      = 'Minot FAA AP'
   LRR       = 'F'
   MLRA      = '55A'
   LATG      = 48.27
   LONGG     = -101.28
   ELEVG     = 523
   StartYear = 1961
   EndYear   = 1988

case ('MET53A.MET','MET58C.MET')
   WMOnumber = '72767'
   WBANumber = '94014'
   Station   = 'Williston'
   State     = 'ND'
   Note      = ' '
   LRR       = 'F,G'
   MLRA      = 'F-53A,G-58C'
   LATG      = 48.18
   LONGG     = -103.64
   ELEVG     = 604.1
   StartYear = 1962
   EndYear   = 1983

case ('W14935.DVF')
   WMOnumber = '72552'
   WBANumber = '14935'
   Station   = 'Grand Island'
   State     = 'NE'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '71'
   LATG      = 40.97
   LONGG     = -98.32
   ELEVG     = 561
   StartYear = 1961
   EndYear   = 1990

case ('MET71.MET','MET75.MET')
   WMOnumber = '72552'
   WBANumber = '14935'
   Station   = 'Grand Island'
   State     = 'NE'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '71,75'
   LATG      = 40.97
   LONGG     = -98.32
   ELEVG     = 561
   StartYear = 1948
   EndYear   = 1983

case ('W14941.DVF')
   WMOnumber = '72556'
   WBANumber = '14941'
   Station   = 'Norfolk'
   State     = 'NE'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '102B'
   LATG      = 41.98
   LONGG     = -97.43
   ELEVG     = 471
   StartYear = 1961
   EndYear   = 1990

case ('W24023.DVF')
   WMOnumber = '72562'
   WBANumber = '24023'
   Station   = 'North Platte'
   State     = 'NE'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '72'
   LATG      = 41.13
   LONGG     = -100.68
   ELEVG     = 846
   StartYear = 1961
   EndYear   = 1990

case ('W94918.DVF')
   WMOnumber = '72553'
   WBANumber = '94918' ! 14983 from 1888 - 1938
   Station   = 'Omaha N WSFO'
   State     = 'NE'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '107'
   LATG      = 41.37
   LONGG     = -96.02
   ELEVG     = 399
   StartYear = 1961
   EndYear   = 1990

case ('MET106.MET','MET107.MET')
   WMOnumber = '72550'
   WBANumber = '14942'
   Station   = 'Omaha Eppley AF'
   State     = 'NE'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '106,107'
   LATG      = 41.30
   LONGG     = -95.89
   ELEVG     = 299.9
   StartYear = 1948
   EndYear   = 1983

case ('W24028.DVF')
   WMOnumber = '72566'
   WBANumber = '24028'
   Station   = 'Scottsbluff'
   State     = 'NE'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '67'
   LATG      = 41.87
   LONGG     = -103.60
   ELEVG     = 1202
   StartYear = 1961
   EndYear   = 1990

case ('MET64.MET','MET65.MET')
   WMOnumber = '72566'
   WBANumber = '24028'
   Station   = 'Scottsbluff'
   State     = 'NE'
   Note      = 'Station is in MLRA 67.'
   LRR       = 'G'
   MLRA      = '64,65'
   LATG      = 41.87
   LONGG     = -103.60
   ELEVG     = 1202
   StartYear = 1952
   EndYear   = 1983

case ('W14745.DVF')
   WMOnumber = '72605'
   WBANumber = '14745'
   Station   = 'Concord'
   State     = 'NH'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '144A'
   LATG      = 43.20
   LONGG     = -71.50
   ELEVG     = 104
   StartYear = 1961
   EndYear   = 1990

case ('MET145.MET')
   WMOnumber = '72605'
   WBANumber = '14745'
   Station   = 'Concord'
   State     = 'NH'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '145'
   LATG      = 43.20
   LONGG     = -71.50
   ELEVG     = 104
   StartYear = 1948
   EndYear   = 1983

case ('W93730.DVF')
   WMOnumber = '72407'
   WBANumber = '93730'
   Station   = 'Atlantic City'
   State     = 'NJ'
   Note      = ' '
   LRR       = 'S'
   MLRA      = '149A'
   LATG      = 39.45
   LONGG     = -74.57
   ELEVG     = 20
   StartYear = 1961
   EndYear   = 1990

case ('W14734.DVF')
   WMOnumber = '72502'
   WBANumber = '14734'
   Station   = 'Newark'
   State     = 'NJ'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '144A'
   LATG      = 40.70
   LONGG     = -74.17
   ELEVG     = 2
   StartYear = 1961
   EndYear   = 1990

case ('W23050.DVF')
   WMOnumber = '72365'
   WBANumber = '23050'
   Station   = 'Albuquerque'
   State     = 'NM'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '42'
   LATG      = 35.05
   LONGG     = -106.62
   ELEVG     = 1619
   StartYear = 1961
   EndYear   = 1990

case ('MET36.MET','MET37.MET','MET70.MET')
   WMOnumber = '72365'
   WBANumber = '23050'
   Station   = 'Albuquerque'
   State     = 'NM'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '36,37,70'
   LATG      = 35.05
   LONGG     = -106.62
   ELEVG     = 1619
   StartYear = 1950
   EndYear   = 1983

case ('W23048.DVF')
   WMOnumber = ' '
   WBANumber = '23048'
   Station   = 'Tucumcari'
   State     = 'NM'
   Note      = 'Tucumcari FAA AP'
   LRR       = 'G'
   MLRA      = '70'
   LATG      = 35.18
   LONGG     = -103.60
   ELEVG     = 1231
   StartYear = 1963
   EndYear   = 1981

case ('W24121.DVF')
   WMOnumber = ' '
   WBANumber = '24121'
   Station   = 'Elko'
   State     = 'NV'
   Note      = 'Elko Municipal AP'
   LRR       = 'D'
   MLRA      = '25'
   LATG      = 40.83
   LONGG     = -115.78
   ELEVG     = 1539
   StartYear = 1961
   EndYear   = 1990

case ('MET25.MET')
   WMOnumber = ' '
   WBANumber = '24121'
   Station   = 'Elko'
   State     = 'NV'
   Note      = 'Elko Municipal AP'
   LRR       = 'D'
   MLRA      = '25'
   LATG      = 40.83
   LONGG     = -115.78
   ELEVG     = 1539
   StartYear = 1949
   EndYear   = 1983

case ('W23154.DVF')
   WMOnumber = '72486'
   WBANumber = '23154'
   Station   = 'Ely'
   State     = 'NV'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '28B'
   LATG      = 39.28
   LONGG     = -114.85
   ELEVG     = 1906
   StartYear = 1961
   EndYear   = 1990

case ('MET28B.MET','MET29.MET')
   WMOnumber = '72486'
   WBANumber = '23154'
   Station   = 'Ely'
   State     = 'NV'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '28B'
   LATG      = 39.28
   LONGG     = -114.85
   ELEVG     = 1906
   StartYear = 1948
   EndYear   = 1983

case ('W23169.DVF')
   WMOnumber = '72386'
   WBANumber = '23169'
   Station   = 'Las Vegas'
   State     = 'NV'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '30'
   LATG      = 36.08
   LONGG     = -115.17
   ELEVG     = 659
   StartYear = 1961
   EndYear   = 1990

case ('MET30.MET')
   WMOnumber = '72386'
   WBANumber = '23169'
   Station   = 'Las Vegas'
   State     = 'NV'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '30'
   LATG      = 36.08
   LONGG     = -115.17
   ELEVG     = 659
   StartYear = 1949
   EndYear   = 1973

case ('W23185.DVF')
   WMOnumber = '72488'
   WBANumber = '23185'
   Station   = 'Reno'
   State     = 'NV'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '26'
   LATG      = 39.50
   LONGG     = -119.78
   ELEVG     = 1342
   StartYear = 1961
   EndYear   = 1990

case ('MET21.MET','MET22.MET','MET26.MET','MET27.MET')
   WMOnumber = '72488'
   WBANumber = '23185'
   Station   = 'Reno'
   State     = 'NV'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '26'
   LATG      = 39.50
   LONGG     = -119.78
   ELEVG     = 1342
   StartYear = 1948
   EndYear   = 1983

case ('W23153.DVF')
   WMOnumber = ' '
   WBANumber = '23153'
   Station   = 'Tonopah'
   State     = 'NV'
   Note      = 'Tonopah AP'
   LRR       = 'D'
   MLRA      = '29'
   LATG      = 38.07
   LONGG     = -117.08
   ELEVG     = 1654
   StartYear = 1961
   EndYear   = 1990

case ('W24128.DVF')
   WMOnumber = '72583'
   WBANumber = '24128'
   Station   = 'Winnemucca'
   State     = 'NV'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '24'
   LATG      = 40.90
   LONGG     = -117.80
   ELEVG     = 1311
   StartYear = 1961
   EndYear   = 1990

case ('MET24.MET')
   WMOnumber = '72583'
   WBANumber = '24128'
   Station   = 'Winnemucca'
   State     = 'NV'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '24'
   LATG      = 40.90
   LONGG     = -117.80
   ELEVG     = 1311.
   StartYear = 1950
   EndYear   = 1983

case ('W14735.DVF')
   WMOnumber = '72518'
   WBANumber = '14735'
   Station   = 'Albany'
   State     = 'NY'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '144A'
   LATG      = 42.75
   LONGG     = -73.80
   ELEVG     = 84.
   StartYear = 1961
   EndYear   = 1990

case ('MET144B.MET')
   WMOnumber = '72515'
   WBANumber = '04725'
   Station   = 'Binghamton (not Albany)'
   State     = 'NY'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '144B'
   LATG      = 42.22
   LONGG     = -75.98
   ELEVG     = 488.
   StartYear = 1948
   EndYear   = 1983

case ('W04725.DVF')
   WMOnumber = '72515'
   WBANumber = '04725'
   Station   = 'Binghamton'
   State     = 'NY'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '140'
   LATG      = 42.22
   LONGG     = -75.98
   ELEVG     = 488
   StartYear = 1961
   EndYear   = 1990

case ('MET140.MET')
   WMOnumber = '72515'
   WBANumber = '04725'
   Station   = 'Binghamton'
   State     = 'NY'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '140'
   LATG      = 42.22
   LONGG     = -75.98
   ELEVG     = 488
   StartYear = 1948
   EndYear   = 1983

case ('W14733.DVF')
   WMOnumber = '72528'
   WBANumber = '14733'
   Station   = 'Buffalo'
   State     = 'NY'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '101'
   LATG      = 42.93
   LONGG     = -78.73
   ELEVG     = 215
   StartYear = 1961
   EndYear   = 1990

case ('W94725.DVF')
   WMOnumber = ' '
   WBANumber = '94725'
   Station   = 'Massena'
   State     = 'NY'
   Note      = 'Massena AP'
   LRR       = 'R'
   MLRA      = '142'
   LATG      = 44.93
   LONGG     = -74.85
   ELEVG     = 65
   StartYear = 1961
   EndYear   = 1990

case ('W94728.DVF')
   WMOnumber = '72503'
   WBANumber = '94728'
   Station   = 'NYC (Central Park/LGA)'
   State     = 'NY'
   Note      = 'LaGuardia Airport (LGA) is WBAN 14732; WMO I.D. 72503'
   LRR       = 'S'
   MLRA      = '149B'
   LATG      = 40.77
   LONGG     = -73.90
   ELEVG     = 3.0
   StartYear = 1961
   EndYear   = 1990

case ('MET149B.MET')
   WMOnumber = '72503'
   WBANumber = '14732'
   Station   = 'NYC (LaGuardia AP)'
   State     = 'NY'
   Note      = ' '
   LRR       = 'S'
   MLRA      = '149B'
   LATG      = 40.77
   LONGG     = -73.90
   ELEVG     = 3.0
   StartYear = 1948
   EndYear   = 1983

case ('W14768.DVF')
   WMOnumber = '72529'
   WBANumber = '14768'
   Station   = 'Rochester'
   State     = 'NY'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '101'
   LATG      = 43.13
   LONGG     = -77.67
   ELEVG     = 183
   StartYear = 1961
   EndYear   = 1990

case ('MET101.MET')
   WMOnumber = '72529'
   WBANumber = '14768'
   Station   = 'Rochester'
   State     = 'NY'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '101'
   LATG      = 43.13
   LONGG     = -77.67
   ELEVG     = 183
   StartYear = 1948
   EndYear   = 1983

case ('W14771.DVF')
   WMOnumber = '72519'
   WBANumber = '14771'
   Station   = 'Syracuse'
   State     = 'NY'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '101'
   LATG      = 43.12
   LONGG     = -76.12
   ELEVG     = 125
   StartYear = 1961
   EndYear   = 1990

case ('MET141.MET')
   WMOnumber = '72519'
   WBANumber = '14771'
   Station   = 'Syracuse'
   State     = 'NY'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '141'
   LATG      = 43.12
   LONGG     = -76.12
   ELEVG     = 125
   StartYear = 1947
   EndYear   = 1983

case ('W14895.DVF')
   WMOnumber = '72521'
   WBANumber = '14895'
   Station   = 'Akron/Canton'
   State     = 'OH'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '139'
   LATG      = 40.92
   LONGG     = -81.43
   ELEVG     = 368
   StartYear = 1961
   EndYear   = 1990

case ('MET139.MET')
   WMOnumber = '72521'
   WBANumber = '14895'
   Station   = 'Akron/Canton'
   State     = 'OH'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '139'
   LATG      = 40.92
   LONGG     = -81.43
   ELEVG     = 368
   StartYear = 1949
   EndYear   = 1983

case ('W14820.DVF')
   WMOnumber = '72524'
   WBANumber = '14820'
   Station   = 'Cleveland'
   State     = 'OH'
   Note      = "Hopkins Int'l."
   LRR       = 'L'
   MLRA      = '100'
   LATG      = 41.42
   LONGG     = -81.87
   ELEVG     = 235
   StartYear = 1961
   EndYear   = 1990

case ('W14821.DVF')
   WMOnumber = '72428'
   WBANumber = '14821'
   Station   = 'Columbus'
   State     = 'OH'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '111'
   LATG      = 40.00
   LONGG     = -82.88
   ELEVG     = 248
   StartYear = 1961
   EndYear   = 1990

case ('MET124.MET')
   WMOnumber = '72428'
   WBANumber = '14821'
   Station   = 'Columbus'
   State     = 'OH'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '124'
   LATG      = 40.00
   LONGG     = -82.88
   ELEVG     = 248
   StartYear = 1948
   EndYear   = 1968

case ('W93815.DVF')
   WMOnumber = '72429'
   WBANumber = '93815'
   Station   = 'Dayton'
   State     = 'OH'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '111'
   LATG      = 39.90
   LONGG     = -84.20
   ELEVG     = 303
   StartYear = 1961
   EndYear   = 1990

case ('W14891.DVF')
   WMOnumber = ' '
   WBANumber = '14891'
   Station   = 'Mansfield'
   State     = 'OH'
   Note      = 'Mansfield Lahm AP'
   LRR       = 'M'
   MLRA      = '111'
   LATG      = 40.82
   LONGG     = -82.52
   ELEVG     = 395
   StartYear = 1961
   EndYear   = 1990

case ('W94830.DVF')
   WMOnumber = '72536'
   WBANumber = '94830'
   Station   = 'Toledo'
   State     = 'OH'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '99'
   LATG      = 41.60
   LONGG     = -83.80
   ELEVG     = 204
   StartYear = 1961
   EndYear   = 1990

case ('W14852.DVF')
   WMOnumber = '72525'
   WBANumber = '14852'
   Station   = 'Youngstown'
   State     = 'OH'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '139'
   LATG      = 41.25
   LONGG     = -80.67
   ELEVG     = 360
   StartYear = 1961
   EndYear   = 1990

case ('W13967.DVF')
   WMOnumber = '72353'
   WBANumber = '13967'
   Station   = 'Oklahoma City'
   State     = 'OK'
   Note      = 'Will Rogers '
   LRR       = 'H'
   MLRA      = '80A'
   LATG      = 35.40
   LONGG     = -97.60
   ELEVG     = 392
   StartYear = 1961
   EndYear   = 1990

case ('MET84A.MET')
   WMOnumber = '72353'
   WBANumber = '13967'
   Station   = 'Oklahoma City'
   State     = 'OK'
   Note      = 'Station (Will Rogers) is in MLRA 80A.'
   LRR       = 'H'
   MLRA      = '84A'
   LATG      = 35.40
   LONGG     = -97.60
   ELEVG     = 392
   StartYear = 1948
   EndYear   = 1983

case ('W13968.DVF')
   WMOnumber = '72356'
   WBANumber = '13968'
   Station   = 'Tulsa'
   State     = 'OK'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '112'
   LATG      = 36.20
   LONGG     = -95.90
   ELEVG     = 198
   StartYear = 1961
   EndYear   = 1990

case ('MET112.MET')
   WMOnumber = '72356'
   WBANumber = '13968'
   Station   = 'Tulsa'
   State     = 'OK'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '112'
   LATG      = 36.20
   LONGG     = -95.90
   ELEVG     = 198
   StartYear = 1948
   EndYear   = 1983

case ('W94224.DVF')
   WMOnumber = '72791'
   WBANumber = '94224'
   Station   = 'Astoria'
   State     = 'OR'
   Note      = ' '
   LRR       = 'A'
   MLRA      = '1'
   LATG      = 46.15
   LONGG     = -123.88
   ELEVG     = 2
   StartYear = 1961
   EndYear   = 1990

case ('MET1.MET')
   WMOnumber = '72791'
   WBANumber = '94224'
   Station   = 'Astoria'
   State     = 'OR'
   Note      = ' '
   LRR       = 'A'
   MLRA      = '1'
   LATG      = 46.15
   LONGG     = -123.88
   ELEVG     = 2
   StartYear = 1953
   EndYear   = 1983

case ('W24221.DVF')
   WMOnumber = '72693'
   WBANumber = '24221'
   Station   = 'Eugene'
   State     = 'OR'
   Note      = ' '
   LRR       = 'A'
   MLRA      = '2'
   LATG      = 44.12
   LONGG     = -123.22
   ELEVG     = 109
   StartYear = 1961
   EndYear   = 1990

case ('W24225.DVF')
   WMOnumber = '72597'
   WBANumber = '24225'
   Station   = 'Medford'
   State     = 'OR'
   Note      = ' '
   LRR       = 'A'
   MLRA      = '5'
   LATG      = 42.38
   LONGG     = -122.88
   ELEVG     = 396
   StartYear = 1961
   EndYear   = 1990

case ('MET5.MET')
   WMOnumber = '72597'
   WBANumber = '24225'
   Station   = 'Medford'
   State     = 'OR'
   Note      = ' '
   LRR       = 'A'
   MLRA      = '5'
   LATG      = 42.38
   LONGG     = -122.88
   ELEVG     = 396
   StartYear = 1948
   EndYear   = 1983

case ('W24284.DVF')
   WMOnumber = ' '
   WBANumber = '24284'
   Station   = 'North Bend'
   State     = 'OR'
   Note      = 'North Bend Municipal AP'
   LRR       = 'A'
   MLRA      = '1'
   LATG      = 43.42
   LONGG     = -124.25
   ELEVG     = 2
   StartYear = 1961
   EndYear   = 1990

case ('W24155.DVF')
   WMOnumber = '72688'
   WBANumber = '24155'
   Station   = 'Pendleton'
   State     = 'OR'
   Note      = ' '
   LRR       = 'B'
   MLRA      = '8'
   LATG      = 45.68
   LONGG     = -118.85
   ELEVG     = 452
   StartYear = 1961
   EndYear   = 1990

case ('MET10.MET','MET11.MET','MET12.MET','MET23.MET')
   WMOnumber = '72688'
   WBANumber = '24155'
   Station   = 'Pendleton'
   State     = 'OR'
   Note      = ' '
   LRR       = 'B'
   MLRA      = '8'
   LATG      = 45.68
   LONGG     = -118.85
   ELEVG     = 452
   StartYear = 1948
   EndYear   = 1983

case ('W24229.DVF')
   WMOnumber = '72698'
   WBANumber = '24229'
   Station   = 'Portland'
   State     = 'OR'
   Note      = ' '
   LRR       = 'A'
   MLRA      = '2'
   LATG      = 45.60
   LONGG     = -122.60
   ELEVG     = 6
   StartYear = 1961
   EndYear   = 1990

case ('W24230.DVF')
   WMOnumber = ' '
   WBANumber = '24230'
   Station   = 'Redmond/Bend'
   State     = 'OR'
   Note      = 'Roberts Field'
   LRR       = 'B'
   MLRA      = '6'
   LATG      = 44.27
   LONGG     = -121.15
   ELEVG     = 933
   StartYear = 1961
   EndYear   = 1990

case ('W24232.DVF')
   WMOnumber = '72694'
   WBANumber = '24232'
   Station   = 'Salem'
   State     = 'OR'
   Note      = 'McNary Field'
   LRR       = 'A'
   MLRA      = '2'
   LATG      = 44.92
   LONGG     = -123.00
   ELEVG     = 60
   StartYear = 1961
   EndYear   = 1990

case ('MET2.MET','MET3.MET')
   WMOnumber = '72694'
   WBANumber = '24232'
   Station   = 'Salem'
   State     = 'OR'
   Note      = 'McNary Field'
   LRR       = 'A'
   MLRA      = '2,3'
   LATG      = 44.92
   LONGG     = -123.00
   ELEVG     = 60
   StartYear = 1948
   EndYear   = 1983

case ('W14737.DVF')
   WMOnumber = '72517'
   WBANumber = '14737'
   Station   = 'Allentown'
   State     = 'PA'
   Note      = ' '
   LRR       = 'S'
   MLRA      = '147'
   LATG      = 40.65
   LONGG     = -75.43
   ELEVG     = 118
   StartYear = 1961
   EndYear   = 1990

case ('MET147.MET','MET148.MET')
   WMOnumber = '72517'
   WBANumber = '14737'
   Station   = 'Allentown'
   State     = 'PA'
   Note      = ' '
   LRR       = 'S'
   MLRA      = '147,148'
   LATG      = 40.65
   LONGG     = -75.43
   ELEVG     = 118
   StartYear = 1948
   EndYear   = 1983

case ('W04751.DVF')
   WMOnumber = ' '
   WBANumber = '04751'
   Station   = 'Bradford'
   State     = 'PA'
   Note      = 'Bradford Regional AP'
   LRR       = 'N'
   MLRA      = '127'
   LATG      = 41.80
   LONGG     = -78.63
   ELEVG     = 646
   StartYear = 1961
   EndYear   = 1990

case ('W14860.DVF')
   WMOnumber = '72526'
   WBANumber = '14860'
   Station   = 'Erie'
   State     = 'PA'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '100'
   LATG      = 42.08
   LONGG     = -80.18
   ELEVG     = 222
   StartYear = 1961
   EndYear   = 1990

case ('MET100.MET')
   WMOnumber = '72526'
   WBANumber = '14860'
   Station   = 'Erie'
   State     = 'PA'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '100'
   LATG      = 42.08
   LONGG     = -80.18
   ELEVG     = 222
   StartYear = 1961
   EndYear   = 1983

case ('W14751.DVF')
   WMOnumber = ' '
   WBANumber = '14751'
   Station   = 'Harrisburg'
   State     = 'PA'
   Note      = 'Harrisburg Capital City AP'
   LRR       = 'S'
   MLRA      = '147'
   LATG      = 40.22
   LONGG     = -76.85
   ELEVG     = 104
   StartYear = 1961
   EndYear   = 1990

case ('W13739.DVF')
   WMOnumber = '72408'
   WBANumber = '13739'
   Station   = 'Philadelphia'
   State     = 'PA'
   Note      = ' '
   LRR       = 'S'
   MLRA      = '149A'
   LATG      = 39.88
   LONGG     = -75.25
   ELEVG     = 2
   StartYear = 1961
   EndYear   = 1990

case ('MET149A.MET')
   WMOnumber = '72408'
   WBANumber = '13739'
   Station   = 'Philadelphia'
   State     = 'PA'
   Note      = ' '
   LRR       = 'S'
   MLRA      = '149A'
   LATG      = 39.88
   LONGG     = -75.25
   ELEVG     = 2
   StartYear = 1948
   EndYear   = 1983

case ('W94823.DVF')
   WMOnumber = '72520'
   WBANumber = '94823'
   Station   = 'Pittsburgh'
   State     = 'PA'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '126'
   LATG      = 40.50
   LONGG     = -80.22
   ELEVG     = 347
   StartYear = 1961
   EndYear   = 1990

case ('MET126.MET','MET127.MET')
   WMOnumber = '72520'
   WBANumber = '94823'
   Station   = 'Pittsburgh'
   State     = 'PA'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '126,127'
   LATG      = 40.50
   LONGG     = -80.22
   ELEVG     = 347
   StartYear = 1948
   EndYear   = 1983

case ('W14777.DVF')
   WMOnumber = '72513'
   WBANumber = '14777'
   Station   = 'Wilkes-Barre/Scranton/Avoca'
   State     = 'PA'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '140'
   LATG      = 41.33
   LONGG     = -75.73
   ELEVG     = 284
   StartYear = 1961
   EndYear   = 1990

case ('W14778.DVF')
   WMOnumber = '72514'
   WBANumber = '14778'
   Station   = 'Williamsport-Lycoming'
   State     = 'PA'
   Note      = ' '
   LRR       = 'S'
   MLRA      = '147'
   LATG      = 41.25
   LONGG     = -76.92
   ELEVG     = 158
   StartYear = 1961
   EndYear   = 1990

case ('W41415.DVF')
   WMOnumber = '91217'
   WBANumber = '41415'
   Station   = 'Guam'
   State     = 'PI'
   Note      = 'Guam Taguac WSMO'
   LRR       = '-'
   MLRA      = '199'
   LATG      = 13.55
   LONGG     = 144.83
   ELEVG     = 111
   StartYear = 1961
   EndYear   = 1990

case ('W11641.DVF')
   WMOnumber = ' '
   WBANumber = '11641'
   Station   = 'San Juan'
   State     = 'PR'
   Note      = 'San Juan Isla Verde'
   LRR       = 'Z'
   MLRA      = '272'
   LATG      = 18.43
   LONGG     = -66.00
   ELEVG     = 19
   StartYear = 1961
   EndYear   = 1990

case ('W14765.DVF')
   WMOnumber = '72507'
   WBANumber = '14765'
   Station   = 'Providence'
   State     = 'RI'
   Note      = 'T.F. Green State Airport'
   LRR       = 'R'
   MLRA      = '144A'
   LATG      = 41.73
   LONGG     = -71.43
   ELEVG     = 16
   StartYear = 1961
   EndYear   = 1990

case ('W13880.DVF')
   WMOnumber = '72208'
   WBANumber = '13880'
   Station   = 'Charleston'
   State     = 'SC'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '153A'
   LATG      = 32.90
   LONGG     = -80.03
   ELEVG     = 12
   StartYear = 1961
   EndYear   = 1990

case ('W13883.DVF')
   WMOnumber = '72310'
   WBANumber = '13883'
   Station   = 'Columbia'
   State     = 'SC'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '137'
   LATG      = 33.95
   LONGG     = -81.12
   ELEVG     = 65
   StartYear = 1961
   EndYear   = 1990

case ('W03870.DVF')
   WMOnumber = '72312'
   WBANumber = '03870'
   Station   = 'Greenville/Spartanburg'
   State     = 'SC'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '136'
   LATG      = 34.90
   LONGG     = -82.22
   ELEVG     = 292
   StartYear = 1963
   EndYear   = 1990

case ('W14936.DVF')
   WMOnumber = '72654'
   WBANumber = '14936'
   Station   = 'Huron'
   State     = 'SD'
   Note      = ' '
   LRR       = 'F'
   MLRA      = '55C'
   LATG      = 44.38
   LONGG     = -98.22
   ELEVG     = 390
   StartYear = 1961
   EndYear   = 1990

case ('W24025.DVF')
   WMOnumber = ' '
   WBANumber = '24025'
   Station   = 'Pierre'
   State     = 'SD'
   Note      = 'Pierre Municipal AP'
   LRR       = 'F'
   MLRA      = '53C'
   LATG      = 44.38
   LONGG     = -100.28
   ELEVG     = 528
   StartYear = 1961
   EndYear   = 1990

case ('W24090.DVF')
   WMOnumber = '72662'
   WBANumber = '24090'
   Station   = 'Rapid City'
   State     = 'SD'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '60A'
   LATG      = 44.05
   LONGG     = -103.07
   ELEVG     = 964
   StartYear = 1961
   EndYear   = 1990

case ('W14944.DVF')
   WMOnumber = '72651'
   WBANumber = '14944'
   Station   = 'Sioux Falls'
   State     = 'SD'
   Note      = 'Foss Field'
   LRR       = 'M'
   MLRA      = '102B'
   LATG      = 43.57
   LONGG     = -96.73
   ELEVG     = 432
   StartYear = 1961
   EndYear   = 1990

case ('MET53C.MET','MET55C.MET','MET63A.MET','MET63B.MET',&
      &'MET66.MET','MET102A.MET','MET103.MET')
   WMOnumber = '72651'
   WBANumber = '14944'
   Station   = 'Sioux Falls'
   State     = 'SD'
   Note      = 'Foss Field'
   LRR       = 'G,F,M'
   MLRA      = '53C,55C,63A,63B,66,102A,103'
   LATG      = 43.57
   LONGG     = -96.73
   ELEVG     = 432
   StartYear = 1944
   EndYear   = 1983

case ('W13877.DVF')
   WMOnumber = ' '
   WBANumber = '13877'
   Station   = 'Bristol'
   State     = 'TN'
   Note      = 'Bristol Tri City AP'
   LRR       = 'N'
   MLRA      = '128'
   LATG      = 36.48
   LONGG     = -82.40
   ELEVG     = 465
   StartYear = 1961
   EndYear   = 1990

case ('MET128.MET','MET130.MET')
   WMOnumber = ' '
   WBANumber = '13877'
   Station   = 'Bristol'
   State     = 'TN'
   Note      = 'Bristol Tri City AP'
   LRR       = 'N'
   MLRA      = '128,130'
   LATG      = 36.48
   LONGG     = -82.40
   ELEVG     = 465
   StartYear = 1948
   EndYear   = 1983

case ('W13882.DVF')
   WMOnumber = '72324'
   WBANumber = '13882'
   Station   = 'Chattanooga'
   State     = 'TN'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '128'
   LATG      = 35.03
   LONGG     = -85.20
   ELEVG     = 211
   StartYear = 1961
   EndYear   = 1990

case ('W13891.DVF')
   WMOnumber = '72326'
   WBANumber = '13891'
   Station   = 'Knoxville'
   State     = 'TN'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '128'
   LATG      = 35.82
   LONGG     = -83.98
   ELEVG     = 268
   StartYear = 1961
   EndYear   = 1990

case ('W13893.DVF')
   WMOnumber = '72334'
   WBANumber = '13893'
   Station   = 'Memphis'
   State     = 'TN'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '134'
   LATG      = 35.05
   LONGG     = -90.00
   ELEVG     = 81
   StartYear = 1961
   EndYear   = 1990

case ('W13897.DVF')
   WMOnumber = '72327'
   WBANumber = '13897'
   Station   = 'Nashville'
   State     = 'TN'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '123'
   LATG      = 36.12
   LONGG     = -86.68
   ELEVG     = 180
   StartYear = 1961
   EndYear   = 1990

case ('MET122.MET','MET123.MET')
   WMOnumber = '72327'
   WBANumber = '13897'
   Station   = 'Nashville'
   State     = 'TN'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '122,123'
   LATG      = 36.12
   LONGG     = -86.68
   ELEVG     = 180
   StartYear = 1948
   EndYear   = 1983

case ('W13962.DVF')
   WMOnumber = '72266'
   WBANumber = '13962'
   Station   = 'Abilene'
   State     = 'TX'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '80B'
   LATG      = 32.42
   LONGG     = -99.68
   ELEVG     = 544
   StartYear = 1961
   EndYear   = 1990

case ('MET80B','MET81.MET')
   WMOnumber = '72266'
   WBANumber = '13962'
   Station   = 'Abilene'
   State     = 'TX'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '80B'
   LATG      = 32.42
   LONGG     = -99.68
   ELEVG     = 544
   StartYear = 1948
   EndYear   = 1983

case ('W23047.DVF')
   WMOnumber = '72363'
   WBANumber = '23047'
   Station   = 'Amarillo'
   State     = 'TX'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '77'
   LATG      = 35.23
   LONGG     = -101.70
   ELEVG     = 1093
   StartYear = 1961
   EndYear   = 1990

case ('W13958.DVF')
   WMOnumber = '72254'
   WBANumber = '13958'
   Station   = 'Austin'
   State     = 'TX'
   Note      = 'Mueller'
   LRR       = 'J'
   MLRA      = '86'
   LATG      = 30.28
   LONGG     = -97.70
   ELEVG     = 189
   StartYear = 1961
   EndYear   = 1990

case ('MET82.MET','MET86.MET','MET87.MET')
   WMOnumber = '72254'
   WBANumber = '13958'
   Station   = 'Austin'
   State     = 'TX'
   Note      = 'Mueller'
   LRR       = 'J'
   MLRA      = '82,86,87'
   LATG      = 30.28
   LONGG     = -97.70
   ELEVG     = 189
   StartYear = 1948
   EndYear   = 1983

case ('W12919.DVF')
   WMOnumber = '72250'
   WBANumber = '12919'
   Station   = 'Brownsville'
   State     = 'TX'
   Note      = ' '
   LRR       = 'I'
   MLRA      = '83D'
   LATG      = 25.90
   LONGG     = -97.43
   ELEVG     = 6
   StartYear = 1961
   EndYear   = 1990

case ('MET83D.MET')
   WMOnumber = '72250'
   WBANumber = '12919'
   Station   = 'Brownsville'
   State     = 'TX'
   Note      = ' '
   LRR       = 'I'
   MLRA      = '83D'
   LATG      = 25.90
   LONGG     = -97.43
   ELEVG     = 6
   StartYear = 1948
   EndYear   = 1983

case ('W12924.DVF')
   WMOnumber = '72251'
   WBANumber = '12924'
   Station   = 'Corpus Christi'
   State     = 'TX'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '150A'
   LATG      = 27.77
   LONGG     = -97.50
   ELEVG     = 12
   StartYear = 1961
   EndYear   = 1990

case ('MET83B.MET','MET83C.MET')
   WMOnumber = '72251'
   WBANumber = '12924'
   Station   = 'Corpus Christi'
   State     = 'TX'
   Note      = ' '
   LRR       = 'I'
   MLRA      = '83B,83C'
   LATG      = 27.77
   LONGG     = -97.50
   ELEVG     = 12
   StartYear = 1948
   EndYear   = 1983

case ('W23044.DVF')
   WMOnumber = '72270'
   WBANumber = '23044'
   Station   = 'El Paso'
   State     = 'TX'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '42'
   LATG      = 31.80
   LONGG     = -106.40
   ELEVG     = 1194
   StartYear = 1961
   EndYear   = 1990

case ('MET42.MET')
   WMOnumber = '72270'
   WBANumber = '23044'
   Station   = 'El Paso'
   State     = 'TX'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '42'
   LATG      = 31.80
   LONGG     = -106.40
   ELEVG     = 1194
   StartYear = 1948
   EndYear   = 1983

case ('W03927.DVF')
   WMOnumber = '72259' ! Fort Worth Greater S at Lat 32.83,Lon -97.05,elev 201
   WBANumber = '03927'
   Station   = 'Fort Worth'
   State     = 'TX'
   Note      = ' '
   LRR       = 'J'
   MLRA      = '86'
   LATG      = 32.90
   LONGG     = -97.03
   ELEVG     = 168
   StartYear = 1961
   EndYear   = 1990

case ('MET84B.MET')
   WMOnumber = '72259'
   WBANumber = '03927'
   Station   = 'Fort Worth'
   State     = 'TX'
   Note      = ' '
   LRR       = 'J'
   MLRA      = '84B'
   LATG      = 32.90
   LONGG     = -97.03
   ELEVG     = 168
   StartYear = 1948
   EndYear   = 1983

case ('MET84C.MET')
   WMOnumber = '72258'
   WBANumber = '13960'
   Station   = 'Dallas'
   State     = 'TX'
   Note      = 'Love Field '
   LRR       = 'J'
   MLRA      = '84B'
   LATG      = 32.85
   LONGG     = -96.85
   ELEVG     = 148.4
   StartYear = 1950
   EndYear   = 1983

case ('W12960.DVF')
   WMOnumber = '72243'
   WBANumber = '12960'
   Station   = 'Houston'
   State     = 'TX'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '150A'
   LATG      = 29.97
   LONGG     = -95.35
   ELEVG     = 29
   StartYear = 1970
   EndYear   = 1990

case ('MET152B')
   WMOnumber = ''
   WBANumber = '12945'
   Station   = 'Houston'
   State     = 'TX'
   Note      = 'COOP ID 414305; Houston WB City.'
   LRR       = 'T'
   MLRA      = '152B'
   LATG      = 29.93
   LONGG     = -95.37
   ELEVG     = 13.1
   StartYear = 1948    ! WBAN 12945 operated from 1941 (or 1909) to 1969
   EndYear   = 1983
   ! Apparently this file is a composite or mis-identified;
   ! although the PIC manual says this file is 1963-1983, the file actually
   ! contains entries for 1948-1983.

case ('W23042.DVF')
   WMOnumber = '72267'
   WBANumber = '23042'
   Station   = 'Lubbock'
   State     = 'TX'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '77'
   LATG      = 33.65
   LONGG     = -101.82
   ELEVG     = 992
   StartYear = 1961
   EndYear   = 1990

case ('MET77.MET')
   WMOnumber = '72267'
   WBANumber = '23042'
   Station   = 'Lubbock'
   State     = 'TX'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '77'
   LATG      = 33.65
   LONGG     = -101.82
   ELEVG     = 992
   StartYear = 1948
   EndYear   = 1983

case ('W93987.DVF')
   WMOnumber = ' '
   WBANumber = '93987'
   Station   = 'Lufkin'
   State     = 'TX'
   Note      = 'Lufkin Angelina Co'
   LRR       = 'P'
   MLRA      = '133B'
   LATG      = 31.23
   LONGG     = -94.75
   ELEVG     = 86
   StartYear = 1961
   EndYear   = 1990

case ('W23023.DVF')
   WMOnumber = '72265'
   WBANumber = '23023'
   Station   = 'Midland/Odessa'
   State     = 'TX'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '77'
   LATG      = 31.95
   LONGG     = -102.18
   ELEVG     = 872
   StartYear = 1961
   EndYear   = 1990

case ('W12917.DVF')
   WMOnumber = '72241'
   WBANumber = '12917'
   Station   = 'Port Arthur'
   State     = 'TX'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '150A'
   LATG      = 29.95
   LONGG     = -94.02
   ELEVG     = 5
   StartYear = 1961
   EndYear   = 1990

case ('W23034.DVF')
   WMOnumber = '72263'
   WBANumber = '23034'
   Station   = 'San Angelo'
   State     = 'TX'
   Note      = 'Mathis Field'
   LRR       = 'H'
   MLRA      = '78'
   LATG      = 31.37
   LONGG     = -100.50
   ELEVG     = 580
   StartYear = 1961
   EndYear   = 1990

case ('W12921.DVF')
   WMOnumber = '72253'
   WBANumber = '12921'
   Station   = 'San Antonio'
   State     = 'TX'
   Note      = ' '
   LRR       = 'J'
   MLRA      = '86'
   LATG      = 29.53
   LONGG     = -98.47
   ELEVG     = 240
   StartYear = 1961
   EndYear   = 1990

case ('MET83A.MET')
   WMOnumber = '72253'
   WBANumber = '12921'
   Station   = 'San Antonio'
   State     = 'TX'
   Note      = ' '
   LRR       = 'I'
   MLRA      = '83A'
   LATG      = 29.53
   LONGG     = -98.47
   ELEVG     = 240
   StartYear = 1948
   EndYear   = 1983

case ('W12912.DVF')
   WMOnumber = '72255'
   WBANumber = '12912'
   Station   = 'Victoria'
   State     = 'TX'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '150A'
   LATG      = 28.85
   LONGG     = -96.92
   ELEVG     = 32
   StartYear = 1961
   EndYear   = 1990

case ('MET150A.MET','MET150B.MET')
   WMOnumber = '72255'
   WBANumber = '12912'
   Station   = 'Victoria'
   State     = 'TX'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '150A,150B'
   LATG      = 28.85
   LONGG     = -96.92
   ELEVG     = 32
   StartYear = 1962
   EndYear   = 1983

case ('W13959.DVF')
   WMOnumber = '72256'
   WBANumber = '13959'
   Station   = 'Waco'
   State     = 'TX'
   Note      = ' '
   LRR       = 'J'
   MLRA      = '86'
   LATG      = 31.62
   LONGG     = -97.22
   ELEVG     = 152
   StartYear = 1961
   EndYear   = 1990

case ('MET85.MET')
   WMOnumber = '72256'
   WBANumber = '13959'
   Station   = 'Waco'
   State     = 'TX'
   Note      = ' '
   LRR       = 'J'
   MLRA      = '86'
   LATG      = 31.62
   LONGG     = -97.22
   ELEVG     = 152
   StartYear = 1950
   EndYear   = 1983

case ('W13966.DVF')
   WMOnumber = '72351'
   WBANumber = '13966'
   Station   = 'Wichita Falls'
   State     = 'TX'
   Note      = ' '
   LRR       = 'H'
   MLRA      = '78'
   LATG      = 33.97
   LONGG     = -98.48
   ELEVG     = 303
   StartYear = 1961
   EndYear   = 1990

case ('MET78.MET','MET80A')
   WMOnumber = '72351'
   WBANumber = '13966'
   Station   = 'Wichita Falls'
   State     = 'TX'
   Note      = 'Station is in MLRA 78; good for Texas part of 80A.'
   LRR       = 'H'
   MLRA      = '78,80A'
   LATG      = 33.97
   LONGG     = -98.48
   ELEVG     = 303
   StartYear = 1948
   EndYear   = 1983

case ('W93129.DVF')
   WMOnumber = ' '
   WBANumber = '93129'
   Station   = 'Cedar City'
   State     = 'UT'
   Note      = 'Cedar City Municipal AP'
   LRR       = 'D'
   MLRA      = '28A'
   LATG      = 37.70
   LONGG     = 113.10
   ELEVG     = 1710
   StartYear = 1961
   EndYear   = 1990

case ('W24127.DVF')
   WMOnumber = '72572'
   WBANumber = '24127'
   Station   = 'Salt Lake City'
   State     = 'UT'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '28A'
   LATG      = 40.78
   LONGG     = -111.95
   ELEVG     = 1286
   StartYear = 1961
   EndYear   = 1990

case ('MET28A.MET','MET47.MET')
   WMOnumber = '72572'
   WBANumber = '24127'
   Station   = 'Salt Lake City'
   State     = 'UT'
   Note      = ' '
   LRR       = 'D'
   MLRA      = '28A,47'
   LATG      = 40.78
   LONGG     = -111.95
   ELEVG     = 1286
   StartYear = 1948
   EndYear   = 1983

case ('W13733.DVF')
   WMOnumber = '72410'
   WBANumber = '13733'
   Station   = 'Lynchburg'
   State     = 'VA'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '136'
   LATG      = 37.33
   LONGG     = -79.20
   ELEVG     = 281
   StartYear = 1961
   EndYear   = 1990

case ('W13737.DVF')
   WMOnumber = '72308'
   WBANumber = '13737'
   Station   = 'Norfolk'
   State     = 'VA'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '153B'
   LATG      = 36.90
   LONGG     = -76.20
   ELEVG     = 7
   StartYear = 1961
   EndYear   = 1990

case ('MET153B.MET')
   WMOnumber = '72308'
   WBANumber = '13737'
   Station   = 'Norfolk'
   State     = 'VA'
   Note      = ' '
   LRR       = 'T'
   MLRA      = '153B'
   LATG      = 36.90
   LONGG     = -76.20
   ELEVG     = 7
   StartYear = 1949
   EndYear   = 1983

case ('W13740.DVF')
   WMOnumber = '72401'
   WBANumber = '13740'
   Station   = 'Richmond'
   State     = 'VA'
   Note      = ' '
   LRR       = 'P'
   MLRA      = '133A'
   LATG      = 37.50
   LONGG     = -77.33
   ELEVG     = 50
   StartYear = 1961
   EndYear   = 1990

case ('W13741.DVF')
   WMOnumber = '72411'
   WBANumber = '13741'
   Station   = 'Roanoke'
   State     = 'VA'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '130'
   LATG      = 37.32
   LONGG     = -79.97
   ELEVG     = 350
   StartYear = 1961
   EndYear   = 1990

case ('W93738.DVF')
   WMOnumber = '72403'
   WBANumber = '93738'
   Station   = "Washington DC Dulles Int'l. AP"
   State     = 'VA'
   Note      = 'Located in Sterling, Virginia'
   LRR       = 'S'
   MLRA      = '148'
   LATG      = 38.95
   LONGG     = -77.45
   ELEVG     = 88
   StartYear = 1961
   EndYear   = 1990

case ('W14742.DVF')
   WMOnumber = '72617'
   WBANumber = '14742'
   Station   = 'Burlington'
   State     = 'VT'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '142'
   LATG      = 44.47
   LONGG     = -73.15
   ELEVG     = 101
   StartYear = 1961
   EndYear   = 1990

case ('MET142.MET','MET143.MET')
   WMOnumber = '72617'
   WBANumber = '14742'
   Station   = 'Burlington'
   State     = 'VT'
   Note      = ' '
   LRR       = 'R'
   MLRA      = '142,143'
   LATG      = 44.47
   LONGG     = -73.15
   ELEVG     = 101
   StartYear = 1948
   EndYear   = 1983

case ('W24227.DVF')
   WMOnumber = '72792'
   WBANumber = '24227'
   Station   = 'Olympia'
   State     = 'WA'
   Note      = ' '
   LRR       = 'A'
   MLRA      = '2'
   LATG      = 46.97
   LONGG     = -122.90
   ELEVG     = 59
   StartYear = 1961
   EndYear   = 1990

case ('W94240.DVF')
   WMOnumber = '72797'
   WBANumber = '94240'
   Station   = 'Quillayute'
   State     = 'WA'
   Note      = ' '
   LRR       = 'A'
   MLRA      = '1'
   LATG      = 47.95
   LONGG     = -124.55
   ELEVG     = 55
   StartYear = 1967
   EndYear   = 1990

case ('W24233.DVF')
   WMOnumber = '72793'
   WBANumber = '24233'
   Station   = 'Seattle/Tacoma AP'
   State     = 'WA'
   Note      = ' '
   LRR       = 'A'
   MLRA      = '2'
   LATG      = 47.45
   LONGG     = -122.30
   ELEVG     = 122
   StartYear = 1961
   EndYear   = 1990

case ('W24157.DVF')
   WMOnumber = '72785'
   WBANumber = '24157'
   Station   = 'Spokane'
   State     = 'WA'
   Note      = ' '
   LRR       = 'B'
   MLRA      = '9'
   LATG      = 47.63
   LONGG     = -117.53
   ELEVG     = 718
   StartYear = 1961
   EndYear   = 1990

case ('MET9.MET')
   WMOnumber = '72785'
   WBANumber = '24157'
   Station   = 'Spokane'
   State     = 'WA'
   Note      = ' '
   LRR       = 'B'
   MLRA      = '9'
   LATG      = 47.63
   LONGG     = -117.53
   ELEVG     = 718
   StartYear = 1948
   EndYear   = 1972

case ('W24243.DVF')
   WMOnumber = '72781'
   WBANumber = '24243'
   Station   = 'Yakima'
   State     = 'WA'
   Note      = ' '
   LRR       = 'B'
   MLRA      = '7'
   LATG      = 46.57
   LONGG     = -120.53
   ELEVG     = 324
   StartYear = 1961
   EndYear   = 1990

case ('MET6.MET','MET7.MET','MET8.MET')
   WMOnumber = '72781'
   WBANumber = '24243'
   Station   = 'Yakima'
   State     = 'WA'
   Note      = ' '
   LRR       = 'B'
   MLRA      = '6,7,8'
   LATG      = 46.57
   LONGG     = -120.53
   ELEVG     = 324
   StartYear = 1948
   EndYear   = 1983

case ('W14991.DVF')
   WMOnumber = ' '
   WBANumber = '14991'
   Station   = 'Eau Claire'
   State     = 'WI'
   Note      = 'Eau Claire County AP'
   LRR       = 'K'
   MLRA      = '90'
   LATG      = 44.87
   LONGG     = -91.48
   ELEVG     = 271
   StartYear = 1961
   EndYear   = 1990

case ('W14898.DVF')
   WMOnumber = '72645'
   WBANumber = '14898'
   Station   = 'Green Bay'
   State     = 'WI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '95A'
   LATG      = 44.48
   LONGG     = -88.13
   ELEVG     = 214
   StartYear = 1961
   EndYear   = 1990

case ('MET95A.MET')
   WMOnumber = '72645'
   WBANumber = '14898'
   Station   = 'Green Bay'
   State     = 'WI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '95A'
   LATG      = 44.48
   LONGG     = -88.13
   ELEVG     = 214
   StartYear = 1950
   EndYear   = 1983

case ('W14920.DVF')
   WMOnumber = '72643'
   WBANumber = '14920'
   Station   = 'La Crosse'
   State     = 'WI'
   Note      = ' '
   LRR       = 'M'
   MLRA      = '105'
   LATG      = 43.87
   LONGG     = -91.25
   ELEVG     = 207
   StartYear = 1961
   EndYear   = 1990

case ('W14837.DVF')
   WMOnumber = '72641'
   WBANumber = '14837'
   Station   = 'Madison'
   State     = 'WI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '95B'
   LATG      = 43.13
   LONGG     = -89.33
   ELEVG     = 262
   StartYear = 1961
   EndYear   = 1990

case ('MET95B.MET')
   WMOnumber = '72641'
   WBANumber = '14837'
   Station   = 'Madison'
   State     = 'WI'
   Note      = ' '
   LRR       = 'L'
   MLRA      = '95B'
   LATG      = 43.13
   LONGG     = -89.33
   ELEVG     = 262
   StartYear = 1948
   EndYear   = 1983

case ('W14839.DVF')
   WMOnumber = '72640'
   WBANumber = '14839'
   Station   = 'Milwaukee'
   State     = 'WI'
   Note      = "Mitchell Int'l. Airport"
   LRR       = 'M'
   MLRA      = '110'
   LATG      = 42.95
   LONGG     = -87.90
   ELEVG     = 205
   StartYear = 1961
   EndYear   = 1990

case ('W13866.DVF')
   WMOnumber = '72414'
   WBANumber = '13866'
   Station   = 'Charleston'
   State     = 'WV'
   Note      = 'Charleston Yeager AP'
   LRR       = 'N'
   MLRA      = '126'
   LATG      = 38.37
   LONGG     = -81.60
   ELEVG     = 310
   StartYear = 1961
   EndYear   = 1990

case ('W13729.DVF')
   WMOnumber = '72417'
   WBANumber = '13729'
   Station   = 'Elkins'
   State     = 'WV'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '127'
   LATG      = 38.88
   LONGG     = -79.85
   ELEVG     = 594
   StartYear = 1961
   EndYear   = 1990

case ('W03860.DVF')
   WMOnumber = '72425'
   WBANumber = '03860'
   Station   = 'Huntington'
   State     = 'WV'
   Note      = ' '
   LRR       = 'N'
   MLRA      = '125'
   LATG      = 38.37
   LONGG     = -82.55
   ELEVG     = 252
   StartYear = 1961
   EndYear   = 1990

case ('W24089.DVF')
   WMOnumber = '72569'
   WBANumber = '24089'
   Station   = 'Casper'
   State     = 'WY'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '58B'
   LATG      = 42.92
   LONGG     = -106.47
   ELEVG     = 1627
   StartYear = 1961
   EndYear   = 1990

case ('W24018.DVF')
   WMOnumber = '72564'
   WBANumber = '24018'
   Station   = 'Cheyenne'
   State     = 'WY'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '67'
   LATG      = 41.15
   LONGG     = -104.82
   ELEVG     = 1867
   StartYear = 1961
   EndYear   = 1990

case ('MET49.MET')
   WMOnumber = '72564'
   WBANumber = '24018'
   Station   = 'Cheyenne'
   State     = 'WY'
   Note      = 'Station is in MLRA 67'
   LRR       = 'G'
   MLRA      = '49'
   LATG      = 41.15
   LONGG     = -104.82
   ELEVG     = 1867
   StartYear = 1948
   EndYear   = 1983

case ('W24021.DVF')
   WMOnumber = '72576'
   WBANumber = '24021'
   Station   = 'Lander'
   State     = 'WY'
   Note      = ' '
   LRR       = 'E'
   MLRA      = '46'
   LATG      = 42.82
   LONGG     = -108.73
   ELEVG     = 1694
   StartYear = 1961
   EndYear   = 1990

case ('MET10A.MET','MET11A.MET','MET11B.MET','MET13.MET','MET32.MET',&
      &'MET33.MET')
   WMOnumber = '72576'
   WBANumber = '24021'
   Station   = 'Lander'
   State     = 'WY'
   Note      = ' '
   LRR       = 'E'
   MLRA      = '46'
   LATG      = 42.82
   LONGG     = -108.73
   ELEVG     = 1694
   StartYear = 1950
   EndYear   = 1982

case ('W24027.DVF')
   WMOnumber = ' '
   WBANumber = '24027'
   Station   = 'Rock Springs'
   State     = 'WY'
   Note      = 'Rock Springs AP'
   LRR       = 'D'
   MLRA      = '34'
   LATG      = 41.60
   LONGG     = -109.07
   ELEVG     = 2055
   StartYear = 1961
   EndYear   = 1990

case ('W24029.DVF')
   WMOnumber = '72666'
   WBANumber = '24029'
   Station   = 'Sheridan'
   State     = 'WY'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '58B'
   LATG      = 44.77
   LONGG     = -106.97
   ELEVG     = 1208
   StartYear = 1961
   EndYear   = 1990

case ('MET58B.MET','MET58D.MET,','MET60A.MET','MET60B.MET','MET61.MET',&
      &'MET62.MET')
   WMOnumber = '72666'
   WBANumber = '24029'
   Station   = 'Sheridan'
   State     = 'WY'
   Note      = ' '
   LRR       = 'G'
   MLRA      = '58B,58D,60A,60B,61,62'
   LATG      = 44.77
   LONGG     = -106.97
   ELEVG     = 1208
   StartYear = 1948
   EndYear   = 1983

case ('CAZ6.MET','CBZ6.MET','CCZ6.MET','CDZ6.MET','CEZ6.MET','CFZ6.MET')
   WBANumber = ' '
   WMOnumber = '07249'
   Station   = 'Orleans'
   State     = 'France'
   Note      = 'Precipitation data includes irrigation additions.'
   LRR       = ' '
   MLRA      = ' '
   LATG      = 47.98
   LONGG     = 1.75
   ELEVG     = 125
   StartYear = 1901
   EndYear   = 1966

case ('CZZ6.MET')
   WBANumber = ' '
   WMOnumber = '07249'
   Station   = 'Orleans/Bricy'
   State     = 'France'
   Note      = ' '
   LRR       = ' '
   MLRA      = ' '
   LATG      = 47.98
   LONGG     = 1.75
   ELEVG     = 125
   StartYear = 1901
   EndYear   = 1966

case ('HZZ6.MET')
   WBANumber = ' '
   WMOnumber = '10147'
   Station   = 'Hamburg/Fuhlsbuttel'
   State     = 'Germany'
   Note      = ' '
   LRR       = ' '
   MLRA      = ' '
   LATG      = 53.38
   LONGG     = 10.05
   ELEVG     = 16
   StartYear = 1901
   EndYear   = 1966

case ('JZZ6.MET')
   WBANumber = ' '
   WMOnumber = '02963'
   Station   = 'Jokioinen'
   State     = 'Finland'
   Note      = ' '
   LRR       = ' '
   MLRA      = ' '
   LATG      = 60.82
   LONGG     = 23.5
   ELEVG     = 103
   StartYear = 1901
   EndYear   = 1966

case ('KZZ6.MET')
   WBANumber = ' '
   WMOnumber = 'Unkn.'
   Station   = 'Munich West'
   State     = 'Germany'
   Note      = 'Station elevation approximate '
   LRR       = ' '
   MLRA      = ' '
   LATG      = 48.10
   LONGG     = 11.30
   ELEVG     = 500.0
   StartYear = 1901
   EndYear   = 1966

case ('NZZ6.MET')
   WBANumber = ' '
   WMOnumber = 'Unkn.'
   Station   = 'Exeter (MidDevon)'
   State     = 'United Kingdom'
   Note      = 'Precip scaled to change annual average from 741 to 1038 mm'
   LRR       = ' '
   MLRA      = ' '
   LATG      = 50.8
   LONGG     = -3.8
   ELEVG     = 30
   StartYear = 1901
   EndYear   = 1966
   ! Exeter airport is WMO 03839 at 50.44/-3.25, elev 30m.

case ('OZZ6.MET')
   WBANumber = ' '
   WMOnumber = '08546'
   Station   = 'Porto'
   State     = 'Portugal'
   Note      = 'Precip scaled to change annual average from 1402 to 1150 mm.'
   LRR       = ' '
   MLRA      = ' '
   LATG      = 41.08
   LONGG     = -8.36
   ELEVG     = 100
   StartYear = 1901
   EndYear   = 1966

case ('PAZ6.MET','PBZ6.MET','PCZ6.MET','PDZ6.MET','PEZ6.MET','PFZ6.MET')
   WBANumber = ' '
   WMOnumber = '16084'
   Station   = 'Piacenza'
   State     = 'Italy'
   Note      = 'Precipitation data includes irrigation additions.'
   LRR       = ' '
   MLRA      = ' '
   LATG      = 44.92
   LONGG     = 9.73
   ELEVG     = 138
   StartYear = 1901
   EndYear   = 1966

case ('PZZ6.MET')
   WBANumber = ' '
   WMOnumber = '16084'
   Station   = 'Piacenza'
   State     = 'Italy'
   Note      = ' '
   LRR       = ' '
   MLRA      = ' '
   LATG      = 44.92
   LONGG     = 9.73
   ELEVG     = 138
   StartYear = 1901
   EndYear   = 1966

case ('SAZ6.MET','SBZ6.MET','SCZ6.MET','SDZ6.MET','SEZ6.MET','SFZ6.MET')
   WBANumber = ' '
   WMOnumber = '08391'
   Station   = 'Sevilla/San Pablo'
   State     = 'Spain'
   Note      = 'Precipitation data includes irrigation additions.'
   LRR       = ' '
   MLRA      = ' '
   LATG      = 37.25
   LONGG     = -5.54
   ELEVG     = 31
   StartYear = 1901
   EndYear   = 1966

case ('SZZ6.MET')
   WBANumber = ' '
   WMOnumber = '08391'
   Station   = 'Sevilla/San Pablo'
   State     = 'Spain'
   Note      = ' '
   LRR       = ' '
   MLRA      = ' '
   LATG      = 37.25
   LONGG     = -5.54
   ELEVG     = 31
   StartYear = 1901
   EndYear   = 1966

case ('TAZ6.MET','TBZ6.MET','TCZ6.MET','TDZ6.MET','TEZ6.MET','TFZ6.MET')
   WBANumber = ' '
   WMOnumber = 'Unkn.'
   Station   = 'Thiva (Thebes)'
   State     = 'Greece'
   Note      = 'Precipitation data includes irrigation additions.'
   LRR       = ' '
   MLRA      = ' '
   LATG      = 38.32
   LONGG     = 23.32
   ELEVG     = 10    ! W.A.G.
   StartYear = 1901
   EndYear   = 1966

case ('TZZ6.MET')
   WBANumber = ' '
   WMOnumber = 'Unkn.'
   Station   = 'Thiva (Thebes)'
   State     = 'Greece'
   Note      = 'Precip scaled to change annual average from 721 to 500 mm.'
   LRR       = ' '
   MLRA      = ' '
   LATG      = 38.32
   LONGG     = 23.32
   ELEVG     = 10    ! W.A.G.
   StartYear = 1901
   EndYear   = 1966

end select StationData

end subroutine LoadStationData

end module StationData
