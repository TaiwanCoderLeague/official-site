import tornado.web
import logging

from tool.datastore import User
from tool import memcache

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        uid = self.get_secure_cookie("uid")
        if not uid:
        	return None
        user = memcache.get('USER_'+uid)
        if not user:
        	user = User.by_id(int(uid))
        return user