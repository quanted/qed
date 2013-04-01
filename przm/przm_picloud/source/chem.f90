Module m_chem

   Use General_Vars
   Implicit None
   Private
   Public :: q10dk

Contains

   Subroutine q10dk
      ! switches half-life when itflag=2
      ! Modification date: 3/11/96 waterborne

      Implicit None
      INCLUDE 'PPARM.INC'
      INCLUDE 'CHYDR.INC'
      INCLUDE 'CPEST.INC'
      INCLUDE 'CCROP.INC'
      INCLUDE 'CMISC.INC'
      INCLUDE 'CMET.INC'

      Integer :: L, jb, ib, ibm1
      Real :: tthkns, modfc, t, q10fac, msfac
      Character :: mesage*80

      Real, Parameter :: Zero = 0.0
      Real, Parameter :: One = 1.0
      Real, Parameter :: Ten = 10.0

      mesage = 'Q10DK'
      Call subin (mesage)

      Do L = 1, nchem
         Select Case(DK2FLG)
         Case(0)
            Call Aux1()

         Case(1)
            If (julday==dkstrt(L) .And. dkstat(L)==0) Then
               Call Aux2a()
               dkstat(L) = 1
            Else If (julday==dkend(L) .And. dkstat(L)==1) Then
               Call Aux2e()
               dkstat(L) = 0
            Else If (dkstat(L) == 0) Then
               Call Aux2e()
            Else If (dkstat(L) == 1) Then
               Call Aux2a()
            End If
         End Select
      End Do
      Call subout

   Contains


      Subroutine Aux1()

         ! The only difference between Aux1 and Aux2a
         ! is that Aux1 does not execute statements dkr[w,s]## = dk[w,s]###
         Implicit None

         ! assign horizon soil profile values to individual soil layers
         ib     = nhoriz
         t      = Zero
         tthkns = thkns(ib)

         Do jb = ncom2, 1, -1
            ibm1   = ib - 1
            t      = t + delx(jb)
            modfc  = Zero
            q10fac = qfac(L)**((spt(jb)-tbase(L))/Ten)

            Select Case(msflg(L))
            Case(MS_Absolute_FC)
               msfac = (thetn(jb)/mslab(L))**mseff(L)
            Case(MS_Relative_FC)
               msfac = (thetn(jb)/(thefc(jb)*mslab(L)))**mseff(L)
            Case Default
               msfac = One
            End Select

            If ((t<=tthkns+0.01) .Or. (ib==1)) Then
               dwrate(L,jb) = dwrat1(L,ib)*q10fac*msfac
               dsrate(L,jb) = dsrat1(L,ib)*q10fac*msfac
               dgrate(L,jb) = dgrat1(L,ib)*q10fac
            Else If (ib /= 1) Then
               modfc        = (t - tthkns)/delx(jb)
               dwrate(L,jb) = (dwrat1(L,ib)*(One-modfc)+dwrat1(L,ibm1)*modfc) * q10fac*msfac
               dsrate(L,jb) = (dsrat1(L,ib)*(One-modfc)+dsrat1(L,ibm1)*modfc) * q10fac*msfac
               dgrate(L,jb) = (dgrat1(L,ib)*(One-modfc)+dgrat1(L,ibm1)*modfc) * q10fac
               ib           = ib - 1
               tthkns       = tthkns + thkns(ib)
            End If
         End Do

      End Subroutine Aux1


      Subroutine Aux2a()

         ! The only difference between Aux1 and Aux2a
         ! is that Aux1 does not execute statements dkr[w,s]## = dk[w,s]###
         Implicit None

         ! assign horizon soil profile values to individual soil layers
         ib     = nhoriz
         t      = Zero
         tthkns = thkns(ib)

         Do jb = ncom2, 1, -1
            ibm1   = ib - 1
            t      = t + delx(jb)
            modfc  = Zero
            q10fac = qfac(L)**((spt(jb)-tbase(L))/Ten)

            Select Case(msflg(L))
            Case(MS_Absolute_FC)
               msfac = (thetn(jb)/mslab(L))**mseff(L)
            Case(MS_Relative_FC)
               msfac = (thetn(jb)/(thefc(jb)*mslab(L)))**mseff(L)
            Case Default
               msfac = One
            End Select

            If ((t<=tthkns+0.01) .Or. (ib==1)) Then
               dwrate(L,jb) = dwrat1(L,ib)*q10fac*msfac
               dsrate(L,jb) = dsrat1(L,ib)*q10fac*msfac
               dgrate(L,jb) = dgrat1(L,ib)*q10fac

               Select Case(L)
               Case(2)
                  dkrw12(jb) = dkw112(ib)
                  dkrs12(jb) = dks112(ib)
               Case(3)
                  dkrw13(jb) = dkw113(ib)
                  dkrw23(jb) = dkw123(ib)
                  dkrs13(jb) = dks113(ib)
                  dkrs23(jb) = dks123(ib)
               End Select

            Else If (ib /= 1) Then
               modfc        = (t - tthkns)/delx(jb)
               dwrate(L,jb) = (dwrat1(L,ib)*(One-modfc)+dwrat1(L,ibm1)*modfc) * q10fac*msfac
               dsrate(L,jb) = (dsrat1(L,ib)*(One-modfc)+dsrat1(L,ibm1)*modfc) * q10fac*msfac
               dgrate(L,jb) = (dgrat1(L,ib)*(One-modfc)+dgrat1(L,ibm1)*modfc) * q10fac

               Select Case(L)
               Case(2)
                  dkrw12(jb) = dkw112(ib)*(One-modfc) + dkw112(ibm1)*modfc
                  dkrs12(jb) = dks112(ib)*(One-modfc) + dks112(ibm1)*modfc
               Case(3)
                  dkrw13(jb) = dkw113(ib)*(One-modfc) + dkw113(ibm1)*modfc
                  dkrw23(jb) = dkw123(ib)*(One-modfc) + dkw123(ibm1)*modfc
                  dkrs13(jb) = dks113(ib)*(One-modfc) + dks113(ibm1)*modfc
                  dkrs23(jb) = dks123(ib)*(One-modfc) + dks123(ibm1)*modfc
               End Select

               ib     = ib - 1
               tthkns = tthkns + thkns(ib)
            End If
         End Do

      End Subroutine Aux2a


      Subroutine Aux2e()

         Implicit None

         ! assign horizon soil profile values to individual soil layers
         ib     = nhoriz
         t      = Zero
         tthkns = thkns(ib)

         Do jb = ncom2, 1, -1
            ibm1   = ib - 1
            t      = t + delx(jb)
            modfc  = Zero
            q10fac = qfac(L)**((spt(jb)-tbase(L))/Ten)

            Select Case(msflg(L))
            Case(MS_Absolute_FC)
               msfac = (thetn(jb)/mslab(L))**mseff(L)
            Case(MS_Relative_FC)
               msfac = (thetn(jb)/(thefc(jb)*mslab(L)))**mseff(L)
            Case Default
               msfac = One
            End Select

            If ((t<=tthkns+0.01) .Or. (ib==1)) Then
               dwrate(L,jb) = dwrat2(L,ib)*q10fac*msfac
               dsrate(L,jb) = dsrat2(L,ib)*q10fac*msfac
               dgrate(L,jb) = dgrat2(L,ib)*q10fac

               Select Case(L)
               Case(2)
                  dkrw12(jb) = dkw212(ib)
                  dkrs12(jb) = dks212(ib)
               Case(3)
                  dkrw13(jb) = dkw213(ib)
                  dkrw23(jb) = dkw223(ib)
                  dkrs13(jb) = dks213(ib)
                  dkrs23(jb) = dks223(ib)
               End Select

            Else If (ib /= 1) Then
               modfc        = (t - tthkns)/delx(jb)
               dwrate(L,jb) = (dwrat2(L,ib)*(One-modfc)+dwrat2(L,ibm1)*modfc) * q10fac*msfac
               dsrate(L,jb) = (dsrat2(L,ib)*(One-modfc)+dsrat2(L,ibm1)*modfc) * q10fac*msfac
               dgrate(L,jb) = (dgrat2(L,ib)*(One-modfc)+dgrat2(L,ibm1)*modfc) * q10fac

               Select Case(L)
               Case(2)
                  dkrw12(jb) = dkw212(ib)*(One-modfc) + dkw212(ibm1)*modfc
                  dkrs12(jb) = dks212(ib)*(One-modfc) + dks212(ibm1)*modfc
               Case(3)
                  dkrw13(jb) = dkw213(ib)*(One-modfc) + dkw213(ibm1)*modfc
                  dkrw23(jb) = dkw223(ib)*(One-modfc) + dkw223(ibm1)*modfc
                  dkrs13(jb) = dks213(ib)*(One-modfc) + dks213(ibm1)*modfc
                  dkrs23(jb) = dks223(ib)*(One-modfc) + dks223(ibm1)*modfc
               End Select

               ib     = ib - 1
               tthkns = tthkns + thkns(ib)
            End If
         End Do

      End Subroutine Aux2e

   End Subroutine q10dk

End Module m_chem

