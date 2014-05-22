# Library for "global" functions

import webapp2 as webapp
from google.appengine.ext.webapp import template
import os
# import inspect

# Check Cookie
def SkinChk(ChkCookie, titleText):
    templatepath = os.path.dirname(__file__) + '/../templates/'
    if ChkCookie == 'EPA':
        html = template.render(templatepath + '01uberheaderEPA.html', {'title':titleText})
    else:
        html = template.render(templatepath + '01uberheader.html', {'title':titleText})
    return html

def SkinChkMain(ChkCookie):
    templatepath = os.path.dirname(__file__) + '/../templates/'
    if ChkCookie == 'EPA':
        html = template.render(templatepath + '01uberheader_mainEPA.html', {})
    else:
        html = template.render(templatepath + '01uberheader_main.html', {})
    return html

# def inspectTest():
#     inspectTestVar = inspect.getmodule(frm[0]).__name__
#     test = """
#     <p>BLAH BLAH BLAH: %s</p>
#     """%inspectTestVar
#     return test