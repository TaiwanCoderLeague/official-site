import logging

from google.appengine.ext import ndb

class User(ndb.Model):
    uid = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    name = ndb.StringProperty(required=True)
    profile_url = ndb.StringProperty(required=True)
    access_token = ndb.StringProperty(required=True)
    @staticmethod
    def parent_key():
        return ndb.Key.from_path('/','user')
    @classmethod
    def by_uid(cls,uid):
        q = cls.query(ancestor=cls.parent_key())
        q.query(cls.uid==uid)
        return q.fetch()
        
