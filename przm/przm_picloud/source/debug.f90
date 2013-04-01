
Module m_Debug

   ! This module collects all debugging variables and subroutines.
   !
   ! Mark debug statements in przm with "! m_debug"
   Implicit None
   Private
   Public :: Set_debug
   Logical, Save, Public :: new_code = .False.
   Logical, Save, Public :: timing_program = .False.
   Integer, Save, Public :: u0debug = 802

   ! Options are read from the environmental variable przm_Env
   Character(Len=*), Parameter :: przm_Env = 'przm_'

Contains

   Subroutine Set_debug()

      ! Set debug options.
      ! Messages are issued only if the environmental is not empty.
      Implicit None
      Character(Len=100) :: tbuf
      Integer :: tlen
      Integer :: uu, i

      Call GetEnv(przm_Env, tbuf)
      tlen = Len_Trim(tbuf)
      If (tlen <= 0) Then
         ! Messages are issued only if the environmental is not empty.
         Return
      End If

      ! Options:
      ! --new_code : set variable "new_code" to .True.
      ! --timing : print timing value
      new_code = (Index(tbuf(1:tlen), '--new_code') > 0)
      timing_program = (Index(tbuf(1:tlen), '--timing') > 0)

      uu = u0debug
      Do i = 1, 2
         Write (uu, 9120) przm_Env, tbuf(1:tlen)
9120     Format (//, ' ====== %', a, '% ==>', a, '<==')

         Write (uu, 9140) ' new_code == ', new_code
         Write (uu, 9140) ' timing_program == ', timing_program
9140     Format (1x, a, L1)

         Write (uu, '(//)')

         uu = 6
      End Do

   End Subroutine Set_debug

End Module m_Debug

