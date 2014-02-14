import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import http_check_pages
import webapp2
from google.appengine.api import mail


results_html = http_check_pages.check_pages("eco")
mail.send_mail("purucker.tom@gmail.com", "purucker.tom@gmail.com", "gae sendmail test", results_html)

#print("before")
#check_results = http_check_pages.check_pages("eco")
#print("after")