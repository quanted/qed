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
from ubertool.ecosystem_inputs import EcosystemInputs
import logging


class UbertoolEcosystemInputsConfigurationPage(webapp.RequestHandler):
    def post(self):
        logger = logging.getLogger("UbertoolEcosystemInputsConfigurationPage")
        form = cgi.FieldStorage()
        config_name = str(form.getvalue('config_name'))
        user = users.get_current_user()
        q = db.Query(EcosystemInputs)
        q.filter('user =',user)
        q.filter("config_name =", config_name)
        eco_inputs = q.get()
        if eco_inputs is None:
            eco_inputs = EcosystemInputs()
        if user:
            logger.info(user.user_id())
            eco_inputs.user = user
        eco_inputs.config_name = config_name
        eco_inputs.x_poc = float(form.getvalue('x_poc'))
        eco_inputs.x_doc = float(form.getvalue('x_doc'))
        eco_inputs.c_ox = float(form.getvalue('c_ox'))
        eco_inputs.w_t = float(form.getvalue('w_t'))
        eco_inputs.c_ss = float(form.getvalue('c_ss'))
        eco_inputs.oc = float(form.getvalue('oc'))
        eco_inputs.put()
        self.redirect("run_ubertool.html")
        
app = webapp.WSGIApplication([('/.*', UbertoolEcosystemInputsConfigurationPage)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

