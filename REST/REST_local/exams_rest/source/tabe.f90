subroutine TABE(NYR)
! Created 19 December 1983 (L.A. Burns)
! Revised 08-Aug-1988 (LAB) -- title revision
! Revisions 10/22/88--run-time implementation of machine dependencies
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
Implicit None
integer :: NYR, K
! Set up page header for report on temporal simulation
write (RPTLUN,5000) VERSN,MODEG,trim(ECONAM)
do K = 1, KCHEM
   write (RPTLUN,fmt='(A)') ' Chemical:  '//trim(CHEMNA(K))
end do
write (RPTLUN,5020) ! dashed line
write (RPTLUN,fmt='(A/A,I0,A)')&
   ' Table 19.  Summary time-trace of spatially averaged, volume-',&
   '   weighted monthly mean chemical concentrations during ',NYR,'.'
write (RPTLUN,5020) ! dashed line
write (RPTLUN,fmt='(A,4(/A))')&
   '   Month   Average Chemical Concentrations     Total Chemical Mass',&
   '   -----   -------------------------------     -------------------',&
   '          Water Column      Benthic Sediments  Water Col  Benthic',&
   '      -------------------- ------------------- --------- ---------',&
   '      Free-mg/L Sorb-mg/kg Pore-mg/L Sed-mg/kg  Total kg  Total kg'
write (RPTLUN,5020) ! dashed line
return
5000 format ('1Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode ',I0/' Ecosystem: ',A)
5020 format (1X,77('-'))  ! dashed line
end Subroutine TABE
