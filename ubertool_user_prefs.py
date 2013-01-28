import sys
sys.path.append("../ubertool")
from ubertool import Ubertool
from ubertool import Use

from google.appengine.api import users
from google.appengine.ext import db

class UbertoolUserPrefs(db.Expando):
    userid=db.StringProperty
    ubertool_configs = db.ListProperty(db.ReferenceProperty(Ubertool))
    use_configs = db.ListProperty(db.ReferenceProperty(Use))
    

    