! COMMON BLOCK FOR IRRIGATION SUBROUTINES

      REAL Q0 , KS , HF , DW , BT , ZRS , XL , SF , EN , FS(1000) ,     &
     &     QS(1000) , SMDef , DX ,  PCDepl , RATeap , FLEach , XFRac ,  &
     &     APDep , UC , IRRr
      INTEGER NSPace , IRType , IRNone
      LOGICAL :: REAlly_not_thrufl
      COMMON /IRGTI / NSPace , IRType , IRNone
      COMMON /IRGTL / REAlly_not_thrufl
      COMMON /IRGTR4/ Q0 , KS , HF , DW , BT , ZRS , XL , SF , EN , QS ,&
     &                FS , SMDef ,  DX , PCDepl , RATeap , FLEach ,     &
     &                XFRac , APDep , UC , IRRr
