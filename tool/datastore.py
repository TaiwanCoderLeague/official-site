import logging

from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    img_key = ndb.StringProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    account = ndb.StringProperty()
    passward = ndb.StringProperty()
    fbuser = ndb.BooleanProperty(required=True)
    fid = ndb.StringProperty()
    profile_url = ndb.StringProperty()
    access_token = ndb.StringProperty()
    @staticmethod
    def parent_key():
        return ndb.Key('/','user')
    @classmethod
    def by_fid(cls,fid):
        q = cls.query(ancestor=cls.parent_key())
        q = q.filter(cls.fid==fid)
        return q.get()
    @classmethod
    def by_id(cls,uid):
        return cls.get_by_id(uid,parent=cls.parent_key())
        
class Image(ndb.Model):
    img = ndb.BlobProperty(indexed=False)
    created = ndb.DateTimeProperty(auto_now_add=True)