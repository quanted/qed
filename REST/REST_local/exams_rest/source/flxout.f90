subroutine FLXOUT(Y)
! FLXOUT analyzes and reports the steady-state fate of the chemical. The
! information reported for each process includes the mass flux (kg/time)
! attributable to the process, the percentage of load consumed in the process,
! and a projected half-life that would result from each process acting in
! isolation. The processes are also summed by category (chemical, biological,
! transport), and a total system half-life is estimated from the total flux in
! order to specify a time-frame for the integration routines.
! Created August 1979 by L.A. Burns.
! Revised 27-DEC-85 (LAB)
! Revisions 10/22/88--run-time implementation of machine dependencies
use Floating_Point_Comparisons ! Revision 09-Feb-1999
use Implementation_Control
use Global_Variables
use Local_Working_Space
use Internal_Parameters
use Rates_and_Sums
Implicit None
real (kind (0D0)) :: Y(KOUNT,KCHEM)
! Local variables for this subroutine
real :: BIO, CHE, GNDOUT, HAFLS, HAFLT, HAFLW, PERCET, SUM_lives, TIME1,&
   TIME2, SOCACU, SOCBIO(2), SOCCHE, SOCDP, SOCHYD, SOCOUT, SOCOX,&
   SOCPHO, SOCSOX, SOCVOL, TOTBIO, SOCRED, TOTLOS, VOL, TOTLOD
real :: AUTOLD, ALLOLD, SURWAT, TEMP, HAFTMP(KCHEM)
integer :: J, K, K2
character(len=2) :: KOUT
! KOUT is character representation of chemical number.
real, dimension(4) :: TLOCAL = (/1.0,24.0,730.5,8766.0/)
character(len=6), dimension(4) :: NAMTIM = &
      (/' hours','  days','months',' years'/)
HAFTMP = 0.0
Chemicals: do K2 = 1, KCHEM
   Reporting: if (RPTFIL) then
   write (KOUT,fmt='(I2)') K2 ! Load character representation of K2
   if (KOUT(1:1) == ' ') KOUT(1:1) = '0'
   write (RPTLUN,5010) VERSN,MODEG,trim(ECONAM) ! Write page header
   write (RPTLUN,5020) trim(CHEMNA(K2))
   write (RPTLUN,5030) ! dashed line
   write (RPTLUN,fmt='(A)') ' Table 18.'//KOUT//&
      '. Analysis of steady-state fate of organic chemical.'
   write (RPTLUN,5030) ! dashed line
   write (RPTLUN,fmt='(A)')& ! headers for mass flux table
      '  Steady-state Values        Mass Flux    % of Load   Half-Life*'
   ! Analysis of mass fluxes at steady-state
   ! Calculate mass export rates from system at steady-state
   ! (factor of 1.0E-06 converts mg/hr to kg/hr):
   end if Reporting
   SOCOUT = 0.0
   GNDOUT = 0.0
   SURWAT = 0.0
   do J = 1, KOUNT
      TEMP = 1.0E-06*Y(J,K2)*EXPOKL(J,K2)
      SOCOUT = SOCOUT+TEMP
      if (TYPEG(J) == 'B'.and.TYPEG(J-1) == 'B') then
         GNDOUT = GNDOUT+TEMP
      else
         SURWAT = SURWAT+TEMP
      endif
   end do
   ! Compute volatilization and transformations of chemical, accumulate total
   ! mass fluxes for ecosystem. Initialize mass fluxes: all as kg/hr
   SOCVOL = 0.0      ! Volatilization, kg/hr
   SOCCHE = 0.0      ! Chemical transformation, kg/hr
   SOCHYD = 0.0      ! Hydrolysis
   SOCOX = 0.0       ! Oxidation
   SOCDP = 0.0       ! Direct photolysis
   SOCSOX = 0.0      ! Singlet oxygen photooxidation
   SOCBIO(1) = 0.0   ! Biolysis in water column
   SOCBIO(2) = 0.0   ! Biolysis in bottom sediments
   SOCRED = 0.0      ! Reductive transformations
   ! Compute process rates for segments in numerical order
   do J = 1, KOUNT
      ! 1. Volatilization: only from epilimnion - mg/L/hr
      VOL = VOLKL(J,K2)*Y(J,K2)
      SOCVOL = SOCVOL+1.0E-06*VOL*WATVOL(J) ! kg/hr total volatilization
      ! 2. Hydrolysis: 3 limb (acid, base, neutral) process
      CHE = HYDRKL(J,K2)*Y(J,K2)
      SOCCHE = SOCCHE+CHE*WATVOL(J)          ! mg/hr
      SOCHYD = SOCHYD+1.0E-06*CHE*WATVOL(J)  ! kg/hr
      CHE = OXIDKL(J,K2)*Y(J,K2) ! 3. Oxidation: (mg/L/hr)
      SOCCHE = SOCCHE+CHE*WATVOL(J)          ! mg/hr
      SOCOX = SOCOX+1.0E-06*CHE*WATVOL(J)    ! kg/hr
      CHE = PHOTKL(J,K2)*Y(J,K2) ! 4. Direct photolysis
      SOCCHE = SOCCHE+CHE*WATVOL(J)          ! mg/hr
      SOCDP = SOCDP+1.0E-06*CHE*WATVOL(J)    ! kg/hr
      CHE = S1O2KL(J,K2)*Y(J,K2) ! 5. Singlet oxygen photooxidation
      SOCCHE = SOCCHE+CHE*WATVOL(J)          ! mg/hr
      SOCSOX = SOCSOX+1.E-06*CHE*WATVOL(J)   ! kg/hr
      CHE = REDKL(J,K2)*Y(J,K2) ! 6. Reductive transformations
      SOCCHE = SOCCHE+CHE*WATVOL(J)
      SOCRED = SOCRED+1.0E-06*CHE*WATVOL(J)
      ! 7. Microbial transformation: dependent on aqueous
      ! concentration and population levels of bacteria.
      if (TYPEG(J) /= 'B') then ! Water column
         BIO = Y(J,K2)*BIOLKL(J,K2)
         SOCBIO(1) = SOCBIO(1)+1.0E-06*BIO*WATVOL(J)
         ! SOCBIO converted from mg/L/hr to kg/hr
      else ! Bottom sediments
         BIO = Y(J,K2)*BIOLKL(J,K2)
         SOCBIO(2) = SOCBIO(2)+1.E-06*BIO*WATVOL(J)
      endif
   end do ! End of transformation loop
   SOCCHE = SOCCHE*1.0E-06 ! Convert mg/hr to kg/hr
   ! Compute total flux and residual accumulation rate
   TOTLOS = SOCOUT+SOCVOL+SOCBIO(1)+SOCBIO(2)+SOCCHE
   SOCACU = abs((TRANLD(K2)+SYSLDL(K2))-TOTLOS)
   ! Compute total system-level half-life in hours
   ! Allow for entry of some compounds with zeros
   HAFLT = 168.00 ! Set nominal half-life at 7 days
   ! Then, if the compound is active, compute the actual halflife
   if (TOTLOS .NotEqual. 0.0) HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/TOTLOS
   HAFTMP(K2) = HAFLT
   ! Run decay kinetic simulation for 2 half-lives
   TENDL = 2.0D+00*HAFLT
   ! Determine appropriate temporal unit for reporting results
   if (TENDL .LessThanOrEqual. 288.0) then
      KDTIME = 1                   ! Time less than 12 days: report in hours
   elseif (TENDL .LessThanOrEqual. 8766.0) then
                                   ! Time more than 12 days but < 1 yr, so
      KDTIME = 2                   ! report in days
   elseif (TENDL .LessTHanOrEqual. 105192.0) then
                                   ! More than one but less than 12 years, so
      KDTIME = 3                   ! report in months
   else                            ! More than 12 years: report in years
      KDTIME = 4
   endif
   TFACTR = TLOCAL(KDTIME) ! adjustment factor for report times
   Reports: if (RPTFIL) then
   ! Complete table heading based on time frame to be used
   if (RPTFIL) write (RPTLUN,5060) NAMTIM(KDTIME),NAMTIM(KDTIME)
   5060 format ('       by Process',13X,'Kg/',A5,18X,A6)
   if (RPTFIL) write (RPTLUN,5070)
   5070 format (1X,21('-'),7X,10('-'),3X,9('-'),3X,10('-'))
   ! Compute temporary values of chemical loadings
   TOTLOD = SYSLDL(K2)+TRANLD(K2)
   ALLOLD = SYSLDL(K2)
   AUTOLD = TRANLD(K2)
   ! If necessary, enter dummy value of TOTLOD (i.e., allow for
   ! entry of some chemicals with zero loads):
   if (TOTLOD .Equals. 0.0) TOTLOD = 1.0
   ! Convert mass fluxes and load to kg/(appropriate time unit):
   ! If working in hours, simply go on:
   if (KDTIME > 1) then ! Convert mass fluxes by time factor
      SOCHYD = SOCHYD*TFACTR
      SOCOX = SOCOX*TFACTR
      SOCDP = SOCDP*TFACTR
      SOCSOX = SOCSOX*TFACTR
      SOCBIO(1) = SOCBIO(1)*TFACTR
      SOCBIO(2) = SOCBIO(2)*TFACTR
      SOCRED = SOCRED*TFACTR
      SOCVOL = SOCVOL*TFACTR
      SOCOUT = SOCOUT*TFACTR
      SOCCHE = SOCCHE*TFACTR
      SOCACU = SOCACU*TFACTR
      GNDOUT = GNDOUT*TFACTR
      SURWAT = SURWAT*TFACTR
      TOTLOD = TOTLOD*TFACTR
      ALLOLD = ALLOLD*TFACTR
      AUTOLD = AUTOLD*TFACTR
   endif
   ! Write out process mass fluxes
   if (SOCHYD .Equals. 0.0) then ! Hydrolysis
      write (RPTLUN,5080)
   else
      PERCET = 100.*SOCHYD/TOTLOD
      HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCHYD
      write (RPTLUN,5080) SOCHYD,PERCET,HAFLT
   endif
   5080  format (' Hydrolysis',:,17X,1PG11.4,4X,0PF6.2,4X,1PG11.4)
   
   if (SOCRED .Equals. 0.0) then ! Reductive transformation
      write (RPTLUN,5090)
   else
      PERCET = 100.*SOCRED/TOTLOD
      HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCRED
      write (RPTLUN,5090) SOCRED,PERCET,HAFLT
   endif
   5090 format (' Reduction',:,18X,1PG11.4,4X,0PF6.2,4X,1PG11.4)
   
   if (SOCOX .Equals. 0.0) then ! Radical oxidation
      write (RPTLUN,5100)
   else
      PERCET = 100.*SOCOX/TOTLOD
      HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCOX
      write (RPTLUN,5100) SOCOX,PERCET,HAFLT
   endif
   5100 format (' Radical oxidation',:,10X,1PG11.4,4X,0PF6.2,4X,1PG11.4)
   
   SOCPHO = SOCDP ! Direct photolysis
   ! SOCPHO is available for summing all photochemical processes
   if (SOCPHO .Equals. 0.0) then
      write (RPTLUN,5110)
   else
      PERCET = 100.*SOCPHO/TOTLOD
      HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCPHO
      write (RPTLUN,5110) SOCPHO,PERCET,HAFLT
   endif
   5110 format (' Direct photolysis',:,10X,1PG11.4,4X,0PF6.2,4X,1PG11.4)

   if (SOCSOX .Equals. 0.0) then ! Singlet oxygen photooxidation
      write (RPTLUN,5120)
   else
      PERCET = 100.*SOCSOX/TOTLOD
      HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCSOX
      write (RPTLUN,5120) SOCSOX,PERCET,HAFLT
   endif
   5120 format (' Singlet oxygen oxidation',:,3X,1PG11.4,4X,0PF6.2,4X,1PG11.4)
   
   CHEMPC(K2) = 100.0*SOCCHE/TOTLOD ! Total chemical transformations

   if (SOCBIO(1) .Equals. 0.0) then! Microbial transformations in water column
      write (RPTLUN,5130)
   else
      PERCET = 100.*SOCBIO(1)/TOTLOD
      HAFLW = 0.69315*(Z(5,K2)+Z(6,K2))/SOCBIO(1)
      write (RPTLUN,5130) SOCBIO(1),PERCET,HAFLW
   endif
   5130 format (' Bacterioplankton',:,11X,1PG11.4,4X,0PF6.2,4X,1PG11.4)

   if (SOCBIO(2) .Equals. 0.0) then ! Bottom sediments
      write (RPTLUN,5140)
   else
      PERCET = 100.*SOCBIO(2)/TOTLOD
      HAFLS = 0.69315*(Z(5,K2)+Z(6,K2))/SOCBIO(2)
      write (RPTLUN,5140) SOCBIO(2),PERCET,HAFLS
   endif
   5140 format (' Benthic Bacteria',:,11X,1PG11.4,4X,0PF6.2,4X,1PG11.4)
   
   ! (Under the first-order assumptions used in this analysis,
   ! the derivatives can be summed and related to total mass.)
   TOTBIO = SOCBIO(1)+SOCBIO(2)    ! Total microbial transformation
   BIOPCT(K2) = 100.0*TOTBIO/TOTLOD

   EXPPCT(K2) = 100.0*SOCOUT/TOTLOD ! Water-borne export
   if (SURWAT .Equals. 0.0) then
      write (RPTLUN,5150)
   else
      PERCET = 100.*SURWAT/TOTLOD
      HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SURWAT
      write (RPTLUN,5150) SURWAT,PERCET,HAFLT
   endif
   5150 format&
      (' Surface Water-borne Export',:,1X,1PG11.4,4X,0PF6.2,4X,1PG11.4)
   if (GNDOUT .Equals. 0.0) then
      write (RPTLUN,5160)
   else ! Report groundwater export
      PERCET = 100.*GNDOUT/TOTLOD
      HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SURWAT
      write (RPTLUN,5160) GNDOUT,PERCET,HAFLT
   endif
   5160 format (' Seepage export',:,13X,1PG11.4,4X,0PF6.2,4X,1PG11.4)
   
   VOLPCT(K2) = 100.*SOCVOL/TOTLOD  ! Volatilization
   if (SOCVOL .Equals. 0.0) then
      write (RPTLUN,5170)
   else
      HAFLT = 0.69315*(Z(5,K2)+Z(6,K2))/SOCVOL
      write (RPTLUN,5170) SOCVOL,VOLPCT(K2),HAFLT
   endif
   5170 format (' Volatilization',13X,1PG11.4,4X,0PF6.2,4X,1PG11.4)
   write (RPTLUN,5030) ! dashed line

   ! Check closure on mass balance and report results
   TOTLOS = SOCOUT+SOCVOL+TOTBIO+SOCCHE ! Loss by all processes combined
   write (RPTLUN,fmt='(A,2(/A,1PG11.4))')&
      ' Chemical Mass Balance:',&
      '    Sum of fluxes =         ',TOTLOS,&
      '    Sum of loadings =       ',TOTLOD
   PERCET = 100.0*ALLOLD/TOTLOD
   write (RPTLUN,fmt='(A,16X,F6.1)')&
      '       Allochthonous load:',PERCET
   PERCET = 100.*AUTOLD/TOTLOD
   write (RPTLUN,fmt='(A,16X,F6.1)')&
      '       Autochthonous load:',PERCET
   PERCET = 100.*SOCACU/TOTLOD   ! Remaining accumulation rate
   write (RPTLUN,fmt='(A,1PG9.2,3X,0PF6.1)')&
      '    Residual Accumulation =   ', SOCACU, PERCET
   write (RPTLUN,5030) ! dashed line
   write (RPTLUN,fmt='(A)')&
   ' * Pseudo-first-order estimates based on flux/resident mass.'
   end if Reports
end do Chemicals ! End of loop on chemicals
! **************************************************************************
! The time constants of chemicals can be very different,
! thus take an average of the projected half-lives
SUM_lives = sum(HAFTMP)
HAFLT = SUM_lives/float(KCHEM)
! Run decay kinetic simulation for 2 half-lives:
TENDL = 2.0D+00*HAFLT
! Determine appropriate temporal unit for reporting results:
! 1. Time less than 12 days: report in hours
if (TENDL .LessThanOrEqual. 288.0) then; KDTIME = 1
! 2. Time more than 12 days but less than 1 year, report in days
elseif (TENDL .LessThanOrEqual. 8766.) then; KDTIME = 2
! 3. More than one year but less than 12 years, report in months
elseif (TENDL .LessThanOrEqual. 105192.) then; KDTIME = 3
! 4. More than 12 years: report in years
else ; KDTIME = 4
endif
TFACTR = TLOCAL(KDTIME) ! adjustment factor for report times
! Convert time frame to appropriate integers
TIME1 = TENDL/12./TFACTR
TIME2 = float(int(TIME1))
if ((TIME1-TIME2) .GreaterThanOrEqual. 0.5) TIME2 = TIME2+1.0
TINCRL = 0.0D+00
TINCRL = TFACTR*TIME2
! TINCR restricted to at least one hour:
if (TINCRL .LessThan. 1.0) TINCRL = 1.0D+00
TENDL = 0.0D+00
TENDL = TINCRL*12.0D+00
! Persistence time simulations begin from T (nominally)=zero:
T = 0.0D+00
! Transfer the time frame to global variables to enable  the
! CONTINUE command:
TCODEG = KDTIME
CINTG = TINCRL
TINITG = T
TENDG = TENDL
! For use in steady-state post-processor (SUMUP), now convert
! the autochthonous and allochthonous chemical loadings to
! match the time frame to be used in the persistence integrations
do K = 1, KCHEM
   SYSLDL(K) = SYSLDL(K)*TFACTR
   TRANLD(K) = TRANLD(K)*TFACTR
end do
return
5010 format ('1','Exposure Analysis Modeling System -- EXAMS Version ',&
     A,', Mode',I2/' Ecosystem: ',A)
5020 format (' Chemical:  ',A)
5030 format (1X,77('-')) ! dashed line
end Subroutine FLXOUT
