import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from tasks import http_check_pages
import webapp2
from google.appengine.api import mail

results_html = str(http_check_pages.cron_check_pages())
mail.send_mail("purucker.tom@gmail.com", "purucker.tom@gmail.com", "ubertool cron_check_pages.py results", results_html)

#print("before")
#check_results = http_check_pages.check_pages("eco")
#print("after")