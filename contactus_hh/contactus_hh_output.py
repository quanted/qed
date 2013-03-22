# -*- coding: utf-8 -*-

import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import cgi
import cgitb
from google.appengine.api import mail

cgitb.enable()

def sendanemail(name,subj, rply, msg):
    message = mail.EmailMessage(sender="Ubertool Support <pypest@pypest.appspotmail.com>")
    message.subject = subj
    message.to = "Ubertool Support <ecoubertool@gmail.com>" 
    message.reply_to= rply
    message.cc = rply   
    message.body = '''A message submitted by %s, %s \n''' %(name, rply)
    message.body = message.body+msg
    message.send()

class contactusOutputPage(webapp.RequestHandler):
    def post(self):        
        form = cgi.FieldStorage()
        name = form.getvalue('nm_name')
        rply = form.getvalue('nm_email')
        subj = form.getvalue('nm_sub')
        msg = form.getvalue('nm_msg')
        
        sendanemail(name,subj, rply, msg)

        templatepath = os.path.dirname(__file__) + '/../templates/'
        html = template.render(templatepath + '01hh_uberheader.html', {'title':'Ubertool'})
        html = html + template.render(templatepath + '02hh_uberintroblock_nomodellinks.html', {'model':''})
        html = html + template.render (templatepath + '03hh_ubertext_links_left.html', {})
        html = html + template.render(templatepath + '04ubercontact_start.html', {'model':''})
        html = html + template.render(templatepath + '04ubercontact_end.html', {'sub_title': ''})
        html = html + template.render(templatepath + '05hh_ubertext_links_right.html', {})
        html = html + template.render(templatepath + '06hh_uberfooter.html', {'links': ''})
        self.response.out.write(html)
        
app = webapp.WSGIApplication([('/.*', contactusOutputPage)], debug=True)

        
def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
