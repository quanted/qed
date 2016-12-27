import os
import sys


# Change working directory so relative paths (and template lookup) work again
os.chdir(os.path.dirname(__file__))
curr_wd = os.getcwd()
print("WSGI Current working directory: {}".format(curr_wd))

# # Add Flask app & parent directory to Python PATH
sys.path.insert(0, curr_wd)                             # '/var/www/ubertool/ubertool_ecorest'
print(sys.path)
# ... build or import your bottle application here ...
import flask_cgi

application = flask_cgi.app
