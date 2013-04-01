!...   THIS IS THE INCLUDE FILE ACCUM.INC

      REAL MINpw , MOUtw , MEOutw , YINpw , YOUtw , YEOutw , MINpp ,    &
     &     MOUtp , MDOut , YINpp , YOUtp , YDOut , MSTr , YSTr ,        &
     &     MOUtw5 , YOUtw5 , MSTrp , YSTrp , MINpw1 , MINpw2 , MOUtp5 , &
     &     MOUtp6 , YOUtp5 , MOUtw1 , MOUtw2 , MOUtw3 , MOUtw4 , MSTr1 ,&
     &     MSTr2 , YINpw1 , YINpw2 , YOUtw1 , YOUtw2 , YOUtw3 , YOUtw4 ,&
     &     YSTr1 , YSTr2 , MINpp1 , MINpp2 , MOUtp1 , MOUtp2 , MOUtp3 , &
     &     MOUtp4 , MSTrp1 , YINpp1 , YINpp2 , YOUtp1 , YOUtp2 ,        &
     &     YOUtp3 , YOUtp4 , YSTrp1 , YOUtp6 , YOUtw6 , MOUtw6 ,        &
     &     DCOflx , MCOflx , YCOflx , MOOutw , YOOutw , DOUtfl ,        &
     &     MOUtfl , YOUtfl , MOUtp8 , YOUtp8 , MINpp8 , VOUtm , VOUty , &
     &     MOUtpv , YOUtpv , MOUtp7 , YOUtp7 , YINpp8 , MTRfm , YTRfm , &
     &     DINflo , MINflo , YINflo , YIRrr , MIRrr , DSNinf(3) ,       &
     &     MSNinf(3) , YSNinf(3) ,                                      &
!**** THE FOLLOWING ADDED FOR LATERAL PESTICIDE FLUXES ********
     &     MOUtp9 , YOUtp9 , MLOut , YLOut

!     DINFLO, MINFLO, and YINFLO are accumulators for lateral inflow of
!     water from septic effluent.  DSNINF, MSNINF, and YSNINF are
!     accumulators for inflow of nitrogen species from septic effluent.

      COMMON /ACCUMR4/ MOUtw5 , YOUtw5 , MINpw1 , MINpw2 , MOUtw1 ,     &
     &                 MOUtw2 , MOUtw3 , MOUtw4 , MSTr1 , MSTr2 ,       &
     &                 YINpw1 , YINpw2 , YOUtw1 , YOUtw2 , YOUtw3 ,     &
     &                 YOUtw4 , YSTr1 , YSTr2 , YOUtw6 , MOUtw6 ,       &
     &                 DOUtfl , MOUtfl , YOUtfl , MOUtpv , YOUtpv ,     &
     &                 DINflo , MINflo , YINflo , DSNinf , MSNinf ,     &
     &                 YSNinf , YIRrr , MIRrr

      COMMON /ACCUMR41/ MINpw(ncmpts) , MOUtw(ncmpts) , MEOutw(ncmpts) ,&
     &                  YINpw(ncmpts) , YOUtw(ncmpts) , YEOutw(ncmpts) ,&
     &                  MSTr(ncmpts) , YSTr(ncmpts) , MOUtp5(3) ,       &
     &                  MOUtp6(3) , YOUtp2(3) , MINpp1(3) , MOUtp1(3) , &
     &                  MOUtp2(3) , MOUtp3(3) , MOUtp4(3) , MSTrp1(3) , &
     &                  YINpp1(3) , YOUtp1(3) , YOUtp3(3) , YOUtp4(3) , &
     &                  YSTrp1(3) , YOUtp5(3) , YOUtp6(3) , DCOflx(3) , &
     &                  MCOflx(3) , YCOflx(3) , MOOutw(ncmpts) ,        &
     &                  YOOutw(ncmpts) , MOUtp7(3) , YOUtp7(3) ,        &
     &                  MOUtp8(3) , YOUtp8(3) , MINpp8(3) , YINpp8(3) , &
!**** THE FOLLOWING ADDED FOR LATERAL PESTICIDE FLUXES ********
     &                  MOUtp9(3) , YOUtp9(3)

      COMMON /ACCUMR42/ MOUtp(3,ncmpts) , YDOut(3,ncmpts) ,             &
     &                  MINpp(3,ncmpts) , MDOut(3,ncmpts) ,             &
     &                  YINpp(3,ncmpts) , YOUtp(3,ncmpts) ,             &
     &                  MSTrp(3,ncmpts) , YSTrp(3,ncmpts) ,             &
     &                  MINpp2(3,ncmpts) , YINpp2(3,ncmpts) ,           &
     &                  VOUtm(3,ncmpts) , VOUty(3,ncmpts) ,             &
     &                  MTRfm(3,ncmpts) , YTRfm(3,ncmpts) ,             &
!**** THE FOLLOWING ADDED FOR LATERAL PESTICIDE FLUXES ********
     &                  MLOut(3,ncmpts) , YLOut(3,ncmpts)

