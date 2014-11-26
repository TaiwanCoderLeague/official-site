# from pymongo import MongoClient
# from google.appengine.ext import db

# import logging

# class Key(db.Model):
#     username = db.StringProperty(required=True)
#     passward = db.StringProperty(required=True)
#     @classmethod
#     def get(cls):
#         q = cls.all()
#         return q.get()
# dbuser = Key.get()
# logging.info("database user = "+str(dbuser.username)+'  '+str(dbuser.passward))
# if not dbuser:
# 	dbuser = Key(username="twclorange",passward="twclorange7122")
# 	dbuser.put()

# client = MongoClient('mongodb://'+dbuser.username+':'+dbuser.passward+'@ds053090.mongolab.com:53090/twclorange')
# database = client['twclorange'] 
# collection = database['collection_name'] 
