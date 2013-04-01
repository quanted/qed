!...    THIS IS THE INCLUDE FILE CCROP.INC

      REAL ANEtd , CINtcp , COVmax , COVer , WEIght ,  WFMax , AMXdr ,  &
     &     HEIght , HTMax
      INTEGER IYRem , IYRmat , MAT , IEMer , IHAr , NCPds , NDC ,       &
     &        IYRhar ,  INCrop , NCRop , NCP , TNDgs , ICNcn , NCOmrz , &
     &        INIcrp ,  IFScnd , IPScnd , IUSlec , UCFlg
      COMMON /CRPI  / NCPds , NCRop , NCP , NDC , NCOmrz , INIcrp ,     &
     &                IUSlec , UCFlg
      COMMON /CRPI1 / IYRem(mxcpd) , IYRmat(mxcpd) , MAT(mxcpd) ,       &
     &                 IEMer(mxcpd) , IHAr(mxcpd) , INCrop(mxcpd) ,     &
     &                 TNDgs(mxcpd) , ICNcn(nc) , IYRhar(mxcpd) ,       &
     &                 IPScnd(3)
      COMMON /CRPI2 / IFScnd(3,nc)
      COMMON /CRPR4 / ANEtd , COVer , WEIght , HEIght
      COMMON /CRPR41/ CINtcp(nc) , COVmax(nc) , WFMax(nc) , HTMax(nc) , &
     &                 AMXdr(nc)
