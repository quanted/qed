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

hms_protected = ["hydrology", "workflow", "meteorology"]
hms_public = [
	"workflow/precip_data_extraction/",
	"workflow/precip_compare",
	"meteorology/precipitation",
	"hydrology/evapotranspiration/"
]

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
		self.hms_admin = "hmsadmin"
		self.hms_username = "hmsuser"
		self.hashed_pass = {}		# dictionary of user:passwords
		self.apps_with_password = ["hms", "pram", "cts/biotrans", "cts/stress", "cyanweb"]
		self.hms_protected = ["hydrology", "workflow", "meteorology"]
		self.hms_public = [
			"workflow/precip_data_extraction/",
			"workflow/precip_compare",
			"meteorology/precipitation",
			"hydrology/evapotranspiration/"
		]
		self.open_endpoints = [
			"rest/api/"
		]
		self.set_password_via_config()
		self.load_passwords()

	def __call__(self, request):
		response = self.get_response(request)
		return response

	def load_passwords(self):
		"""
		Loads passwords for each user from the secrets file.
		:return:
		"""
		for a in self.apps_with_password:
			if "hms" in a:
				self.hashed_pass["hms_public"] = self.get_hashed_password("secret_key_hms.txt")
				self.hashed_pass["hms_private"] = self.get_hashed_password("secret_key_hms_private.txt")
			elif "pram" in a:
				self.hashed_pass["qed"] = self.get_hashed_password("secret_key_login.txt")
			elif "cts" in a:
				self.hashed_pass["qed"] = self.get_hashed_password("secret_key_login.txt")

	def set_password_via_config(self):
		"""
		Modifies apps_with_password list based on deployment environment.
		Used for fine-tuning passwords on apps on a server-by-server basis.
		"""
		env_name = os.environ.get('ENV_NAME')
		if not env_name:
			return
		if env_name == 'gdit_aws_dev':
			self.apps_with_password.append("cts")  # adds password for all of cts on gdit aws dev server

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

		elif access_type == "hms_public":
			if not current_user.username == self.hms_username:
				return False
			if not current_user.is_authenticated:
				return False
			return True

		elif access_type == "hms_private":
			if not current_user.username == self.hms_admin:
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
		token = request.GET.get('token')  # potential 'token' query for cyano-web password reset

		if not self.needs_qed_password(path + redirect_path):
			return

		# Check that user is autheniticated for the page its trying to access
		if any(endpoint in (path + redirect_path) for endpoint in self.hms_public):
			has_access = self.check_authentication(request, "hms_public")
		if has_access is False:
			if any(endpoint in (path + redirect_path) for endpoint in self.hms_protected):
				has_access = self.check_authentication(request, "hms_private")
			else:
				has_access = self.check_authentication(request, "qed")

		if has_access:
			return

		if not self.login_url.match(path):
			# Returns login page:
			if token:
				return redirect('{}?next={}?token={}'.format(settings.REQUIRE_LOGIN_PATH, path, token))
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
		if any(p in path for p in self.open_endpoints):
			return False
		for app in self.apps_with_password:
			if app in path and "hms" in app:
				if any(hms_app in path for hms_app in self.hms_protected):
					return True
			elif app in path:
				return True
		return False

	def handle_site_wide_login(self, username, password, next_page):
		# check if username is correct:
		if username != self.qed_username:
			logging.warning("username {} incorrect..".format(username))
			return True
		# check if password is correct:
		if not bcrypt.checkpw(password.encode('utf-8'), self.hashed_pass["qed"]):
			logging.warning("password incorrect for user: {}".format(username))
			return True
		return False

	def handle_hms_endpoint_login(self, username, password, next_page):
		# check if username is correct:
		if username != self.hms_admin:
			logging.warning("username {} incorrect..".format(username))
			return True
		# check if password is correct:
		if not bcrypt.checkpw(password.encode('utf-8'), self.hashed_pass["hms_private"]):
			logging.warning("password incorrect for user: {}".format(username))
			return True
		return False

	def handle_public_hms_endpoint_login(self, username, password, next_page):
		# check if username is correct:
		if username != self.hms_username:
			logging.warning("username {} incorrect..".format(username))
			return True
		# check if password is correct:
		if not bcrypt.checkpw(password.encode('utf-8'), self.hashed_pass["hms_public"]):
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
		show_login = False
		# Checks if username and password is correct:
		if any(endpoint in next_page for endpoint in self.hms_public):
			show_login = self.handle_public_hms_endpoint_login(username, password, next_page)
		if show_login is True:
			if any(endpoint in next_page for endpoint in self.hms_protected):
				# Adds hms-specific password to endpoint:
				show_login = self.handle_hms_endpoint_login(username, password, next_page)
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

	for hms_endpoint in hms_protected:
		if hms_endpoint in next_page:
			login_text = """
			<h3>Click <a href="https://www.epa.gov/ceam/forms/contact-hms-helpdesk" target="_blank">here</a>
			to request user ID and password (request may take up to a day to process).</h3>
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