#coding=utf-8
import logging

from basehandler import BaseHandler
from tool.datastore import Message


class MessagePage(BaseHandler):
    def get_roomname(self):
        return 'Class '+'TWCL'[self.current_user.chatclass]

    @BaseHandler.authenticated
    def get(self,path):
        kw = dict()
        if not path:
            kw['roomname'] = self.get_roomname()
            kw['message'] = Message.by_room(kw['roomname'])
            self.render('message.html',**kw)

    @BaseHandler.authenticated
    def post(self,path):
        kw = dict()
        kw['content'] = self.get_argument(name='content',default='')

        if not kw['content']:
            return self.error(403)

        if path:
            pass
        else:
            kw['parent'] = Message.room_key(self.get_roomname())
            kw['author'] = self.current_user.key
            new_message = Message(**kw)
            new_message.put()
            # self.render_json(dict(content=kw['content']))
            self.get(path)
