module coreCalculations
!Written by Dirk F. Young (Virginia, USA)
implicit none

contains

    subroutine reducer2                         
        !THIS SUBROUTINE REDUCES THE MODEL EQUIVALENT PARAMETERS TO
        !THE COEFFICIENTS NECESSARY FOR THE SUBROUTINE SIMULDIFF2
        !VALUES FOR A,B,E,F ARE RETURNED
        use nonInputVariables, ONLY: num_records, gamma_1,gamma_2,omega,theta,lamda, A,B,E,F
        implicit none 
        
        !July 1, 2010: prior versions had B & E switched
        A = -gamma_1 - omega*theta
        B = omega * theta
        E = omega+lamda
        F = -gamma_2-omega-lamda
    
    end subroutine reducer2

subroutine simuldiff2 (A,B,E,F,m1,m2,T_end,mn1,mn2,mavg1,mavg2)
        implicit none
        real(8),intent(in):: A,B,E,F    !diff eqn coefficients
        real(8),intent(in):: m1,m2      !initial values for m1 and m2
        real(8),intent(in):: T_end      !time duration
        
        real(8),intent(out)::mn1,mn2    !values for m1 and m2 after time T_end
        real(8),intent(out)::mavg1      !average mass over T_end
        real(8),intent(out)::mavg2      !average mass over T_end
        
        real(8):: root1,root2,DD,EE,FF,X1,Y1,af,fxa,bxe,dif,bbb,rt1,rt2,exrt1,exrt2,ccc,ddd,gx,hx
        real(8):: term1,term2,term3,term4

        af=A+F
        fxa=F*A
        bxe=B*E
        dif=4*(fxa-bxe)
        bbb=sqrt(af*af-dif)
        
        root1 = (af+bbb)/2.
        root2 = (af-bbb)/2.
        DD = (root1-A)/B
        EE = (root2-A)/B
        FF = EE-DD
        X1 = (EE*m1-m2)/FF
        Y1 = (m2-DD*m1)/FF
          
    !calculate new concentrations for next step
        rt1 = root1*T_end
        rt2 = root2*T_end
        exrt1 = exp(rt1)
        exrt2 = exp(rt2)
        ccc = X1*exrt1
        ddd = Y1*exrt2
        
        mn1 = ccc+ddd
        mn2= DD*ccc+EE*ddd

    !   AVERAGE DAILY CONCENTRATION: 
    !   SET UP FOR DAILY AVERAGE, BUT CAN BE CHANGED BY CHANGING T1 AND T2
        gx=X1/root1
        hx=Y1/root2

        term1 = gx*exrt1                    !term3 = -X1/root1*exp(root1*T1)
        term2 = hx*exrt2                    !term4 = -Y1/root2*exp(root2*T1
        term3 = -gx
        term4 = -hx

        mavg1=(term1+term2+term3+term4)/T_end   !mavg1=(term1+term2+term3+term4)/(T2-T1)
        mavg2=(term1*DD+term2*EE+term3*DD+term4*EE)/T_end  !average compartment 2 mass    
    end subroutine simuldiff2


end module coreCalculations