Module m_Canopy

   Use General_Vars
   Implicit None
   Private
   Public :: Canopy

Contains

   Subroutine Canopy (utemp, uwind, zch, totr, crc)

      Use m_Wind
      Use I_errchk
      Implicit None

      ! CH denotes canopy height
      ! RH denotes reference height
      !
      ! Utemp(2) - Air temperature (Celsius)
      !     Utemp(1): Air temperature at the soil surface
      !     Utemp(2): Ambient temperature
      !
      ! Uwind(2) - wind speed (meter/day)
      !     Uwind(1): wind speed at the soil surface
      !     Uwind(2): wind speed at the top of the canopy
      !
      ! ZCH  - canopy height (meter)  ( Zch > 0 )
      ! TOTR - total canopy resistance (cm/day)
      !
      ! CRC(2) - canopy resistance (cm/day)
      !     crc(1): total resistance in the lower half of the canopy
      !     crc(2): total resistance in the upper half of the canopy
      !
      ! History:
      ! * Wed Mar 24 15:29:51 EST 2004
      !   - translated to f90
      !   - total canopy resistance computed by integration,
      !     rather than a Riemann sum approximation.
      !   - The formulation of phi_h, phi_m, and psi_m updated as
      !     described in Thibodeaux. 1996. Environmental Chemodynamics:
      !     Movement of Chemicals in Air, Water, and Soil. Wiley.
      !     2nd Edition.
      !   - various bugs fixed; code cleaned.
      !
      ! * Modification date: 2/18/92 JAM
      !   To calculates the overall vertical transport resistance

      Real,  Intent(in) :: zch
      Real, Intent(out) :: totr
      Real,  Intent(in) :: utemp(2)
      Real,  Intent(in) :: uwind(2)
      Real, Intent(out) :: crc(2)

      Real :: gradw, gradt, RiNum, phi_h, phi_m, psi_m, ustar
      Real :: d, z0, diffch, e2, c1, c2, ct, meanT, uch, zeta
      Real :: temp0, RiMax
      Character :: mesage*80

      Real, Parameter :: Zero = 0.0

      ! If the Richardson number is "close" to Fuzzy, then
      ! the Richardson number is effectively equal to zero.
      Real, Parameter :: Fuzzy = 0.003

      ! To convert from 1/m to 1/cm :
      ! value in 1/m is equivalent to (value * Im_to_Icm) 1/cm
      Real, Parameter :: Im_to_Icm = 1.0e-02

      ! Temperature conversion: kelvin = Celsius + c2k
      Real, Parameter :: c2k = 273.15

      ! Maximum value of the Richardson number
      Real, Parameter :: Max_Richardson = 0.19

      ! g_grav: acceleration due to gravity. Express in m/day^2
      ! so that the Richardson number is dimensionless.
      ! g_grav = 9.8 m/s^2
      !        = 9.8 m/s^2 * (86400 s/day)**2 = 7.31567E+10 m/day^2
      Real, Parameter :: g_grav = 9.8 * 86400.0**2

      mesage = 'CANOPY'
      Call subin (mesage)

      ! Gradients
      gradt = (utemp(2)-utemp(1)) / zch      ! kelvin/meter
      gradw = (uwind(2)-uwind(1)) / zch      ! 1/day
      meanT = Sum(utemp(1:2))/2 + c2k        ! mean Temperature, kelvin

      ! Computes Richardson number (RiNum) (dimensionless).
      ! Louis J. Thibodeaux. 1996. Environmental Chemodynamics:
      ! Movement of Chemicals in Air, Water, and Soil. Wiley.
      ! 2nd Edition, p 373-375.
      ! Typically, -2.0 <= RiNum < 0.2, but for some of
      ! the PRZM scenarios RiNum fell outside the nominal range.
      RiNum = g_grav / meanT * gradt / gradw**2

      ! Computes the dimensionless height (zeta). See
      ! Louis J. Thibodeaux. 1996. Environmental Chemodynamics:
      ! Movement of Chemicals in Air, Water, and Soil. Wiley.
      ! 2nd Edition, p 379-381.
      If (RiNum < (-Fuzzy)) Then
         ! Richardson number less than "fuzzy zero".
         zeta = RiNum

      Else If (RiNum > Fuzzy) Then
         ! Richardson number greater than "fuzzy zero".
         ! Make sure function for zeta is always evaluated with
         ! Richardson numbers < 0.2
         RiMax = Min (Max_Richardson, RiNum)
         zeta = RiMax / (1.0 - 5.0*RiMax)

      Else
         ! Abs(RiNum) <= Fuzzy, i.e., RiNum is equal to "Fuzzy Zero"
         zeta = Zero
      End If

      ! phi_h: stability function for sensible heat (dimensionless)
      ! phi_m: stability function for momentum (dimensionless)
      ! psi_m: integrated momentum stability parameter (dimensionless)
      If (zeta < Zero) Then
         phi_h = 1.0 / Sqrt(1.0 - 15.0*zeta)
         phi_m = Sqrt(phi_h)
         temp0 = (1.0+phi_m**2)/2.0 * ((1.0+phi_m)/2.0)**2
         psi_m = Pi/2.0 - 2.0*Atan(phi_m) + Log(temp0)
      Else
         ! zeta >= 0
         phi_h = 1.0 + 5.0*zeta
         phi_m = phi_h
         psi_m = -5.0 * zeta
      End If

      ! Computes zero displacement height, D (meter)
      ! and the roughness length, Z0 (meter)
      Call Get_Crop_Params (zch, z0, d)

      uch = Uwind(2)

      ! Compute friction velocity, USTAR (meter/day)
      ustar = vonKarman * uch / (Log((zch-d)/z0) - psi_m)

      ! Thermal eddy diffusivity (m^2/day) at canopy height
      diffch = ustar * vonKarman * (zch-d) / phi_h

      ! Compute canopy resistance.
      ! Let K(z) be the thermal eddy diffusivity at height z,
      !     K(z) = diffch * Exp[4*(z/ZCH - 1)]
      !
      ! The resistance at height z is 1/K(z).
      ! The resistance in the lower half of the canopy is:
      !
      !               z=zch/2   dz     e^2 (e^2-1) zch
      !     crc(1) = Integral [----] = ---------------
      !                z=0     K(z)       4 diffch
      !
      ! The resistance in the upper half of the canopy is:
      !
      !               z=zch     dz     (e^2-1) zch
      !     crc(2) = Integral [----] = -----------
      !              z=zch/2   K(z)     4 diffch
      !
      ! The total canopy resistance is:
      !     totr = crc(1) + crc(2), or
      !
      !             z=zch     dz     (e^4-1) zch
      !     totr = Integral [----] = -----------
      !              z=0     K(z)     4 diffch
      !
      ! Crc and totr are computed in day/meter.
      ! Im_to_Icm converts to day/cm.

      e2 = Exp(2.0)     ! e^2
      c2 = (e2 - 1) * zch / (4 * diffch) * Im_to_Icm
      c1 = e2 * c2
      ct = (e2**2 - 1) * zch / (4 * diffch) * Im_to_Icm

      crc(1) = c1
      crc(2) = c2
      totr   = ct

      Call subout

   End Subroutine Canopy

End Module m_Canopy
