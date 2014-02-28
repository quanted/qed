copy PA1App-P.RUN PRZM3.RUN
call "przm3123_win.exe"
call "exams_win.exe" PA1App-P.EXA PA1App-P.PEX PA1App-P.ERR PA1App-P.WRN
copy report.xms PA1App-P.XMS
copy ecoriskc.xms PA1App-P.YMS
copy ecotoxc.xms PA1App-P.ZMS
copy cprzm31.hyd CPA1AppP1.HYD
copy cprzm31.cnc CPA1AppP1.CNC
copy cprzm31.msb CPA1AppP1.MSB
del report.xms
del ecoriskc.xms
del ecotoxc.xms
del p2e*.*
del *.plt
del *.prn
del *.prz
del *.zts
del *.msb