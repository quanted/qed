! include file CPEST.INC

      REAL*8 PVFlux , UPFlux , DFFlux , ADFlux , SUPflx , SDKflx ,      &
     &        DKFlux , ERFlux , ROFlux , WOFlux , RZFlux , TRFlux ,     &
     &        LATflx , LTFlux , RFFlux , TTRflx , TSRcfx , SRCflx
      REAL*4 KD , KDOrg , SPEstr , PEStr , PLDkrt , FEXtrc , DISp ,     &
     &        FILtra , FOLpst , FPDlos , WTErm , PLNtap , OC , FRNdcf , &
     &        TAPp , DEPi , DWRate , GAMma , PBAl , CPBal , UPTkf ,     &
     &        ELTerm , SOIlap , FOLp0 , DSRate , HENryk , FMRmvl ,      &
     &        DGRate , DAIr , KH , ENPy , CONduc , OKH , SPTemp ,       &
     &        CNCpnd , MASso , CC , PLVkrt , FPVlos , CNDbdy , CRCnc ,  &
     &        ELTt , SRCw , SRCs , APPeff , DRFt , RTRw , RTRs , TCNc , &
     &        DKRw13 , DKRw23 , DKRw12 , DKRs13 , DKRs23 , DKRs12 ,     &
     &        DSRat1 , DSRat2 , DWRat1 , DWRat2 , DGRat1 , DGRat2 ,     &
     &        DKW112 , DKW113 , DKW123 , DKW212 , DKW213 , DKW223 ,     &
     &        DKS112 , DKS113 , DKS123 , DKS212 , DKS213 , DKS223 ,     &
     &        PTRn12 , PTRn13 , PTRn23 , FPLos12 , FPLos13 , FPLos23 ,  &
     &        QFAc , TBAse , MSLab , MSEff , MW21 , MW31 , MW32
      REAL YRCnc1 , YRCnc2
      REAL YRInf1 , YRInf2 , YRFlx1 , YRFlx2
      REAL*8 A , B , C , F , X
      INTEGER NAPpc , NAPs , FAM , IAPdy , IAPyr , MCFlag , NCHem ,     &
     &         WIN , WINday , DK2flg , MSFlg
      INTEGER NCOmbe , NCOmen , DKDay , DKMnth , DKStrt , DKNum ,       &
     &         DKEnd , DKStat , CAM , CRPapp
      COMMON /PSTI  / NAPpc , NAPs , FAM , MCFlag , NCHem , WIN , DK2flg
      COMMON /PSTI1 / IAPyr(napp) , IAPdy(napp) , WINday(napp)


      ! MSFlg == { MS_Absolute_FC or MS_Relative_FC } if ITFLAG == 2
      !       == unused otherwise.
      ! Usage:
      !    If (ITFLAG == 2) Then
      !       If (MSFLG(L) == MS_Absolute_FC) Then
      !          Msfac = (Thetn(Jb)/Mslab(L))**Mseff(L)
      !       Else If (MSFLG(L) == MS_Relative_FC) Then
      !          Msfac = (Thetn(Jb)/(Thefc(Jb)*Mslab(L)))**Mseff(L)
      !       End If
      !    Else
      !       Msfac = 1.0
      !    End If
      !
      ! After validating the input value of MSFLG, we will set
      ! MSFLG = 0 if ITFLAG != 2. This allows:
      !      Select Case(msflg(L))
      !      Case(MS_Absolute_FC)
      !         msfac = (thetn(jb)/mslab(L))**mseff(L)
      !      Case(MS_Relative_FC)
      !         msfac = (thetn(jb)/(thefc(jb)*mslab(L)))**mseff(L)
      !      Case Default
      !         msfac = One
      !      End Select
      !
      ! Regardless of ITFLAG.

      COMMON /PSTI2 / NCOmbe(ncmpts) , NCOmen(ncmpts) , DKDay(3) ,      &
     &                 DKMnth(3) , DKStrt(3) , DKNum(3) , DKEnd(3) ,    &
     &                 DKStat(3) , CRPapp(3) , MSFlg(3)
      COMMON /PSTI3 / CAM(3,napp)
      COMMON /PSTR4 / FILtra , ELTt , CNCpnd , YRCnc1 , YRCnc2 ,        &
     &                 PTRn12 , PTRn13 , PTRn23 , FPLos12 , FPLos13 ,   &
     &                 FPLos23 , MW21 , MW31 , MW32
      COMMON /PSTR41/ PLDkrt(3) , FEXtrc(3) , ELTerm(3) , FOLpst(3) ,   &
     &                 FPDlos(3) , PLNtap(3) , ERFlux(3) , CONduc(3) ,  &
     &                 DAIr(3) , OC(ncmpts) , WOFlux(3) , SUPflx(3) ,   &
     &                 SDKflx(3) , FOLp0(3) , ROFlux(3) , PBAl(3) ,     &
     &                 CNDbdy(3) , CPBal(3) , RZFlux(3) , HENryk(3) ,   &
     &                 ENPy(3) , PLVkrt(3) , FPVlos(3) , CRCnc(2) ,     &
     &                 FMRmvl(3) , TTRflx(3) , DKRw12(ncmpts) ,         &
     &                 DKRw13(ncmpts) , DKRw23(ncmpts) , DKW112(ncmpts) &
     &                ,  DKW113(ncmpts) , DKW123(ncmpts) ,              &
     &                DKW212(ncmpts) ,  DKW213(ncmpts) , DKW223(ncmpts) &
     &                , DKRs12(ncmpts) ,  DKRs13(ncmpts) ,              &
     &                DKRs23(ncmpts) , DKS112(ncmpts) ,  DKS113(ncmpts) &
     &                , DKS123(ncmpts) , DKS212(ncmpts) ,               &
     &                 DKS213(ncmpts) , DKS223(ncmpts) , TSRcfx(3) ,    &
     &                 TCNc(3) , LATflx(3) , UPTkf(3) , FRNdcf(3) ,     &
     &                 QFAc(3) , TBAse(3) , MSLab(3) , MSEff(3) ,       &
     &                 YRInf1(3) , YRInf2(3) , YRFlx1(3) , YRFlx2(3)
      COMMON /PSTR42/ KD(3,ncmpts) , KDOrg(3,ncmpts) , SPEstr(3,ncmpts) &
     &                  , PEStr(3,ncmpts) , DISp(3,ncmpts) ,            &
     &                TAPp(3,napp)  , DEPi(3,napp) , APPeff(3,napp) ,   &
     &                DRFt(3,napp) ,  DWRate(3,ncmpts) ,                &
     &                DFFlux(3,ncmpts) ,  ADFlux(3,ncmpts) ,            &
     &                UPFlux(3,ncmpts) ,  DKFlux(3,ncmpts) ,            &
     &                SOIlap(3,ncmpts) ,  DSRate(3,ncmpts) ,            &
     &                DGRate(3,ncmpts) ,  PVFlux(3,ncmpts) ,            &
     &                KH(3,ncmpts) , OKH(3,ncmpts) ,  SPTemp(3,ncmpts) ,&
     &                CC(3,npii) , MASso(3,ncmpts) ,  SRCw(3,ncmpts) ,  &
     &                SRCs(3,ncmpts) , TRFlux(3,ncmpts)  ,              &
     &                RTRw(3,ncmpts) , RTRs(3,ncmpts) ,                 &
     &                 SRCflx(3,ncmpts) , LTFlux(3,ncmpts) ,            &
     &                 DWRat1(3,ncmpts) , DWRat2(3,ncmpts) ,            &
     &                 DSRat1(3,ncmpts) , DSRat2(3,ncmpts) ,            &
     &                 DGRat1(3,ncmpts) , DGRat2(3,ncmpts) ,            &
     &                 RFFlux(3,ncmpts) , WTErm(3,ncmpts) ,             &
     &                 GAMma(3,ncmpts)
      COMMON /PSTR81/ A(ncmpts) , B(ncmpts) , C(ncmpts) , X(ncmpts) ,   &
     &                 F(ncmpts)
