from urlparse import urlparse
import time
import Cookie
import cgi
import cgitb
cgitb.enable()
import webapp2 as webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import logging
import sys
from django.utils import simplejson
import openid
from openid.extensions import sreg
from openid.store.filestore import FileOpenIDStore
from openid.consumer import discover
from datetime import datetime,timedelta
import urllib
from google.appengine.api import urlfetch
import json
sys.path.append("utils")
import json_utils
from datetime import datetime

logger = logging.getLogger("AuthService")

backend_auth_server = "http://127.0.0.1:8887"

def quoteattr(s):
    qs = cgi.escape(s, 1)
    return '"%s"' % (qs,)


class OpenIDAuthService(webapp.RequestHandler):

    def get(self,method):
        #print "in OpenID AUth service get with cookies: "
        #print self.request.cookies
        self.path = self.request.url
        self.parsed_uri = urlparse(self.path)
        self.query = {}
        for k, v in cgi.parse_qsl(self.parsed_uri[4]):
            self.query[k] = v
        print self.query
        self.setUser()
        path = self.parsed_uri[2].lower()
        if path == '/openidserver':
           self.serverEndPoint(self.query)
        elif path == '/loginsubmit':
            self.doLogin()
        else:
            self.response.status ='404 Not Found'

    def post(self,method):
        #print "in OpenID AUth service post with request: "
        #print self.request
        self.path = self.request.url
        self.parsed_uri = urlparse(self.path)

        data = json.loads(self.request.body)
        data = json_utils.convert(data)

        path = self.parsed_uri[2]
        if path == '/login':
            logger.info(data)
            self.doBasicLogin(data)
        elif path == '/allow':
            self.handleAllow(self.query)
        else:
            self.response.status ='404 Not Found'

    def handleAllow(self, query):
        # pretend this next bit is keying off the user's session or something,
        # right?
        request = self.server.lastCheckIDRequest.get(self.user)

        if 'yes' in query:
            if 'login_as' in query:
                self.user = self.query['login_as']

            if request.idSelect():
                identity = self.server.base_url + 'id/' + query['identifier']
            else:
                identity = request.identity

            trust_root = request.trust_root
            if self.query.get('remember', 'no') == 'yes':
                self.server.approved[(identity, trust_root)] = 'always'

            response = self.approved(request, identity)

        elif 'no' in query:
            response = request.answer(False)

        else:
            assert False, 'strange allow post.  %r' % (query,)

        self.displayResponse(response)


    def setUser(self):
        self.user = self.request.GET['user']

    def isAuthorized(self, identity_url, trust_root):
        if self.user is None:
            return False

        if identity_url != self.server.base_url + 'id/' + self.user:
            return False

        key = (identity_url, trust_root)
        return self.server.approved.get(key) is not None

    def serverEndPoint(self, query):
        logger.info("In serverEndPoint method")
        try:
            request = self.server.openid.decodeRequest(query)
        except server.ProtocolError, why:
            self.displayResponse(why)
            return
        logger.info("request:"+request)
        if request is None:
            # Display text indicating that this is an endpoint.
            self.showAboutPage()
            return

        if request.mode in ["checkid_immediate", "checkid_setup"]:
            self.handleCheckIDRequest(request)
        else:
            response = self.server.openid.handleRequest(request)
            self.displayResponse(response)

    def addSRegResponse(self, request, response):
        sreg_req = sreg.SRegRequest.fromOpenIDRequest(request)

        # In a real application, this data would be user-specific,
        # and the user should be asked for permission to release
        # it.
        sreg_data = {
            'nickname':self.user
            }

        sreg_resp = sreg.SRegResponse.extractResponse(sreg_req, sreg_data)
        response.addExtension(sreg_resp)

    def approved(self, request, identifier=None):
        response = request.answer(True, identity=identifier)
        self.addSRegResponse(request, response)
        return response

    def handleCheckIDRequest(self, request):
        is_authorized = self.isAuthorized(request.identity, request.trust_root)
        if is_authorized:
            response = self.approved(request)
            self.displayResponse(response)
        elif request.immediate:
            response = request.answer(False)
            self.displayResponse(response)
        else:
            self.server.lastCheckIDRequest[self.user] = request
            self.showDecidePage(request)

    def displayResponse(self, response):
        try:
            webresponse = self.server.openid.encodeResponse(response)
        except server.EncodingError, why:
            text = why.response.encodeToKVForm()
            self.showErrorPage('<pre>%s</pre>' % cgi.escape(text))
            return

        self.send_response(webresponse.code)
        for header, value in webresponse.headers.iteritems():
            self.send_header(header, value)
        self.writeUserHeader()
        self.end_headers()

        if webresponse.body:
            self.wfile.write(webresponse.body)

    def doLogin(self):
        logger.info('self.query')
        logger.info(self.query)
        if 'submit' in self.query:
            if 'user' in self.query:
                self.user = self.query['user']
                results = self.submitOpenId(self.user)
                login_data = json.loads(results.content)
                logger.info("Login results")
                logger.info(login_data)
                sid = json_utils.convert(login_data[u'sid'])
                expires = json_utils.convert(login_data[u'expires'])
                userid = json_utils.convert(login_data[u'userid'])
                self.response.set_cookie('SACSID',value=sid)
                self.response.set_cookie('dev_appserver_login', value=sid)
                self.response.set_cookie('user', value=userid)
            else:
                self.user = None
            self.redirect(self.query['success_to'])
        elif 'cancel' in self.query:
            self.redirect(self.query['fail_to'])
        else:
            assert 0, 'strange login %r' % (self.query,)

    def doBasicLogin(self, params):
        config_params = {}
        config_params['password'] = params['password']
        userid = params['userid']
        form_data = simplejson.dumps(config_params)
        url = backend_auth_server+"/user/login/"+userid
        results = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
        login_data = json.loads(results.content)
        logger.info("Login results")
        logger.info(login_data)
        sid = json_utils.convert(login_data[u'sid'])
        expires = json_utils.convert(login_data[u'expires'])
        userid = json_utils.convert(login_data[u'userid'])
        decision = json_utils.convert(login_data[u'decision'])
        decision_data = {};
        logger.info("decision: ")
        logger.info(decision)
        decision_data['decision'] = decision
        self.response.set_cookie('SACSID',value=sid)
        self.response.set_cookie('dev_appserver_login', value=sid)
        self.response.set_cookie('user', value=userid)
        self.response.headers['Content-Type'] = 'application/json'
        batch_json = simplejson.dumps(decision_data)
        self.response.out.write(batch_json)


    def submitOpenId(self, openId):
        config_params = {}
        config_params['openid'] = openId
        form_data = simplejson.dumps(config_params)
        url = backend_auth_server+"/user/openid/login"
        results = urlfetch.fetch(url=url,
                        payload=form_data,
                        method=urlfetch.POST,
                        headers={'Content-Type': 'application/json'})
        return results

    def redirect(self, url):
        self.response.status ='302'
        self.response.headers['Location'] = url

    def writeUserHeader(self):
        if self.user is None:
            t1970 = time.gmtime(0)
            expires = time.strftime(
                'Expires=%a, %d-%b-%y %H:%M:%S GMT', t1970)
            self.send_header('Set-Cookie', 'user=;%s' % expires)
        else:
            self.send_header('Set-Cookie', 'user=%s' % self.user)

class GoogleAuthService(webapp.RequestHandler):

    def get(self):
        pass

    def post(self):
        pass

class BasicAuthService(webapp.RequestHandler):

    def get(self):
        pass

    def post(self):
        pass

app = webapp.WSGIApplication([('/(.*)', OpenIDAuthService),
                                ('/auth/google', GoogleAuthService),
                                ('/auth/basic', BasicAuthService)], debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()

