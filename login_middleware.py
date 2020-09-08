from django.conf import settings
from django.contrib.auth import login as django_login
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseForbidden
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
hms_pass = ["hms/rest/api/", "/hms/api_doc/swagger/"]


class Http403Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if HttpResponseForbidden.status_code == response.status_code:
            return login(request, "<span style='color:red;'>Your session has timed out, please log back in to refresh your session.</span>")
        else:
            return response


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
        self.hashed_pass = {}  # dictionary of user:passwords
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
            elif "cyanweb" in a:
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
            if "cts" not in self.apps_with_password:
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
            if not (current_user.username == self.hms_admin or current_user.username == self.hms_username):
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
        # if any(endpoint in (path + redirect_path) for endpoint in self.hms_public):
        #     has_access = self.check_authentication(request, "hms_public")
        ispublic = bool(os.getenv("HMS_RELEASE", 0))
        if has_access is False:
            if 'hms' in redirect_path or 'hms' in path:
                if ispublic:
                    has_access = True
                elif not any(endpoint in path or redirect_path for endpoint in hms_pass):
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
                if any(p in path for p in hms_pass):
                    return False
                else:
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
        if username != self.hms_admin or username != self.hms_username:
            logging.warning("username {} incorrect..".format(username))
            return True
        # check if password is correct:
        if not bcrypt.checkpw(password.encode('utf-8'), self.hashed_pass["hms_private"]) or \
                not bcrypt.checkpw(password.encode('utf-8'), self.hashed_pass["hms_public"]):
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

        if self.hashed_pass is None:
            self.set_password_via_config()
            self.load_passwords()

        # redirect if hashed pw unable to be set, or user didn't enter password:
        if not self.hashed_pass or not password:
            return redirect('/login?next={}'.format(next_page))
        show_login = False
        # Checks if username and password is correct:
        if not any(endpoint in next_page for endpoint in hms_pass):
            # show_login = self.handle_public_hms_endpoint_login(username, password, next_page)
            if show_login:
                show_login = self.handle_hms_endpoint_login(username, password, next_page)
            if show_login:
                show_login = self.handle_site_wide_login(username, password, next_page)

        if show_login:
            return redirect('/login?next={}'.format(next_page))

        # Add user to django db if not already there:
        if not User.objects.filter(username=username).exists():
            _user = User.objects.create_user(username, 'email@address.com', password)
            _user.save()  # save username and plain pass to django db

        user = authenticate(request, username=username, password=password)  # auths, then returns user obj (too redundant)

        if user is not None:
            if user.is_active:
                # Redirect to a success page.
                request.session.set_expiry(86400)   # one day
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

def login(request, message=""):
    next_page = request.GET.get('next')
    html = render_to_string('login_prompt_02.html', {
        'TITLE': 'User Login', 'next': next_page, 'TEXT': message
    }, request=request)
    response = HttpResponse()
    response.write(html)
    return response
