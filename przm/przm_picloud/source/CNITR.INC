!     common for PRZM2 version of nitrogen module taken from HSPF
      INTEGER NCMPP1
      PARAMETER (NCMPP1=NCMPTS+1)
      COMMON /CNITR / VNUtfg , FORafg , ITMaxa , NUPtfg , FIXnfg ,      &
     &                AMVofg , ALPnfg , VNPrfg , NIAdfg , NC1 , NCRp ,  &
     &                CRPdat , CRPday , CRPfrc , NUPtgt , NMXrat ,      &
     &                NIAfxm , NIAcnm , KPLnm , KRBnm , KRAnm , KRLnm , &
     &                BNPrfm , LNPrfm , NUPtfm , NUPtm , GNPm , NPM ,   &
     &                DNThrs , ORNpm , ANUfm , KVOl , THVol , TRFvol ,  &
     &                NWCnt , NECnt , AGPltn , LITtrn , NIT , TNIt ,    &
     &                NDFc , KPLn , KREtbn , BGNprf , AGKprn , KREtan , &
     &                LINprf , NUPtg , PNUtg , ANUtf , NRXf , NCFx1 ,   &
     &                NCFx2 , NCFx3 , NCFx4 , NCFx5 , NCFx6 , NCFx7 ,   &
     &                NCFx8 , NCFx9 , NCFx10 , NCFx11 , NCFx12 ,        &
     &                NCFx13 , NCFx14 , NCFx15 , NCFx16 , NCFx17 ,      &
     &                NCFx18 , NCFx19 , NCFx20 , NCFx21 , NCFx22 ,      &
     &                NCFx23 , NCFx24 , NCFx25 , NCFx26 , NCFx27 ,      &
     &                NCFx28 , SOSedn , PONo3 , PONh4 , POOrn , PONitr ,&
     &                TOTnit , TONit0 , NBUff , CNIt , NAPfrc
      INTEGER VNUtfg , FORafg , ITMaxa , NUPtfg , FIXnfg , AMVofg ,     &
     &        ALPnfg , VNPrfg , NIAdfg(6) , NC1 , NCRp , CRPdat(4,3) ,  &
     &        CRPday(13,3) , NWCnt(6) , NECnt(1)
      REAL CRPfrc(13,3) , NUPtgt , NMXrat , NIAfxm(12,3) , NIAcnm(12,3) &
     &     , KPLnm(12,NCMPTS) , KRBnm(12,NCMPTS) , KRAnm(12) , KRLnm(12)&
     &     , BNPrfm(12) , LNPrfm(12) , NUPtfm(12) , NUPtm(12,NCMPTS) ,  &
     &     GNPm(11) , NPM(11,NCMPTS) , DNThrs(NCMPTS) , ORNpm(4,NCMPTS) &
     &     , ANUfm(12,NCMPTS) , KVOl(NCMPTS) , THVol , TRFvol , AGPltn ,&
     &     LITtrn , NIT(8,NCMPTS) , TNIt(8) , NDFc(NCMPP1) ,            &
     &     KPLn(NCMPTS) , KREtbn(NCMPTS) , BGNprf , AGKprn ,            &
     &     KREtan(NCMPTS) , LINprf , NUPtg(NCMPTS) , PNUtg(NCMPTS) ,    &
     &     ANUtf(NCMPTS) , NRXf(16,NCMPTS)
      REAL NCFx1(7,3) , NCFx2(NCMPTS,3) , NCFx3(NCMPP1,3) ,             &
     &     NCFx4(NCMPTS,3) , NCFx5(NCMPP1,3) , NCFx6(NCMPP1,3) ,        &
     &     NCFx7(NCMPP1,3) , NCFx8(NCMPP1,3) , NCFx9(NCMPP1,3) ,        &
     &     NCFx10(3,3) , NCFx11(3,3) , NCFx12(NCMPP1,3) ,               &
     &     NCFx13(NCMPTS,3) , NCFx14(NCMPP1,3) , NCFx15(NCMPTS,3) ,     &
     &     NCFx16(NCMPP1,3) , NCFx17(NCMPP1,3) , NCFx18(NCMPP1,3) ,     &
     &     NCFx19(NCMPP1,3) , NCFx20(NCMPP1,3) , NCFx21(NCMPP1,3) ,     &
     &     NCFx22(NCMPP1,3) , NCFx23(NCMPP1,3) , NCFx24(1,3) ,          &
     &     NCFx25(NCMPP1,3) , NCFx26(NCMPP1,3) , NCFx27(NCMPP1,3) ,     &
     &     NCFx28(NCMPP1,3) , SOSedn , PONo3 , PONh4 , POOrn , PONitr , &
     &     TOTnit , TONit0 , NBUff(366,6) , CNIt(8,NCMPTS) ,            &
     &     NAPfrc(napp)

      EQUIVALENCE (SEDn,NCFx1(1,1))
      EQUIVALENCE (PSAms,NCFx2(1,1))
      EQUIVALENCE (OSAms,NCFx3(1,1))
      EQUIVALENCE (PSNo3,NCFx4(1,1))
      EQUIVALENCE (OSNo3,NCFx5(1,1))
      EQUIVALENCE (DENif,NCFx6(1,1))
      EQUIVALENCE (AMNit,NCFx7(1,1))
      EQUIVALENCE (AMImb,NCFx8(1,1))
      EQUIVALENCE (ORNmn,NCFx9(1,1))
      EQUIVALENCE (NIAddr,NCFx10(1,1))
      EQUIVALENCE (NIAdwt,NCFx11(1,1))
      EQUIVALENCE (NFIxfx,NCFx12(1,1))
      EQUIVALENCE (PSSln,NCFx13(1,1))
      EQUIVALENCE (OSSln,NCFx14(1,1))
      EQUIVALENCE (PSSrn,NCFx15(1,1))
      EQUIVALENCE (OSSrn,NCFx16(1,1))
      EQUIVALENCE (NIImb,NCFx17(1,1))
      EQUIVALENCE (AMVol,NCFx18(1,1))
      EQUIVALENCE (REFron,NCFx19(1,1))
      EQUIVALENCE (NIUpa,NCFx20(1,1))
      EQUIVALENCE (AMUpa,NCFx21(1,1))
      EQUIVALENCE (NIUpb,NCFx22(1,1))
      EQUIVALENCE (AMUpb,NCFx23(1,1))
      EQUIVALENCE (RETagn,NCFx24(1,1))
      EQUIVALENCE (RTLln,NCFx25(1,1))
      EQUIVALENCE (RTRln,NCFx26(1,1))
      EQUIVALENCE (RTLbn,NCFx27(1,1))
      EQUIVALENCE (RTRbn,NCFx28(1,1))

      REAL SEDn(7) , PSAms(NCMPTS) , OSAms(NCMPP1) , PSNo3(NCMPTS) ,    &
     &     OSNo3(NCMPP1) , DENif(NCMPP1) , AMNit(NCMPP1) , AMImb(NCMPP1)&
     &     , ORNmn(NCMPP1) , NIAddr(3) , NIAdwt(3) , NFIxfx(NCMPP1) ,   &
     &     PSSln(NCMPTS) , OSSln(NCMPP1) , PSSrn(NCMPTS) , OSSrn(NCMPP1)&
     &     , NIImb(NCMPP1) , AMVol(NCMPP1) , REFron(NCMPP1) ,           &
     &     NIUpa(NCMPP1) , AMUpa(NCMPP1) , NIUpb(NCMPP1) , AMUpb(NCMPP1)&
     &     , RETagn , RTLln(NCMPP1) , RTRln(NCMPP1) , RTLbn(NCMPP1) ,   &
     &     RTRbn(NCMPP1)
