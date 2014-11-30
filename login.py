import logging

from basehandler import BaseHandler
from tool import users

class LoginPage(BaseHandler):
	def get(self):
		# if self.current_user:
		# 	self.redirect('/')
		self.render('login.html')
	def post(self):
		if self.get_argument(name='facebook',default=''):
			cookies = dict((n, self.cookies[n].value) for n in self.cookies.keys())
			fb_cookie = users.get_fb_cookie(cookies)
			if not fb_cookie:
				return None
			user = users.check_facebook_user(fb_cookie)
			if not user:
				user = users.new_facebook_user(fb_cookie)
			self.set_secure_cookie('uid',str(user.key.id()))
			return self.redirect('/')