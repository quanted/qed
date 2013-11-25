import csv
import przm_batchmodel


filepath="przm_batch.csv"

chem_name = []
NOA = []
Scenarios = []
Unit = []
appdate = []
apm = []
apr = []
cam = []
depi = []

# Apt_p = []

# Ap_m_l = []

def loop_html(thefile):
    f=open(thefile, 'r')
    reader = csv.reader(f)
    header = reader.next()
    exclud_list = ['', " ", "  ", "   ", "    ", "     ", "      ", "       ", "        ", "         ", "          "]
    i=1

    iter_html=""
    for row in reader:
        if row[3] in exclud_list:
            break
        chem_name_temp = str(row[0])
        chem_name.append(chem_name_temp)
        NOA_temp = str(row[1])
        NOA.append(NOA_temp)
        Scenarios_temp = str(row[2])
        Scenarios.append(Scenarios_temp)
        Unit_temp = str(row[3])
        Unit.append(Unit_temp)
        appdate_temp = str(row[4]).split(',')
        appdate.append(appdate_temp)
        apm_temp = str(row[5]).split(',')
        apm.append(apm_temp)
        apr_temp = str(row[6]).split(',')
        apr.append(apr_temp)
        cam_temp = str(row[7]).split(',')
        cam.append(cam_temp)
        depi_temp = str(row[8]).split(',')
        depi.append(depi_temp)
        przm_temp = przm_batchmodel.przm_batch(chem_name_temp, NOA_temp, Scenarios_temp, Unit_temp, appdate_temp, apm_temp, apr_temp, cam_temp, depi_temp)

        # print apr_temp
        print vars(przm_temp)
        i=i+1


a=loop_html(filepath)

