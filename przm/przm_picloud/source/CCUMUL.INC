! CUMMUL common to allow VADOFT output to have annual summary like PRZM output

      REAL*8 ANNmef(mxnszo,3) , ANNcyv(mxnszo,3) , ANNmif(mxnszo,3) ,   &
     &       ANNccp(mxnszo,3) , ANNccw(mxnszo) , ANNwif(mxnszo) ,       &
     &       ANNwef(mxnszo)
      COMMON /CUMMUL/ ANNmef , ANNcyv , ANNmif , ANNccp , ANNccw ,      &
     &                ANNwif , ANNwef
