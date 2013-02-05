import os
os.environ['DJANGO_SETTINGS_MODULE']='settings'
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import db
import cgi
import cgitb
cgitb.enable()
import datetime
import logging


class UbertoolSelectChemicalConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolSelectChemicalConfigurationPage")
        form = cgi.FieldStorage()
        user = users.get_current_user()
        if user:
            logger.info(user.user_id())
        chemical_name = form.getvalue('formulated_product_name')
        pc_code = "123-456-789"
        cookie_string = 'formulated_product_name=%s'%pc_code
        self.response.headers.add_header('Set-Cookie',cookie_string)
        self.redirect("site_data.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolSelectChemicalConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
