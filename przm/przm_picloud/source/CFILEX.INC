!     Include File CFILEX.INC

! FILOPC - number of files open
! FPRZIN - przm input file unit number
! FPRZRS - przm restart file unit number
! FPRZOT - przm output file unit number
! FMETEO - meteorology file unit number
! FSPTIC - septic effluent file unit number
! FNITAD - nitrogen atmospheric deposition file unit number
! FVADIN - vadoft input file unit number
! FVADOT - vadoft output file unit number
! FVTP10 - vadoft tape 10 file unit number
! FVRSTF - vadoft flow restart file unit number
! FVRSTT - vadoft transport restart file unit number
! FTMSRS - time series file unit number
! FMCIN  - ???
! FMCOUT - ???
! FMCOU2 - ???
! FCON   - ???
! FECHO  - ???
! FWDMS  - wdms file unit number

      INTEGER FILopc , FPRzin(mxzone) , FPRzrs(mxzone) , FPRzot(mxzone) &
     &        , FMEteo(mxzone) , FSPtic(mxzone) , FNItad(mxzone) ,      &
     &        FVAdin(mxnszo) , FVAdot(mxnszo) , FVTp10(mxnszo) ,        &
     &        FVRstf(mxnszo) , FVRstt(mxnszo) , FTMsrs(mxzone) , FMCin ,&
     &        FMCout , FMCou2 , FCOn , FECho , FWDms
      COMMON /FILEX / FILopc , FPRzin , FPRzrs , FWDms , FPRzot ,       &
     &                FMEteo , FSPtic , FNItad , FVAdin , FVAdot ,      &
     &                FVTp10 , FVRstf , FVRstt , FTMsrs , FMCin ,       &
     &                FMCout , FMCou2 , FCOn , FECho
