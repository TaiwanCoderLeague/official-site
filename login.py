import logging

from basehandler import BaseHandler
from tool import users
from tool.config import APP_Key

class LoginPage(BaseHandler):
    def post(self):
        fb_login = self.get_argument(name='fblogin',default='')
        if fb_login == '1':
            #Login with FB,
            #if user doesn't exist, sign up with FB,
            #if user doesn't sign in with FB,return 403.
            cookies = dict((n, self.cookies[n].value) for n in self.cookies.keys())
            fb_cookie = users.get_fb_cookie(cookies)
            logging.error(cookies)
            if not fb_cookie:
                return self.error(403)
            user = users.check_facebook_user(fb_cookie)
            if not user:
                user = users.new_facebook_user(fb_cookie)
            self.set_secure_cookie('uid',str(user.key.id()))
            return self.redirect('/')
        else:
            # Sign with username and passward.
            kw = dict()
            kw['username'] = self.get_argument(name='username',default='')
            kw['passward'] = self.get_argument(name='passward',default='')
            # --------begin-Needs to be done.-------.
            #users.check_user(**kw)
            self.error(404)
            # --------end---Needs to be done.-------

