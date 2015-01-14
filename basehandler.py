#coding=utf-8
import tornado.web
import logging

from tool import memcache
from tool.datastore import User
from tool.config import APP_Key


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        uid = self.get_secure_cookie("uid")
        if not uid:
            return None
        user = memcache.get('USER_'+uid)
        if not user:
        	user = User.by_id(int(uid))
        return user

    def render(self,*a,**kw):
        kw['FACEBOOK_APP_ID'] = APP_Key.get('FACEBOOK_APP_ID')
        kw['current_user'] = self.current_user
        kw['request_url'] = self.request.uri
        super(BaseHandler, self).render(*a,**kw)

    def error(self,error):
        raise tornado.web.HTTPError(error)

    @staticmethod
    def authenticated(*a):
        return tornado.web.authenticated(*a)
