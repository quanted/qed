Module m_IniVar

   Use General_Vars
   Implicit None
   Private
   Public :: IniVar

Contains

   Subroutine IniVar ()

      ! Initialize various variables

      Use m_Wind
      Implicit None
      Include 'PPARM.INC'
      Include 'CMET.INC'

      ! Description taken from the przm manual.
      ! przm input file RECORD 31
      ! ZWIND: height of wind speed measurement above the soil surface (meter).
      ! The wind speed anemometer is usually fixed at 10 meters (30 feet)
      ! above the ground surface.  This height may differ at some weather
      ! stations such as at a class A station where the anemometer may be
      ! attached to the evaporation pan.  The correct value can be obtained
      ! from the meteorological data reports for the station whose data are
      ! in the simulation.
      !
      ! Thu Apr 08 16:54:02 EDT 2004 --
      ! o The variable ZWIND was replaced with uWind_Reference_Height

      ! The wind measurements in the meteorological Daily Values File (*.dvf)
      ! were normalized to 10 meters, Open Flat Terrain.
      uWind_Environs = t_Open_Flat_Terrain
      Call Get_Aerodynamic_Parameters(uWind_Environs, uWind_Reference_Height, &
            uWind_z0, uWind_D)

   End Subroutine IniVar

End Module m_IniVar
