#coding=utf-8
"""
User can login with account and passward,or with FB.
"""
import logging

from basehandler import BaseHandler
from tool import users
from tool.config import APP_Key


class SignupPage(BaseHandler):
    def get(self):
        if self.current_user:
            return self.redirect('/')

        referer = self.get_argument(name='next',default='/')
        self.render('signup.html',
                        referer_url = referer,
                        has_error = False,
                        account = '',
                    )

    def post(self):
        if self.current_user:
            return self.error(403)

        referer = self.get_argument(name='referer',default='/')
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
            return self.redirect(referer)
        else:
            # Sign up with account and passward.
            kw = dict()
            kw['account'] = self.get_argument(name='account',default='')
            kw['passward'] = self.get_argument(name='passward',default='')
            kw['verify'] = self.get_argument(name='verify',default='')
            # Check string.
            if not users.match_string(kw['account'],r'^[a-zA-Z0-9_-]{8,20}$'):
                kw['has_error'] = True
                kw['error_title'] = 'User Name Invalid!'
                kw['error_message'] = '使用者名稱錯誤，使用者名稱必須介於8到20個字元，並且只包含大小寫英文字母、數字、底線或減號!'
            elif not users.match_string(kw['passward'],r'^.{8,20}$'):
                kw['has_error'] = True
                kw['error_title'] = 'Passward Invalid!'
                kw['error_message'] = '密碼錯誤，密碼必須介於8到20個字元!'
            elif kw['passward'] != kw['verify']:
                logging.error(kw['passward'] +' '+ kw['verify'])
                kw['has_error'] = True
                kw['error_title'] = 'Passward Verify Invalid!'
                kw['error_message'] = '密碼驗證不符合!'
            elif users.get_user(kw['account']):
                kw['has_error'] = True
                kw['error_title'] = 'User Already Exists!'
                kw['error_message'] = '使用者名稱已經存在，請使用其他的名稱!'
            else:
                uid = users.new_user(**kw)
                self.set_secure_cookie('uid',str(uid))
                return self.redirect(referer)
            # if there are some thing wrong.
            kw['referer_url'] = referer
            self.render('signup.html',**kw)


class LoginPage(BaseHandler):
    def get(self):
        if self.current_user:
            return self.redirect('/')

        referer = self.get_argument(name='next',default='/')
        self.render('login.html',
                        referer_url = referer,
                        has_error = False,
                        account = '',
                    )

    def post(self):
        if self.current_user:
            return self.error(403)

        # redirect to whitch url user login from.
        referer = self.get_argument(name='referer',default='/')
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
            return self.redirect(referer)
        else:
            # Sign in with account and passward.
            kw = dict()
            kw['account'] = self.get_argument(name='account',default='')
            kw['passward'] = self.get_argument(name='passward',default='')
            # Check user passward.
            user = None
            if kw['account']:
                user = users.get_user(kw['account'])
            if not user:
                kw['has_error'] = True
                kw['error_title'] = 'User Name Invalid!'
                kw['error_message'] = '使用者名稱錯誤或使用者不存在!'
            elif not kw['passward'] or not users.check_user(user,kw['passward']):
                kw['has_error'] = True
                kw['error_title'] = 'Passward Invalid!'
                kw['error_message'] = '使用者名稱或密碼錯誤!'
            else:
                self.set_secure_cookie('uid',str(user.key.id()))
                return self.redirect(referer)
            # if there are some thing wrong.
            kw['referer_url'] = referer
            self.render('login.html',**kw)


class LogoutPage(BaseHandler):
    def get(self):
        self.set_secure_cookie('uid','')
        return self.redirect('/')
