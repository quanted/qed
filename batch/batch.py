#Create flexible object containing a dictionary of inputs, outputs, target operation, batch id for processing and retrieval
from google.appengine.ext import db

class Batch(db.Expando):
    user = db.UserProperty
    completed = db.BooleanProperty
    created = db.DateTimeProperty(auto_now_add=True)