#coding=utf-8
import logging

from basehandler import BaseHandler

class MessagePage(BaseHandler):
    @BaseHandler.authenticated
    def get(self):
        self.render('message.html')
