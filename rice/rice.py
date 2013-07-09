import google.appengine.ext.db as db
import datetime
import time

class Rice(db.Model):
    config_name = db.StringProperty()
    user = db.UserProperty()
    chemical_name = db.StringProperty()
    mai = db.FloatProperty()
    dsed = db.FloatProperty()
    area = db.FloatProperty()
    pb = db.FloatProperty()
    dw = db.FloatProperty()
    osed = db.FloatProperty()
    Kd = db.FloatProperty()
    mai1_out=db.FloatProperty()
    cw_out=db.FloatProperty()
    
    created = db.DateTimeProperty(auto_now_add=True)
