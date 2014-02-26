subroutine WeatherHeader(ALUN)
use Global_Variables, only: LATG, LONGG, ELEVG
use Local_Working_Space, only : State, Station, LRR, MLRA, StartYear, &
      EndYear, WBANumber, WMOnumber, FirstYear, LastYear, Note
! StartYear, EndYear are integers. The values herein reflect the 
!    PRZM met file documentation, which is not always accurate. The
!    values reported by Exams when a met file is read (FirstYear, LastYear)
!    are derived from analysis of the data file itself.
! State, LRR, MLRA are character(10)
! MLRA is character(64)
! Station is character(64)
! WBANumber is character(5)
! WMOnumber is character(5)
! FirstYear and LastYear establish the time span covered by the met file
! Note holds additional information about the met file where needed
! MLRA and Note are written even when blank to stabilize the output file format
implicit none
integer, intent(in) :: ALUN

write (ALUN, fmt='(A)') &
   '! Weather Station: '//trim(Station)//', '//trim(State)

write (ALUN, fmt='(A,F7.2,A,F7.2,A,F7.1,A)')&
   '!    at latitude ',LATG,', longitude ',&
   LONGG,', elevation ',ELEVG,' m'

write (ALUN, fmt='(A)', advance = 'NO') '!'

if (len_trim(WBANumber)>0) write (ALUN,fmt='(4X,A)',advance='NO') &
   'WBAN '//WBANumber

if (len_trim(WMOnumber)>0) write (ALUN,fmt='(4X,A)',advance='NO') &
   'WMO I.D. '//WMONumber

if (len_trim(LRR)>0) write (ALUN, fmt='(A)', advance='NO') &
   ' in Land Resource Region '//trim(LRR)//','

write (ALUN, fmt='(A)') ' ' ! to finish the line and force advance

write (ALUN,fmt='(A)') &
  & '!    Major Land Resource Area '//trim(MLRA)//'.'//'  Note: '//trim(Note)
!if (len_trim(MLRA)>0) write (ALUN, fmt='(A)') &
!   '!    Major Land Resource Area '//trim(MLRA)//'.'
!
!if (len_trim(Note)>0) write (ALUN,fmt='(A)') '!    Note: '//trim(Note)

write (ALUN, fmt='(A,I0,A,I0)')&
   '!    Meteorological data coverage: ',FirstYear,' -- ',LastYear
end subroutine WeatherHeader
