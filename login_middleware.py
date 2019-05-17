from django.conf import settings
from django.contrib.auth import login as django_login
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
import re
import os
import logging
import bcrypt



class RequireLoginMiddleware:
	"""
	Require Login middleware. If enabled, each Django-powered page will
	require authentication.
	
	If an anonymous user requests a page, he/she is redirected to the login
	page set by REQUIRE_LOGIN_PATH or /accounts/login/ by default.
	"""
	def __init__(self, get_response):
		self.get_response = get_response
		self.login_url = re.compile(settings.REQUIRE_LOGIN_PATH)
		self.username = "qeduser"
		self.hashed_pass = None
		self.apps_with_password = ["", "cts"]
		try:
			_hash_pass = open('secrets/secret_key_login.txt', 'r')  # read in hashed password from file
			self.hashed_pass = _hash_pass.read().encode('utf-8')  # encode for bcrypt
		except Exception as e:
			logging.warning("Exception reading hashed password from file..")
			self.hashed_pass = None

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def process_view(self, request, view_func, view_args, view_kwargs):
		assert hasattr(request, 'user')
		path = request.path
		redirect_path = request.POST.get('next', "")
		if not self.needs_password(path + redirect_path):
			return
		if not request.user.is_authenticated:
			if not self.login_url.match(path):
				return redirect('{}?next={}'.format(settings.REQUIRE_LOGIN_PATH, path))
			if request.POST and self.login_url.match(path):
				return self.login_auth(request)

	def needs_password(self, path):
		"""
		Checks requested path against apps that need a
		password wall. Returns True if path has app name
		in it that needs password protected.
		"""
		for app in self.apps_with_password:
			if app in path:
				return True
		return False

	def login_auth(self, request):

		username = request.POST.get('username')
		password = request.POST.get('password')
		next_page = request.POST.get('next')

		# redirect if hashed pw unable to be set, or user didn't enter password:
		if not self.hashed_pass or not password:
			return redirect('/login?next={}'.format(next_page))
		# check if username is correct:
		if username != self.username:
			logging.warning("username {} incorrect..".format(username))
			return redirect('/login?next={}'.format(next_page))
		# check if password is correct:
		if not bcrypt.checkpw(password.encode('utf-8'), self.hashed_pass):
			logging.warning("password incorrect for user: {}".format(username))
			return redirect('/login?next={}'.format(next_page))
		# Add user to django db if not already there:
		if not User.objects.filter(username=username).exists():
			_user = User.objects.create_user(username, 'email@address.com', password)
			_user.save()  # save username and plain pass to django db

		user = authenticate(username=username, password=password)  # auths, then returns user obj (too redundant)

		if user is not None:
			if user.is_active:
				# Redirect to a success page.
				django_login(request, user)  # is this needed?? (todo: logout if inactive for some time)
				return redirect(next_page)
			else:
				# Return a 'disabled account' error message
				return redirect('/login?next={}'.format(next_page))
		else:
			# Return an 'invalid login' error message.
			return redirect('/login?next={}'.format(next_page))



#######################################################################################
################################ User Login Pages #####################################
#######################################################################################

def login(request):
	next_page = request.GET.get('next')
	html = render_to_string('01epa_drupal_header.html', {
		'SITE_SKIN': os.environ['SITE_SKIN'],
		'TITLE': u"Q.E.D."
	})
	html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
	html += render_to_string('03epa_drupal_section_title_splash.html', {})
	html += render_to_string('06ubertext_start_index_drupal.html', {
		'TITLE': 'User Login',
		'TEXT_PARAGRAPH': ""
	})
	html += render_to_string('07ubertext_end_drupal.html', {})
	html += render_to_string('login_prompt.html', {'next': next_page}, request=request)
	html += render_to_string('09epa_drupal_ubertool_css.html', {})
	html += render_to_string('10epa_drupal_footer.html', {})
	response = HttpResponse()
	response.write(html)
	return response