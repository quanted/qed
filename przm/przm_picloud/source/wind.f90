Module m_Wind

   Use General_Vars
   Implicit None
   Private
   Public :: Get_Crop_Params
   Public :: Get_Aerodynamic_Parameters

   ! Aerodynamic Environments, used by Get_Aerodynamic_Parameters
   Integer, Parameter, Public :: t_Open_Flat_Terrain = 1
   Integer, Parameter, Public :: t_Class_A_Pan_Anemometer = 2
   Integer, Parameter, Public :: t_FAO_Reference_Short_Grass_Crop = 3
   Integer, Parameter, Public :: t_User = 4  ! Values read from the input file.

   ! The wind measurements in the meteorological Daily Values File (*.dvf)
   ! were normalized to 10 meters, Open Flat Terrain.
   !> Plan for the future: read from the PRZM file the aerodynamic
   !>      environment of the metereological file (e.g., *.dvf).

   Integer, Save, Public :: uWind_Environs = t_Open_Flat_Terrain
   Real,    Save, Public :: uWind_Reference_Height, uWind_z0, uWind_D

   ! Height of the stagnant air layer above the soil = 5 mm = 0.5 cm
   ! In the literature, generally denoted as "d".
   ! Value expressed in cm.
   Real, Save, Public :: Height_stagnant_air_layer_cm = 0.5

   ! Minimum Canopy Height = 0.05 m = 5 cm
   ! In the literature, Canopy Height is generally denoted as "Zch".
   ! Minimum_Canopy_Height_cm -- value in cm
   ! Minimum_Canopy_Height_c  -- value in meter
   ! 1 cm is equivalent to 1.0E-02 m
   Real, Parameter, Public :: Minimum_Canopy_Height_cm = 5.0
   Real, Parameter, Public :: Minimum_Canopy_Height_m = Minimum_Canopy_Height_cm * 1.0E-02

   ! von Karman's constant, dimensionless
   Real, Parameter, Public :: vonKarman = 0.4

Contains

   Subroutine Get_Aerodynamic_Parameters (Wind_Env, Wind_Reference_Height, Wind_z0, Wind_D)

      ! Returns Aerodynamic Parameters for wind speed computations
      !         for the named environment.
      !
      ! Wind_Env -- (integer) environment type: t_Open_Flat_Terrain or
      !             t_Class_A_Pan_Anemometer, t_FAO_Reference_Short_Grass_Crop
      !
      ! Wind_Reference_Height -- reference height (meter)
      ! Wind_z0 -- surface roughness length or roughness height (meter)
      ! Wind_D  -- zero plane displacement (meter)
      !
      ! Let u_2 and u_1 be wind speeds measured at
      ! heights z_2 and z_1 respectively. Then
      !
      !        u_2                    u_1
      ! ------------------  =  ------------------
      ! Ln((z_2-d_2)/z0_2)     Ln((z_1-d_1)/z0_1)
      !
      ! where
      !     u_i : wind speed at height z_i
      !     z_i : height at which the measurement was taken (m)
      !     d_i : zero plane displacement (m)
      !     z0_i: surface roughness length or roughness height (m)
      !
      ! This equation assumes the atmosphere is neutrally stable,
      ! i.e., phi_m = 1, which implies psi_m = 0. See the PRZM
      ! manual and subroutine "Canopy" for more information.

      Implicit None

      Integer, Intent(In) :: Wind_Env
      Real,   Intent(Out) :: Wind_Reference_Height
      Real,   Intent(Out) :: Wind_z0
      Real,   Intent(Out) :: Wind_D

      Select Case (Wind_Env)
      Case(t_Open_Flat_Terrain)
         ! The wind measurements in the meteorological Daily Values File
         ! (*.dvf) were normalized to 10 meters, Open Flat Terrain (used
         ! for Metereological Stations):
         Wind_Reference_Height = 10.0
         Wind_z0 = 0.03
         Wind_D  = 0.0

      Case(t_Class_A_Pan_Anemometer)
         Wind_Reference_Height = 0.6
         Wind_z0 = 0.01476
         Wind_D  = 0.08

      Case(t_FAO_Reference_Short_Grass_Crop)
         Wind_Reference_Height = 2.0
         Wind_z0 = 0.01476
         Wind_D  = 0.08

      Case(t_User)
         !> This is a plan for the future.
         !> User provides all parameters in the PRZM input file.
         !> Requires modification of the PRZM input file.
         Wind_Reference_Height = uWind_Reference_Height
         Wind_z0 = uWind_z0
         Wind_D  = uWind_D

      Case Default
         ! Error

      End Select

   End Subroutine Get_Aerodynamic_Parameters



   Subroutine Get_Crop_Params (Crop_Height, Z0, D)

      ! Given a height, compute the zero displacement
      ! height and the roughness length
      !
      ! Crop_Height -- The canopy height (meter)
      ! D  -- The zero plane displacement height (meter)
      ! Z0 -- The roughness length (meter).

      Implicit None

      Real,  Intent(In) :: Crop_Height
      Real, Intent(Out) :: D
      Real, Intent(Out) :: Z0

      Real :: logd, logz0

      If (Crop_Height > Minimum_Canopy_Height_m) Then
         ! (Thibodeaux 1996) Regression for Zero plane displacement.
         ! height generated for 0.02 m < Crop_Height < 25 m
         ! Zero displacement height, m
         logd = 0.9793*Log10(Crop_Height) - 0.1536
         D    = 10.0 ** logd

         ! Roughness Height, m
         ! Valid for tall crops (Thibodeaux 1996).
         logz0 = 0.997*Log10(Crop_Height) - 0.883     ! copy 1/2; propagate changes
         Z0    = 10.0 ** logz0
      Else
         ! The crop height is less than the Minimum_Canopy_Height_m:
         ! the roughness height is set equal to the value
         ! of the regression for z0 evaluated at
         ! Crop_Height = Minimum_Canopy_Height_m
         logz0 = 0.997*Log10(Minimum_Canopy_Height_m) - 0.883  ! copy 2/2; propagate changes
         Z0    = 10.0 ** logz0
         D  = 0.0
      End If

   End Subroutine Get_Crop_Params


End Module m_Wind
