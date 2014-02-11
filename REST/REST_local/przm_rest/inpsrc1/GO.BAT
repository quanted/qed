copy "C:\Program Files (x86)\express\examsenv\*.exv"
call runprzm.bat
"C:\Program Files (x86)\express\progs\mkhed.exe" 0
del report.xms
del ecoriskc.xms
del ecotoxc.xms
del p2e*.*
del *.plt
del *.prn
del *.prz
del *.zts
del *.msb
