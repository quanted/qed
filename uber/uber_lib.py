# Library for "global" functions

import webapp2 as webapp
from google.appengine.ext.webapp import template
import os
import inspect

# Check Cookie
# class ChkCookieClass(webapp.RequestHandler):
def SkinChk(ChkCookie):
    templatepath = os.path.dirname(__file__) + '/../templates/'
    # ChkCookie = self.request.cookies.get("ubercookie")
    if ChkCookie == 'EPA':
        html = template.render(templatepath + '01uberheaderEPA.html', {'title':'Ubertool'})
    else:
        html = template.render(templatepath + '01uberheader.html', {'title':'Ubertool'})
    return html

def SkinChkMain(ChkCookie):
    templatepath = os.path.dirname(__file__) + '/../templates/'
    # ChkCookie = self.request.cookies.get("ubercookie")
    if ChkCookie == 'EPA':
        html = template.render(templatepath + '01uberheader_mainEPA.html', {'title':'Ubertool'})
    else:
        html = template.render(templatepath + '01uberheader_main.html', {'title':'Ubertool'})
    return html

def inspectTest():
    inspectTestVar = inspect.getmodule(frm[0]).__name__
    test = """
    <p>BLAH BLAH BLAH: %s</p>
    """%inspectTestVar
    return test