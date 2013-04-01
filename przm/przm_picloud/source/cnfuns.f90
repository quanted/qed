
Module m_CN_functions

   ! Given normal antecedent moisture conditions (AMC ii),
   ! compute Curve Numbers (CN) for dry conditions (AMC i) or
   ! wet conditions (AMC iii)
   !
   ! 0 <= CN_ii <= 100
   ! CN_ii == 100 => impervious or water surface
   ! CN_ii  < 100 => natural surfaces
   !
   ! References: 
   !  * Chow, V.T., Maidment, D.R., and Mays, L.W. 1988.
   !    Applied Hydrology. McGraw-Hill Book Co., New York, NY., Page 149.
   !  * SWRRB: a basin scale simulation model for soil and water.
   !    Arnold, J.G.; William, J.R.; Nicks, A.D.; Sammons, N.B.;
   !    Texas A&M University Press, College Station. 1990.
   !  * Soil Conservation Service. 1985. National Engineering
   !    Handbook Section 4: Hydrology. USDA.

   use m_readvars
   Implicit None
   Private
   Include 'PPARM.INC'
   include 'CHYDR.INC'
   Include 'CCROP.INC'
   
   ! Use_cn_beta - use the curve numbers from przm beta, as opposed
   ! 	to the Chow formulation of curve numbers

   Public :: cn_1_func, cn_3_func, Curve_Numbers_from_Beta
   Public :: Fill_CN_Array

Contains

   subroutine Fill_CN_Array ()
   
      	! generate curve numbers for antecedent conditions I and III
	! according to the "globally" selected formulation, flit_num
	! replacement for curve numbers environmentas used in przm 3.12.3 [19]
	! curve number code is called to fill the CN array. 
	! Fri Apr 14 14:03:47 EDT 2006 
	! * I'm on deadline right now, and do not have the time to
	!   program individual cn-1 and cn-3 function using the beta
	!   formulation, so I am just reproducing the environment in 
	!   which ch the cn arrays are filled.
   
   Integer :: K, I
   
   select case(flit_num)
   Case(cn_beta)
        DO I = 1, 3
           Call Curve_Numbers_from_Beta (I)
        End Do
	
   Case(cn_chow)
   	! generate curve numbers for antecedent conditions I and III
	! curve numbers using the chow formulation. 
	Do I = 1, NDC
           DO K = 1, 3
              CN(I,K,1) = cn_1_func(CN(I,K,2))
              CN(I,K,3) = cn_3_func(CN(I,K,2))
           End Do
        End Do
   
   Case Default
   	! flit_num contains an unrecognized option.
	! this is an internal error. 
   end select 
   end subroutine Fill_CN_Array

   
   Integer Elemental Function cn_1_func(CN_ii)

      ! Compute Curve Number 1 (CN1) for dry conditions (AMC i)
      Implicit None
      Integer, Intent(In) :: CN_ii

      cn_1_func = 4.2 * CN_ii / (10.0 - 0.058*CN_ii)

   End Function cn_1_func


   Integer Elemental Function cn_3_func(CN_ii)

      ! Compute Curve Number 3 (CN3) for wet conditions (AMC iii)
      Implicit None
      Integer, Intent(In) :: CN_ii

      cn_3_func = 23.0 * CN_ii / (10.0 + 0.13*CN_ii)

   End Function cn_3_func

   subroutine Curve_Numbers_from_Beta (I)
   
   ! code lifted from pzm beta.
   ! this subroutine computes curve numbers according to the przm-beta
   ! curve number formulation. 
   !
   Integer, Intent(In) :: I
   Integer :: k, j, JT10, JP1, JP1T10 
   Real, Dimension(10) :: &        
         rmult1 = (/ 0.40,0.45,0.50,0.55,0.62,0.67,0.73,0.79,0.87,1.00 /), &
         rmult3 = (/ 2.22,1.85,1.67,1.50,1.40,1.30,1.21,1.14,1.07,1.00 /)
   real :: FRAC	 
	 
   ! generate curve numbers for antecedent conditions I and III;
   ! code taken from subroutine przmrd, file rsinp2.for (przm beta)

        DO 30 K=1,3
          DO 20 J=1,9
            JT10=J*10
            JP1=J+1
            JP1T10=JP1*10
            IF (CN(I,K,2).GT.JT10 .AND. CN(I,K,2).LE.JP1T10) THEN
              FRAC=(CN(I,K,2)-JT10)/10.
              CN(I,K,1)=((RMULT1(JP1)-RMULT1(J))*FRAC+RMULT1(J))*CN(I,K,2)
              CN(I,K,3)=((RMULT3(JP1)-RMULT3(J))*FRAC+RMULT3(J))*CN(I,K,2)
            ENDIF
20        CONTINUE
30      CONTINUE
   end subroutine Curve_Numbers_from_Beta
   
   
End Module m_CN_functions

