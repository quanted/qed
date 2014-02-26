subroutine ENDMON(Month)
! Created 07 December 1983 (L.A. Burns) by fission from DRIVER.
! Revised 25 April 1984 (LAB) -- command language
! Revisions 10/22/88--run-time implementation of machine dependencies
! Revisions 07/24/2001 -- using "ndays" to acquire days in current month
use Implementation_Control; use Global_Variables; use Local_Working_Space
use Internal_Parameters; Implicit None
! Local variables
real :: YTEMP, YTEMP2
integer :: I, J, K, Month
! Month is the number of the month (1-12) being processed
FLUXCT = FLUXCT+1.0
Z = 0.0
Chems: do K = 1, KCHEM
   Segments: do J = 1, KOUNT
      ! Calculate average total concentration:
      YTEMP = YSUM(J,K)/ndays(month)
      YTEMP2 = YTEMP*WATVOL(J)
      ! Estimate average flux (mg/hr) and add to running sums:
      YEXPO(K) = YEXPO(K)+EXPOKL(J,K)*YTEMP
      YHYDR(K) = YHYDR(K)+HYDRKL(J,K)*YTEMP2
      YRED(K) = YRED(K)+REDKL(J,K)*YTEMP2
      ! Separate water column and benthic segments:
      Water_column: if (TYPEG(J) /= 'B') then
         ! Estimated flux for processes confined to water column:
         YBIOW(K) = YBIOW(K)+BIOLKL(J,K)*YTEMP2
         YOXID(K) = YOXID(K)+OXIDKL(J,K)*YTEMP2
         YPHOT(K) = YPHOT(K)+PHOTKL(J,K)*YTEMP2
         YS1O2(K) = YS1O2(K)+S1O2KL(J,K)*YTEMP2
         YVOLK(K) = YVOLK(K)+VOLKL(J,K)*YTEMP2
         ! Water column--dissolved (true solution):
         Z(1,K) = Z(1,K)+VOLG(J)*YTEMP*ALPHA(29,J,K)
         ! Sorbed (mg/kg):
         Z(2,K) = Z(2,K)+VOLG(J)*ALPHA(30,J,K)*YTEMP/SEDCOL(J)
         ! Chemical mass in kilograms (1.0E-06 mg/kg):
         Z(5,K) = Z(5,K)+YTEMP2*1.0E-06
      else ! Benthic segments, as above:
         ! Estimate flux for processes confined to benthic segments:
         YBIOS(K) = YBIOS(K)+BIOLKL(J,K)*YTEMP2
         if (TYPEG(J-1) == 'B') YGWAT(K) = YGWAT(K)+EXPOKL(J,K)*YTEMP
         Z(3,K) = Z(3,K)+VOLG(J)*YTEMP*ALPHA(29,J,K) ! Dissolved
         Z(4,K) = Z(4,K)+VOLG(J)*ALPHA(30,J,K)*YTEMP/SEDCOL(J) ! Sorbed
         Z(6,K) = Z(6,K)+YTEMP2*1.0E-06 ! Mass
      end if Water_column
   end do Segments
   ! Compute average values:
   Z(1,K) = Z(1,K)/Total_Limnetic_Volume ! mg/l dissolved in the water column
   Z(2,K) = Z(2,K)/Total_Limnetic_Volume ! mg/kg sorbed in the water column
   Z(3,K) = Z(3,K)/Total_Benthic_Volume  ! mg/L dissolved in pore water
   Z(4,K) = Z(4,K)/Total_Benthic_Volume  ! mg/kg sorbed in benthic sediment
   ! Print line to runlog: concentrations at month's end --
   write (RPTLUN,fmt='(3X,A3,1PG9.2,3(1X,G9.2),2X,G9.2,1X,G9.2)')&
      NAMONG(NDAT),(Z(I,K),I=1,6)
end do Chems
! At month's end, increment chemical species summations:
Chemicals: do K = 1, KCHEM
   Compartments: do J = 1, KOUNT
      ! Sum of total concentrations (mg/L of aqueous phase):
      YTOT(1,J,K) = YTOT(1,J,K)+YSUM(J,K)
      ! Sum of total concentrations expressed as mg/kg of solids:
!      YTOT(2,J,K) = YTOT(2,J,K)+YSUM(J,K)*WATVOL(J)/SEDMSL(J)
      YTOT(2,J,K) = YTOT(2,J,K)+YSUM(J,K)/SEDCOL(J)
      ! Accumulate masses:
      YTOT(3,J,K) = YTOT(3,J,K)+YSUM(J,K)*WATVOL(J)*1.0E-06
      do I = 1, 29
        YSUMS(I,J,K) = YSUMS(I,J,K)+YSUM(J,K)*ALPHA(I,J,K)
      end do
      ! Weight sum of sorbed concentrations with sediment concentration:
      YSUMS(30,J,K) = YSUMS(30,J,K)+YSUM(J,K)*ALPHA(30,J,K)/SEDCOL(J)
      YSUMS(31,J,K) = YSUMS(31,J,K)+YSUM(J,K)*ALPHA(31,J,K)
      ! Weight sum of biosorbed concentrations with biomass:
      YSUMS(32,J,K) = YSUMS(32,J,K)+YSUM(J,K)*ALPHA(32,J,K)/BIOTOL(J)
   end do Compartments
end do Chemicals
return
end Subroutine ENDMON
