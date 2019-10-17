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



PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

hms_endpoint = "hms/workflow/precip_compare"
hms_endpoints = ["hms/workflow/precip_compare", "hms/meteorology/precipitation"]



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
		self.qed_username = "qeduser"
		self.hms_username = "hmsuser"
		self.hashed_pass = None  # qed-wide login pass
		self.hashed_pass_hms = None  # hms-specific pass for precip compare workflow
		self.apps_with_password = ["hms", "pram", "cts/biotrans", "cts/stress", "hms/workflow/precip_compare"]
		self.hashed_pass = self.get_hashed_password("secret_key_login.txt")
		self.hashed_pass_hms = self.get_hashed_password("secret_key_hms.txt")

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def get_hashed_password(self, filename):
		"""
		Reads file where hashed pass is stored (.gitignored).
		filename - name of hased pass file, with extension (e.g., secret_key.txt).
		"""
		try:
			_hash_pass = open(os.path.join(PROJECT_ROOT, 'secrets', filename), 'r')  # read in hashed password from file
			return _hash_pass.read().encode('utf-8')  # encode for bcrypt
		except Exception as e:
			logging.warning("Exception reading hashed password from file..")
			return None

	def check_authentication(self, request, access_type="qed"):
		"""
		Checks access based on username and requested url.
		"""
		current_user = request.user  # current user object

		if access_type == "qed":
			if not current_user.username == self.qed_username:
				return False
			if not current_user.is_authenticated:
				return False
			return True

		elif access_type == "hms":
			if not current_user.username == self.hms_username:
				return False
			if not current_user.is_authenticated:
				return False
			return True

		return False

	def process_view(self, request, view_func, view_args, view_kwargs):
		assert hasattr(request, 'user')
		path = request.path
		redirect_path = request.POST.get('next', "")
		user = request.POST.get('user')
		has_access = False

		if not self.needs_qed_password(path + redirect_path):
			return

		# Check that user is autheniticated for the page its trying to access
		for hms_endpoint in hms_endpoints:
			if hms_endpoint in (path + redirect_path):
				has_access = self.check_authentication(request, "hms")
				break
		else:
			has_access = self.check_authentication(request, "qed")

		if has_access:
			return

		if not self.login_url.match(path):
			# Returns login page:
			return redirect('{}?next={}'.format(settings.REQUIRE_LOGIN_PATH, path))

		if request.POST and self.login_url.match(path):
			# Checks login attempt:
			return self.login_auth(request)

	def needs_qed_password(self, path):
		"""
		Checks requested path against apps that need a
		password wall. Returns True if path has app name
		in it that needs password protected.
		"""
		for app in self.apps_with_password:
			if app in path:
				return True
		return False

	def handle_site_wide_login(self, username, password, next_page):
		# check if username is correct:
		if username != self.qed_username:
			logging.warning("username {} incorrect..".format(username))
			return True
		# check if password is correct:
		if not bcrypt.checkpw(password.encode('utf-8'), self.hashed_pass):
			logging.warning("password incorrect for user: {}".format(username))
			return True
		return False

	def handle_hms_endpoint_login(self, username, password, next_page):
		# check if username is correct:
		if username != self.hms_username:
			logging.warning("username {} incorrect..".format(username))
			return True
		# check if password is correct:
		if not bcrypt.checkpw(password.encode('utf-8'), self.hashed_pass_hms):
			logging.warning("password incorrect for user: {}".format(username))
			return True
		return False

	def login_auth(self, request):

		username = request.POST.get('username')
		password = request.POST.get('password')
		next_page = request.POST.get('next')

		# redirect if hashed pw unable to be set, or user didn't enter password:
		if not self.hashed_pass or not password:
			return redirect('/login?next={}'.format(next_page))

		# Checks if username and password is correct:
		for hms_endpoint in hms_endpoints:
			if hms_endpoint in next_page:
				# Adds hms-specific password to endpoint:
				show_login = self.handle_hms_endpoint_login(username, password, next_page)
				break
		else:
			# Assumes other endpoints are for qed-wide password
			show_login = self.handle_site_wide_login(username, password, next_page)

		if show_login == True:
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

	login_text = "<h3>Enter QED credentials to continue</h3>"
	additional_text = ""  # e.g., directions for access

	for hms_endpoint in hms_endpoints:
		if hms_endpoint in next_page:
			login_text = """
			<h3>Click <a href="https://www.epa.gov/ceam/forms/contact-hms-helpdesk" target="_blank">here</a>
			to request user ID and password.</h3>
			"""
			break

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
	html += render_to_string('login_prompt.html', {'next': next_page, 'text': login_text}, request=request)
	html += render_to_string('09epa_drupal_ubertool_css.html', {})
	html += render_to_string('10epa_drupal_footer.html', {})
	response = HttpResponse()
	response.write(html)
	return response