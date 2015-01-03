#coding=utf-8
#coding=utf-8
import logging

from basehandler import BaseHandler

class HomePage(BaseHandler):
    def get(self):
        self.render('home.html')
