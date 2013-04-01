Module IO_LUNS

   ! Logical unit numbers used by PRZM

   Use General_Vars
   Implicit None
   Private

          ! 156 -> 1.cnc
          ! 157 -> 2.cnc
          ! 158 -> 3.cnc
          ! 159 -> 1.msb
          ! 160 -> 2.msb
          ! 161 -> 3.msb
          ! 162 -> 1.hyd

   Integer, Dimension(1:MaxChems), Public :: lun_CNC, lun_msb, lun_hyd

End Module IO_LUNS

