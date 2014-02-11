#import http_check_pages
import webapp2
from google.appengine.api import mail

mail.send_mail("purucker.tom@gmail.com", "purucker.tom@gmail.com", "gae sendmail test", "test")

#print("before")
#check_results = http_check_pages.check_pages("eco")
#print("after")