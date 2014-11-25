from pymongo import MongoClient
from google.appengine.ext import db

class Key(db.Model):
    username = db.StringProperty(required=True)
    passward = db.StringProperty(required=True)
    @classmethod
    def get(cls):
        q = cls.all()
        return q.get()
dbuser = Key.get()

client = MongoClient('mongodb://'+dbuser.username+':'+dbuser.passward+'@ds053090.mongolab.com:53090/twclorange')
database = client['twclorange'] 
# collection = database['collection_name'] 