#coding=utf-8
"""
User can login with account and passward,or with FB.
"""
import logging

from basehandler import BaseHandler
from tool import users
from tool.config import APP_Key


class LoginPage(BaseHandler):
    def get(self):
        return self.error(404)

    def post(self):
        fb_login = self.get_argument(name='fblogin',default='')
        if fb_login == '1':
            #Login with FB,
            cookies = dict((n, self.cookies[n].value) for n in self.cookies.keys())
            fb_cookie = users.get_fb_cookie(cookies)
            #if user doesn't sign in with FB,return 403.
            if not fb_cookie:
                return self.error(403)
            user = users.check_facebook_user(fb_cookie)
            #if user doesn't exist, sign up with FB,
            if not user:
                user = users.new_facebook_user(fb_cookie)
            self.set_secure_cookie('uid',str(user.key.id()))
            return self.redirect('/')
        else:
            # Sign with account and passward.
            kw = dict()
            kw['account'] = self.get_argument(name='account',default='')
            kw['passward'] = self.get_argument(name='passward',default='')
            # --------begin-Needs to be done.-------.
            #users.check_user(**kw)
            self.error(404)
            # --------end---Needs to be done.-------


class LogoutPage(BaseHandler):
    def get(self):
        self.set_secure_cookie('uid','')
        return self.redirect('/')
