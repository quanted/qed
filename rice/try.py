'''
Created on Jan 18, 2013

@author: th
'''

import os, sys
from google.appengine.ext import db

class Person(db.Expando):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    hobbies = db.StringListProperty()

p = Person(first_name="Albert", last_name="Johnson")
p.hobbies = ["chess", "travel"]

p.chess_elo_rating = 1350

p.travel_countries_visited = ["Spain", "Italy", "USA", "Brazil"]
p.travel_trip_count = 13

p1 = Person()
p1.favorite = 42


class FirstModel(db.Model):
    prop = db.IntegerProperty()

class SecondModel(db.Model):
    reference = db.ReferenceProperty(FirstModel)

obj1 = FirstModel()
obj1.prop = 42
obj1.put()
