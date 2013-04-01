! common block to store variables to be output with next message
      COMMON /CHMSG / ICNt , IMSvl , RCNt , RMSvl , DATim , CCNt
      INTEGER ICNt , IMSvl(mxmsi) , RCNt , DATim(5) , CCNt
      REAL RMSvl(mxmsr)
      COMMON /CHMSGC/ CMSvl
      CHARACTER*1 CMSvl(mxmsc)
