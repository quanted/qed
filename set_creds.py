import os
import sys
import bcrypt
import subprocess
import django
from django.conf import settings

django.setup()
from django.contrib.auth.models import User

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

root_path = os.path.abspath(os.path.split(__file__)[0])
sys.path.insert(0, root_path)

from temp_config.set_environment import DeployEnv



def store_user_info(username, password):
	# Add user to django db if not already there:
	if not User.objects.filter(username=username).exists():
		_user = User.objects.create_user(username, 'email@address.com', password)
		_user.save()  # save username and plain pass to django db

def main(secrets_full_path, password, database):
	
	# Removes existing DB (pitfall fix here - if renewing password, table needs to be remigrated)
	file_path = os.path.join(PROJECT_ROOT, database)
	if os.path.exists(file_path):
		os.remove(file_path)

	# Updates database with tables:
	subprocess.run(["python", "manage.py", "migrate", "auth", "--noinput"])
	subprocess.run(["python", "manage.py", "migrate", "sessions", "--noinput"])

	# Creates hashed password, stores at secrets_full_path
	p = str(password).encode('utf-8')
	hash = bcrypt.hashpw(p, bcrypt.gensalt())
	# fileout = open("secret_key_login.txt", 'w')
	fileout = open(secrets_full_path, 'w')
	fileout.write(hash.decode())
	fileout.close()

	store_user_info(username, password)



if __name__ == '__main__':

	secrets_full_path = None  # full path and filename for secret (e.g., /full/path/secrets/secret_key.txt)
	password = None  # password to encrypt and store at secrets_full_path
	username = None
	database = "db.sqlite3"  # name of db for login walls

	try:
		secrets_full_path = sys.argv[1]
	except IndexError:
		raise Exception("Need full path and name of secrets file as 1st arg.")

	try:
		password = sys.argv[2]
	except IndexError:
		raise Exception("Need password as 2nd arg.")

	try:
		username = sys.argv[3]
	except IndexError:
		raise Exception("Need username as 3rd arg.")

	try:
		database = sys.argv[4]
	except IndexError:
		print("No database for 4th arg, defaulting to {}".format(database))

	# Determine env vars to use:
	runtime_env = DeployEnv()
	runtime_env.load_deployment_environment()

	if os.environ.get('DJANGO_SETTINGS_FILE'):
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get('DJANGO_SETTINGS_FILE'))
	else:
		os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

	try:
		main(secrets_full_path, password, database)
	except Exception:
		raise