#coding=utf-8
import memcache
import logging

from google.appengine.ext import ndb

# debug = {
#     'cookie_secret'      :'ejmo;powfoi4388hfgy2rh3bhfweo0-=',
#     'FACEBOOK_APP_ID'    :'5',
#     'FACEBOOK_APP_SECRET':'',
# }

class APP_Key(ndb.Model):
    name = ndb.StringProperty(required=True)
    value = ndb.StringProperty(required=True)
    @classmethod
    def get(cls,name):
        value = memcache.get('APP_Key_'+name)
        if not value:
            q = cls.query(cls.name == name).get()
            value = ''
            if q:
                value = q.value
            memcache.set('APP_Key_'+name,value)
        return value

# def debug_init():
#     empty = APP_Key.get('empty')
#     if empty:
#         return None
#     empty = APP_Key(name='empty',value='1')
#     empty.put()
#     for i in debug:
#         tmp = APP_Key(name=i,value=debug[i])
#         tmp.put()
# debug_init()
