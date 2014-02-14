import httplib
from tasks import http_check_tables
from django.utils.safestring import mark_safe
import datetime
import time

unter_models = ["exponential", "logistic", "gompertz", "foxsurplus", "maxsus", "yulefurry", "fellerarley", "leslie", "lesliedr", "leslie_probit", 
            "loons", "webice", "beekhoury", "beepop", "hopomo", "es_mapping"]
eco_models = ["terrplant", "sip", "stir", "dust", "trex2", "therps", "iec", "agdrift", "agdrift_trex", "earthworm", "rice", "geneec", "kabam", "przm",
            "przm5", "exams", "pfam", "przm_exams", "vvwm", "swc", "ddm", "superprzm", "sam"]
hh_models = ["fdadiet", "idream", "ocexposure", "resexposure", "swim", "efast", "wpem", "iaqx", "antimicrobial", "consexpo", "rddr", "hedgas", "benchdose", "qsarhe",
            "dietexphe", "orehe", "inerts", "qsarreg", "dietexpreg", "orereg"]
html_page_names = ["_description.html", "_input.html", "_algorithms.html", "_references.html", "_batchinput.html", "_history.html"]
url = "pypest.appspot.com"

def cron_check_pages():
    frameworks = [eco_models, hh_models, unter_models]
    pagenames=html_page_names
    url_strings = []
    http_counter = []
    http_page = []
    http_status = []
    http_reason = []
    fail_list = []
    for framework in frameworks:
        models = framework
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
        #http_page.append(mark_safe("<a href='http://" + url + url_string + "'>" + url_string + "</a>")) 
        if r1.status != 200: 
            fail_list.append(url_string)
        #http_reason.append(r1.reason)
        if r1.status == 200: counter_ok = counter_ok + 1
    counter_fail = counter - counter_ok
    cron_text = 'This is an automated email. ' + '\n' + str(counter_fail) + ' of ' + str(counter) + ' pages are not serving correctly:' + '\n'
    for fail in fail_list:
        cron_text = cron_text + url + fail + '\n'
    return cron_text

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
    if(framework=="unter"):
        models = unter_models
    elif(framework=="hh"):
        models = hh_models
    elif(framework=="eco"):
        models = eco_models         
    #qaqc takes too long and needs to be run separately
    pagenames=html_page_names
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
