import httplib
import http_check_tables
from django.utils.safestring import mark_safe
import datetime
import time



def check_pages(framework):
    #url needs to be modified to know what version/branch currently on and to run locally
    #print os.environ['CURRENT_VERSION_ID']
    #version_id = self.request.environ["CURRENT_VERSION_ID"].split('.')[1]
    #timestamp = long(version_id) / pow(2,28) 
    #version = datetime.datetime.fromtimestamp(timestamp).strftime("%d/%m/%y %X")
    #print version_id
    #print timestamp
    #print version 
    start_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    start_time = time.time()

    url = "pypest.appspot.com"
    if(framework=="unter"):
        models = ["exponential", "logistic", "gompertz", "foxsurplus", "maxsus", "yulefurry", "fellerarley", "leslie", "lesliedr", "leslie_probit", 
            "loons", "webice", "beekhoury", "beepop", "hopomo", "es_mapping"]
    elif(framework=="hh"):
        models = ["fdadiet", "idream", "ocexposure", "resexposure", "swim", "efast", "wpem", "iaqx", "antimicrobial", "consexpo", "rddr", "hedgas", "benchdose", "qsarhe",
            "dietexphe", "orehe", "inerts", "qsarreg", "dietexpreg", "orereg"]
    elif(framework=="eco"):
        models = ["terrplant", "sip", "stir", "dust", "trex2", "therps", "iec", "agdrift", "earthworm", "rice", "geneec", "kabam", "przm",
            "przm5", "exams", "pfam", "przm_exams", "vvwm", "swc", "ddm", "superprzm", "sam"]            
    #qaqc takes too long and needs to be run separately
    pagenames=["_description.html", "_input.html", "_algorithms.html", "_references.html", "_batchinput.html", "_history.html"]
    url_strings = []
    http_counter = []
    http_page = []
    http_status = []
    http_reason = []

    for model in models:
        for pagename in pagenames:
            url_strings.append("/" + model + pagename)

    conn = httplib.HTTPConnection(host=url)
    counter = 0
    counter_ok = 0
    for url_string in url_strings:
        #conn = httplib.HTTPConnection(host=url)
        counter = counter + 1
        conn.request("GET",url_string)
        r1 = conn.getresponse()
        #xx = "<p>" + xx + str(counter) + " " + mark_safe("<a href='http://" + url + url_string + "'>" + url_string + "</a>") + " " + str(r1.status) + " " + r1.reason + "<br>"
        http_counter.append(counter) 
        http_page.append(mark_safe("<a href='http://" + url + url_string + "'>" + url_string + "</a>")) 
        http_status.append(r1.status)
        http_reason.append(r1.reason)
        if r1.status == 200: counter_ok = counter_ok + 1

    http_headings = http_check_tables.gethttpheader()
    end_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    end_time=time.time()
    elapsed_time = "Elapsed time was %g seconds" % (end_time - start_time) + "."
    time_text = "Started " + start_date + "; Ended " + end_date + "; " + elapsed_time + "<br>"
    http_html = http_check_tables.table_report_integration_results(http_headings, http_counter, http_page, http_status, http_reason, counter, counter_ok, time_text)
    return http_html
